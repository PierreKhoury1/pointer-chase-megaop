import csv
import os
import shutil
import subprocess
from collections import defaultdict

DEPTHS = [2, 3, 5, 8]
BINARIES = [
    ("O2", "guarded", "contract_guarded"),
    ("O2", "contract", "contract_contract"),
    ("O3", "guarded", "contract_guarded_O3"),
    ("O3", "contract", "contract_contract_O3"),
]

EVENTS = ["instructions", "cycles", "branches", "branch-misses"]


def parse_size(value: str) -> int:
    value = value.strip().upper()
    if value.endswith("K"):
        return int(value[:-1]) * 1024
    if value.endswith("M"):
        return int(value[:-1]) * 1024 * 1024
    return int(value)


def read_cache_sizes() -> dict:
    sizes = {}
    base = "/sys/devices/system/cpu/cpu0/cache"
    for idx in os.listdir(base):
        path = os.path.join(base, idx)
        if not os.path.isdir(path):
            continue
        try:
            with open(os.path.join(path, "level"), "r") as f:
                level = f.read().strip()
            with open(os.path.join(path, "type"), "r") as f:
                cache_type = f.read().strip()
            with open(os.path.join(path, "size"), "r") as f:
                size = f.read().strip()
        except OSError:
            continue
        if level == "1" and cache_type.lower() == "data":
            sizes["L1"] = parse_size(size)
        elif level == "2":
            sizes["L2"] = parse_size(size)
        elif level == "3":
            sizes["L3"] = parse_size(size)
    return sizes


