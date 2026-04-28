# ============================================================
# ATMS Latitude-Binned Diagnostics (QC2-filtered)
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

from .utils_loaders import (
    load_omb,
    load_oma_explicit,
    load_qc_universal,
)


LAT_BINS = np.array([
    -90, -75, -60, -45, -30, -15, 0,
     15,  30,  45,  60,  75,  90
])


def _bin_mean(lat, values):
    """
    Bin values by latitude and compute mean in each bin.
    """
    nbins = len(LAT_BINS) - 1
    out = np.zeros(nbins)

    for i in range(nbins):
        mask = (lat >= LAT_BINS[i]) & (lat < LAT_BINS[i+1])
        if np.any(mask):
            out[i] = np.nanmean(values[mask])
        else:
            out[i] = np.nan

    centers = 0.5 * (LAT_BINS[:-1] + LAT_BINS[1:])
    return centers, out


def plot_latbins_atms(f, var, label, outdir):
    """
    ATMS latitude-binned diagnostics (QC2-filtered).
    Uses ombg/oman via loader functions.
    """
    print("[ATMS] Latitude-binned diagnostics (QC2-filtered)...")

    os.makedirs(outdir, exist_ok=True)

    # Load OMB/OMA via loaders (handles ombg/oman groups)
    omb = load_omb(f, var)
    oma = load_oma_explicit(f, var)

    if omb is None or oma is None:
        print(f"[SKIP] {label}: missing OMB/OMA for latitude-binned diagnostics")
        return

    try:
        lat = f["MetaData/latitude"][:]
    except KeyError:
        raise KeyError("ATMS diag missing MetaData/latitude")

    # QC mask (Location, Channel)
    qc = load_qc_universal(f, var)
    mask = (qc == 0)

    # Broadcast latitude to (Location, Channel)
    lat2d = np.broadcast_to(lat[:, None], qc.shape)

    # Apply mask to all arrays → 1D flattened arrays
    omb = omb[mask]
    oma = oma[mask]
    lat = lat2d[mask]

    # Compute stats
    latc, mean_omb = _bin_mean(lat, omb)
    _,    mean_oma = _bin_mean(lat, oma)

    # Std via mean of squared departures, then sqrt
    _, mean_omb2 = _bin_mean(lat, omb**2)
    _, mean_oma2 = _bin_mean(lat, oma**2)
    std_omb = np.sqrt(mean_omb2)
    std_oma = np.sqrt(mean_oma2)

    # RMS (same as std here, but kept explicit)
    _, rms_omb = _bin_mean(lat, np.sqrt(omb**2))
    _, rms_oma = _bin_mean(lat, np.sqrt(oma**2))

    fig, axes = plt.subplots(2, 1, figsize=(8, 10), constrained_layout=True)

    # ---------------------------------------------------------
    # Panel 1: Mean & Std (dual axis)
    # ---------------------------------------------------------
    ax = axes[0]
    ax.plot(latc, mean_omb, "o-", color="blue", label="Mean OMB")
    ax.plot(latc, mean_oma, "o-", color="red", label="Mean OMA")
    ax.set_ylabel("Mean")

    ax2 = ax.twinx()
    ax2.plot(latc, std_omb, "s--", color="orange", label="Std OMB")
    ax2.plot(latc, std_oma, "s--", color="purple", label="Std OMA")
    ax2.set_ylabel("Std")

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)

    ax.set_xlabel("Latitude")
    ax.set_title("ATMS Latitude-Binned Mean & Std (QC2)", loc="left")

    # ---------------------------------------------------------
    # Panel 2: RMS
    # ---------------------------------------------------------
    ax = axes[1]
    ax.plot(latc, rms_omb, "^-", color="black", label="RMS OMB")
    ax.plot(latc, rms_oma, "^-", color="magenta", label="RMS OMA")
    ax.set_ylabel("RMS")
    ax.set_xlabel("Latitude")
    ax.set_title("ATMS Latitude-Binned RMS (QC2)", loc="left")
    ax.legend(loc="upper right", fontsize=8)

    outfile = os.path.join(outdir, "atms_latbins_qc2.png")
    fig.savefig(outfile, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {outfile}")
