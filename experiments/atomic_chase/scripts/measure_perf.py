import csv
import glob
import os
import shutil
import subprocess
from collections import defaultdict

DEPTHS = [2, 3, 5, 8]
BINARIES = [
    ("O2", "naive", "bench_naive"),
    ("O2", "atomic", "bench_atomic"),
    ("O3", "naive", "bench_naive_O3"),
    ("O3", "atomic", "bench_atomic_O3"),
]

EVENT_PROFILES = [
    ("hardware", ["instructions", "cycles", "branches", "branch-misses"]),
    ("software_fallback", ["task-clock", "context-switches", "cpu-migrations", "page-faults"]),
]


def find_perf() -> str:
    env_perf = os.environ.get("PERF_PATH")
    if env_perf and os.path.isfile(env_perf) and os.access(env_perf, os.X_OK):
        return env_perf

    home = os.path.expanduser("~")
    local_candidates = [
        os.path.join(home, "WSL2-Linux-Kernel", "tools", "perf", "perf"),
        os.path.join(home, "Downloads", "WSL2-Linux-Kernel", "tools", "perf", "perf"),
    ]
    for candidate in local_candidates:
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    candidates = glob.glob("/usr/lib/linux-tools-*/perf")
    if candidates:
        return sorted(candidates)[-1]

    in_path = shutil.which("perf")
    if in_path:
        return in_path

    raise RuntimeError("perf binary not found. Set PERF_PATH or install/build perf.")


def normalize_event(event_name: str) -> str:
    # perf often emits events as "event:u"; strip any modifiers for matching.
    return event_name.split(":", 1)[0]


def run_perf(perf_path: str, binary: str, depth: int, events: list[str]) -> dict:
    cmd = [
        perf_path,
        "stat",
        "-x,",
        "-e",
        ",".join(events),
        "--",
        "taskset",
        "-c",
        "0",
        f"./{binary}",
        str(depth),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    results = {event: None for event in events}
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


def select_event_profile(perf_path: str) -> tuple[str, list[str]]:
    probe_binary = BINARIES[0][2]
    probe_depth = DEPTHS[0]

    for profile_name, events in EVENT_PROFILES:
        metrics = run_perf(perf_path, probe_binary, probe_depth, events)
        if any(v is not None for v in metrics.values()):
            return profile_name, events

    # Keep output schema stable even if nothing is supported.
    return EVENT_PROFILES[-1]


def main():
    perf_path = find_perf()
    event_profile, events = select_event_profile(perf_path)
    out_csv = os.path.join("results_perf.csv")
    out_md = os.path.join("results_perf.md")
    out_graph_dir = os.path.join("graphs", "perf")

    os.makedirs(out_graph_dir, exist_ok=True)

    rows = []
    for opt, mode, binary in BINARIES:
        for depth in DEPTHS:
            metrics = run_perf(perf_path, binary, depth, events)
            row = {
                "event_profile": event_profile,
                "opt": opt,
                "mode": mode,
                "depth": depth,
            }
            row.update(metrics)
            rows.append(row)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["event_profile", "opt", "mode", "depth"] + events)
        for r in rows:
            writer.writerow([r["event_profile"], r["opt"], r["mode"], r["depth"]] + [r.get(e, "") for e in events])

    with open(out_md, "w", newline="\n") as f:
        f.write("## Atomic chase perf (per depth)\n\n")
        f.write(f"- perf binary: `{perf_path}`\n")
        f.write(f"- event profile: `{event_profile}`\n\n")
        header = "| event_profile | opt | mode | depth | " + " | ".join(events) + " |\n"
        align = "|---|---|---|---:|" + "---:|" * len(events) + "\n"
        f.write(header)
        f.write(align)
        for r in rows:
            vals = " | ".join(str(r.get(e, "")) for e in events)
            f.write(f"| {r['event_profile']} | {r['opt']} | {r['mode']} | {r['depth']} | {vals} |\n")

    # Graphs (optional)
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        print("matplotlib not available; skipping graph generation.")
        return

    grouped = defaultdict(list)
    for r in rows:
        grouped[(r["opt"], r["mode"])].append(r)
    for key in grouped:
        grouped[key].sort(key=lambda x: x["depth"])

    for event in events:
        plt.figure(figsize=(9, 5))
        plotted = False
        for (opt, mode), series in grouped.items():
            xs = [s["depth"] for s in series]
            ys = [s[event] for s in series]
            if any(v is None for v in ys):
                continue
            plt.plot(xs, ys, marker="o", label=f"{mode} {opt}")
            plotted = True
        plt.title(f"{event} vs depth")
        plt.xlabel("depth")
        plt.ylabel(event)
        plt.xticks(DEPTHS)
        plt.grid(True, linestyle="--", alpha=0.4)
        if plotted:
            plt.legend()
        else:
            plt.text(0.5, 0.5, "No supported data for this event", ha="center", va="center", transform=plt.gca().transAxes)
        out_path = os.path.join(out_graph_dir, f"perf_{event.replace('-', '_')}.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=160)
        plt.close()


if __name__ == "__main__":
    main()
