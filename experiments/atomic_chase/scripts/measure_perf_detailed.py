import csv
import os
import shutil
import subprocess


EVENTS = [
    "cycles",
    "instructions",
    "branches",
    "branch-misses",
    "stalled-cycles-frontend",
    "stalled-cycles-backend",
    "cache-references",
    "cache-misses",
    "LLC-loads",
    "LLC-load-misses",
    "L1-dcache-loads",
    "L1-dcache-load-misses",
    "dTLB-loads",
    "dTLB-load-misses",
    "iTLB-loads",
    "iTLB-load-misses",
]

WORKSETS = [
    ("L1", 2048, 5_000_000),
    ("L2", 16384, 3_000_000),
    ("L3", 524288, 1_000_000),
    ("DRAM", 4_194_304, 500_000),
]

DEPTH = 8
BINARIES = [
    ("guarded", "./contract_guarded"),
    ("contract", "./contract_contract"),
]
REPEAT = int(os.environ.get("PERF_REPEAT", "1"))
OUT_PREFIX = os.environ.get("PERF_OUT_PREFIX", "results_perf_detailed")
WORKSET_FILTER = os.environ.get("PERF_WORKSETS")


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


def run_perf(
    perf_path: str, binary: str, depth: int, nodes: int, iters: int, repeat: int
) -> dict:
    cmd = [
        perf_path,
        "stat",
        "-x,",
        "-e",
        ",".join(EVENTS),
    ]
    if repeat > 1:
        cmd.extend(["-r", str(repeat)])
    cmd.extend(
        [
            "--",
            "taskset",
            "-c",
            "0",
            binary,
            str(depth),
            str(nodes),
            str(iters),
        ]
    )
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    results = {event: None for event in EVENTS}
    scale = {event: None for event in EVENTS}
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
                    stddev_pct[event] = float(parts[3].rstrip("%"))
                except ValueError:
                    stddev_pct[event] = None
            if len(parts) > 4 and parts[4]:
                try:
                    scale[event] = float(parts[4])
                except ValueError:
                    scale[event] = None
    results["scale"] = scale
    results["stddev_pct"] = stddev_pct
    return results


def safe_div(num, den):
    if num is None or den is None or den == 0:
        return None
    return num / den


def format_num(val):
    if val is None:
        return "n/a"
    if abs(val) >= 1e9:
        return f"{val/1e9:.3f}G"
    if abs(val) >= 1e6:
        return f"{val/1e6:.3f}M"
    if abs(val) >= 1e3:
        return f"{val/1e3:.3f}k"
    return f"{val:.3f}"


def format_pct(val):
    if val is None:
        return "n/a"
    return f"{val*100:.2f}%"


