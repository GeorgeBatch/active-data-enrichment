import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics


def ranking_auc(
    y_scores,
    y_trues,
    pos_label,
    greater_is_better=True,
    top_k=None,
    verbose=False,
):
    """
    Compute the ranking AUC of a ranking list of elements.
    """

    # cosine similarity is a distance, so we want to rank the closest ones higher
    if not greater_is_better:
        y_scores = [-score for score in y_scores]

    # when y_scores are probabilities of the positive class, we rank them
    #     from highest to lowest (descending order) => reverse=True
    # when y_scores are distances, we have already reverced the sign so the closest ones
    #     have highest negative distance. Again we rank them
    #     from highest to lowest (descending order) => reverse=True
    sorted_matches = sorted(
        [tup for tup in zip(y_trues, y_scores)], key=lambda x: x[1], reverse=True
    )

    n_elements = len(y_trues)
    total_possible_matches = (np.array(y_trues) == pos_label).sum()
    cumulative_ranked_matches = np.array([tup[0] for tup in sorted_matches]).cumsum()
    cumulative_tpr_from_total = cumulative_ranked_matches / total_possible_matches

    if verbose:
        print("n_elements", n_elements)
        print("total_possible_matches\n", total_possible_matches, "\n")
        print("cumulative_ranked_matches\n", cumulative_ranked_matches, "\n")

    # --------------------------------------------------------------------------
    # Cumulative tpr from Cumulative Possible Matches
    # --------------------------------------------------------------------------
    cumulative_possible_matches = np.array([total_possible_matches] * n_elements)
    cumulative_possible_matches[:total_possible_matches] = np.arange(
        1, total_possible_matches + 1, 1
    )

    if verbose:
        print("cumulative_possible_matches\n", cumulative_possible_matches, "\n")
        print("ratio\n", cumulative_ranked_matches / cumulative_possible_matches, "\n")

    cumulative_tpr_from_cumulative_possible_matches = (
        cumulative_ranked_matches / cumulative_possible_matches
    )
    cumulative_tpr_from_cumulative_possible_matches_from_zero = [0] + list(
        cumulative_tpr_from_cumulative_possible_matches
    )

    x = np.arange(1, n_elements + 1)
    y = cumulative_tpr_from_cumulative_possible_matches
    average_y = np.mean(y)
    auc = metrics.auc(x=x, y=y) / (x[-1] - x[0])

    # --------------------------------------------------------------------------
    # Top-K stats
    # --------------------------------------------------------------------------
    # cumulative_false_ranked_matches = cumulative_possible_matches - cumulative_ranked_matches
    population_proportion = total_possible_matches / n_elements

    if verbose:
        print("population_proportion:", population_proportion)

    cumulative_expected_proportion = np.arange(1, n_elements + 1) / n_elements
    cumulative_expected_number_of_matches = (
        cumulative_expected_proportion * total_possible_matches
    )
    if top_k and verbose:
        # subtract 1 because of 0-indexing
        print(
            f"Matches in top-{top_k} ranked ROIs:", cumulative_ranked_matches[top_k - 1]
        )
        print(
            f"Coverage from total possible matches ({total_possible_matches}) in top-{top_k} ranked ROIs",
            cumulative_tpr_from_total[top_k - 1],
        )
        print(
            f"Coverage from cumulative possible matches ({cumulative_possible_matches[top_k-1]}) in top-{top_k} ranked ROIs",
            cumulative_tpr_from_cumulative_possible_matches[top_k - 1],
        )

    result = {
        "x": x,
        "y": y,
        "average_y": average_y,
        "auc": auc,
        "population_proportion": population_proportion,
        "total_possible_matches": total_possible_matches,
        "n_elements": n_elements,
    }

    return result