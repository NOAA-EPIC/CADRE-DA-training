#!/usr/bin/env python3

import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import griddata

from spectra_core import SpectraCore


# ---------------------------------------------------------
# Load background field (single ATM file, 6 tiles → global lat/lon)
# ---------------------------------------------------------
def load_bkg_field_global(atm_file, varname, level):
    with Dataset(atm_file) as nc:
        lon = nc["lon"][:]   # (tile, grid_yt, grid_xt)
        lat = nc["lat"][:]   # (tile, grid_yt, grid_xt)

        fields = []
        lons = []
        lats = []

        for t in range(6):
            f_tile = nc[varname][0, t, level, :, :]
            fields.append(f_tile.flatten())
            lons.append(lon[t].flatten())
            lats.append(lat[t].flatten())

        field_global = np.concatenate(fields)
        lon_global   = np.concatenate(lons)
        lat_global   = np.concatenate(lats)

    # Regrid to regular lat-lon like SpectraCore.build_global
    lon_new = np.linspace(-180, 180, 360)
    lat_new = np.linspace(-90, 90, 181)
    Lon, Lat = np.meshgrid(lon_new, lat_new)

    field_interp = griddata(
        points=(lon_global, lat_global),
        values=field_global,
        xi=(Lon, Lat),
        method="nearest"
    )

    return field_interp


# ---------------------------------------------------------
# Background: overlay bkg + inc + percentage text (boxed)
# ---------------------------------------------------------
def plot_bkg_overlay(k, Ek_bkg, Ek_inc, long_name, level, outname, pct_text):
    fig, ax = plt.subplots(figsize=(7, 5))

    # Background
    ax.loglog(k, Ek_bkg, color="k", linewidth=1.5, label="Background")

    # Increment overlay
    ax.loglog(k, Ek_inc, color="tab:red", linewidth=1.5, label="Increment")

    # More specific title
    ax.set_title(
        f"{long_name} Isotropic Spectra — Background vs Increment (Level {level})"
    )

    ax.set_xlabel("Total wavenumber k")
    ax.set_ylabel("E(k)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()

    # Annotation block (black text, smaller font, boxed)
    ax.text(
        0.02, 0.02,
        pct_text + "\n"
        "Expected DA contribution:\n"
        "  Large scales (k<10): 0.5–5%\n"
        "  Mid scales (10<k<40): 0.1–1%\n"
        "  Small scales (k>40): 0.01–0.1%",
        transform=ax.transAxes,
        fontsize=8,
        color="black",
        verticalalignment="bottom",
        bbox=dict(
            facecolor="white",
            edgecolor="black",
            boxstyle="round,pad=0.3",
            alpha=0.7
        )
    )

    fig.tight_layout()
    fig.savefig(outname, dpi=150)
    plt.close()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    # --- YAML handling (supports --yaml or positional) ---
    if "--yaml" in sys.argv:
        idx = sys.argv.index("--yaml")
        yaml_file = sys.argv[idx + 1]
    else:
        yaml_file = sys.argv[1]

    with open(yaml_file) as f:
        cfg = yaml.safe_load(f)

    bkg_cfg = cfg["background"]
    inc_cfg = cfg["increments"]
    map_cfg = cfg["mapping"]
    spec_cfg = cfg["spectra"]

    atm_file = bkg_cfg["atm_file"]
    levels = spec_cfg["levels"]
    outdir = spec_cfg["output_dir"]
    os.makedirs(outdir, exist_ok=True)

    # SpectraCore instance for increments
    core = SpectraCore(grid_prefix=inc_cfg["grid_prefix"], suffix=".nc")

    for entry in map_cfg:
        bkg_name  = entry["bkg"]
        inc_name  = entry["inc"]
        long_name = entry.get("long_name", inc_name)

        core.varname = inc_name  # set increment variable

        for lev in levels:
            print(f"Processing {long_name} at level {lev}")

            # --- Background: single ATM file, 6 tiles → global ---
            bkg_field = load_bkg_field_global(atm_file, bkg_name, lev)
            spec_bkg = core.isotropic_spectrum(bkg_field)

            # --- Increment: 6 tiles via SpectraCore.build_global ---
            Lon, Lat, inc_field = core.build_global(inc_cfg["prefix"], lev)
            spec_inc = core.isotropic_spectrum(inc_field)

            k = np.arange(len(spec_bkg))

            # --- Percentage contribution ---
            percent = 100.0 * spec_inc / np.maximum(spec_bkg, 1e-12)
            pmin = np.nanmin(percent)
            pmax = np.nanmax(percent)
            pct_text = f"Increment contribution: {pmin:.3f}% – {pmax:.3f}%"

            # --- Background figure only ---
            outname_bkg = os.path.join(
                outdir, f"bkg_{inc_name}_L{lev}.png"
            )
            plot_bkg_overlay(k, spec_bkg, spec_inc, long_name, lev, outname_bkg, pct_text)

    print("Done.")


if __name__ == "__main__":
    main()
