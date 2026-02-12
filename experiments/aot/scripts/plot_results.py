import csv
import os
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


PATTERNS = ["plain", "const", "dyn", "checks"]
PATTERN_LABELS = {
    "plain": "plain deref",
    "const": "const offset",
    "dyn": "dynamic offset",
    "checks": "explicit checks",
}
MARKERS = {
    "plain": "o",
    "const": "s",
    "dyn": "^",
    "checks": "D",
}
COMPILER_STYLES = {
    ("gcc", "O0"): "-",
    ("gcc", "O2"): "--",
    ("clang", "O0"): ":",
    ("clang", "O2"): "-.",
}
METRICS = [
    ("loads", "Loads"),
    ("branches", "Branches"),
    ("basic_blocks", "Basic Blocks"),
    ("instructions", "Instructions"),
]

ROOT = Path(__file__).resolve().parents[3]
AOT_DIR = ROOT / "experiments" / "aot"
RAW_CSV = AOT_DIR / "data" / "raw" / "results_aot.csv"
PLOTS_DIR = AOT_DIR / "plots"
COMPILER_PLOTS_DIR = PLOTS_DIR / "compiler"
COMBINED_PLOTS_DIR = PLOTS_DIR / "combined"


def load_results(path: Path):
    data = defaultdict(lambda: defaultdict(list))
    depths = set()
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            compiler = row["compiler"]
            opt = row["opt"]
            pattern = row["pattern"]
            depth = int(row["depth"])
            depths.add(depth)
            entry = {
                "depth": depth,
                "loads": int(row["loads"]),
                "branches": int(row["branches"]),
                "basic_blocks": int(row["basic_blocks"]),
                "instructions": int(row["instructions"]),
            }
            data[(compiler, opt)][pattern].append(entry)
    for key in data:
        for pattern in data[key]:
            data[key][pattern].sort(key=lambda r: r["depth"])
    return sorted(depths), data


def plot_one(compiler: str, opt: str, depths, grouped, out_dir: Path):
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    fig.suptitle(f"{compiler.upper()} {opt} pointer-chasing metrics")

    for ax, (metric, label) in zip(axes.flat, METRICS):
        for pattern in PATTERNS:
            series = grouped.get(pattern, [])
            xs = [r["depth"] for r in series]
            ys = [r[metric] for r in series]
            if not xs:
                continue
            ax.plot(
                xs,
                ys,
                marker=MARKERS[pattern],
                linewidth=1.6,
                label=PATTERN_LABELS[pattern],
            )
        ax.set_title(label)
        ax.set_xlabel("Depth")
        ax.set_ylabel(label)
        ax.set_xticks(depths)
        ax.grid(True, linestyle="--", alpha=0.4)

    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.93])

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{compiler}_{opt}.png"
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def main() -> None:
    csv_path = RAW_CSV
    depths, data = load_results(csv_path)
    out_dir = COMPILER_PLOTS_DIR
    for (compiler, opt), grouped in data.items():
        plot_one(compiler, opt, depths, grouped, out_dir)
    plot_combined(depths, data, COMBINED_PLOTS_DIR)


def plot_combined(depths, data, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for metric, label in METRICS:
        fig, ax = plt.subplots(figsize=(11, 6))
        for (compiler, opt), grouped in data.items():
            linestyle = COMPILER_STYLES.get((compiler, opt), "-")
            for pattern in PATTERNS:
                series = grouped.get(pattern, [])
                xs = [r["depth"] for r in series]
                ys = [r[metric] for r in series]
                if not xs:
                    continue
                ax.plot(
                    xs,
                    ys,
                    marker=MARKERS[pattern],
                    linestyle=linestyle,
                    linewidth=1.6,
                    label=f"{compiler} {opt} - {PATTERN_LABELS[pattern]}",
                )

        ax.set_title(f"All compilers/opts - {label}")
        ax.set_xlabel("Depth")
        ax.set_ylabel(label)
        ax.set_xticks(depths)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(loc="upper left", fontsize=8, ncol=2, frameon=False)

        out_path = out_dir / f"combined_{metric}.png"
        fig.tight_layout()
        fig.savefig(out_path, dpi=160)
        plt.close(fig)


if __name__ == "__main__":
    main()
