import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt


AOT_CSV = os.path.join("build", "results_aot.csv")
HS_CSV = os.path.join("build", "hotspot", "results_hotspot.csv")
OUT_DIR = os.path.join("build")
GRAPH_DIR = os.path.join("build", "graphs")

PATTERNS = ["plain", "const", "dyn", "checks"]
PATTERN_LABELS = {
    "plain": "plain deref",
    "const": "const offset",
    "dyn": "dynamic offset",
    "checks": "explicit checks",
}

AOT_STYLES = {
    ("gcc", "O0"): {"linestyle": "-", "marker": "o"},
    ("gcc", "O2"): {"linestyle": "--", "marker": "o"},
    ("clang", "O0"): {"linestyle": ":", "marker": "s"},
    ("clang", "O2"): {"linestyle": "-.", "marker": "s"},
}

HS_STYLE = {"linestyle": "-", "marker": "D", "color": "black", "linewidth": 2.0}

METRIC_PAIRS = [
    ("loads", "deref_ops", "AOT loads vs HotSpot deref_ops"),
    ("branches", "guards", "AOT branches vs HotSpot guards"),
    ("instructions", "ir_nodes", "AOT instructions vs HotSpot ir_nodes"),
]


def load_aot(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "compiler": row["compiler"],
                    "opt": row["opt"],
                    "pattern": row["pattern"],
                    "depth": int(row["depth"]),
                    "loads": int(row["loads"]),
                    "branches": int(row["branches"]),
                    "basic_blocks": int(row["basic_blocks"]),
                    "instructions": int(row["instructions"]),
                }
            )
    return rows


def load_hotspot(path):
    data = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["pattern"], int(row["depth"]))
            data[key] = {
                "deref_ops": int(row["deref_ops"]),
                "guards": int(row["guards"]),
                "deopts": int(row["deopts"]),
                "ir_nodes": int(row["ir_nodes"]),
            }
    return data


def write_combined(aot_rows, hs_rows):
    out_csv = os.path.join(OUT_DIR, "combined_aot_hotspot.csv")
    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "compiler",
                "opt",
                "pattern",
                "depth",
                "loads",
                "branches",
                "basic_blocks",
                "instructions",
                "hs_deref_ops",
                "hs_guards",
                "hs_deopts",
                "hs_ir_nodes",
            ]
        )
        for row in aot_rows:
            key = (row["pattern"], row["depth"])
            hs = hs_rows.get(key, {})
            writer.writerow(
                [
                    row["compiler"],
                    row["opt"],
                    row["pattern"],
                    row["depth"],
                    row["loads"],
                    row["branches"],
                    row["basic_blocks"],
                    row["instructions"],
                    hs.get("deref_ops", ""),
                    hs.get("guards", ""),
                    hs.get("deopts", ""),
                    hs.get("ir_nodes", ""),
                ]
            )

    out_md = os.path.join(OUT_DIR, "combined_aot_hotspot.md")
    with open(out_md, "w", newline="\n") as f:
        f.write("## AOT vs HotSpot (combined)\n\n")
        comps = sorted({(r["compiler"], r["opt"]) for r in aot_rows})
        for compiler, opt in comps:
            f.write(f"### {compiler} {opt}\n\n")
            f.write(
                "| pattern | depth | loads | branches | basic_blocks | instructions | hs_deref_ops | hs_guards | hs_deopts | hs_ir_nodes |\n"
            )
            f.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
            for row in aot_rows:
                if row["compiler"] != compiler or row["opt"] != opt:
                    continue
                key = (row["pattern"], row["depth"])
                hs = hs_rows.get(key, {})
                f.write(
                    f"| {row['pattern']} | {row['depth']} | {row['loads']} | {row['branches']} | "
                    f"{row['basic_blocks']} | {row['instructions']} | {hs.get('deref_ops','')} | "
                    f"{hs.get('guards','')} | {hs.get('deopts','')} | {hs.get('ir_nodes','')} |\n"
                )
            f.write("\n")


def plot_combined(aot_rows, hs_rows):
    os.makedirs(GRAPH_DIR, exist_ok=True)
    depths = sorted({r["depth"] for r in aot_rows})

    aot_grouped = defaultdict(list)
    for row in aot_rows:
        key = (row["compiler"], row["opt"], row["pattern"])
        aot_grouped[key].append(row)
    for key in aot_grouped:
        aot_grouped[key].sort(key=lambda r: r["depth"])

    hs_grouped = defaultdict(list)
    for (pattern, depth), vals in hs_rows.items():
        hs_grouped[pattern].append({"depth": depth, **vals})
    for pattern in hs_grouped:
        hs_grouped[pattern].sort(key=lambda r: r["depth"])

    for aot_metric, hs_metric, title in METRIC_PAIRS:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
        fig.suptitle(title)
        for ax, pattern in zip(axes.flat, PATTERNS):
            for (compiler, opt, pat), rows in aot_grouped.items():
                if pat != pattern:
                    continue
                style = AOT_STYLES.get((compiler, opt), {"linestyle": "-", "marker": "o"})
                xs = [r["depth"] for r in rows]
                ys = [r[aot_metric] for r in rows]
                ax.plot(
                    xs,
                    ys,
                    label=f"{compiler} {opt}",
                    **style,
                )
            hs_series = hs_grouped.get(pattern, [])
            if hs_series:
                xs = [r["depth"] for r in hs_series]
                ys = [r[hs_metric] for r in hs_series]
                ax.plot(xs, ys, label="hotspot", **HS_STYLE)
            ax.set_title(PATTERN_LABELS[pattern])
            ax.set_xlabel("Depth")
            ax.set_ylabel(aot_metric if aot_metric != "instructions" else "insts / ir_nodes")
            ax.set_xticks(depths)
            ax.grid(True, linestyle="--", alpha=0.4)

        handles, labels = axes.flat[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False)
        fig.tight_layout(rect=[0, 0, 1, 0.93])

        out_path = os.path.join(GRAPH_DIR, f"aot_vs_hotspot_{aot_metric}.png")
        fig.savefig(out_path, dpi=160)
        plt.close(fig)


def main():
    aot_rows = load_aot(AOT_CSV)
    hs_rows = load_hotspot(HS_CSV)
    write_combined(aot_rows, hs_rows)
    plot_combined(aot_rows, hs_rows)


if __name__ == "__main__":
    main()