def main():
    perf_path = find_perf()
    out_csv = f"{OUT_PREFIX}.csv"
    out_md = f"{OUT_PREFIX}.md"

    rows = []
    worksets = WORKSETS
    if WORKSET_FILTER:
        requested = {w.strip() for w in WORKSET_FILTER.split(",") if w.strip()}
        worksets = [w for w in WORKSETS if w[0] in requested]
        if not worksets:
            raise RuntimeError(
                f"No matching worksets for PERF_WORKSETS={WORKSET_FILTER}"
            )

    for workset, nodes, iters in worksets:
        for mode, binary in BINARIES:
            metrics = run_perf(perf_path, binary, DEPTH, nodes, iters, REPEAT)
            row = {
                "workset": workset,
                "nodes": nodes,
                "iters": iters,
                "mode": mode,
                "depth": DEPTH,
            }
            row.update(metrics)
            rows.append(row)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["workset", "nodes", "iters", "mode", "depth"] + EVENTS)
        for r in rows:
            writer.writerow(
                [r["workset"], r["nodes"], r["iters"], r["mode"], r["depth"]]
                + [r.get(e, "") for e in EVENTS]
            )

    with open(out_md, "w", newline="\n") as f:
        f.write("## perf stat (detailed stalls)\n\n")
        f.write(f"- perf binary: `{perf_path}`\n")
        f.write("- taskset: `-c 0`\n")
        f.write(f"- depth: `{DEPTH}`\n")
        f.write(f"- repeats: `{REPEAT}`\n\n")

        for workset, nodes, iters in worksets:
            f.write(f"### {workset} (nodes={nodes}, iters={iters})\n\n")
            subset = [r for r in rows if r["workset"] == workset]

            def get(mode):
                for r in subset:
                    if r["mode"] == mode:
                        return r
                return None

            g = get("guarded")
            c = get("contract")

            f.write("| metric | guarded | contract |\n")
            f.write("|---|---:|---:|\n")

            for event in EVENTS:
                f.write(
                    f"| {event} | {format_num(g.get(event))} | {format_num(c.get(event))} |\n"
                )

            # Derived metrics
            g_ipc = safe_div(g.get("instructions"), g.get("cycles"))
            c_ipc = safe_div(c.get("instructions"), c.get("cycles"))
            g_front = safe_div(g.get("stalled-cycles-frontend"), g.get("cycles"))
            c_front = safe_div(c.get("stalled-cycles-frontend"), c.get("cycles"))
            g_back = safe_div(g.get("stalled-cycles-backend"), g.get("cycles"))
            c_back = safe_div(c.get("stalled-cycles-backend"), c.get("cycles"))

            g_branch_miss = safe_div(g.get("branch-misses"), g.get("branches"))
            c_branch_miss = safe_div(c.get("branch-misses"), c.get("branches"))

            g_cache_miss = safe_div(g.get("cache-misses"), g.get("cache-references"))
            c_cache_miss = safe_div(c.get("cache-misses"), c.get("cache-references"))

            g_l1_miss = safe_div(g.get("L1-dcache-load-misses"), g.get("L1-dcache-loads"))
            c_l1_miss = safe_div(c.get("L1-dcache-load-misses"), c.get("L1-dcache-loads"))

            g_llc_miss = safe_div(g.get("LLC-load-misses"), g.get("LLC-loads"))
            c_llc_miss = safe_div(c.get("LLC-load-misses"), c.get("LLC-loads"))

            g_dtlb_miss = safe_div(g.get("dTLB-load-misses"), g.get("dTLB-loads"))
            c_dtlb_miss = safe_div(c.get("dTLB-load-misses"), c.get("dTLB-loads"))

            g_cycles_per_llc = safe_div(g.get("cycles"), g.get("LLC-load-misses"))
            c_cycles_per_llc = safe_div(c.get("cycles"), c.get("LLC-load-misses"))
            g_cycles_stddev = None
            c_cycles_stddev = None
            if REPEAT > 1:
                g_stddev_pct = g.get("stddev_pct", {}).get("cycles")
                c_stddev_pct = c.get("stddev_pct", {}).get("cycles")
                if g_stddev_pct is not None and g.get("cycles") is not None:
                    g_cycles_stddev = g.get("cycles") * g_stddev_pct / 100.0
                if c_stddev_pct is not None and c.get("cycles") is not None:
                    c_cycles_stddev = c.get("cycles") * c_stddev_pct / 100.0

            f.write("\n| derived metric | guarded | contract |\n")
            f.write("|---|---:|---:|\n")
            f.write(f"| IPC | {format_num(g_ipc)} | {format_num(c_ipc)} |\n")
            f.write(f"| % frontend stalls | {format_pct(g_front)} | {format_pct(c_front)} |\n")
            f.write(f"| % backend stalls | {format_pct(g_back)} | {format_pct(c_back)} |\n")
            f.write(f"| branch miss rate | {format_pct(g_branch_miss)} | {format_pct(c_branch_miss)} |\n")
            f.write(f"| cache miss rate | {format_pct(g_cache_miss)} | {format_pct(c_cache_miss)} |\n")
            f.write(f"| L1d miss rate | {format_pct(g_l1_miss)} | {format_pct(c_l1_miss)} |\n")
            f.write(f"| LLC miss rate | {format_pct(g_llc_miss)} | {format_pct(c_llc_miss)} |\n")
            f.write(f"| dTLB miss rate | {format_pct(g_dtlb_miss)} | {format_pct(c_dtlb_miss)} |\n")
            f.write(f"| cycles per LLC miss | {format_num(g_cycles_per_llc)} | {format_num(c_cycles_per_llc)} |\n")
            if REPEAT > 1:
                f.write(f"| cycles stddev | {format_num(g_cycles_stddev)} | {format_num(c_cycles_stddev)} |\n")
            f.write("\n")

    # Try TopdownL1 (if supported) for L1 and DRAM
    topdown_path = f"{OUT_PREFIX}_topdown.txt"
    supported = True
    try:
        subprocess.run(
            [
                perf_path,
                "stat",
                "-M",
                "TopdownL1",
                "--",
                "true",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        supported = False

    if supported:
        with open(topdown_path, "w", newline="\n") as f:
            f.write("# TopdownL1 output (guarded/contract)\n\n")
            targets = (worksets[0], worksets[-1]) if worksets else []
            for workset, nodes, iters in targets:
                f.write(f"## {workset} (nodes={nodes}, iters={iters})\n")
                for mode, binary in BINARIES:
                    f.write(f"### {mode}\n")
                    cmd = [
                        perf_path,
                        "stat",
                        "-M",
                        "TopdownL1",
                        "--",
                        "taskset",
                        "-c",
                        "0",
                        binary,
                        str(DEPTH),
                        str(nodes),
                        str(iters),
                    ]
                    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    f.write(proc.stderr)
                    f.write("\n")
    else:
        with open(topdown_path, "w", newline="\n") as f:
            f.write("TopdownL1 not supported on this CPU/perf configuration.\n")


if __name__ == "__main__":
    main()
