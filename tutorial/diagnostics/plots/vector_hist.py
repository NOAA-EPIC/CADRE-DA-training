#!/usr/bin/env python3
"""
Vector observation histograms:
  - SATWND, SCATWND, or any u/v wind components
  - Produces two histograms: u and v
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from .utils_loaders import load_qc_any, load_omb, load_oma_explicit
from .utils_common import make_output_dir, annotate_assimilated, kde_safe


def _extract_uv(omb, oma):
    """
    Split OMB/OMA arrays into u and v components.
    Assumes last dimension = 2 (u, v).
    """
    if omb.ndim != 2 or omb.shape[1] != 2:
        raise ValueError("Expected OMB shape (nlocs, 2) for vector obs")

    return omb[:, 0], omb[:, 1], oma[:, 0], oma[:, 1]


def _plot_component(ax, data_omb, data_oma, nbins, title):
    """
    Plot a single component histogram + KDE.
    """
    ax.hist(data_omb, bins=nbins, color="lightgrey",
            edgecolor=None, alpha=0.7, density=True)

    kde_safe(ax, data_omb, color="dimgray", linewidth=2, label="OMB KDE")
    kde_safe(ax, data_oma, color="red", linewidth=2, label="OMA KDE")

    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)


def plot_vector_hist(f, varname, label, outdir):
    """
    Plot u and v component histograms for vector wind obs.
    """
    make_output_dir(outdir)

    qc2 = load_qc_any(f, varname)
    if qc2 is None:
        print(f"[SKIP] {label} vector hist: QC missing")
        return

    omb = load_omb(f, varname)
    oma = load_oma_explicit(f, varname)

    # Expect shape (nlocs, 2)
    omb = np.asarray(omb)
    oma = np.asarray(oma)
    qc2 = np.asarray(qc2).reshape(-1)

    if omb.ndim != 2 or omb.shape[1] != 2:
        print(f"[SKIP] {label} vector hist: not 2-component")
        return

    u_omb, v_omb, u_oma, v_oma = _extract_uv(omb, oma)

    valid_u = (qc2 == 0) & np.isfinite(u_omb)
    valid_v = (qc2 == 0) & np.isfinite(v_omb)

    N = int(np.sum(valid_u) + np.sum(valid_v))
    if N == 0:
        print(f"[SKIP] {label} vector hist: no valid data")
        return

    # Adaptive bin count
    std = np.std(np.concatenate([u_omb[valid_u], v_omb[valid_v]]))
    if std < 0.3:
        nbins = 120
    elif std < 1.0:
        nbins = 100
    else:
        nbins = 80

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    _plot_component(axes[0], u_omb[valid_u], u_oma[valid_u], nbins, f"{label} U-component")
    _plot_component(axes[1], v_omb[valid_v], v_oma[valid_v], nbins, f"{label} V-component")

    fig.suptitle(f"{label} Vector Wind Histograms (QC2==0)", y=0.98, fontsize=13)
    annotate_assimilated(fig, N)

    fname = os.path.join(outdir, f"{label.lower()}_vector_hist.png")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(fname, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {fname}")