def build_worksets() -> list[tuple[str, int, int, int]]:
    sizes = read_cache_sizes()
    node_size = 16
    worksets = []
    if "L1" in sizes:
        nodes = max(256, sizes["L1"] // node_size)
        worksets.append(("L1", sizes["L1"], nodes, 5_000_000))
    if "L2" in sizes:
        nodes = max(1024, sizes["L2"] // node_size)
        worksets.append(("L2", sizes["L2"], nodes, 3_000_000))
    if "L3" in sizes:
        nodes = max(4096, sizes["L3"] // node_size)
        worksets.append(("L3", sizes["L3"], nodes, 1_000_000))
    # DRAM-sized working set (64MB)
    dram_bytes = 64 * 1024 * 1024
    nodes = max(8192, dram_bytes // node_size)
    worksets.append(("DRAM", dram_bytes, nodes, 500_000))
    return worksets


def find_perf() -> str:
    env_perf = os.environ.get("PERF_PATH")
    if env_perf and os.path.isfile(env_perf) and os.access(env_perf, os.X_OK):
        return env_perf
    in_path = shutil.which("perf")
    if in_path:
        return in_path
    raise RuntimeError("perf binary not found. Set PERF_PATH or install perf.")


def normalize_event(event_name: str) -> str:
    return event_name.split(":", 1)[0]


def run_perf(perf_path: str, binary: str, depth: int, nodes: int, iters: int) -> dict:
    cmd = [
        perf_path,
        "stat",
        "-x,",
        "-e",
        ",".join(EVENTS),
        "--",
        "taskset",
        "-c",
        "0",
        f"./{binary}",
        str(depth),
        str(nodes),
        str(iters),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    results = {event: None for event in EVENTS}
    for line in proc.stderr.splitlines():
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        value, _, event = parts[0], parts[1], parts[2]
        event = normalize_event(event)
        if event in results:
            if value in ("<not counted>", "<not supported>", "<not available>"):
                results[event] = None
            else:
                try:
                    results[event] = float(value.replace(",", ""))
                except ValueError:
                    results[event] = None
    return results


def main():
    perf_path = find_perf()
    out_csv = "results_contract_perf.csv"
    out_md = "results_contract_perf.md"

    rows = []
    worksets = build_worksets()
    for label, bytes_size, nodes, iters in worksets:
        for opt, mode, binary in BINARIES:
            for depth in DEPTHS:
                metrics = run_perf(perf_path, binary, depth, nodes, iters)
                row = {
                    "workset": label,
                    "bytes": bytes_size,
                    "nodes": nodes,
                    "iters": iters,
                    "opt": opt,
                    "mode": mode,
                    "depth": depth,
                }
                row.update(metrics)
                if metrics.get("cycles") is not None:
                    row["cycles_per_iter"] = metrics["cycles"] / iters
                else:
                    row["cycles_per_iter"] = None
                rows.append(row)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "workset",
                "bytes",
                "nodes",
                "iters",
                "opt",
                "mode",
                "depth",
            ]
            + EVENTS
            + ["cycles_per_iter"]
        )
        for r in rows:
            writer.writerow(
                [
                    r["workset"],
                    r["bytes"],
                    r["nodes"],
                    r["iters"],
                    r["opt"],
                    r["mode"],
                    r["depth"],
                ]
                + [r.get(e, "") for e in EVENTS]
                + [r.get("cycles_per_iter", "")]
            )

    with open(out_md, "w", newline="\n") as f:
        f.write("## Pointer-chase contract perf (per depth)\n\n")
        f.write(f"- perf binary: `{perf_path}`\n")
        f.write("- taskset: `-c 0`\n\n")
        header = (
            "| workset | bytes | nodes | iters | opt | mode | depth | "
            + " | ".join(EVENTS)
            + " | cycles/iter |\n"
        )
        align = "|---|---:|---:|---:|---|---|---:|" + "---:|" * len(EVENTS) + "---:|\n"
        f.write(header)
        f.write(align)
        for r in rows:
            vals = " | ".join(str(r.get(e, "")) for e in EVENTS)
            f.write(
                f"| {r['workset']} | {r['bytes']} | {r['nodes']} | {r['iters']} | "
                f"{r['opt']} | {r['mode']} | {r['depth']} | {vals} | {r['cycles_per_iter']} |\n"
            )

    # Summarize speedup by workset/opt/depth
    grouped = defaultdict(dict)
    for r in rows:
        key = (r["workset"], r["opt"], r["depth"])
        grouped[key][r["mode"]] = r

    with open(out_md, "a", newline="\n") as f:
        f.write("\n### Speedup (guarded / contract)\n\n")
        f.write("| workset | opt | depth | cycles/iter guarded | cycles/iter contract | speedup |\n")
        f.write("|---|---|---:|---:|---:|---:|\n")
        for (workset, opt, depth), modes in grouped.items():
            g = modes.get("guarded")
            c = modes.get("contract")
            if not g or not c:
                continue
            cg = g.get("cycles_per_iter")
            cc = c.get("cycles_per_iter")
            if cg is None or cc is None or cc == 0:
                continue
            speedup = cg / cc
            f.write(f"| {workset} | {opt} | {depth} | {cg:.4f} | {cc:.4f} | {speedup:.3f} |\n")

    # Graph: speedup vs workset (avg across depths)
    def avg_speedup(rows_by_key):
        values = []
        for _, modes in rows_by_key.items():
            g = modes.get("guarded")
            c = modes.get("contract")
            if not g or not c:
                continue
            cg = g.get("cycles_per_iter")
            cc = c.get("cycles_per_iter")
            if cg is None or cc is None or cc == 0:
                continue
            values.append(cg / cc)
        if not values:
            return None
        return sum(values) / len(values)

    # organize by workset + opt
    workset_order = [w[0] for w in worksets]
    by_workset_opt = {}
    for r in rows:
        key = (r["workset"], r["opt"], r["depth"])
        by_workset_opt.setdefault(key, {})[r["mode"]] = r

    avg_by_workset_opt = {}
    for workset in workset_order:
        for opt in ["O2", "O3"]:
            subset = {
                (w, o, d): modes
                for (w, o, d), modes in by_workset_opt.items()
                if w == workset and o == opt
            }
            avg = avg_speedup(subset)
            if avg is not None:
                avg_by_workset_opt[(workset, opt)] = avg

    # simple SVG plot (categorical x axis)
    graph_dir = os.path.join("graphs", "contract")
    out_svg = os.path.join(graph_dir, "contract_speedup_vs_workset.svg")
    os.makedirs(graph_dir, exist_ok=True)

    W, H = 900, 520
    margin = dict(l=70, r=30, t=30, b=70)
    plot_w = W - margin["l"] - margin["r"]
    plot_h = H - margin["t"] - margin["b"]

    x_positions = {}
    if workset_order:
        step = plot_w / max(1, len(workset_order) - 1)
        for i, w in enumerate(workset_order):
            x_positions[w] = margin["l"] + i * step

    values = list(avg_by_workset_opt.values())
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
    lines.append(f"<text x='{W/2}' y='20' text-anchor='middle' font-family='sans-serif' font-size='16'>Speedup vs Working Set Size</text>")

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
        t = i / 5
        y = min_y + (max_y - min_y) * t
        py = y_to_px(y)
        lines.append(f"<line x1='{x0-6}' y1='{py}' x2='{x0}' y2='{py}' stroke='#333'/>")
        lines.append(f"<text x='{x0-10}' y='{py+4}' text-anchor='end' font-family='sans-serif' font-size='12'>{y:.2f}</text>")
        lines.append(f"<line x1='{x0}' y1='{py}' x2='{x1}' y2='{py}' stroke='#ddd'/>")

    lines.append(f"<text x='{W/2}' y='{H-20}' text-anchor='middle' font-family='sans-serif' font-size='13'>working set</text>")
    lines.append(f"<text x='18' y='{H/2}' text-anchor='middle' font-family='sans-serif' font-size='13' transform='rotate(-90 18 {H/2})'>speedup (guarded/contract)</text>")

    palette = {"O2": "#1f77b4", "O3": "#d62728"}
    for opt in ["O2", "O3"]:
        pts = []
        for w in workset_order:
            val = avg_by_workset_opt.get((w, opt))
            if val is None:
                continue
            pts.append((x_positions[w], y_to_px(val)))
        if not pts:
            continue
        path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        color = palette.get(opt, "#555")
        lines.append(f"<path d='{path}' fill='none' stroke='{color}' stroke-width='2'/>")
        for x, y in pts:
            lines.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3' fill='{color}'/>")

    # legend
    legend_x = margin["l"] + 10
    legend_y = margin["t"] + 10
    for i, opt in enumerate(["O2", "O3"]):
        color = palette.get(opt, "#555")
        y = legend_y + i * 18
        lines.append(f"<rect x='{legend_x}' y='{y-8}' width='10' height='10' fill='{color}'/>")
        lines.append(f"<text x='{legend_x+16}' y='{y}' font-family='sans-serif' font-size='12'>{opt}</text>")

    lines.append("</svg>")

    with open(out_svg, "w", newline="\n") as f:
        f.write("\n".join(lines))

    converter = shutil.which("rsvg-convert")
    if converter:
        out_png = os.path.join(graph_dir, "contract_speedup_vs_workset.png")
        subprocess.run([converter, "-o", out_png, out_svg], check=True)


if __name__ == "__main__":
    main()
