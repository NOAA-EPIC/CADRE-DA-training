#!/usr/bin/env python3

import yaml
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import sys

# ---------------------------------------------------------
# Load FV3 tile increment
# ---------------------------------------------------------
def load_tile(prefix, tile, var, level):
    path = f"{prefix}{tile}.nc"
    with Dataset(path) as nc:
        data = nc[var][0, level, :, :]
    return data

# ---------------------------------------------------------
# Load FV3 grid tile (corner → center)
# ---------------------------------------------------------
def load_grid(grid_prefix, tile):
    path = f"{grid_prefix}{tile}.nc"
    with Dataset(path) as nc:
        lon = nc["x"][:]
        lat = nc["y"][:]

    lon_c = 0.25 * (lon[0:-1:2, 0:-1:2] +
                    lon[1::2,   0:-1:2] +
                    lon[0:-1:2, 1::2] +
                    lon[1::2,   1::2])

    lat_c = 0.25 * (lat[0:-1:2, 0:-1:2] +
                    lat[1::2,   0:-1:2] +
                    lat[0:-1:2, 1::2] +
                    lat[1::2,   1::2])

    lon_c = (lon_c + 180) % 360 - 180
    return lon_c, lat_c

# ---------------------------------------------------------
# FV3 127-level pressure grid (mbar)
# ---------------------------------------------------------
PFULL_MBAR = np.array([
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    1,1,2,2,3,4,5,7,8,
    10,12,14,16,19,21,24,28,31,35,39,43,47,52,56,61,67,72,
    78,84,90,97,104,112,120,128,136,145,154,164,174,184,195,
    207,219,231,243,256,270,283,297,312,326,342,357,373,389,
    405,421,438,454,471,488,505,522,539,555,572,589,605,621,
    637,653,668,683,698,713,727,741,754,767,780,792,804,815,
    826,837,847,857,866,875,884,892,900,907,914,921,928,934,
    940,945,950,955,960,965,969,973,977,980,984,987,990,993,
    995,998
])

def load_pressure(level):
    return float(PFULL_MBAR[level])

# ---------------------------------------------------------
# Build global lat/lon field from 6 tiles
# ---------------------------------------------------------
def build_global(prefix, grid_prefix, var, level):
    fields = []
    lons = []
    lats = []

    for t in range(1, 7):
        fields.append(load_tile(prefix, t, var, level))
        lon_c, lat_c = load_grid(grid_prefix, t)
        lons.append(lon_c)
        lats.append(lat_c)

    field_flat = np.concatenate([f.flatten() for f in fields])
    lon_flat   = np.concatenate([g.flatten() for g in lons])
    lat_flat   = np.concatenate([g.flatten() for g in lats])

    lon_new = np.linspace(-180, 180, 360)
    lat_new = np.linspace(-90, 90, 181)
    Lon, Lat = np.meshgrid(lon_new, lat_new)

    field_interp = griddata(
        (lon_flat, lat_flat),
        field_flat,
        (Lon, Lat),
        method="nearest"
    )

    return Lon, Lat, field_interp

# ---------------------------------------------------------
# Compute zonal mean for all 127 levels
# ---------------------------------------------------------
def compute_zonal_mean_full(prefix, grid_prefix, var):
    nlev = len(PFULL_MBAR)
    lat_new = np.linspace(-90, 90, 181)
    zm = np.zeros((nlev, len(lat_new)))

    for lev in range(nlev):
        _, Lat, field = build_global(prefix, grid_prefix, var, lev)
        zm[lev, :] = np.nanmean(field, axis=1)

    return zm, lat_new, PFULL_MBAR
# ---------------------------------------------------------
# Contrast settings for T/u/v
# ---------------------------------------------------------
MAP_VMIN = -5
MAP_VMAX = 5
DIFF_VMIN = -1.0
DIFF_VMAX = 1.0

# ---------------------------------------------------------
# Humidity-specific ranges (WIDER → less colorful)
# ---------------------------------------------------------
def get_map_limits(var, is_diff=False):
    v = var.lower()
    if "sphum" in v or "qv" in v or "q_inc" in v:
        if is_diff:
            return -4e-4, 4e-4     # wider → softer colors
        else:
            return -1.5e-3, 1.5e-3 # wider → softer colors
    else:
        return (DIFF_VMIN, DIFF_VMAX) if is_diff else (MAP_VMIN, MAP_VMAX)

