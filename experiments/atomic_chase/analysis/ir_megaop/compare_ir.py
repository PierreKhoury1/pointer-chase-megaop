import os
import re
import subprocess
from collections import defaultdict


def compile_baseline():
    src = "ptrchase_baseline.c"
    out_ll = "ptrchase_baseline.ll"
    subprocess.run(["clang", "-O2", "-S", "-emit-llvm", src, "-o", out_ll], check=True)
    return out_ll


def count_ir_instructions(path: str) -> dict:
    counts = defaultdict(int)
    current = None
    define_re = re.compile(r"^define\s+.*@([^\(]+)\(")
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith(";"):
                continue
            if line.startswith("declare "):
                continue
            m = define_re.match(line)
            if m:
                current = m.group(1)
                continue
            if current is None:
                continue
            if line == "}":
                current = None
                continue
            if line.endswith(":"):
                continue
            if line.startswith("attributes ") or line.startswith("!"):
                continue
            counts[current] += 1
    return counts


def main():
    baseline_ll = compile_baseline()
    mega_ll = "ptrchase_mega.ll"
    if not os.path.exists(mega_ll):
        raise RuntimeError(f"missing {mega_ll}")

    base_counts = count_ir_instructions(baseline_ll)
    mega_counts = count_ir_instructions(mega_ll)

    out_md = "ir_counts.md"
    with open(out_md, "w", newline="\n") as f:
        f.write("## IR instruction counts (proxy for node count)\n\n")
        f.write(f"- baseline IR: `{baseline_ll}`\n")
        f.write(f"- mega-op IR: `{mega_ll}`\n\n")
        f.write("| function | baseline insts | mega-op insts | reduction |\n")
        f.write("|---|---:|---:|---:|\n")

        # explicit pair: chase_normal (baseline) -> chase_mega (mega-op)
        if "chase_normal" in base_counts and "chase_mega" in mega_counts:
            base = base_counts["chase_normal"]
            mega = mega_counts["chase_mega"]
            reduction = base - mega
            f.write(f"| chase_normal -> chase_mega | {base} | {mega} | {reduction} |\n")

        # include remaining baseline-only and mega-only functions
        for fn, base in base_counts.items():
            if fn == "chase_normal":
                continue
            mega = mega_counts.get(fn, None)
            if mega is None:
                f.write(f"| {fn} | {base} | - | - |\n")
                continue
            reduction = base - mega
            f.write(f"| {fn} | {base} | {mega} | {reduction} |\n")

        for fn, mega in mega_counts.items():
            if fn == "chase_mega":
                continue
            if fn not in base_counts:
                f.write(f"| {fn} | - | {mega} | - |\n")

    print(out_md)


if __name__ == "__main__":
    main()
