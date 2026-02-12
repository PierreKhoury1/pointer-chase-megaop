import csv
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict


DEPTHS = [2, 3, 5, 8]
PATTERNS = ["plain", "const", "dyn", "checks"]
TARGET_METHOD_RE = re.compile(r"^(plain|const|dyn|checks)_d(2|3|5|8)$")

# Bytecode opcodes (numeric) that represent dereference operations.
BC_DEREF = {
    "178",  # getstatic
    "180",  # getfield
    "46", "47", "48", "49", "50", "51", "52", "53",  # xaload
}

GUARD_REASONS = {
    "null_check",
    "range_check",
    "class_check",
    "type_check",
    "array_check",
}

ROOT = Path(__file__).resolve().parents[3]
AOT_DIR = ROOT / "experiments" / "aot"
HOTSPOT_SRC = ROOT / "experiments" / "hotspot" / "src" / "ChaseBench.java"
BRIDGE_DIR = AOT_DIR / "hotspot_bridge"
BRIDGE_BUILD_DIR = BRIDGE_DIR / "build"
BRIDGE_LOG_DIR = BRIDGE_DIR / "logs"
RAW_OUT_DIR = AOT_DIR / "data" / "raw"
PROC_OUT_DIR = AOT_DIR / "data" / "processed"


def run(cmd, **kwargs):
    subprocess.run(cmd, check=True, **kwargs)


def compile_java(source_path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    javac = shutil.which("javac")
    if not javac:
        raise RuntimeError("javac not found in PATH.")
    run([javac, "-d", out_dir, source_path])


def run_java(classpath: str, out_dir: str) -> str:
    java = shutil.which("java")
    if not java:
        raise RuntimeError("java not found in PATH.")

    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "hotspot_log.xml")

    flags = [
        "-Xbatch",
        "-XX:+UnlockDiagnosticVMOptions",
        "-XX:-TieredCompilation",
        "-XX:CompileThreshold=1000",
        "-XX:+PrintCompilation",
        "-XX:+LogCompilation",
        f"-XX:LogFile={log_path}",
        "-XX:CompileCommand=compileonly,ChaseBench::*",
        "-XX:CompileCommand=dontinline,ChaseBench::*",
    ]

    run([java, "-cp", classpath, *flags, "ChaseBench"])
    return log_path


def parse_log_compilation(path: str) -> Dict[str, Dict[str, int]]:
    tree = ET.parse(path)
    root = tree.getroot()

    per_method: Dict[str, Dict[str, int]] = {}

    for task in root.iter("task"):
        method_attr = task.attrib.get("method", "")
        if not method_attr.startswith("ChaseBench "):
            continue

        method_name = method_attr.split()[1]
        if not TARGET_METHOD_RE.match(method_name):
            continue

        bc_total = 0
        deref_ops = 0
        deopts = 0
        guards = 0

        for bc in task.iter("bc"):
            bc_total += 1
            if bc.attrib.get("code") in BC_DEREF:
                deref_ops += 1

        for trap in task.iter("uncommon_trap"):
            deopts += 1
            reason = trap.attrib.get("reason", "")
            if reason in GUARD_REASONS:
                guards += 1

        # Keep the most recent compilation for the method.
        per_method[method_name] = {
            "deref_ops": deref_ops,
            "guards": guards,
            "deopts": deopts,
            "ir_nodes": bc_total,
        }

    return per_method


def write_outputs(results: Dict[str, Dict[str, int]], raw_out_dir: Path, proc_out_dir: Path):
    rows = []
    for name, counts in results.items():
        m = TARGET_METHOD_RE.match(name)
        if not m:
            continue
        pattern, depth = m.group(1), int(m.group(2))
        rows.append((pattern, depth, counts))

    rows.sort(key=lambda r: (PATTERNS.index(r[0]), r[1]))

    raw_out_dir.mkdir(parents=True, exist_ok=True)
    proc_out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = raw_out_dir / "results_hotspot.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pattern", "depth", "deref_ops", "guards", "deopts", "ir_nodes"])
        for pattern, depth, counts in rows:
            writer.writerow(
                [pattern, depth, counts["deref_ops"], counts["guards"], counts["deopts"], counts["ir_nodes"]]
            )

    md_path = proc_out_dir / "results_hotspot.md"
    with open(md_path, "w", newline="\n") as f:
        f.write("## HotSpot (C2) pointer-chase metrics\n\n")
        f.write("| pattern | depth | deref_ops | guards | deopts | ir_nodes |\n")
        f.write("|---|---:|---:|---:|---:|---:|\n")
        for pattern, depth, counts in rows:
            f.write(
                f"| {pattern} | {depth} | {counts['deref_ops']} | {counts['guards']} | "
                f"{counts['deopts']} | {counts['ir_nodes']} |\n"
            )
        f.write("\n")
        f.write("Notes:\n")
        f.write("- deref_ops: count of bytecode ops `getfield/getstatic` and array loads within the parse for the highest-level compile.\n")
        f.write("- guards: count of `uncommon_trap` entries with reasons like null/range/type/class checks.\n")
        f.write("- deopts: total `uncommon_trap` count in the parse (proxy for side-exit points).\n")
        f.write("- ir_nodes: proxy = total bytecode count in the parse for the highest-level compile.\n")
        f.write("- For true C2 IR node counts, a fastdebug JVM with `PrintIdealGraphFile` is required.\n")
        f.write("- Tiered compilation is disabled (`-XX:-TieredCompilation`) to capture a single C2-style compile.\n")


def main() -> None:
    out_dir = BRIDGE_BUILD_DIR
    java_src = HOTSPOT_SRC
    log_dir = BRIDGE_LOG_DIR

    # Keep compiler output in a writable local build dir.
    java_copy = out_dir / "ChaseBench.java"
    if not java_copy.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(java_src, "r", encoding="utf-8") as src:
            with open(java_copy, "w", newline="\n") as dst:
                dst.write(src.read())
    compile_java(str(java_copy), str(out_dir))
    log_path = run_java(str(out_dir), str(out_dir))

    log_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(log_path, log_dir / "hotspot_log.xml")

    results = parse_log_compilation(log_path)
    write_outputs(results, RAW_OUT_DIR, PROC_OUT_DIR)


if __name__ == "__main__":
    main()
