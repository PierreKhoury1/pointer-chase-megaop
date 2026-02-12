import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
EXP_DIR = SCRIPT_DIR.parent
SRC_DIR = EXP_DIR / "src"
CLASS_DIR = EXP_DIR / ".build" / "classes_int"
LOG_ROOT = EXP_DIR / "logs"


def compile_java():
    if not shutil.which("javac"):
        raise RuntimeError("javac not found in PATH")
    CLASS_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["javac", "-d", str(CLASS_DIR), str(SRC_DIR / "ContractBench.java")],
        check=True,
    )


def read_cache_bytes():
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
                size = f.read().strip().upper()
        except OSError:
            continue
        if level == "1" and cache_type.lower() == "data":
            if size.endswith("K"):
                return int(size[:-1]) * 1024
            if size.endswith("M"):
                return int(size[:-1]) * 1024 * 1024
    return 32 * 1024


def run(mode, depth, nodes, iters):
    log_dir = LOG_ROOT / "jit_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"ContractBench_{mode}_d{depth}_n{nodes}_i{iters}.log"

    cmd = [
        "java",
        "-cp",
        str(CLASS_DIR),
        "-Xms512m",
        "-Xmx512m",
        "-XX:+UseSerialGC",
        "-XX:-TieredCompilation",
        "-XX:CICompilerCount=1",
        "-XX:+UnlockDiagnosticVMOptions",
        "-XX:+PrintCompilation",
        "-XX:+PrintInlining",
        "ContractBench",
        mode,
        str(depth),
        str(nodes),
        str(iters),
    ]
    with open(log_path, "w", newline="\n") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
    print(str(log_path))


def main():
    if len(sys.argv) < 3:
        print("usage: python3 run_jit_log.py <mode> <depth> [nodes] [iters]")
        print("  mode: guarded | contract")
        print("  default nodes: L1-sized working set")
        print("  default iters: 5,000,000")
        sys.exit(1)

    mode = sys.argv[1]
    depth = int(sys.argv[2])
    if len(sys.argv) > 3:
        nodes = int(sys.argv[3])
    else:
        l1_bytes = read_cache_bytes()
        nodes = max(512, l1_bytes // 4)
    iters = int(sys.argv[4]) if len(sys.argv) > 4 else 5_000_000

    if mode not in ("guarded", "contract"):
        raise RuntimeError("mode must be guarded or contract")

    compile_java()
    run(mode, depth, nodes, iters)


if __name__ == "__main__":
    main()
