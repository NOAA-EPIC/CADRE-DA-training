# ============================================================
# ATMS Scan-Position Diagnostics (QC2-filtered)
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

from .utils_loaders import (
    load_omb,
    load_oma_explicit,
    load_qc_universal,
)

WINDOW_CH = [1, 2, 16, 17]
O2_CH     = list(range(3, 16))
H2O_CH    = list(range(18, 23))


def _compute_stats_by_scan(omb, oma, scanpos, channels, ch_group):
    scan_positions = np.unique(scanpos)
    nscan = len(scan_positions)

    mean_omb = np.zeros(nscan)
    mean_oma = np.zeros(nscan)
    std_omb  = np.zeros(nscan)
    std_oma  = np.zeros(nscan)
    rms_omb  = np.zeros(nscan)
    rms_oma  = np.zeros(nscan)

    for i, sp in enumerate(scan_positions):
        mask = (scanpos == sp) & np.isin(channels, ch_group)

        omb_sp = omb[mask]
        oma_sp = oma[mask]

        mean_omb[i] = np.nanmean(omb_sp)
        mean_oma[i] = np.nanmean(oma_sp)
        std_omb[i]  = np.nanstd(omb_sp)
        std_oma[i]  = np.nanstd(oma_sp)
        rms_omb[i]  = np.sqrt(np.nanmean(omb_sp**2))
        rms_oma[i]  = np.sqrt(np.nanmean(oma_sp**2))

    return scan_positions, mean_omb, mean_oma, std_omb, std_oma, rms_omb, rms_oma


def _plot_panel(ax, scanpos, mean_omb, mean_oma, std_omb, std_oma, rms_omb, rms_oma, title):
    ax.plot(scanpos, mean_omb, "o-", color="blue", label="Mean OMB")
    ax.plot(scanpos, mean_oma, "o-", color="red", label="Mean OMA")
    ax.set_ylabel("Mean")

    ax2 = ax.twinx()
    ax2.plot(scanpos, std_omb, "s--", color="orange", label="Std OMB")
    ax2.plot(scanpos, std_oma, "s--", color="purple", label="Std OMA")
    ax2.plot(scanpos, rms_omb, "^-", color="black", label="RMS OMB")
    ax2.plot(scanpos, rms_oma, "^-", color="magenta", label="RMS OMA")
    ax2.set_ylabel("Std / RMS")

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)

    ax.set_xlabel("Scan Position")
    ax.set_title(title, loc="left", fontsize=12)


def plot_scan_position_atms(f, var, label, outdir):
    print("[ATMS] Scan-position diagnostics (QC2-filtered)...")

    os.makedirs(outdir, exist_ok=True)

    # CORRECT: use loader functions (ombg/oman)
    omb = load_omb(f, var)
    oma = load_oma_explicit(f, var)

    if omb is None or oma is None:
        print(f"[SKIP] {label}: missing OMB/OMA for scan-position diagnostics")
        return

    # Load scan-position from MetaData group
    try:
        scanpos = f["MetaData/sensorScanPosition"][:]
    except KeyError:
        raise KeyError("ATMS diag missing MetaData/sensorScanPosition")

    # Load channel numbers from MetaData group
    try:
        channels = f["MetaData/sensorChannelNumber"][:]
    except KeyError:
        raise KeyError("ATMS diag missing MetaData/sensorChannelNumber")
    
    qc = load_qc_universal(f, var)          # (Location, Channel)
    mask = (qc == 0)                        # (Location, Channel)

    # Broadcast scanpos to (Location, Channel) then mask
    scanpos2d = np.broadcast_to(scanpos[:, None], qc.shape)   # (Location, Channel)

    omb = omb[mask]              # 1D: valid (loc, ch)
    oma = oma[mask]              # 1D
    channels = channels[mask]    # 1D
    scanpos = scanpos2d[mask]    # 1D, aligned with omb/oma/channels
    
    fig, axes = plt.subplots(3, 1, figsize=(8, 12), constrained_layout=True)

    sp, momb, moma, stomb, stoma, rmb, rma = _compute_stats_by_scan(
        omb, oma, scanpos, channels, WINDOW_CH
    )
    _plot_panel(axes[0], sp, momb, moma, stomb, stoma, rmb, rma,
                "ATMS Scan-Position — Window Channels (QC2)")

    sp, momb, moma, stomb, stoma, rmb, rma = _compute_stats_by_scan(
        omb, oma, scanpos, channels, O2_CH
    )
    _plot_panel(axes[1], sp, momb, moma, stomb, stoma, rmb, rma,
                "ATMS Scan-Position — O₂ Temperature Channels (QC2)")

    sp, momb, moma, stomb, stoma, rmb, rma = _compute_stats_by_scan(
        omb, oma, scanpos, channels, H2O_CH
    )
    _plot_panel(axes[2], sp, momb, moma, stomb, stoma, rmb, rma,
                "ATMS Scan-Position — H₂O Channels (QC2)")

    outfile = f"{outdir}/atms_scan_position_qc2.png"
    fig.savefig(outfile, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {outfile}")
