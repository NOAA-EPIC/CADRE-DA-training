#!/usr/bin/env python3

import argparse
import yaml
import os

from spectra_core import SpectraCore
from plots import SpectraPlotter


def main():
    parser = argparse.ArgumentParser(description="FV3-JEDI Spectral Diagnostics (Tiles → Lat/Lon)")
    parser.add_argument("--config", "--yaml", dest="config", required=True,
                        help="YAML configuration file")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    vars_list  = cfg["vars"]
    levels     = cfg["levels"]
    exps       = cfg["experiments"]
    outdir     = cfg.get("output_dir", "./plot-outputs")
    nicas_L    = cfg.get("nicas_length_scale", None)

    if "grid" in cfg and "prefix" in cfg["grid"]:
        grid_prefix = cfg["grid"]["prefix"]
    else:
        grid_prefix = cfg["grid_prefix"]

    os.makedirs(outdir, exist_ok=True)

    ctrl = exps[0]
    exp  = exps[1]

    ctrl_name   = ctrl["name"]
    ctrl_prefix = ctrl["prefix"]
    exp_name    = exp["name"]
    exp_prefix  = exp["prefix"]

    print("\n==============================================")
    print(" FV3-JEDI Spectral Diagnostics (Tiles → Lat/Lon)")
    print("==============================================")
    print(f" CTRL: {ctrl_name} → {ctrl_prefix}")
    print(f" EXP:  {exp_name} → {exp_prefix}")
    print(f" Vars: {vars_list}")
    print(f" Levels: {levels}")
    print(f" Grid prefix: {grid_prefix}")
    print(f" Output dir: {outdir}")
    print("==============================================\n")

    spec_plotter = SpectraPlotter()

    for var in vars_list:
        print(f"\n=== Processing variable: {var} ===")

        core = SpectraCore(varname=var, grid_prefix=grid_prefix)
        print("Loading global fields for all 127 levels...")
        core.load_fields(ctrl_prefix, exp_prefix, nlevels=127)

        for lev in levels:
            print(f"  → Level {lev}")

            outname = (
                f"{outdir}/"
                f"{var}_{ctrl_name}_vs_{exp_name}_spectra_L{lev}.png"
            )

            spec_plotter.plot_spectra(
                core, lev, ctrl_name, exp_name,
                fname=outname,
                nicas_length_scale=nicas_L
            )

    print("\nAll spectral diagnostics complete.\n")


if __name__ == "__main__":
    main()
