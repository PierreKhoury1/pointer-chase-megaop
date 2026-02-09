import csv
import os
import shutil
import subprocess

DEPTHS = [2, 3, 5, 8]

# Assumed per-hop latency (cycles) by cache regime.
MEM_LATENCY = {
    "L1": 4.0,
    "L2": 12.0,
    "L3": 40.0,
    "DRAM": 200.0,
}

# Fixed overhead (cycles) for the hypothetical mega-op.
MEGA_OP_OVERHEAD = 2.0

# Baseline per-hop overheads (cycles) for a guarded loop.
BASE_GUARD_OVERHEAD = 2.0
BASE_LOOP_OVERHEAD = 1.0
BASE_FIXED_OVERHEAD = 2.0


def main():
    out_csv = "results_megaop_sim.csv"
    out_md = "results_megaop_sim.md"
    graph_dir = os.path.join("graphs", "megaop")
    os.makedirs(graph_dir, exist_ok=True)

    rows = []
    avg_by_workset = {}
    for workset in ("L1", "L2", "L3", "DRAM"):
        mem_lat = MEM_LATENCY.get(workset)
        if mem_lat is None:
            continue
        for depth in DEPTHS:
            baseline = BASE_FIXED_OVERHEAD + depth * (mem_lat + BASE_GUARD_OVERHEAD + BASE_LOOP_OVERHEAD)
            mega = MEGA_OP_OVERHEAD + mem_lat * depth
            speedup = baseline / mega if mega > 0 else 0.0
            rows.append(
                {
                    "workset": workset,
                    "depth": depth,
                    "baseline_cycles": baseline,
                    "mega_cycles": mega,
                    "speedup": speedup,
                }
            )

        speedups = [r["speedup"] for r in rows if r["workset"] == workset]
        avg_by_workset[workset] = sum(speedups) / len(speedups)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["workset", "depth", "baseline_cycles", "mega_cycles", "speedup"])
        for r in rows:
            writer.writerow(
                [
                    r["workset"],
                    r["depth"],
                    f"{r['baseline_cycles']:.6f}",
                    f"{r['mega_cycles']:.6f}",
                    f"{r['speedup']:.6f}",
                ]
            )

    with open(out_md, "w", newline="\n") as f:
        f.write("## Mega-op simulator (fixed-latency op)\n\n")
        f.write("- baseline model: guarded pointer-chase loop\n")
        f.write(f"- baseline fixed overhead: `{BASE_FIXED_OVERHEAD}` cycles\n")
        f.write(f"- baseline per-hop overhead: guard `{BASE_GUARD_OVERHEAD}` + loop `{BASE_LOOP_OVERHEAD}` cycles\n")
        f.write(f"- mega-op overhead: `{MEGA_OP_OVERHEAD}` cycles\n")
        f.write("- per-hop memory latency assumptions (cycles):\n")
        for k, v in MEM_LATENCY.items():
            f.write(f"  - {k}: {v}\n")
        f.write("\n")
        f.write("| workset | depth | baseline cycles/iter | mega-op cycles/iter | speedup |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for r in rows:
            f.write(
                f"| {r['workset']} | {r['depth']} | {r['baseline_cycles']:.3f} | "
                f"{r['mega_cycles']:.3f} | {r['speedup']:.3f} |\n"
            )
        f.write("\n### Avg speedup by workset\n\n")
        f.write("| workset | avg speedup |\n")
        f.write("|---|---:|\n")
        for workset, avg in avg_by_workset.items():
            f.write(f"| {workset} | {avg:.3f} |\n")

    # simple SVG plot (avg speedup vs workset)
    workset_order = ["L1", "L2", "L3", "DRAM"]
    values = [avg_by_workset.get(w) for w in workset_order if w in avg_by_workset]

    out_svg = os.path.join(graph_dir, "megaop_speedup_vs_workset.svg")
    W, H = 900, 520
    margin = dict(l=70, r=30, t=30, b=70)
    plot_w = W - margin["l"] - margin["r"]
    plot_h = H - margin["t"] - margin["b"]

    x_positions = {}
    if workset_order:
        step = plot_w / max(1, len(workset_order) - 1)
        for i, w in enumerate(workset_order):
            x_positions[w] = margin["l"] + i * step

    if values:
        min_y = min(values)
        max_y = max(values)
    else:
        min_y, max_y = 0.8, 1.2
    pad = (max_y - min_y) * 0.1 if max_y > min_y else 0.1
    min_y -= pad
    max_y += pad

    def y_to_px(y):
        return margin["t"] + (max_y - y) / (max_y - min_y) * plot_h

    lines = []
    lines.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>")
    lines.append("<rect width='100%' height='100%' fill='white'/>")
    lines.append(f"<text x='{W/2}' y='20' text-anchor='middle' font-family='sans-serif' font-size='16'>Simulated Mega-op Speedup vs Working Set</text>")

    x0 = margin["l"]
    y0 = margin["t"] + plot_h
    x1 = margin["l"] + plot_w
    y1 = margin["t"]
    lines.append(f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#333'/>")
    lines.append(f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#333'/>")

    for w in workset_order:
        px = x_positions[w]
        lines.append(f"<line x1='{px}' y1='{y0}' x2='{px}' y2='{y0+6}' stroke='#333'/>")
        lines.append(f"<text x='{px}' y='{y0+22}' text-anchor='middle' font-family='sans-serif' font-size='12'>{w}</text>")

    for i in range(6):
        frac = i / 5
        y = min_y + (max_y - min_y) * frac
        py = y_to_px(y)
        lines.append(f"<line x1='{x0-6}' y1='{py}' x2='{x0}' y2='{py}' stroke='#333'/>")
        lines.append(f"<text x='{x0-10}' y='{py+4}' text-anchor='end' font-family='sans-serif' font-size='12'>{y:.2f}</text>")
        lines.append(f"<line x1='{x0}' y1='{py}' x2='{x1}' y2='{py}' stroke='#ddd'/>")

    lines.append(f"<text x='{W/2}' y='{H-20}' text-anchor='middle' font-family='sans-serif' font-size='13'>working set</text>")
    lines.append(f"<text x='18' y='{H/2}' text-anchor='middle' font-family='sans-serif' font-size='13' transform='rotate(-90 18 {H/2})'>speedup (baseline/mega-op)</text>")

    pts = []
    for w in workset_order:
        val = avg_by_workset.get(w)
        if val is None:
            continue
        pts.append((x_positions[w], y_to_px(val)))
    if pts:
        path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        lines.append(f"<path d='{path}' fill='none' stroke='#1f77b4' stroke-width='2'/>")
        for x, y in pts:
            lines.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3' fill='#1f77b4'/>")

    lines.append("</svg>")

    with open(out_svg, "w", newline="\n") as f:
        f.write("\n".join(lines))

    converter = shutil.which("rsvg-convert")
    if converter:
        out_png = os.path.join(graph_dir, "megaop_speedup_vs_workset.png")
        subprocess.run([converter, "-o", out_png, out_svg], check=True)


if __name__ == "__main__":
    main()
