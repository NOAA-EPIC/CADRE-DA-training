import os
import numpy as np
import matplotlib.pyplot as plt

from .utils_loaders import (
    load_qc_any,
    load_obsvalue,
    load_omb,
    load_oma_explicit,
)

def plot_scalar_hist(f, varname, label, outdir):
    os.makedirs(outdir, exist_ok=True)

    qc2 = load_qc_any(f, varname)
    if qc2 is None:
        print(f"[SKIP] {label} scalar hist: QC missing")
        return

    obs = load_obsvalue(f, varname)
    if obs is None:
        print(f"[SKIP] {label} scalar hist: ObsValue missing")
        return

    # Flatten everything
    qc2 = qc2.ravel()
    obs = obs.ravel()

    # Try to load OMB/OMA
    omb = load_omb(f, varname)
    oma = load_oma_explicit(f, varname)

    # ------------------------------------------------------------
    # GNSSRO fallback: no OMB → plot ObsValue only
    # ------------------------------------------------------------
    if omb is None:
        print(f"[INFO] {label}: No OMB found — using ObsValue only")

        valid = (qc2 == 0) & np.isfinite(obs)
        if np.sum(valid) == 0:
            print(f"[SKIP] {label}: no valid ObsValue")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(obs[valid], bins=120, color="lightgrey", edgecolor=None, alpha=0.7)
        ax.set_title(f"{label} ObsValue Histogram (QC2==0)")
        ax.set_xlabel("ObsValue")
        ax.set_ylabel("Count")
        ax.grid(True, alpha=0.3)

        fname = os.path.join(outdir, f"{label.lower()}_obsvalue_hist.png")
        fig.savefig(fname, dpi=150)
        plt.close(fig)
        print(f"[SAVED] {fname}")
        return

    # ------------------------------------------------------------
    # Normal scalar OMB/OMA histogram (for conventional obs)
    # ------------------------------------------------------------
    omb = omb.ravel()
    if oma is not None:
        oma = oma.ravel()

    valid_omb = (qc2 == 0) & np.isfinite(omb)

    if np.sum(valid_omb) == 0:
        print(f"[SKIP] {label}: no valid OMB")
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(omb[valid_omb], bins=120, color="lightgrey", edgecolor=None, alpha=0.7)
    ax.set_title(f"{label} OMB Histogram (QC2==0)")
    ax.set_xlabel("OMB")
    ax.set_ylabel("Count")
    ax.grid(True, alpha=0.3)

    fname = os.path.join(outdir, f"{label.lower()}_omb_hist.png")
    fig.savefig(fname, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {fname}")
