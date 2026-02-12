import csv
import os
import re
import subprocess

import matplotlib.pyplot as plt

DEPTHS = [2, 3, 5, 8]
BINARIES = [
    ("O2", "naive", "bench_naive"),
    ("O2", "atomic", "bench_atomic"),
    ("O3", "naive", "bench_naive_O3"),
    ("O3", "atomic", "bench_atomic_O3"),
]

SUMMARY_RE = re.compile(r"^summary:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)")


def run_callgrind(binary: str, depth: int, out_file: str):
    cmd = [
        "valgrind",
        "--tool=callgrind",
        "--collect-jumps=yes",
        "--branch-sim=yes",
        f"--callgrind-out-file={out_file}",
        f"./{binary}",
        str(depth),
    ]
    subprocess.run(cmd, check=True)


def parse_summary(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = SUMMARY_RE.match(line.strip())
            if m:
                return {
                    "Ir": int(m.group(1)),
                    "Bc": int(m.group(2)),
                    "Bcm": int(m.group(3)),
                    "Bi": int(m.group(4)),
                    "Bim": int(m.group(5)),
                }
    raise RuntimeError(f"summary line not found in {path}")


def main():
    out_csv = "results_callgrind.csv"
    out_md = "results_callgrind.md"
    graph_dir = os.path.join("graphs", "callgrind")
    os.makedirs(graph_dir, exist_ok=True)

    rows = []
    for opt, mode, binary in BINARIES:
        for depth in DEPTHS:
            out_file = f"callgrind_{mode}_{opt}_d{depth}.out"
            run_callgrind(binary, depth, out_file)
            counts = parse_summary(out_file)
            row = {"opt": opt, "mode": mode, "depth": depth, **counts}
            rows.append(row)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["opt", "mode", "depth", "Ir", "Bc", "Bcm", "Bi", "Bim"])
        for r in rows:
            writer.writerow(
                [r["opt"], r["mode"], r["depth"], r["Ir"], r["Bc"], r["Bcm"], r["Bi"], r["Bim"]]
            )

    with open(out_md, "w", newline="\n") as f:
        f.write("## Callgrind summary (per depth)\n\n")
        f.write("| opt | mode | depth | Ir | Bc | Bcm | Bi | Bim |\n")
        f.write("|---|---|---:|---:|---:|---:|---:|---:|\n")
        for r in rows:
            f.write(
                f"| {r['opt']} | {r['mode']} | {r['depth']} | {r['Ir']} | {r['Bc']} | "
                f"{r['Bcm']} | {r['Bi']} | {r['Bim']} |\n"
            )

    # Graphs
    events = ["Ir", "Bc", "Bcm"]
    for event in events:
        plt.figure(figsize=(9, 5))
        for opt, mode, _ in BINARIES:
            series = [r for r in rows if r["opt"] == opt and r["mode"] == mode]
            series.sort(key=lambda x: x["depth"])
            xs = [r["depth"] for r in series]
            ys = [r[event] for r in series]
            plt.plot(xs, ys, marker="o", label=f"{mode} {opt}")
        plt.title(f"Callgrind {event} vs depth")
        plt.xlabel("depth")
        plt.ylabel(event)
        plt.xticks(DEPTHS)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend()
        out_path = os.path.join(graph_dir, f"callgrind_{event}.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=160)
        plt.close()

    with open("analysis_callgrind.md", "w", newline="\n") as f:
        f.write("## Callgrind analysis (WSL-safe)\n\n")
        f.write("- Ir approximates instruction references (dynamic).\n")
        f.write("- Bc approximates conditional branches executed.\n")
        f.write("- Bcm approximates conditional branch mispredicts (simulated).\n")
        f.write("- Compare naive vs atomic per depth to quantify control-flow collapse.\n")


if __name__ == "__main__":
    main()
