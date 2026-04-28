#!/usr/bin/env python3
"""
JEDI Log Parser — Comprehensive Diagnostic Report Generator
============================================================
Parses a JEDI variational DA log file and produces a full diagnostic report.

Usage:
    python parse_jedi_log.py <jedi_log_file> [--output report.txt]
"""

import re
import sys
import argparse
from collections import OrderedDict


def parse_configuration(lines):
    config = {}
    full_text = "\n".join(lines[:200])

    m = re.search(r'cost type => (\S+)', full_text)
    if m: config['cost_type'] = m.group(1)

    m = re.search(r'datetime => (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', full_text)
    if m: config['analysis_time'] = m.group(1)

    m = re.search(r'time window => \{begin => (\S+)\s*,\s*length => (\S+)', full_text)
    if m:
        config['window_begin'] = m.group(1)
        config['window_length'] = m.group(2)

    m = re.search(r'npx => (\d+)\s*,\s*npy => (\d+)\s*,\s*npz => (\d+)', full_text)
    if m:
        config['outer_resolution'] = f"C{int(m.group(1)) - 1}"
        config['nlevels'] = int(m.group(3))

    weights = re.findall(r'weight => \{value => ([\d.]+)\}', full_text)
    if len(weights) >= 2:
        config['static_weight'] = float(weights[0])
        config['ensemble_weight'] = float(weights[1])

    m = re.search(r'nmembers => (\d+)', full_text)
    if m: config['ensemble_members'] = int(m.group(1))

    m = re.search(r'algorithm => (\w+)', full_text)
    if m: config['minimizer'] = m.group(1)

    ninner_vals = re.findall(r'ninner => (\d+)', full_text)
    if ninner_vals: config['ninner'] = [int(n) for n in ninner_vals]

    inner_npx = re.findall(r'npx => (\d+)', full_text)
    if len(inner_npx) >= 2:
        config['inner_resolution'] = f"C{int(inner_npx[1]) - 1}"

    return config


def parse_obs_counts(lines):
    obs_counts = OrderedDict()

    # Total loaded locations (nlocs)
    nlocs_pattern = re.compile(
        r'^(\S+(?:\s+\S+)?)\s+(\S+)\s+nlocs\s*=\s*(\d+),\s*nobs\s*=\s*(\d+)',
    )
    for line in lines:
        m = nlocs_pattern.match(line.strip())
        if m:
            obs_type = m.group(1).strip()
            nlocs = int(m.group(3))
            if obs_type not in obs_counts:
                obs_counts[obs_type] = {
                    'nlocs': 0, 'nobs_total': 0,
                    'nobs_assimilated': 0, 'nobs_per_var': OrderedDict(),
                }
            obs_counts[obs_type]['nlocs'] = nlocs

    # Total obs before QC (from "CostJo Observations" block)
    costjo_obs_pattern = re.compile(r'^(\S+(?:\s+\S+)?)\s+nobs=\s*(\d+)\s+Min=')
    in_costjo_obs = False
    seen_total = set()
    for line in lines:
        stripped = line.strip()
        if 'CostJo Observations:' in stripped:
            in_costjo_obs = True
            continue
        if in_costjo_obs:
            m = costjo_obs_pattern.match(stripped)
            if m:
                obs_type = m.group(1).strip()
                nobs = int(m.group(2))
                if obs_type not in seen_total:
                    if obs_type in obs_counts:
                        obs_counts[obs_type]['nobs_total'] = nobs
                    else:
                        obs_counts[obs_type] = {
                            'nlocs': 0, 'nobs_total': nobs,
                            'nobs_assimilated': 0, 'nobs_per_var': OrderedDict(),
                        }
                    seen_total.add(obs_type)
            if 'Jo Observations:' in stripped and 'CostJo' not in stripped:
                break

    # Assimilated obs (from first CostJo Nonlinear block)
    costjo_pattern = re.compile(
        r'CostJo\s*:\s*Nonlinear\s+Jo\((.+?)\)\s*=\s*([\d.e+\-]+),\s*nobs\s*=\s*(\d+)'
    )
    seen_first = set()
    for line in lines:
        m = costjo_pattern.search(line.strip())
        if m:
            obs_type = m.group(1).strip()
            nobs = int(m.group(3))
            if obs_type not in seen_first:
                if obs_type in obs_counts:
                    obs_counts[obs_type]['nobs_assimilated'] = nobs
                seen_first.add(obs_type)

    # Per-variable assimilated obs (from Jo Obs lines)
    jo_obs_pattern = re.compile(
        r'Jo Obs\s*:(\S+(?:\s+\S+)?):(\S+)\s*:\s*Nobs=\s*(\d+)'
    )
    seen_jo = set()
    for line in lines:
        m = jo_obs_pattern.search(line.strip())
        if m:
            obs_type, variable = m.group(1).strip(), m.group(2).strip()
            key = (obs_type, variable)
            if key not in seen_jo:
                if obs_type in obs_counts:
                    obs_counts[obs_type]['nobs_per_var'][variable] = int(m.group(3))
                seen_jo.add(key)

    return obs_counts


