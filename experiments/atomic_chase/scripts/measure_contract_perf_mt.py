import csv
import os
import shutil
import subprocess
from collections import defaultdict

DEPTHS = [8]
REPEATS = 10
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
        worksets.append(("L1", sizes["L1"], nodes, 2_000_000))
    if "L2" in sizes:
        nodes = max(1024, sizes["L2"] // node_size)
        worksets.append(("L2", sizes["L2"], nodes, 1_000_000))
    if "L3" in sizes:
        nodes = max(4096, sizes["L3"] // node_size)
        worksets.append(("L3", sizes["L3"], nodes, 300_000))
    dram_bytes = 64 * 1024 * 1024
    nodes = max(8192, dram_bytes // node_size)
    worksets.append(("DRAM", dram_bytes, nodes, 200_000))
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


def run_perf(perf_path: str, binary: str, depth: int, nodes: int, iters: int, threads: int) -> dict:
    if threads == 1:
        cpu_set = "0"
    else:
        cpu_set = f"0-{threads - 1}"
    cmd = [
        perf_path,
        "stat",
        "-x,",
        "-r",
        str(REPEATS),
        "-e",
        ",".join(EVENTS),
        "--",
        "taskset",
        "-c",
        cpu_set,
        f"./{binary}",
        "guarded" if "guarded" in binary else "contract",
        str(depth),
        str(nodes),
        str(iters),
        str(threads),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    results = {event: None for event in EVENTS}
    stddev_pct = {event: None for event in EVENTS}
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
            if len(parts) > 3 and parts[3].endswith("%"):
                try:
                    stddev_pct[event] = float(parts[3].strip("%"))
                except ValueError:
                    stddev_pct[event] = None
    for event in EVENTS:
        if results[event] is not None and stddev_pct[event] is not None:
            results[f"{event}_stddev"] = results[event] * stddev_pct[event] / 100.0
        else:
            results[f"{event}_stddev"] = None
    return results


def thread_counts():
    total = os.cpu_count() or 1
    counts = [1]
    c = 2
    while c <= total:
        counts.append(c)
        c *= 2
    if counts[-1] != total:
        counts.append(total)
    return counts


def main():
    perf_path = find_perf()
    out_csv = "results_contract_perf_mt.csv"
    out_md = "results_contract_perf_mt.md"

    binaries = [
        ("O2", "guarded", "contract_guarded_mt"),
        ("O2", "contract", "contract_contract_mt"),
    ]

    worksets = build_worksets()
    threads_list = thread_counts()

    rows = []
    for label, bytes_size, nodes, iters in worksets:
        for depth in DEPTHS:
            for threads in threads_list:
                for opt, mode, binary in binaries:
                    metrics = run_perf(perf_path, binary, depth, nodes, iters, threads)
                    row = {
                        "workset": label,
                        "bytes": bytes_size,
                        "nodes": nodes,
                        "iters": iters,
                        "threads": threads,
                        "opt": opt,
                        "mode": mode,
                        "depth": depth,
                    }
                    row.update(metrics)
                    total_iters = iters * threads
                    if metrics.get("cycles") is not None:
                        row["cycles_per_iter"] = metrics["cycles"] / total_iters
                    else:
                        row["cycles_per_iter"] = None
                    if metrics.get("cycles_stddev") is not None:
                        row["cycles_per_iter_stddev"] = metrics["cycles_stddev"] / total_iters
                    else:
                        row["cycles_per_iter_stddev"] = None
                    rows.append(row)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["workset", "bytes", "nodes", "iters", "threads", "opt", "mode", "depth"]
            + EVENTS
            + [f"{e}_stddev" for e in EVENTS]
            + ["cycles_per_iter", "cycles_per_iter_stddev"]
        )
        for r in rows:
            writer.writerow(
                [
                    r["workset"],
                    r["bytes"],
                    r["nodes"],
                    r["iters"],
                    r["threads"],
                    r["opt"],
                    r["mode"],
                    r["depth"],
                ]
                + [r.get(e, "") for e in EVENTS]
                + [r.get(f"{e}_stddev", "") for e in EVENTS]
                + [r.get("cycles_per_iter", ""), r.get("cycles_per_iter_stddev", "")]
            )

    with open(out_md, "w", newline="\n") as f:
        f.write("## Pointer-chase contract perf (multicore)\n\n")
        f.write(f"- perf binary: `{perf_path}`\n")
        f.write(f"- taskset: `-c 0..N`\n")
        f.write(f"- repeats: `{REPEATS}`\n\n")
        header = (
            "| workset | bytes | nodes | iters | threads | opt | mode | depth | "
            + " | ".join(EVENTS)
            + " | cycles/iter | cycles/iter stddev |\n"
        )
        align = "|---|---:|---:|---:|---:|---|---|---:|" + "---:|" * len(EVENTS) + "---:|---:|\n"
        f.write(header)
        f.write(align)
        for r in rows:
            vals = " | ".join(str(r.get(e, "")) for e in EVENTS)
            f.write(
                f"| {r['workset']} | {r['bytes']} | {r['nodes']} | {r['iters']} | {r['threads']} | "
                f"{r['opt']} | {r['mode']} | {r['depth']} | {vals} | {r['cycles_per_iter']} | "
                f"{r['cycles_per_iter_stddev']} |\n"
            )

    grouped = defaultdict(dict)
    for r in rows:
        key = (r["workset"], r["depth"], r["threads"])
        grouped[key][r["mode"]] = r

    with open(out_md, "a", newline="\n") as f:
        f.write("\n### Speedup (guarded / contract)\n\n")
        f.write("| workset | depth | threads | cycles/iter guarded | cycles/iter contract | speedup | speedup stddev |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|\n")
        for (workset, depth, threads), modes in grouped.items():
            g = modes.get("guarded")
            c = modes.get("contract")
            if not g or not c:
                continue
            cg = g.get("cycles_per_iter")
            cc = c.get("cycles_per_iter")
            if cg is None or cc is None or cc == 0:
                continue
            speedup = cg / cc
            sg = g.get("cycles_per_iter_stddev")
            sc = c.get("cycles_per_iter_stddev")
            if sg is not None and sc is not None and cg > 0 and cc > 0:
                speedup_std = speedup * ((sg / cg) ** 2 + (sc / cc) ** 2) ** 0.5
            else:
                speedup_std = None
            if speedup_std is None:
                f.write(f"| {workset} | {depth} | {threads} | {cg:.4f} | {cc:.4f} | {speedup:.3f} | |\n")
            else:
                f.write(
                    f"| {workset} | {depth} | {threads} | {cg:.4f} | {cc:.4f} | "
                    f"{speedup:.3f} | {speedup_std:.3f} |\n"
                )

    # Graph: speedup vs threads for each workset
    graph_dir = os.path.join("graphs", "contract_mt")
    os.makedirs(graph_dir, exist_ok=True)
    out_svg = os.path.join(graph_dir, "contract_speedup_vs_threads.svg")

    workset_order = [w[0] for w in worksets]
    thread_order = threads_list

    # build average speedup per workset/thread (only depth 8)
    avg_by_workset_thread = {}
    err_by_workset_thread = {}
    for workset in workset_order:
        for threads in thread_order:
            modes = grouped.get((workset, DEPTHS[0], threads), {})
            g = modes.get("guarded")
            c = modes.get("contract")
            if not g or not c:
                continue
            cg = g.get("cycles_per_iter")
            cc = c.get("cycles_per_iter")
            if cg is None or cc is None or cc == 0:
                continue
            speedup = cg / cc
            avg_by_workset_thread[(workset, threads)] = speedup
            sg = g.get("cycles_per_iter_stddev")
            sc = c.get("cycles_per_iter_stddev")
            if sg is not None and sc is not None and cg > 0 and cc > 0:
                err_by_workset_thread[(workset, threads)] = speedup * ((sg / cg) ** 2 + (sc / cc) ** 2) ** 0.5

    W, H = 900, 520
    margin = dict(l=70, r=30, t=30, b=70)
    plot_w = W - margin["l"] - margin["r"]
    plot_h = H - margin["t"] - margin["b"]

    x_positions = {}
    if thread_order:
        step = plot_w / max(1, len(thread_order) - 1)
        for i, t in enumerate(thread_order):
            x_positions[t] = margin["l"] + i * step

    values = list(avg_by_workset_thread.values())
    min_y, max_y = (min(values), max(values)) if values else (0.8, 1.2)
    pad = (max_y - min_y) * 0.1 if max_y > min_y else 0.1
    min_y -= pad
    max_y += pad

    def y_to_px(y):
        return margin["t"] + (max_y - y) / (max_y - min_y) * plot_h

    lines = []
    lines.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>")
    lines.append("<rect width='100%' height='100%' fill='white'/>")
    lines.append(f"<text x='{W/2}' y='20' text-anchor='middle' font-family='sans-serif' font-size='16'>Speedup vs Threads (depth 8)</text>")

    x0 = margin["l"]
    y0 = margin["t"] + plot_h
    x1 = margin["l"] + plot_w
    y1 = margin["t"]
    lines.append(f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#333'/>")
    lines.append(f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#333'/>")

    for t in thread_order:
        px = x_positions[t]
        lines.append(f"<line x1='{px}' y1='{y0}' x2='{px}' y2='{y0+6}' stroke='#333'/>")
        lines.append(f"<text x='{px}' y='{y0+22}' text-anchor='middle' font-family='sans-serif' font-size='12'>{t}</text>")

    for i in range(6):
        frac = i / 5
        y = min_y + (max_y - min_y) * frac
        py = y_to_px(y)
        lines.append(f"<line x1='{x0-6}' y1='{py}' x2='{x0}' y2='{py}' stroke='#333'/>")
        lines.append(f"<text x='{x0-10}' y='{py+4}' text-anchor='end' font-family='sans-serif' font-size='12'>{y:.2f}</text>")
        lines.append(f"<line x1='{x0}' y1='{py}' x2='{x1}' y2='{py}' stroke='#ddd'/>")

    lines.append(f"<text x='{W/2}' y='{H-20}' text-anchor='middle' font-family='sans-serif' font-size='13'>threads</text>")
    lines.append(f"<text x='18' y='{H/2}' text-anchor='middle' font-family='sans-serif' font-size='13' transform='rotate(-90 18 {H/2})'>speedup (guarded/contract)</text>")

    palette = {
        "L1": "#1f77b4",
        "L2": "#ff7f0e",
        "L3": "#2ca02c",
        "DRAM": "#d62728",
    }

    for workset in workset_order:
        pts = []
        for t in thread_order:
            val = avg_by_workset_thread.get((workset, t))
            if val is None:
                continue
            pts.append((x_positions[t], y_to_px(val)))
        if not pts:
            continue
        color = palette.get(workset, "#555")
        path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        lines.append(f"<path d='{path}' fill='none' stroke='{color}' stroke-width='2'/>")
        for x, y in pts:
            lines.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3' fill='{color}'/>")

        # error bars
        for t in thread_order:
            err = err_by_workset_thread.get((workset, t))
            val = avg_by_workset_thread.get((workset, t))
            if err is None or val is None:
                continue
            x = x_positions[t]
            y_lo = y_to_px(val - err)
            y_hi = y_to_px(val + err)
            lines.append(f"<line x1='{x:.1f}' y1='{y_lo:.1f}' x2='{x:.1f}' y2='{y_hi:.1f}' stroke='{color}' stroke-width='1'/>")
            lines.append(f"<line x1='{x-4:.1f}' y1='{y_lo:.1f}' x2='{x+4:.1f}' y2='{y_lo:.1f}' stroke='{color}' stroke-width='1'/>")
            lines.append(f"<line x1='{x-4:.1f}' y1='{y_hi:.1f}' x2='{x+4:.1f}' y2='{y_hi:.1f}' stroke='{color}' stroke-width='1'/>")

    # legend
    legend_x = margin["l"] + 10
    legend_y = margin["t"] + 10
    for i, workset in enumerate(workset_order):
        color = palette.get(workset, "#555")
        y = legend_y + i * 18
        lines.append(f"<rect x='{legend_x}' y='{y-8}' width='10' height='10' fill='{color}'/>")
        lines.append(f"<text x='{legend_x+16}' y='{y}' font-family='sans-serif' font-size='12'>{workset}</text>")

    lines.append("</svg>")

    with open(out_svg, "w", newline="\n") as f:
        f.write("\n".join(lines))

    converter = shutil.which("rsvg-convert")
    if converter:
        out_png = os.path.join(graph_dir, "contract_speedup_vs_threads.png")
        subprocess.run([converter, "-o", out_png, out_svg], check=True)


if __name__ == "__main__":
    main()