# ---------------------------------------------------------
# Tapered horizontal colorbar helper
# ---------------------------------------------------------
def tapered_colorbar(fig, im, ax, label=None):
    # Create colorbar
    cbar = fig.colorbar(
        im, ax=ax,
        orientation="horizontal",
        pad=0.12,
        fraction=0.03,
        aspect=30
    )
    cbar.ax.tick_params(labelsize=7)

    pos = cbar.ax.get_position()
    cbar.ax.set_position([
        pos.x0,          # left
        pos.y0 + 0.03,   # bottom (move up by +0.03)
        pos.width,       # width
        pos.height       # height
    ])
    
    if label:
        cbar.set_label(label, fontsize=8)

    cbar.formatter.set_powerlimits((-2, 2))
    cbar.update_ticks()

    # --- CRITICAL: force layout BEFORE adding taper ---
    fig.canvas.draw()

    return cbar

# ---------------------------------------------------------
# Plot 1‑panel increment map
# ---------------------------------------------------------
def plot_single(Lon, Lat, field, var, lev, exp_name, prefix, outname):
    pressure = load_pressure(lev)
    title = f"{var} – Level {lev} ({pressure:.1f} mbar) – {exp_name}"

    vmin, vmax = get_map_limits(var, is_diff=False)

    fig = plt.figure(figsize=(10, 5))
    fig.subplots_adjust(top=0.88)

    fig.suptitle(title, y=0.96, x=0.15, ha="left")

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

    im = ax.pcolormesh(Lon, Lat, field, cmap="coolwarm",
                       shading="auto", vmin=vmin, vmax=vmax)

    tapered_colorbar(fig, im, ax, label=f"{var} Increment") 

    plt.savefig(outname, dpi=150)
    plt.close()

# ---------------------------------------------------------
# Plot 3‑panel increment map
# ---------------------------------------------------------
def plot_three(Lon, Lat, ctrl, exp, var, lev, ctrl_name, exp_name, outname):
    diff = exp - ctrl
    pressure = load_pressure(lev)
    title = f"{var} – Level {lev} ({pressure:.1f} mbar)"

    vmin_map, vmax_map = get_map_limits(var, is_diff=False)
    vmin_diff, vmax_diff = get_map_limits(var, is_diff=True)

    fig = plt.figure(figsize=(18, 5), constrained_layout=True)
    fig.suptitle(title, y=0.95)

    axes = fig.subplots(1, 3, subplot_kw={"projection": ccrs.PlateCarree()})

    # CTRL
    ax = axes[0]
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    im0 = ax.pcolormesh(Lon, Lat, ctrl, cmap="coolwarm",
                        shading="auto", vmin=vmin_map, vmax=vmax_map)
    ax.set_title(ctrl_name)
    tapered_colorbar(fig, im0, ax)

    # EXP
    ax = axes[1]
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    im1 = ax.pcolormesh(Lon, Lat, exp, cmap="coolwarm",
                        shading="auto", vmin=vmin_map, vmax=vmax_map)
    ax.set_title(exp_name)
    tapered_colorbar(fig, im1, ax)

    # DIFF
    ax = axes[2]
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    im2 = ax.pcolormesh(Lon, Lat, diff, cmap="coolwarm",
                        shading="auto", vmin=vmin_diff, vmax=vmax_diff)
    ax.set_title(f"{exp_name} – {ctrl_name}")
    tapered_colorbar(fig, im2, ax)

    plt.savefig(outname, dpi=150)
    plt.close()

# ---------------------------------------------------------
# Zonal‑mean (single experiment)
# ---------------------------------------------------------
def plot_zonal_mean_colormap(lat, pressure, zm, var, exp_name, outname):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Prevent colorbar overlap
    fig.subplots_adjust(bottom=0.20)

    cs = ax.contourf(lat, pressure, zm, levels=31,
                     cmap="RdBu_r", extend="both")

    ax.contour(lat, pressure, zm, levels=10,
               colors="k", linewidths=0.3, alpha=0.5)

    ax.set_yscale("log")
    ax.invert_yaxis()

    ax.axhline(200, color="k", linestyle="--", linewidth=0.3, alpha=0.5)

    ax.text(0, 250, "Jet Level",
            ha="center", va="bottom",
            fontsize=6, color="k",
            alpha=0.5,
            bbox=dict(facecolor="white", alpha=0.3, edgecolor="none"))

    ax.set_ylabel("Pressure (mbar)")
    ax.set_xlabel("Latitude")
    ax.set_title(f"{var} Zonal Mean – {exp_name}")

    tapered_colorbar(fig, cs, ax, label=f"{var} Increment")

    fig.savefig(outname, dpi=150)
    plt.close()

