import csv
import os
import shutil
import subprocess
from collections import defaultdict

CSV_PATH = os.environ.get("CONTRACT_CSV", "results_contract_perf.csv")
OUT_DIR = os.environ.get("CONTRACT_GRAPH_DIR", os.path.join("graphs", "contract"))
DEPTH_FILTER = os.environ.get("CONTRACT_DEPTH", "8")
OUT_SVG = os.path.join(OUT_DIR, "contract_cycles_vs_workset_d8.svg")

WORKSET_ORDER = ["L1", "L2", "L3", "DRAM"]


def main():
    rows = []
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    # cycles/iter by workset/opt/mode at a specific depth
    buckets = defaultdict(list)
    for r in rows:
        if DEPTH_FILTER and r.get("depth") != str(DEPTH_FILTER):
            continue
        workset = r["workset"]
        opt = r["opt"]
        mode = r["mode"]
        cpi = r.get("cycles_per_iter")
        if cpi is None or cpi == "":
            continue
        try:
            cpi_val = float(cpi)
        except ValueError:
            continue
        buckets[(workset, opt, mode)].append(cpi_val)

    avg = {}
    for key, vals in buckets.items():
        if vals:
            avg[key] = sum(vals) / len(vals)

    # collect max for y axis; force baseline to 0
    values = [v for v in avg.values()]
    if values:
        max_y = max(values)
    else:
        max_y = 1.0
    pad = max_y * 0.08 if max_y > 0 else 1.0
    min_y = 0.0
    max_y += pad

    W, H = 900, 520
    margin = dict(l=70, r=30, t=30, b=70)
    plot_w = W - margin["l"] - margin["r"]
    plot_h = H - margin["t"] - margin["b"]

    x_positions = {}
    if WORKSET_ORDER:
        step = plot_w / max(1, len(WORKSET_ORDER) - 1)
        for i, w in enumerate(WORKSET_ORDER):
            x_positions[w] = margin["l"] + i * step

    def y_to_px(y):
        return margin["t"] + (max_y - y) / (max_y - min_y) * plot_h

    lines = []
    lines.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>")
    lines.append("<rect width='100%' height='100%' fill='white'/>")
    title_depth = f"d{DEPTH_FILTER}" if DEPTH_FILTER else "all"
    lines.append(f"<text x='{W/2}' y='20' text-anchor='middle' font-family='sans-serif' font-size='16'>Cycles/Iter vs Working Set ({title_depth})</text>")

    x0 = margin["l"]
    y0 = margin["t"] + plot_h
    x1 = margin["l"] + plot_w
    y1 = margin["t"]
    lines.append(f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#333'/>")
    lines.append(f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#333'/>")

    for w in WORKSET_ORDER:
        px = x_positions[w]
        lines.append(f"<line x1='{px}' y1='{y0}' x2='{px}' y2='{y0+6}' stroke='#333'/>")
        lines.append(f"<text x='{px}' y='{y0+22}' text-anchor='middle' font-family='sans-serif' font-size='12'>{w}</text>")

    for i in range(6):
        t = i / 5
        y = min_y + (max_y - min_y) * t
        py = y_to_px(y)
        lines.append(f"<line x1='{x0-6}' y1='{py}' x2='{x0}' y2='{py}' stroke='#333'/>")
        lines.append(f"<text x='{x0-10}' y='{py+4}' text-anchor='end' font-family='sans-serif' font-size='12'>{y:.0f}</text>")
        lines.append(f"<line x1='{x0}' y1='{py}' x2='{x1}' y2='{py}' stroke='#ddd'/>")

    lines.append(f"<text x='{W/2}' y='{H-20}' text-anchor='middle' font-family='sans-serif' font-size='13'>working set</text>")
    lines.append(f"<text x='18' y='{H/2}' text-anchor='middle' font-family='sans-serif' font-size='13' transform='rotate(-90 18 {H/2})'>cycles/iter</text>")

    palette = {"O2": "#1f77b4", "O3": "#d62728"}
    styles = {
        ("O2", "guarded"): ("#1f77b4", ""),
        ("O2", "contract"): ("#1f77b4", "stroke-dasharray='6 4'"),
        ("O3", "guarded"): ("#d62728", ""),
        ("O3", "contract"): ("#d62728", "stroke-dasharray='6 4'"),
    }

    for opt in ["O2", "O3"]:
        for mode in ["guarded", "contract"]:
            color, dash = styles[(opt, mode)]
            pts = []
            for w in WORKSET_ORDER:
                val = avg.get((w, opt, mode))
                if val is None:
                    continue
                pts.append((x_positions[w], y_to_px(val)))
            if not pts:
                continue
            path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
            lines.append(f"<path d='{path}' fill='none' stroke='{color}' stroke-width='2' {dash}/>")
            for x, y in pts:
                lines.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3' fill='{color}'/>")

    # legend
    legend_x = margin["l"] + 10
    legend_y = margin["t"] + 10
    entries = [
        ("O2 guarded", "#1f77b4", False),
        ("O2 contract", "#1f77b4", True),
        ("O3 guarded", "#d62728", False),
        ("O3 contract", "#d62728", True),
    ]
    for i, (label, color, dashed) in enumerate(entries):
        y = legend_y + i * 18
        lines.append(f"<line x1='{legend_x}' y1='{y-4}' x2='{legend_x+16}' y2='{y-4}' stroke='{color}' stroke-width='2' {'stroke-dasharray=\'6 4\'' if dashed else ''}/>")
        lines.append(f"<text x='{legend_x+22}' y='{y}' font-family='sans-serif' font-size='12'>{label}</text>")

    lines.append("</svg>")

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_SVG, "w", newline="\n") as f:
        f.write("\n".join(lines))

    converter = shutil.which("rsvg-convert")
    if converter:
        out_png = os.path.splitext(OUT_SVG)[0] + ".png"
        subprocess.run([converter, "-o", out_png, OUT_SVG], check=True)


if __name__ == "__main__":
    main()
