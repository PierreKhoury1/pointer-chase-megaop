import csv
import os
import shutil
import subprocess
from pathlib import Path

DEPTHS = [2, 3, 5, 8, 16]
MODES = ["guarded"]
EVENTS = ["instructions", "cycles", "branches", "branch-misses"]
MAX_NODES = 256

SCRIPT_DIR = Path(__file__).resolve().parent
EXP_DIR = SCRIPT_DIR.parent
SRC_DIR = EXP_DIR / "src"
CLASS_DIR = EXP_DIR / ".build" / "classes_byte"
RAW_DIR = EXP_DIR / "data" / "raw"
PROC_DIR = EXP_DIR / "data" / "processed"


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
    elem_size = 1
    worksets = []
    if "L1" in sizes:
        nodes = max(64, sizes["L1"] // elem_size)
        nodes = min(nodes, MAX_NODES)
        worksets.append(("L1", nodes * elem_size, nodes, 5_000_000))
    if "L2" in sizes:
        nodes = max(64, sizes["L2"] // elem_size)
        nodes = min(nodes, MAX_NODES)
        worksets.append(("L2", nodes * elem_size, nodes, 3_000_000))
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


def run_perf(perf_path: str, mode: str, depth: int, nodes: int, iters: int) -> dict:
    cmd = [
        perf_path,
        "stat",
        "-x,",
        "-e",
        ",".join(EVENTS),
        "--",
        "taskset",
        "-c",
        "0",
        "java",
        "-cp",
        str(CLASS_DIR),
        "-Xms512m",
        "-Xmx512m",
        "-XX:+UseSerialGC",
        "-XX:-TieredCompilation",
        "-XX:CICompilerCount=1",
        "ContractBenchByte",
        mode,
        str(depth),
        str(nodes),
        str(iters),
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


def compile_java():
    if not shutil.which("javac"):
        raise RuntimeError("javac not found in PATH")
    CLASS_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["javac", "-d", str(CLASS_DIR), str(SRC_DIR / "ContractBenchByte.java")],
        check=True,
    )


def main():
    perf_path = find_perf()
    compile_java()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROC_DIR.mkdir(parents=True, exist_ok=True)

    out_csv = RAW_DIR / "results_contract_jit_byte_perf.csv"
    out_md = PROC_DIR / "results_contract_jit_byte_perf.md"

    worksets = build_worksets()
    rows = []
    for label, bytes_size, nodes, iters in worksets:
        for depth in DEPTHS:
            for mode in MODES:
                metrics = run_perf(perf_path, mode, depth, nodes, iters)
                row = {
                    "workset": label,
                    "bytes": bytes_size,
                    "nodes": nodes,
                    "iters": iters,
                    "mode": mode,
                    "depth": depth,
                }
                row.update(metrics)
                if metrics.get("cycles") is not None:
                    row["cycles_per_iter"] = metrics["cycles"] / iters
                else:
                    row["cycles_per_iter"] = None
                rows.append(row)

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["workset", "bytes", "nodes", "iters", "mode", "depth"]
            + EVENTS
            + ["cycles_per_iter"]
        )
        for r in rows:
            writer.writerow(
                [
                    r["workset"],
                    r["bytes"],
                    r["nodes"],
                    r["iters"],
                    r["mode"],
                    r["depth"],
                ]
                + [r.get(e, "") for e in EVENTS]
                + [r.get("cycles_per_iter", "")]
            )

    with open(out_md, "w", newline="\n") as f:
        f.write("## Pointer-chase contract (JIT byte) perf (depth=8, guarded)\n\n")
        f.write(f"- perf binary: `{perf_path}`\n")
        f.write("- taskset: `-c 0`\n")
        f.write("- JVM: `-Xms512m -Xmx512m -XX:+UseSerialGC -XX:-TieredCompilation`\n")
        f.write("- NOTE: byte index graph is capped at 256 nodes.\n\n")
        header = (
            "| workset | bytes | nodes | iters | mode | depth | "
            + " | ".join(EVENTS)
            + " | cycles/iter |\n"
        )
        align = "|---|---:|---:|---:|---|---:|" + "---:|" * len(EVENTS) + "---:|\n"
        f.write(header)
        f.write(align)
        for r in rows:
            vals = " | ".join(str(r.get(e, "")) for e in EVENTS)
            f.write(
                f"| {r['workset']} | {r['bytes']} | {r['nodes']} | {r['iters']} | "
                f"{r['mode']} | {r['depth']} | {vals} | {r['cycles_per_iter']} |\n"
            )


if __name__ == "__main__":
    main()