def parse_jo_evolution(lines):
    costjo_pattern = re.compile(
        r'CostJo\s*:\s*Nonlinear\s+Jo\((.+?)\)\s*=\s*([\d.e+\-]+),\s*nobs\s*=\s*(\d+),\s*Jo/n\s*=\s*([\d.e+\-]+),\s*err\s*=\s*([\d.e+\-]+)'
    )
    jo_data = OrderedDict()
    for line in lines:
        m = costjo_pattern.search(line.strip())
        if m:
            obs_type = m.group(1).strip()
            record = {
                'Jo': float(m.group(2)), 'nobs': int(m.group(3)),
                'Jo_n': float(m.group(4)), 'err': float(m.group(5)),
            }
            jo_data.setdefault(obs_type, []).append(record)

    total_pattern = re.compile(r'CostJo\s*:\s*Nonlinear\s+Jo\s*=\s*([\d.e+\-]+)')
    jo_total = []
    for line in lines:
        m = total_pattern.search(line.strip())
        if m and 'Jo(' not in line:
            jo_total.append(float(m.group(1)))

    return jo_data, jo_total


def parse_cost_convergence(lines):
    j_pattern = re.compile(r'Quadratic cost function:\s*J\s*\(\s*(\d+)\)\s*=\s*([\d.e+\-]+)')
    jb_pattern = re.compile(r'Quadratic cost function:\s*Jb\s*\(\s*(\d+)\)\s*=\s*([\d.e+\-]+)')
    jojc_pattern = re.compile(r'Quadratic cost function:\s*JoJc\(\s*(\d+)\)\s*=\s*([\d.e+\-]+)')

    j_vals, jb_vals, jojc_vals = [], [], []
    for line in lines:
        m = j_pattern.search(line)
        if m: j_vals.append((int(m.group(1)), float(m.group(2))))
        m = jb_pattern.search(line)
        if m: jb_vals.append((int(m.group(1)), float(m.group(2))))
        m = jojc_pattern.search(line)
        if m: jojc_vals.append((int(m.group(1)), float(m.group(2))))

    outer_loops, current = [], []
    for i, (it, j) in enumerate(j_vals):
        if it == 0 and current:
            outer_loops.append(current)
            current = []
        rec = {'iter': it, 'J': j}
        if i < len(jb_vals): rec['Jb'] = jb_vals[i][1]
        if i < len(jojc_vals): rec['JoJc'] = jojc_vals[i][1]
        current.append(rec)
    if current: outer_loops.append(current)
    return outer_loops


def parse_departures(lines):
    dep_pattern = re.compile(
        r'Jo Dep\s*:(\S+(?:\s+\S+)?):(\S+)\s*:\s*Nobs=\s*(\d+),\s*Min=\s*([\d.e+\-]+),\s*Max=\s*([\d.e+\-]+),\s*RMS=\s*([\d.e+\-]+)'
    )
    departures, seen = OrderedDict(), set()
    for line in lines:
        m = dep_pattern.search(line.strip())
        if m:
            key = (m.group(1).strip(), m.group(2).strip())
            if key not in seen:
                departures[key] = {
                    'Nobs': int(m.group(3)), 'Min': float(m.group(4)),
                    'Max': float(m.group(5)), 'RMS': float(m.group(6)),
                }
                seen.add(key)
    return departures


