#!/usr/bin/env python3
"""
ATMS per-channel histograms (QC2==0)
Replicates the original behavior from obs_diag_plots.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from .utils_loaders import load_qc_any, load_omb, load_oma_explicit
from .utils_common import annotate_assimilated


def plot_hist_atms(f, varname, label, outdir):
    """
    ATMS histogram for each channel.
    Fully equivalent to the original obs_diag_plots.py implementation.
    """
    os.makedirs(outdir, exist_ok=True)

    qc2 = load_qc_any(f, varname)
    if qc2 is None or qc2.ndim != 2:
        print(f"[SKIP] {label} hist: not radiance or QC missing")
        return

    omb = load_omb(f, varname)
    oma = load_oma_explicit(f, varname)

    # Ensure 2D
    if omb.ndim == 1:
        omb = omb[:, np.newaxis]
    if oma.ndim == 1:
        oma = oma[:, np.newaxis]

    nlocs, nchans = qc2.shape

    for ch in range(nchans):
        qc_mask = (qc2[:, ch] == 0)
        omb_ch = omb[:, ch]
        oma_ch = oma[:, ch]

        valid_omb = qc_mask & np.isfinite(omb_ch)
        valid_oma = qc_mask & np.isfinite(oma_ch)

        N_OMB = int(np.sum(valid_omb))
        if N_OMB == 0:
            continue

        # Adaptive bins
        std = np.std(omb_ch[valid_omb])
        if std < 0.3:
            nbins = 120
        elif std < 1.0:
            nbins = 100
        else:
            nbins = 80

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.hist(omb_ch[valid_omb], bins=nbins, color="lightgrey",
                edgecolor=None, alpha=0.7, density=True)

        try:
            sns.kdeplot(omb_ch[valid_omb], color="dimgray", linewidth=2, ax=ax)
            sns.kdeplot(oma_ch[valid_oma], color="red", linewidth=2, ax=ax)
        except Exception:
            pass

        fig.suptitle(f"{label} Ch {ch+1} Histogram (QC2==0)", y=0.97, fontsize=12)
        annotate_assimilated(fig, N_OMB)

        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.grid(True, alpha=0.3)

        fname = os.path.join(outdir, f"{label.lower()}_ch{ch+1:02d}_hist.png")
        fig.tight_layout(rect=[0, 0, 1, 0.97])
        fig.savefig(fname, dpi=150)
        plt.close(fig)
        print(f"[SAVED] {fname}")
