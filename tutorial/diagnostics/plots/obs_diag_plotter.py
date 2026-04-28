
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from netCDF4 import Dataset

from .utils_loaders import (
    load_obsvalue,
    load_omb,
    load_oma_explicit,
    load_qc_universal,
)

# Existing ATMS diagnostics
from .atms_stats import plot_stats_atms
from .atms_stats_extended import plot_stats_atms_extended

# NEW: QC2-filtered diagnostics
from .atms_scan_position import plot_scan_position_atms
from .atms_latbins import plot_latbins_atms


# ============================================================
# Unified Histogram (ATMS, Scalar, Vector)
# ============================================================

def unified_histogram(omb, oma, qc, title_label, outpath, qc_label="QC", nbins=None):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    omb = np.ravel(omb)
    oma = np.ravel(oma)
    qc  = np.ravel(qc)

    valid_omb = (qc == 0) & np.isfinite(omb)
    valid_oma = (qc == 0) & np.isfinite(oma)

    n_omb = int(np.sum(valid_omb))
    if n_omb == 0:
        print(f"[SKIP] {title_label}: no valid OMB")
        return

    # Bin selection
    if nbins is None:
        std = np.nanstd(omb[valid_omb])
        if np.isfinite(std) and std > 0:
            nbins = 100 if std < 1 else 80
        else:
            nbins = 50

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

    ax.hist(
        omb[valid_omb],
        bins=nbins,
        color="lightgrey",
        edgecolor=None,
        alpha=0.7,
        density=True
    )

    if np.sum(valid_omb) > 1:
        sns.kdeplot(omb[valid_omb], color="dimgray", linewidth=2, ax=ax)
    if np.sum(valid_oma) > 1:
        sns.kdeplot(oma[valid_oma], color="red", linewidth=2, ax=ax)

    ax.set_xlabel("Value")
    ax.set_ylabel("Density")

    # Main title (left-aligned)
    fig.text(
        0.12, 0.93,
        f"{title_label} ({qc_label}==0)",
        ha="left",
        fontsize=12
    )

    # Subtitle (count)
    fig.text(
        0.18, 0.87,
        f"N assimilated = {n_omb}",
        ha="left",
        fontsize=9
    )

    ax.legend(
        handles=[
            plt.Line2D([0], [0], color="dimgray", lw=2, label="OMB"),
            plt.Line2D([0], [0], color="red", lw=2, label="OMA")
        ],
        loc="upper right",
        fontsize=8,
        frameon=False
    )

    # GNSSRO special x-axis expansion
    if "GNSSRO" in title_label.upper():
        xmin, xmax = ax.get_xlim()
        center = 0.5 * (xmin + xmax)
        half = 0.5 * (xmax - xmin)
        ax.set_xlim(center - 0.2 * half, center + 0.2 * half)

    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {outpath}")


# ============================================================
# Main Orchestrator
# ============================================================

