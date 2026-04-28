# plots/qc_plots.py

import matplotlib.pyplot as plt
from .base_plotter import BasePlotter


class QCPlotter(BasePlotter):

    def plot_qc_counts(self, qc_pass, qc_fail, fname=None):
        fig = self.new_figure(width=6, height=5)
        self.add_title(fig, "QC Pass/Fail Counts")

        labels = ["Pass", "Fail"]
        values = [qc_pass, qc_fail]

        plt.bar(labels, values, color=["seagreen", "firebrick"])
        plt.ylabel("Count")

        if fname:
            plt.savefig(fname, dpi=200)
        plt.close(fig)
