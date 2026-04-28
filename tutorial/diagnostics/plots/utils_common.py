#!/usr/bin/env python3
"""
Shared plotting utilities for FV3-JEDI observation diagnostics.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches


# ----------------------------------------------------------------------
# Filesystem helpers
# ----------------------------------------------------------------------

def make_output_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


# ----------------------------------------------------------------------
# Annotation helpers
# ----------------------------------------------------------------------

def annotate_assimilated(fig, N):
    """
    Add a small text annotation with the number of assimilated obs.
    """
    txt = f"N assimilated: {N}"
    fig.text(0.99, 0.01, txt,
             ha="right", va="bottom",
             fontsize=9, color="dimgray")


# ----------------------------------------------------------------------
# ATMS shading helpers
# ----------------------------------------------------------------------

def shade_atms(ax):
    """
    Apply ATMS channel-group shading:
      - Window: 1–2, 16–17
      - O2 Temp: 3–15
      - H2O: 18–22
    Assumes x-axis is channel number (1-based).
    """
    # Window channels: 1–2 and 16–17
    ax.axvspan(0.5, 2.5,   color="#b0b0b0", alpha=0.45)   # Ch 1–2
    ax.axvspan(15.5, 17.5, color="#b0b0b0", alpha=0.45)   # Ch 16–17

    # O2 temperature channels: 3–15
    ax.axvspan(2.5, 15.5,  color="#7fb3ff", alpha=0.35)

    # Water vapor channels: 18–22
    ax.axvspan(17.5, 22.5, color="#7fdc7f", alpha=0.35)


def atms_group_legend(ax, loc="lower right", fontsize=9):
    """
    Add ATMS channel-group legend (Window / O2 / H2O) to a given axis.
    """
    patch_window = mpatches.Patch(color="#b0b0b0", alpha=0.45, label="Window")
    patch_o2     = mpatches.Patch(color="#7fb3ff", alpha=0.35, label="O₂ Temp")
    patch_h2o    = mpatches.Patch(color="#7fdc7f", alpha=0.35, label="H₂O")

    ax.legend(handles=[patch_window, patch_o2, patch_h2o],
              loc=loc, fontsize=fontsize, frameon=True)


# ----------------------------------------------------------------------
# KDE helper
# ----------------------------------------------------------------------

def kde_safe(ax, data, color="dimgray", linewidth=2, label=None):
    """
    Safely draw a KDE curve if data is valid and non-constant.
    """
    data = np.asarray(data)
    data = data[np.isfinite(data)]
    if data.size < 10:
        return
    if np.allclose(np.std(data), 0.0):
        return
    try:
        sns.kdeplot(data, color=color, linewidth=linewidth, ax=ax, label=label)
    except Exception:
        pass


# ----------------------------------------------------------------------
# Axis helpers
# ----------------------------------------------------------------------

def clean_channel_ticks(ax, nchans):
    """
    Set reasonable x-ticks for channel-based plots.
    """
    ax.set_xlim(0.5, nchans + 0.5)
    if nchans <= 22:
        ax.set_xticks(np.arange(1, nchans + 1, 1))
    else:
        ax.set_xticks(np.arange(1, nchans + 1, 2))
    ax.set_xlabel("Channel")