class ObsDiagPlotter:
    def __init__(self, config):
        self.config = config

    def run(self):
        obs_list = self.config.get("observations", [])
        for obs_cfg in obs_list:
            label = obs_cfg["label"]
            otype = obs_cfg["type"]
            var = obs_cfg["variable"]
            diag = obs_cfg.get("diag", obs_cfg.get("file"))
            outdir = obs_cfg.get("outdir", "./plot-outputs-obs")
            diags_cfg = obs_cfg.get("diagnostics", {})

            print(f"[INFO] Processing {label} ({otype}) from {diag}")
            with Dataset(diag, "r") as f:

                # ============================================================
                # ATMS
                # ============================================================
                if otype == "atms":

                    if diags_cfg.get("hist", False):
                        self._plot_atms_histograms(f, var, label, outdir)

                    if diags_cfg.get("stats", False):
                        print(f"[INFO] Generating ATMS stats for {label}")
                        plot_stats_atms(f, var, label, outdir)

                    if diags_cfg.get("extended", False):
                        print(f"[INFO] Generating ATMS extended stats for {label}")
                        plot_stats_atms_extended(f, var, label, outdir)

                    if diags_cfg.get("scanpos", False):
                        print(f"[INFO] Generating ATMS scan-position diagnostics for {label}")
                        plot_scan_position_atms(f, var, label, outdir)

                    if diags_cfg.get("latbins", False):
                        print(f"[INFO] Generating ATMS latitude-binned diagnostics for {label}")
                        plot_latbins_atms(f, var, label, outdir)

                # ============================================================
                # Scalar
                # ============================================================
                elif otype == "scalar":
                    if diags_cfg.get("hist", False):
                        self._plot_scalar_hist(f, var, label, outdir)

                # ============================================================
                # Vector (e.g., winds)
                # ============================================================
                elif otype == "vector":
                    if diags_cfg.get("hist", False):
                        self._plot_vector_hist(f, label, outdir)

                else:
                    print(f"[WARN] Unknown type {otype} for {label}")

        print("[INFO] Diagnostics complete.")


    # ============================================================
    # ATMS Histograms
    # ============================================================

    def _plot_atms_histograms(self, f, varname, label, outdir):
        obs = load_obsvalue(f, varname)
        omb = load_omb(f, varname)
        oma = load_oma_explicit(f, varname)

        if obs is None or omb is None or oma is None:
            print(f"[SKIP] {label}: missing Obs/OMB/OMA")
            return

        qc = load_qc_universal(f, varname)
        if qc.ndim == 1:
            qc = np.repeat(qc[:, None], obs.shape[1], axis=1)

        nchan = obs.shape[1]
        for ch in range(nchan):
            ch_idx = ch + 1
            ch_label = f"{label} Ch {ch_idx:02d} Histogram"
            outpath = os.path.join(outdir, f"{label.lower()}_ch{ch_idx:02d}_hist.png")

            unified_histogram(
                omb[:, ch],
                oma[:, ch],
                qc[:, ch],
                ch_label,
                outpath,
                qc_label="QC2",
            )


    # ============================================================
    # Scalar Histograms
    # ============================================================

    def _plot_scalar_hist(self, f, varname, label, outdir):
        obs = load_obsvalue(f, varname)
        omb = load_omb(f, varname)
        oma = load_oma_explicit(f, varname)

        if obs is None and omb is None and oma is None:
            print(f"[SKIP] {label}: no Obs/OMB/OMA")
            return

        if omb is None:
            print(f"[INFO] {label}: No OMB found — using ObsValue only")
            omb = obs
        if oma is None:
            print(f"[INFO] {label}: No OMA found — using ObsValue only")
            oma = obs

        qc = load_qc_universal(f, varname)

        title_label = f"{label} Histogram"
        outpath = os.path.join(outdir, f"{label.lower()}_hist.png")

        unified_histogram(
            omb,
            oma,
            qc,
            title_label,
            outpath,
            qc_label="QC",
        )


    # ============================================================
    # Vector Histograms (U/V winds)
    # ============================================================

    def _plot_vector_hist(self, f, label, outdir):
        u_name = "windEastward"
        v_name = "windNorthward"

        omb_u = load_omb(f, u_name)
        oma_u = load_oma_explicit(f, u_name)
        omb_v = load_omb(f, v_name)
        oma_v = load_oma_explicit(f, v_name)

        if omb_u is None or oma_u is None or omb_v is None or oma_v is None:
            print(f"[SKIP] {label}: missing OMB/OMA for vector components")
            return

        qc_u = load_qc_universal(f, u_name)
        qc_v = load_qc_universal(f, v_name)

        unified_histogram(
            omb_u,
            oma_u,
            qc_u,
            f"{label} windEastward",
            os.path.join(outdir, f"{label.lower()}_u_hist.png"),
            qc_label="QC1",
        )

        unified_histogram(
            omb_v,
            oma_v,
            qc_v,
            f"{label} windNorthward",
            os.path.join(outdir, f"{label.lower()}_v_hist.png"),
            qc_label="QC1",
        )
