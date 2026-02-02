import csv
import glob
import os
import re
import subprocess
from collections import defaultdict

EVENTS = ["instructions", "cycles", "branches", "branch-misses"]
DEPTHS = [2, 3, 5, 8]
BINARIES = [
    ("O2", "naive", "bench_naive"),
    ("O2", "atomic", "bench_atomic"),
    ("O3", "naive", "bench_naive_O3"),
    ("O3", "atomic", "bench_atomic_O3"),
]


def find_perf() -> str:
    candidates = glob.glob("/usr/lib/linux-tools-*/perf")
    if candidates:
        return sorted(candidates)[-1]
    return "perf"


def run_perf(perf_path: str, binary: str, depth: int) -> dict:
    cmd = [
        perf_path,
        "stat",
        "-x,",
        "-e",
        ",".join(EVENTS),
        "--",
        f"./{binary}",
        str(depth),
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
        if event in EVENTS:
            if value in ("<not counted>", "<not supported>"):
                results[event] = None
            else:
                results[event] = float(value.replace(",", ""))
    return results


def main():
    perf_path = find_perf()
    out_csv = os.path.join("results_perf.csv")
    out_md = os.path.join("results_perf.md")
    out_graph_dir = os.path.join("graphs")

    os.makedirs(out_graph_dir, exist_ok=True)

    rows = []
    for opt, mode, binary in BINARIES:
        for depth in DEPTHS:
            metrics = run_perf(perf_path, binary, depth)
            row = {
                "opt": opt,
                "mode": mode,
                "depth": depth,
            }
            row.update(metrics)
            rows.append(row)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["opt", "mode", "depth"] + EVENTS)
        for r in rows:
            writer.writerow([r["opt"], r["mode"], r["depth"]] + [r.get(e, "") for e in EVENTS])

    with open(out_md, "w", newline="\n") as f:
        f.write("## Atomic chase perf (per depth)\n\n")
        f.write("| opt | mode | depth | instructions | cycles | branches | branch-misses |\n")
        f.write("|---|---|---:|---:|---:|---:|---:|\n")
        for r in rows:
            f.write(
                f"| {r['opt']} | {r['mode']} | {r['depth']} | "
                f"{r.get('instructions','')} | {r.get('cycles','')} | "
                f"{r.get('branches','')} | {r.get('branch-misses','')} |\n"
            )

    # Graphs
    import matplotlib.pyplot as plt

    grouped = defaultdict(list)
    for r in rows:
        grouped[(r["opt"], r["mode"])].append(r)
    for key in grouped:
        grouped[key].sort(key=lambda x: x["depth"])

    for event in EVENTS:
        plt.figure(figsize=(9, 5))
        for (opt, mode), series in grouped.items():
            xs = [s["depth"] for s in series]
            ys = [s[event] for s in series]
            if any(v is None for v in ys):
                continue
            plt.plot(xs, ys, marker="o", label=f"{mode} {opt}")
        plt.title(f"{event} vs depth")
        plt.xlabel("depth")
        plt.ylabel(event)
        plt.xticks(DEPTHS)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend()
        out_path = os.path.join(out_graph_dir, f"perf_{event.replace('-', '_')}.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=160)
        plt.close()


if __name__ == "__main__":
    main()
