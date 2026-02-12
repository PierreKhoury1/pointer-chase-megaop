import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt

INPUT = os.environ.get("PERF_INPUT", "results_perf_detailed_v2.csv")
OUT_PNG = os.environ.get("PERF_OUTPUT", "graphs/perf/perf_overview.png")


def load_rows(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def to_float(v):
    if v is None:
        return None
    v = str(v).strip()
    if v == "" or v.lower() == "n/a":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def main():
    rows = load_rows(INPUT)
    worksets = ["L1", "L2", "L3", "DRAM"]
    modes = ["guarded", "contract"]

    data = {ws: {} for ws in worksets}
    for ws in worksets:
        for mode in modes:
            row = next((r for r in rows if r["workset"] == ws and r["mode"] == mode), None)
            if not row:
                raise RuntimeError(f"Missing data for {ws}/{mode} in {INPUT}")
            cycles = to_float(row.get("cycles"))
            inst = to_float(row.get("instructions"))
            llc_loads = to_float(row.get("LLC-loads"))
            llc_misses = to_float(row.get("LLC-load-misses"))
            ipc = inst / cycles if cycles and inst else None
            llc_miss_rate = llc_misses / llc_loads if llc_loads and llc_misses else None
            data[ws][mode] = {
                "cycles": cycles,
                "ipc": ipc,
                "llc_miss_rate": llc_miss_rate,
            }

    speedup = [data[ws]["guarded"]["cycles"] / data[ws]["contract"]["cycles"] for ws in worksets]
    ipc_guarded = [data[ws]["guarded"]["ipc"] for ws in worksets]
    ipc_contract = [data[ws]["contract"]["ipc"] for ws in worksets]
    llc_guarded = [data[ws]["guarded"]["llc_miss_rate"] for ws in worksets]
    llc_contract = [data[ws]["contract"]["llc_miss_rate"] for ws in worksets]

    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)

    axes[0].plot(worksets, speedup, marker="o", color="#2b6cb0", label="Speedup (guarded/contract)")
    axes[0].axhline(1.0, color="#666", linewidth=1, linestyle="--")
    axes[0].set_ylabel("Speedup")
    axes[0].grid(True, axis="y", alpha=0.3)
    axes[0].legend(frameon=False)

    axes[1].plot(worksets, ipc_guarded, marker="o", color="#2f855a", label="IPC guarded")
    axes[1].plot(worksets, ipc_contract, marker="o", color="#dd6b20", label="IPC contract")
    axes[1].set_ylabel("IPC")
    axes[1].grid(True, axis="y", alpha=0.3)
    axes[1].legend(frameon=False)

    axes[2].plot(worksets, llc_guarded, marker="o", color="#2f855a", label="LLC miss rate guarded")
    axes[2].plot(worksets, llc_contract, marker="o", color="#dd6b20", label="LLC miss rate contract")
    axes[2].set_ylabel("LLC miss rate")
    axes[2].grid(True, axis="y", alpha=0.3)
    axes[2].legend(frameon=False)

    axes[2].set_xlabel("Working set")
    fig.suptitle("Pointer-Chase: Speedup / IPC / LLC Miss Rate vs Working Set")
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    out_path = Path(OUT_PNG)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)


if __name__ == "__main__":
    main()
