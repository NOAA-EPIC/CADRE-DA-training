import os
import numpy as np
import matplotlib.pyplot as plt

from .utils_loaders import load_omb, load_oma_explicit, load_qc_universal


def _channel_groups(nchan):
    # Example grouping for 22-channel ATMS
    # window: 1–7, O2 temp: 8–16, H2O: 17–22
    return {
        "window": (1, 7, "lightgrey"),
        "o2": (8, 16, "lightblue"),
        "h2o": (17, nchan, "lightgreen"),
    }


def plot_stats_atms(f, varname, label, outdir):
    os.makedirs(outdir, exist_ok=True)

    omb = load_omb(f, varname)
    oma = load_oma_explicit(f, varname)
    qc = load_qc_universal(f, varname)

    if omb is None or oma is None:
        print(f"[SKIP] {label} ATMS stats: missing OMB/OMA")
        return

    if qc.ndim == 1:
        qc = np.repeat(qc[:, None], omb.shape[1], axis=1)

    nchan = omb.shape[1]
    chans = np.arange(1, nchan + 1)

    mean_omb = np.full(nchan, np.nan)
    mean_oma = np.full(nchan, np.nan)
    std_omb = np.full(nchan, np.nan)
    std_oma = np.full(nchan, np.nan)

    for ch in range(nchan):
        mask = (qc[:, ch] == 0) & np.isfinite(omb[:, ch]) & np.isfinite(oma[:, ch])
        if np.any(mask):
            mean_omb[ch] = np.mean(omb[mask, ch])
            mean_oma[ch] = np.mean(oma[mask, ch])
            std_omb[ch] = np.std(omb[mask, ch])
            std_oma[ch] = np.std(oma[mask, ch])

    fig, ax1 = plt.subplots(figsize=(7, 4), constrained_layout=True)
    ax2 = ax1.twinx()

    # Shaded channel groups
    groups = _channel_groups(nchan)
    for _, (c1, c2, color) in groups.items():
        ax1.axvspan(c1 - 0.5, c2 + 0.5, color=color, alpha=0.2, zorder=0)

    # Mean
    ax1.plot(chans, mean_omb, "o-", color="blue", label="Mean OMB")
    ax1.plot(chans, mean_oma, "o-", color="red", label="Mean OMA")

    # Std
    ax2.plot(chans, std_omb, "s--", color="orange", label="Std OMB")
    ax2.plot(chans, std_oma, "s--", color="purple", label="Std OMA")

    ax1.set_xlabel("Channel")
    ax1.set_ylabel("Mean")
    ax2.set_ylabel("Std")

    ax1.set_title(f"{label} OMB/OMA Mean/Std (QC2==0)")

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower left", fontsize=8)

    # -----------------------------
    # Line legend (upper-left)
    # -----------------------------
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

    # -----------------------------
    # Channel-group legend (bottom-right)
    # -----------------------------
    group_handles = []
    group_labels = []
    for name, (c1, c2, color) in groups.items():
        group_handles.append(
            plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.25)
        )
        group_labels.append(
            "Window" if name == "window" else ("O₂ Temp" if name == "o2" else "H₂O")
        )

        ax1.legend(
            group_handles,
            group_labels,
            loc="lower right",
            fontsize=8,
            frameon=True
        )

    
    outpath = os.path.join(outdir, f"{label.lower()}_stats.png")
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {outpath}")
