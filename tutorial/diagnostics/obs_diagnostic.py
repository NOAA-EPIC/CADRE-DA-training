import argparse
import yaml

from plots.obs_diag_plotter import ObsDiagPlotter


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--yaml", required=True, help="YAML config for obs diagnostics")
    return p.parse_args()


def main():
    args = parse_args()
    with open(args.yaml, "r") as f:
        cfg = yaml.safe_load(f)

    print(f"[INFO] Loaded config: {args.yaml}")
    plotter = ObsDiagPlotter(cfg)
    plotter.run()


if __name__ == "__main__":
    main()