# ---------------------------------------------------------
# Zonal‑mean (CTRL | EXP | DIFF)
# ---------------------------------------------------------
def plot_zonal_mean_colormap_three(lat, pressure, zm_ctrl, zm_exp,
                                   var, ctrl_name, exp_name, outname):

    zm_diff = zm_exp - zm_ctrl

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)
    fig.suptitle(f"{var} Zonal Mean Cross‑Section", y=1.05)

    panels = [(zm_ctrl, ctrl_name),
              (zm_exp,  exp_name),
              (zm_diff, f"{exp_name} – {ctrl_name}")]

    for ax, (data, title) in zip(axes, panels):
        cs = ax.contourf(lat, pressure, data, levels=31,
                         cmap="RdBu_r", extend="both")

        ax.contour(lat, pressure, data, levels=10,
                   colors="k", linewidths=0.3, alpha=0.5)

        ax.set_yscale("log")
        ax.invert_yaxis()

        ax.axhline(200, color="k", linestyle="--", linewidth=0.6, alpha=0.5)

        ax.text(0, 250, "Jet Level",
                ha="center", va="bottom",
                fontsize=7, color="k",
                fontweight="normal",
                alpha=0.6,
                bbox=dict(facecolor="white", alpha=0.3, edgecolor="none"))

        ax.set_title(title)
        ax.set_xlabel("Latitude")
        ax.set_ylabel("Pressure (mbar)")

        tapered_colorbar(fig, cs, ax, label=f"{var} Increment")

    fig.savefig(outname, dpi=150)
    plt.close()
# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    if "--yaml" in sys.argv:
        idx = sys.argv.index("--yaml")
        yaml_file = sys.argv[idx + 1]
    else:
        yaml_file = sys.argv[1]

    with open(yaml_file) as f:
        cfg = yaml.safe_load(f)

    vars_ = cfg["vars"]
    levels = cfg["levels"]
    exps = cfg["experiments"]
    zm_cfg = cfg.get("zonal_mean", {"enabled": False})

    if "grid" in cfg and "prefix" in cfg["grid"]:
        grid_prefix = cfg["grid"]["prefix"]
    else:
        raise KeyError("YAML must contain grid: prefix: /path/to/C96_grid.tile")

    outdir = cfg["output_dir"]
    os.makedirs(outdir, exist_ok=True)

    nexp = len(exps)

    # -------------------------
    # SINGLE EXPERIMENT MODE
    # -------------------------
    if nexp == 1:
        exp = exps[0]

        for var in vars_:
            for lev in levels:
                print(f"[1‑exp] {var} level {lev}")
                Lon, Lat, field = build_global(exp["prefix"], grid_prefix, var, lev)
                outname = f"{outdir}/{var}_L{lev}_{exp['name']}.png"
                plot_single(Lon, Lat, field, var, lev, exp["name"], exp["prefix"], outname)

        if zm_cfg.get("enabled", False):
            for var in vars_:
                print(f"[1‑exp] Zonal mean full vertical: {var}")
                zm, lat, pressure = compute_zonal_mean_full(exp["prefix"], grid_prefix, var)
                outname = f"{outdir}/{var}_zonal_mean_full_{exp['name']}.png"
                plot_zonal_mean_colormap(lat, pressure, zm, var, exp["name"], outname)

        print("Done (single experiment mode).")
        return

    # -------------------------
    # TWO EXPERIMENT MODE
    # -------------------------
    if nexp == 2:
        ctrl = exps[0]
        exp  = exps[1]

        for var in vars_:
            for lev in levels:
                print(f"[2‑exp] {var} level {lev}")
                Lon, Lat, ctrl_field = build_global(ctrl["prefix"], grid_prefix, var, lev)
                _,   _,   exp_field  = build_global(exp["prefix"],  grid_prefix, var, lev)

                outname = f"{outdir}/{var}_L{lev}_{ctrl['name']}_vs_{exp['name']}.png"
                plot_three(Lon, Lat, ctrl_field, exp_field,
                           var, lev, ctrl["name"], exp["name"], outname)

        if zm_cfg.get("enabled", False):
            for var in vars_:
                print(f"[2‑exp] Zonal mean full vertical: {var}")

                zm_ctrl, lat, pressure = compute_zonal_mean_full(ctrl["prefix"], grid_prefix, var)
                zm_exp,  _,   _        = compute_zonal_mean_full(exp["prefix"],  grid_prefix, var)

                outname = f"{outdir}/{var}_zonal_mean_full_{ctrl['name']}_vs_{exp['name']}.png"
                plot_zonal_mean_colormap_three(lat, pressure,
                                               zm_ctrl, zm_exp,
                                               var, ctrl["name"], exp["name"],
                                               outname)

        print("Done (two experiment mode).")
        return

    print("ERROR: Only 1 or 2 experiments supported.")
    return


if __name__ == "__main__":
    main()
