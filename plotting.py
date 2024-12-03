# Standard imports
import os

import numpy as np
import matplotlib.pyplot as plt


# constants
DPI = 300


def plot_ranking_curves(
    x,
    y,
    total_possible_matches=None,
    n_elements=None,
    population_proportion=None,
    auc=None,
    plot_title=None,
    save=False,
    save_dir=None,
    save_name=None,
    save_ext=None,
):
    if save:
        assert save_dir is not None, "Please provide a directory to save the figure"
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
            print(f"Created directory: {save_dir}")
        assert save_name is not None, "Please provide a name for the saved figure"
        assert save_ext is not None, "Please provide an extension for the saved figure"

    if auc is not None:
        ranking_curve_label = f"ranked: Normalized AUC = {auc.round(2)}"
    else:
        ranking_curve_label = "ranked"

    # to fit into the miccai paper
    plt.rcParams["figure.figsize"] = (5, 2.5)

    # --------------------------------------------------------------------------
    # ranking curve
    plt.plot(
        x,
        y,
        color="darkorange",
        # color="navy", lw=2, linestyle="--",
        label=ranking_curve_label,
    )

    # --------------------------------------------------------------------------
    # expected case ranking curve
    random_auc = 0.5 + (
        (total_possible_matches - 1) * population_proportion
    ) / (2 * (n_elements - 1))
    # horizontal line from (x[0], population_proportion) to (total_possible_matches, population_proportion)
    plt.plot(
        [x[0], total_possible_matches],
        [population_proportion, population_proportion],
        lw=2,
        linestyle="--",
        color="navy",
    )
    # straight diagonal line from (total_possible_matches, population_proportion) to (x[-1], 1)
    plt.plot(
        [total_possible_matches, x[-1]],
        [population_proportion, 1],
        lw=2,
        linestyle="--",
        color="navy",
        label=f"random: Normalized AUC = {np.round(random_auc, 2)}",
    )
    
    # --------------------------------------------------------------------------
    # worst case ranking curve
    worst_case_auc = (total_possible_matches / 2) / (n_elements - 1)
    # horizontal line from (x[0], 0) to (n_elements-total_possible_matches, 0)
    plt.plot(
        [x[0], n_elements - total_possible_matches],
        [0, 0],
        lw=2,
        linestyle="--",
        color="black",
    )
    # straight diagonal line from (n_elements-total_possible_matches, 0) to (x[-1], 1)
    plt.plot(
        [n_elements - total_possible_matches, x[-1]],
        [0, 1],
        lw=2,
        linestyle="--",
        color="black",
        label=f"worst: Normalized AUC = {np.round(worst_case_auc, 2)}",
    )

    # --------------------------------------------------------------------------
    # plot settings
    plt.ylim([-0.05, 1.05])
    plt.xlabel("top-n ranked examples")
    plt.ylabel("recall")
    if plot_title:
        plt.title(plot_title)

    plt.legend()
    # plt.legend(loc="lower right")
    # plt.legend(loc="upper left")

    if save:
        plt.savefig(f"{save_dir}/{save_name}.{save_ext}", dpi=DPI, bbox_inches="tight")
    plt.show()
