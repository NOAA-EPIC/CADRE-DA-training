# plots/base_plotter.py

import matplotlib.pyplot as plt

class BasePlotter:
    def __init__(self):
        plt.rcParams.update({
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10
        })

    def new_figure(self, width=18, height=6, top=0.90):
        fig = plt.figure(figsize=(width, height))
        fig.subplots_adjust(left=0.05, right=0.98, top=top, bottom=0.12, wspace=0.25)
        return fig

    def add_title(self, fig, text):
        title_ax = fig.add_axes([0.01, 0.91, 0.98, 0.045])
        title_ax.text(0, 0.5, text, fontsize=16, ha='left', va='center')
        title_ax.set_axis_off()
