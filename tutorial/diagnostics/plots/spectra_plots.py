# plots/spectra_plots.py

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

from .base_plotter import BasePlotter

# Fixed FV3 127-level pressure grid (mbar)
PFULL_MBAR = np.array([
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    1,1,2,2,3,4,5,7,8,
    10,12,14,16,19,21,24,28,31,35,39,43,47,52,56,61,67,72,
    78,84,90,97,104,112,120,128,136,145,154,164,174,184,195,
    207,219,231,243,256,270,283,297,312,326,342,357,373,389,
    405,421,438,454,471,488,505,522,539,555,572,589,605,621,
    637,653,668,683,698,713,727,741,754,767,780,792,804,815,
    826,837,847,857,866,875,884,892,900,907,914,921,928,934,
    940,945,950,955,960,965,969,973,977,980,984,987,990,993,
    995,998
])


class SpectraPlotter(BasePlotter):

    def plot_spectra(self, core, level, ctrl_name, exp_name,
                     fname=None, nicas_length_scale=None, return_fig=False):

        fig = plt.figure(figsize=(18, 7.5))
        fig.subplots_adjust(left=0.05, right=0.98, top=0.90,
                            bottom=0.12, wspace=0.30)

        # Title axis
        title_ax = fig.add_axes([0.01, 0.91, 0.98, 0.045])

        p = PFULL_MBAR[level] if 0 <= level < len(PFULL_MBAR) else None
        if p is not None:
            title_str = f"{core.varname} Spectral Diagnostics – Level {level} ({p:.1f} mbar)"
        else:
            title_str = f"{core.varname} Spectral Diagnostics – Level {level}"

        title_ax.text(0, 0.5, title_str,
                      fontsize=16, ha='left', va='center')
        title_ax.set_axis_off()

        # ---------------------------------------------------------
        # 1D spectra
        # ---------------------------------------------------------
        ax1 = fig.add_subplot(1, 3, 1)
        ax1.set_box_aspect(1)

        ax1.loglog(core.k, core.spec_ctrl_all[level], label=ctrl_name)
        ax1.loglog(core.k, core.spec_exp_all[level],  label=exp_name)
        ax1.loglog(core.k,
                   np.abs(core.spec_exp_all[level] - core.spec_ctrl_all[level]),
                   label="Difference")

        if nicas_length_scale is not None:
            ax1.text(0.05, 0.95,
                     f"L = {nicas_length_scale/1000:.0f} km",
                     transform=ax1.transAxes,
                     ha="left", va="top", fontsize=10)

        ax1.set_xlabel("Wavenumber")
        ax1.set_ylabel("Power")
        ax1.grid(True, which="both", ls="--")
        ax1.set_title("1D Spectra")
        ax1.legend()

        # ---------------------------------------------------------
        # Variance profile
        # ---------------------------------------------------------
        ax2 = fig.add_subplot(1, 3, 2)
        ax2.set_box_aspect(1)

        var_ratio = core.variance_profile()
        ax2.plot(var_ratio, np.arange(core.nlevels), marker='o')
        ax2.axvline(1.0, color='gray', lw=1)
        ax2.invert_yaxis()
        ax2.set_xlabel("Variance Ratio (EXP / CTRL)")
        ax2.set_ylabel("Model Level")
        ax2.grid(True, ls='--')
        ax2.set_title("Variance Profile")

        # ---------------------------------------------------------
        # 2D spectral ratio
        # ---------------------------------------------------------
        ax3 = fig.add_subplot(1, 3, 3)
        ax3.set_box_aspect(1)

        ratio2d = core.spectral_ratio_2d()
        im = ax3.pcolormesh(core.k, np.arange(core.nlevels), ratio2d,
                            shading="auto", cmap="coolwarm",
                            vmin=0.5, vmax=1.5)

        ax3.set_xscale("log")
        ax3.set_xticks([1, 10, 100, 1000])
        ax3.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
        ax3.invert_yaxis()
        ax3.set_xlabel("Wavenumber")
        ax3.set_ylabel("Model Level")
        ax3.set_title("2D Spectral Ratio")
        plt.colorbar(im, ax=ax3, shrink=0.8)

        if return_fig:
            return fig

        if fname:
            plt.savefig(fname, dpi=200)

        plt.close(fig)
