import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from .utils_loaders import load_omb, load_oma_explicit, load_qc_universal


# ---------------------------------------------------------------------
# Correct ATMS channel groups
# ---------------------------------------------------------------------
def channel_groups():
    return [
        ("Window", 1, 2, "lightgrey"),
        ("O₂ Temp", 3, 15, "lightblue"),
        ("Window", 16, 17, "lightgrey"),
        ("H₂O", 18, 22, "lightgreen"),
    ]


# ---------------------------------------------------------------------
# Extended ATMS Stats
# ---------------------------------------------------------------------
def plot_stats_atms_extended(f, varname, label, outdir):
    os.makedirs(outdir, exist_ok=True)

    omb = load_omb(f, varname)
    oma = load_oma_explicit(f, varname)
    qc = load_qc_universal(f, varname)

    if omb is None or oma is None:
        print(f"[SKIP] {label} ATMS extended stats: missing OMB/OMA")
        return

    if qc.ndim == 1:
        qc = np.repeat(qc[:, None], omb.shape[1], axis=1)

    nchan = omb.shape[1]
    chans = np.arange(1, nchan + 1)

    # Allocate arrays
    mean_omb = np.full(nchan, np.nan)
    mean_oma = np.full(nchan, np.nan)
    std_omb = np.full(nchan, np.nan)
    std_oma = np.full(nchan, np.nan)
    rms_omb = np.full(nchan, np.nan)
    rms_oma = np.full(nchan, np.nan)
    rms_diff = np.full(nchan, np.nan)
    nrms_omb = np.full(nchan, np.nan)
    nrms_oma = np.full(nchan, np.nan)
    bc_rms_omb = np.full(nchan, np.nan)
    bc_rms_oma = np.full(nchan, np.nan)

    # -----------------------------------------------------------------
    # Compute stats per channel
    # -----------------------------------------------------------------
    for ch in range(nchan):
        mask = (qc[:, ch] == 0) & np.isfinite(omb[:, ch]) & np.isfinite(oma[:, ch])
        if not np.any(mask):
            continue

        o = omb[mask, ch].astype("float64")
        a = oma[mask, ch].astype("float64")

        mean_omb[ch] = np.mean(o)
        mean_oma[ch] = np.mean(a)

        std_omb[ch] = np.nanstd(o, ddof=1)
        std_oma[ch] = np.nanstd(a, ddof=1)

        rms_omb[ch] = np.sqrt(np.mean(o**2))
        rms_oma[ch] = np.sqrt(np.mean(a**2))

        rms_diff[ch] = rms_oma[ch] - rms_omb[ch]

        nrms_omb[ch] = rms_omb[ch] / std_omb[ch] if std_omb[ch] > 0 else np.nan
        nrms_oma[ch] = rms_oma[ch] / std_oma[ch] if std_oma[ch] > 0 else np.nan

        bc_rms_omb[ch] = std_omb[ch]
        bc_rms_oma[ch] = std_oma[ch]

    # -----------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)

    ax_meanstd = axes[0, 0]
    ax_rms = axes[0, 1]
    ax_rmsdiff = axes[1, 0]
    ax_norm = axes[1, 1]

    # Shading helper
    def shade(ax):
        for name, c1, c2, color in channel_groups():
            ax.axvspan(c1 - 0.5, c2 + 0.5, color=color, alpha=0.25, zorder=0)
    
    # -------------------------
    # Panel 1: Mean & Std (dual y-axes)
    # -------------------------
    shade(ax_meanstd)

    # Left axis = Mean
    ax_meanstd.plot(chans, mean_omb, "o-", color="blue", label="Mean OMB")
    ax_meanstd.plot(chans, mean_oma, "o-", color="red", label="Mean OMA")
    ax_meanstd.set_ylabel("Mean")

    # Right axis = Std
    ax_std = ax_meanstd.twinx()
    ax_std.plot(chans, std_omb, "s--", color="orange", label="Std OMB")
    ax_std.plot(chans, std_oma, "s--", color="purple", label="Std OMA")
    ax_std.set_ylabel("Std")
    
    ax_meanstd.set_title("Mean & Std (OMB / OMA)")
    ax_meanstd.set_xlabel("Channel")
    
    # Combined legend (upper-left)
    lines1, labels1 = ax_meanstd.get_legend_handles_labels()
    lines2, labels2 = ax_std.get_legend_handles_labels()

    # Combined legend (upper-left)
    leg1 = ax_meanstd.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="lower left",
        fontsize=8,
        frameon=True
    )
    ax_meanstd.add_artist(leg1)   # <-- KEEP THIS LEGEND

    # Channel-group legend (bottom-right)
    ax_meanstd.legend(
        handles=[
            Patch(facecolor="lightgrey", label="Window (1–2, 16–17)"),
            Patch(facecolor="lightblue", label="O₂ Temp (3–15)"),
            Patch(facecolor="lightgreen", label="H₂O (18–22)")
        ],
        loc="lower right",
        fontsize=6,
        frameon=True
    )
   
    # -------------------------
    # Panel 2: RMS
    # -------------------------
    shade(ax_rms)
    ax_rms.plot(chans, rms_omb, "^-", color="black", label="RMS OMB")
    ax_rms.plot(chans, rms_oma, "^-", color="magenta", label="RMS OMA")
    ax_rms.set_title("RMS (OMB / OMA)")
    ax_rms.set_xlabel("Channel")
    ax_rms.set_ylabel("RMS")
    ax_rms.legend(loc="upper left", fontsize=8)       # <--- ADDED

    # -------------------------
    # Panel 3: RMS Difference
    # -------------------------
    shade(ax_rmsdiff)
    ax_rmsdiff.plot(chans, rms_diff, "o-", color="green", label="RMS(OMA) – RMS(OMB)")
    ax_rmsdiff.set_title("RMS Difference (OMA – OMB)")
    ax_rmsdiff.set_xlabel("Channel")
    ax_rmsdiff.set_ylabel("Difference")
    ax_rmsdiff.legend(loc="lower left", fontsize=8)   # <--- ADDED
    
    # -------------------------
    # Panel 4: Normalized + BC RMS
    # -------------------------
    #shade(ax_norm)
    #ax_norm.plot(chans, nrms_omb, "^-", color="black", label="NRMS OMB")
    #ax_norm.plot(chans, nrms_oma, "^-", color="magenta", label="NRMS OMA")
    #ax_norm.plot(chans, bc_rms_omb, "s--", color="orange", label="BC-RMS OMB (Std)")
    #ax_norm.plot(chans, bc_rms_oma, "s--", color="purple", label="BC-RMS OMA (Std)")
    #ax_norm.set_title("Normalized RMS & Bias-Corrected RMS")
    #ax_norm.set_xlabel("Channel")
    #ax_norm.set_ylabel("Value")
    #ax_norm.legend(loc="upper left", fontsize=8)      # <--- ADDED
    # -------------------------
    # Panel 4: Normalized + BC RMS
    # -------------------------
    shade(ax_norm)

    # NRMS
    ax_norm.plot(chans, nrms_omb, "^-", color="black", label="NRMS OMB")
    ax_norm.plot(chans, nrms_oma, "^-", color="magenta", label="NRMS OMA")

    # BC-RMS
    ax_norm.plot(chans, bc_rms_omb, "s--", color="orange", label="BC-RMS OMB")
    ax_norm.plot(chans, bc_rms_oma, "s--", color="purple", label="BC-RMS OMA")

    ax_norm.set_title("Normalized RMS & Bias-Corrected RMS")
    ax_norm.set_xlabel("Channel")
    ax_norm.set_ylabel("RMS")

    # Unified y-axis scaling
    all_vals = np.concatenate([
        nrms_omb, nrms_oma,
        bc_rms_omb, bc_rms_oma
    ])
    all_vals = all_vals[np.isfinite(all_vals)]
    ymin, ymax = np.min(all_vals), np.max(all_vals)
    yr = ymax - ymin
    ax_norm.set_ylim(ymin - 0.1 * yr, ymax + 0.1 * yr)

    # Legend
    ax_norm.legend(loc="upper right", fontsize=8)

    
    # -----------------------------------------------------------------
    # Legend (bottom-right)
    # -----------------------------------------------------------------
    handles = []
    labels = []
    for name, _, _, color in channel_groups():
        handles.append(plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.25))
        labels.append(name)

    #fig.legend(handles, labels, loc="lower right", fontsize=9)

    # -----------------------------------------------------------------
    # Title
    # -----------------------------------------------------------------
    fig.suptitle(
        f"{label} Extended OMB/OMA Stats (QC2==0)",
        fontsize=13,
        y=1.02
    )

    # Save
    outpath = os.path.join(outdir, f"{label.lower()}_stats_extended.png")
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {outpath}")
