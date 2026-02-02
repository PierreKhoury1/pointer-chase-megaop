import csv
import os
from collections import defaultdict

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


def load_results(path: str):
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


def plot_one(compiler: str, opt: str, depths, grouped, out_dir: str):
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

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{compiler}_{opt}.png")
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def main() -> None:
    csv_path = os.path.join("build", "results_aot.csv")
    depths, data = load_results(csv_path)
    out_dir = os.path.join("build", "graphs")
    for (compiler, opt), grouped in data.items():
        plot_one(compiler, opt, depths, grouped, out_dir)
    plot_combined(depths, data, out_dir)


def plot_combined(depths, data, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
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

        out_path = os.path.join(out_dir, f"combined_{metric}.png")
        fig.tight_layout()
        fig.savefig(out_path, dpi=160)
        plt.close(fig)


if __name__ == "__main__":
    main()