def parse_obs_errors(lines):
    err_pattern = re.compile(
        r'^(\S+(?:\s+\S+)?)\s+nobs=\s*(\d+)\s+Min=([\d.e+\-]+),\s*Max=([\d.e+\-]+),\s*RMS=([\d.e+\-]+)'
    )
    errors, in_err, seen = OrderedDict(), False, set()
    for line in lines:
        stripped = line.strip()
        if 'Diagonal observation error covariance' in stripped:
            in_err = True; continue
        if in_err:
            m = err_pattern.match(stripped)
            if m:
                obs_type = m.group(1).strip()
                if obs_type not in seen:
                    errors[obs_type] = {
                        'nobs': int(m.group(2)), 'Min': float(m.group(3)),
                        'Max': float(m.group(4)), 'RMS': float(m.group(5)),
                    }
                    seen.add(obs_type)
        if 'CostJo' in stripped and 'Nonlinear' in stripped: break
    return errors


def generate_report(config, obs_counts, jo_data, jo_total, convergence, departures, obs_errors):
    out = []
    sep = "=" * 80

    out.append(sep)
    out.append("  JEDI Variational DA - Diagnostic Report")
    out.append(sep)
    out.append("")

    # 1. Config
    out.append("-" * 80)
    out.append("  1. CONFIGURATION SUMMARY")
    out.append("-" * 80)
    for key, val in config.items():
        out.append(f"  {key.replace('_',' ').title():<30s}: {val}")
    out.append("")

    # 2. Obs Counts
    out.append("-" * 80)
    out.append("  2. OBSERVATION COUNTS")
    out.append("-" * 80)
    out.append("")
    out.append(f"  {'Obs Type':<30s} {'Locations':>12s} {'Total Obs':>12s} {'Assimilated':>12s} {'Rejected':>10s} {'Assim%':>8s}")
    out.append(f"  {'-'*30} {'-'*12} {'-'*12} {'-'*12} {'-'*10} {'-'*8}")
    g_nlocs, g_total, g_assim = 0, 0, 0
    for obs_type, c in obs_counts.items():
        rej = c['nobs_total'] - c['nobs_assimilated']
        pct = (c['nobs_assimilated'] / c['nobs_total'] * 100) if c['nobs_total'] > 0 else 0
        out.append(f"  {obs_type:<30s} {c['nlocs']:>12,d} {c['nobs_total']:>12,d} {c['nobs_assimilated']:>12,d} {rej:>10,d} {pct:>7.1f}%")
        g_nlocs += c['nlocs']; g_total += c['nobs_total']; g_assim += c['nobs_assimilated']
        if len(c['nobs_per_var']) > 1:
            for var, n in c['nobs_per_var'].items():
                out.append(f"    +-- {var:<26s} {'':>12s} {'':>12s} {n:>12,d}")
    out.append(f"  {'-'*30} {'-'*12} {'-'*12} {'-'*12} {'-'*10} {'-'*8}")
    g_pct = (g_assim / g_total * 100) if g_total > 0 else 0
    out.append(f"  {'TOTAL':<30s} {g_nlocs:>12,d} {g_total:>12,d} {g_assim:>12,d} {g_total-g_assim:>10,d} {g_pct:>7.1f}%")
    out.append("")
    out.append("  Locations = unique obs locations (nlocs).")
    out.append("  Total Obs = nlocs x channels/variables (before QC).")
    out.append("  Assimilated = obs passing all QC (used in Jo).")
    out.append("")

    # 3. Jo/n Evolution
    n_outers = max(len(v) for v in jo_data.values())
    out.append("-" * 80)
    out.append("  3. Jo/n EVOLUTION ACROSS OUTER ITERATIONS")
    out.append("-" * 80)
    out.append("")
    hdr = f"  {'Obs Type':<30s}" + "".join(f" {'Outer '+str(i):>12s}" for i in range(n_outers)) + f" {'Delta':>14s}"
    out.append(hdr)
    out.append(f"  {'-'*30}" + f" {'-'*12}" * n_outers + f" {'-'*14}")
    for obs_type, recs in jo_data.items():
        row = f"  {obs_type:<30s}" + "".join(f" {r['Jo_n']:>12.6f}" for r in recs)
        if len(recs) >= 2:
            row += f" {recs[-1]['Jo_n']-recs[0]['Jo_n']:>+14.6f}"
        out.append(row)
    out.append("")
    if jo_total:
        out.append(f"  Total Jo: {' -> '.join(f'{j:,.1f}' for j in jo_total)}")
        out.append(f"  Reduction: {(1 - jo_total[-1]/jo_total[0])*100:.1f}%")
    out.append("")

    # 4. Convergence
    out.append("-" * 80)
    out.append("  4. COST FUNCTION CONVERGENCE")
    out.append("-" * 80)
    out.append("")
    for li, loop in enumerate(convergence):
        out.append(f"  --- Outer Loop {li} ({len(loop)-1} inner iters) ---")
        out.append(f"  {'Iter':>6s} {'J':>16s} {'Jb':>16s} {'JoJc':>16s}")
        out.append(f"  {'-'*6} {'-'*16} {'-'*16} {'-'*16}")
        for r in loop:
            out.append(f"  {r['iter']:>6d} {r['J']:>16.2f} {r.get('Jb',0):>16.2f} {r.get('JoJc',0):>16.2f}")
        out.append("")

    # 5. Chi-Squared Summary
    out.append("-" * 80)
    out.append("  5. CHI-SQUARED CONSISTENCY (Final Iteration)")
    out.append("-" * 80)
    out.append("")
    out.append("  Jo ~ chi-squared(P).  E[Jo/P] = 1.0 if R,B correct.")
    out.append("")
    out.append(f"  {'Obs Type':<30s} {'Jo':>14s} {'P':>10s} {'Jo/P':>10s} {'Status':>22s}")
    out.append(f"  {'-'*30} {'-'*14} {'-'*10} {'-'*10} {'-'*22}")
    tjo, tp = 0, 0
    for ot, recs in jo_data.items():
        f = recs[-1]
        s = "!! OVERESTIMATED" if f['Jo_n'] < 0.5 else ("!! UNDERESTIMATED" if f['Jo_n'] > 1.5 else ("v R too large" if f['Jo_n'] < 0.8 else ("^ R too small" if f['Jo_n'] > 1.2 else "OK calibrated")))
        out.append(f"  {ot:<30s} {f['Jo']:>14.2f} {f['nobs']:>10,d} {f['Jo_n']:>10.6f} {s:>22s}")
        tjo += f['Jo']; tp += f['nobs']
    out.append(f"  {'-'*30} {'-'*14} {'-'*10} {'-'*10} {'-'*22}")
    tr = tjo/tp if tp else 0
    ts = "!! OVERESTIMATED" if tr < 0.5 else ("!! UNDERESTIMATED" if tr > 1.5 else "OK")
    out.append(f"  {'TOTAL':<30s} {tjo:>14.2f} {tp:>10,d} {tr:>10.6f} {ts:>22s}")
    out.append("")
    out.append(sep)
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="JEDI Log Parser")
    parser.add_argument("logfile", help="Path to JEDI log file")
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()

    with open(args.logfile, 'r') as f:
        raw = f.readlines()

    config = parse_configuration(raw)
    obs_counts = parse_obs_counts(raw)
    jo_data, jo_total = parse_jo_evolution(raw)
    convergence = parse_cost_convergence(raw)
    departures = parse_departures(raw)
    obs_errors = parse_obs_errors(raw)

    report = generate_report(config, obs_counts, jo_data, jo_total, convergence, departures, obs_errors)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
