# Standard imports
import os

import numpy as np
import matplotlib.pyplot as plt


# constants
DPI = 300


def plot_ranking_curves(
    x,
    y,
    y_expected_case,
    y_worst_case,
    auc,
    auc_expected_case,
    auc_worst_case,
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

    # to fit into the miccai paper
    plt.rcParams["figure.figsize"] = (5, 2.5)

    # --------------------------------------------------------------------------
    # ranking curve
    plt.plot(
        x,
        y,
        color="darkorange",
        # color="navy", lw=2, linestyle="--",
        label=f"ranked: Normalized AUC = {auc.round(2)}",
    )

    # --------------------------------------------------------------------------
    # expected case ranking curve
    plt.plot(
        x,
        y_expected_case,
        lw=2,
        linestyle="--",
        color="navy",
        label=f"random: Normalized AUC = {np.round(auc_expected_case, 2)}",
    )
    
    # --------------------------------------------------------------------------
    # worst case ranking curve
    plt.plot(
        x,
        y_worst_case,
        lw=2,
        linestyle="--",
        color="black",
        label=f"worst: Normalized AUC = {np.round(auc_worst_case, 2)}",
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
