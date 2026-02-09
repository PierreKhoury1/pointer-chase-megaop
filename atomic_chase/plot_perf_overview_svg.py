import csv
import os
from pathlib import Path

INPUT = os.environ.get("PERF_INPUT", "results_perf_detailed_v2.csv")
OUT_SVG = os.environ.get("PERF_OUTPUT", "graphs/perf/perf_overview.svg")


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


def load_rows(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def svg_escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


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

    width = 900
    height = 900
    margin_left = 70
    margin_right = 30
    margin_top = 40
    margin_bottom = 60
    gap = 35
    panel_h = (height - margin_top - margin_bottom - 2 * gap) / 3
    panel_w = width - margin_left - margin_right

    xs = [
        margin_left + i * (panel_w / (len(worksets) - 1))
        for i in range(len(worksets))
    ]

    def scale_y(values, y_min=None, y_max=None):
        vals = [v for v in values if v is not None]
        if not vals:
            return 0.0, 1.0
        vmin = min(vals) if y_min is None else y_min
        vmax = max(vals) if y_max is None else y_max
        if vmin == vmax:
            vmax = vmin + 1.0
        pad = 0.08 * (vmax - vmin)
        return vmin - pad, vmax + pad

    def y_to_px(y, y_min, y_max, top):
        return top + panel_h - (y - y_min) / (y_max - y_min) * panel_h

    def polyline(points, color, width=2, dashed=False):
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        return f'<polyline fill="none" stroke="{color}" stroke-width="{width}"{dash} points="{pts}" />'

    def draw_panel(title, series, colors, y_label, top, y_min=None, y_max=None, draw_one_line=False):
        all_vals = []
        for vals in series:
            all_vals.extend([v for v in vals if v is not None])
        y_min_s, y_max_s = scale_y(all_vals, y_min=y_min, y_max=y_max)

        elements = []
        elements.append(
            f'<text x="{margin_left}" y="{top - 10}" font-size="14" font-family="Arial" fill="#222">{svg_escape(title)}</text>'
        )

        # y-axis and grid
        ticks = 4
        for i in range(ticks + 1):
            t = y_min_s + (y_max_s - y_min_s) * i / ticks
            y = y_to_px(t, y_min_s, y_max_s, top)
            elements.append(
                f'<line x1="{margin_left}" y1="{y:.1f}" x2="{margin_left + panel_w}" y2="{y:.1f}" stroke="#eee" />'
            )
            elements.append(
                f'<text x="{margin_left - 8}" y="{y + 4:.1f}" font-size="11" font-family="Arial" fill="#444" text-anchor="end">{t:.2f}</text>'
            )

        # axes
        elements.append(
            f'<line x1="{margin_left}" y1="{top}" x2="{margin_left}" y2="{top + panel_h}" stroke="#333" />'
        )
        elements.append(
            f'<line x1="{margin_left}" y1="{top + panel_h}" x2="{margin_left + panel_w}" y2="{top + panel_h}" stroke="#333" />'
        )

        # optional horizontal line at 1.0
        if draw_one_line and y_min_s <= 1.0 <= y_max_s:
            y = y_to_px(1.0, y_min_s, y_max_s, top)
            elements.append(
                f'<line x1="{margin_left}" y1="{y:.1f}" x2="{margin_left + panel_w}" y2="{y:.1f}" stroke="#999" stroke-dasharray="4 4" />'
            )

        # plot series
        for vals, color in zip(series, colors):
            points = []
            for x, v in zip(xs, vals):
                y = y_to_px(v, y_min_s, y_max_s, top)
                points.append((x, y))
                elements.append(
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}" />'
                )
            elements.append(polyline(points, color))

        # y label
        elements.append(
            f'<text x="{margin_left - 48}" y="{top + panel_h / 2:.1f}" font-size="12" font-family="Arial" fill="#222" text-anchor="middle" transform="rotate(-90 {margin_left - 48},{top + panel_h / 2:.1f})">{svg_escape(y_label)}</text>'
        )

        return "\n".join(elements)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff" />',
        f'<text x="{width / 2:.1f}" y="22" text-anchor="middle" font-size="16" font-family="Arial" fill="#111">Pointer-Chase: Speedup / IPC / LLC Miss Rate vs Working Set</text>',
    ]

    top1 = margin_top
    svg.append(
        draw_panel(
            "Speedup (guarded/contract)",
            [speedup],
            ["#2b6cb0"],
            "Speedup",
            top1,
            draw_one_line=True,
        )
    )

    top2 = margin_top + panel_h + gap
    svg.append(
        draw_panel(
            "IPC",
            [ipc_guarded, ipc_contract],
            ["#2f855a", "#dd6b20"],
            "IPC",
            top2,
        )
    )

    top3 = margin_top + 2 * (panel_h + gap)
    svg.append(
        draw_panel(
            "LLC Miss Rate",
            [llc_guarded, llc_contract],
            ["#2f855a", "#dd6b20"],
            "LLC Miss Rate",
            top3,
        )
    )

    # x-axis labels on bottom panel
    y_label = top3 + panel_h + 30
    for x, label in zip(xs, worksets):
        svg.append(
            f'<text x="{x:.1f}" y="{y_label}" font-size="12" font-family="Arial" fill="#222" text-anchor="middle">{label}</text>'
        )

    # legend
    legend_x = margin_left + panel_w - 210
    legend_y = margin_top + 10
    svg.append(
        f'<rect x="{legend_x}" y="{legend_y}" width="190" height="58" fill="#fff" stroke="#ddd" />'
    )
    svg.append(
        f'<circle cx="{legend_x + 10}" cy="{legend_y + 16}" r="4" fill="#2f855a" />'
    )
    svg.append(
        f'<text x="{legend_x + 22}" y="{legend_y + 20}" font-size="11" font-family="Arial" fill="#222">guarded</text>'
    )
    svg.append(
        f'<circle cx="{legend_x + 10}" cy="{legend_y + 34}" r="4" fill="#dd6b20" />'
    )
    svg.append(
        f'<text x="{legend_x + 22}" y="{legend_y + 38}" font-size="11" font-family="Arial" fill="#222">contract</text>'
    )

    svg.append("</svg>")

    out_path = Path(OUT_SVG)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(svg), encoding="utf-8")


if __name__ == "__main__":
    main()
