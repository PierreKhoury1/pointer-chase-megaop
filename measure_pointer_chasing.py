import os
import re
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple


DEPTHS = [2, 3, 5, 8]
PATTERNS = ["plain", "const", "dyn", "checks"]
COMPILERS = ["gcc", "clang"]
OPTS = ["0", "2"]


@dataclass
class Counts:
    loads: int = 0
    branches: int = 0
    labels: int = 0
    instructions: int = 0

    @property
    def basic_blocks(self) -> int:
        return 1 + self.labels


def build_expr(base: str, offsets: List[str]) -> str:
    expr = base
    for off in offsets:
        expr = f"*({expr} + {off})"
    return expr


def generate_c(path: str) -> List[str]:
    lines: List[str] = []
    lines.append("#include <stdint.h>")
    lines.append("#include <stddef.h>")
    lines.append("")
    lines.append("#if defined(__GNUC__)")
    lines.append("#define NOINLINE __attribute__((noinline))")
    lines.append("#define USED __attribute__((used))")
    lines.append("#else")
    lines.append("#define NOINLINE")
    lines.append("#define USED")
    lines.append("#endif")
    lines.append("")
    lines.append("#define GUARD(ptr) do { if (!(ptr)) __builtin_trap(); } while (0)")
    lines.append("")

    func_names: List[str] = []

    for depth in DEPTHS:
        ptr_type = "int " + "*" * depth

        # Plain dereference
        func = f"plain_d{depth}"
        func_names.append(func)
        deref = "p"
        for _ in range(depth):
            deref = f"*({deref})"
        lines.append(f"NOINLINE USED int {func}({ptr_type} p) {{")
        lines.append(f"  return {deref};")
        lines.append("}")
        lines.append("")

        # Constant offsets
        func = f"const_d{depth}"
        func_names.append(func)
        const_offsets = [2, 5, 17, 3, 7, 11, 13, 19]
        offsets = [str(const_offsets[i]) for i in range(depth)]
        expr = build_expr("p", offsets)
        lines.append(f"NOINLINE USED int {func}({ptr_type} p) {{")
        lines.append(f"  return {expr};")
        lines.append("}")
        lines.append("")

        # Dynamic offsets
        func = f"dyn_d{depth}"
        func_names.append(func)
        offset_args = [f"int o{i+1}" for i in range(depth)]
        offsets = [f"o{i+1}" for i in range(depth)]
        expr = build_expr("p", offsets)
        args = ", ".join([ptr_type + " p"] + offset_args)
        lines.append(f"NOINLINE USED int {func}({args}) {{")
        lines.append(f"  return {expr};")
        lines.append("}")
        lines.append("")

        # Explicit per-level checks (null only), dynamic offsets
        func = f"checks_d{depth}"
        func_names.append(func)
        args = ", ".join([ptr_type + " p"] + offset_args)
        lines.append(f"NOINLINE USED int {func}({args}) {{")
        lines.append("  GUARD(p);")
        current = "p"
        for i in range(1, depth):
            stars = "*" * (depth - i)
            next_ptr = f"p{i}"
            lines.append(f"  int {stars}{next_ptr} = *({current} + o{i});")
            lines.append(f"  GUARD({next_ptr});")
            current = next_ptr
        lines.append(f"  return *({current} + o{depth});")
        lines.append("}")
        lines.append("")

    with open(path, "w", newline="\n") as f:
        f.write("\n".join(lines).strip() + "\n")

    return func_names


def run(cmd: List[str]) -> None:
    subprocess.run(cmd, check=True)


def is_instruction(line: str) -> bool:
    if not line:
        return False
    if line.startswith("."):
        return False
    if line.endswith(":"):
        return False
    if line.startswith("#"):
        return False
    return True


def split_operands(ops: str) -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    for ch in ops:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            part = "".join(buf).strip()
            if part:
                parts.append(part)
            buf = []
            continue
        buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def parse_instruction(line: str) -> Tuple[str, List[str]]:
    # Strip comments
    line = line.split("#", 1)[0].strip()
    if not line:
        return "", []
    parts = line.split(None, 1)
    mnemonic = parts[0]
    operands: List[str] = []
    if len(parts) > 1:
        operands = split_operands(parts[1])
    return mnemonic, operands


def is_mem(op: str) -> bool:
    return "(" in op and ")" in op


def is_reg(op: str) -> bool:
    return op.startswith("%")


def count_in_function(lines: List[str], func_names: List[str]) -> Dict[str, Counts]:
    counts: Dict[str, Counts] = {name: Counts() for name in func_names}
    current: str | None = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        # Function label or block label
        m = re.match(r"^([A-Za-z_.$][\w.$]*):", line)
        if m:
            label = m.group(1)
            if label in counts:
                current = label
            elif current is not None:
                if not label.startswith(".Lfunc_end"):
                    counts[current].labels += 1
            continue

        if current is None:
            continue

        if line.startswith(".size") and current in line:
            current = None
            continue

        if not is_instruction(line):
            continue

        mnemonic, operands = parse_instruction(line)
        if not mnemonic:
            continue

        counts[current].instructions += 1

        # Branches: conditional/unconditional jumps
        if mnemonic.startswith("j"):
            counts[current].branches += 1

        # Loads: mov* with memory source and register dest
        if mnemonic.startswith("mov") and len(operands) == 2:
            src, dst = operands[0], operands[1]
            if is_mem(src) and is_reg(dst):
                counts[current].loads += 1

    return counts


def compile_and_count(c_path: str, func_names: List[str], compiler: str, opt: str) -> Dict[str, Counts]:
    asm_path = os.path.join("build", f"{compiler}_O{opt}.s")
    cmd = [
        compiler,
        "-S",
        f"-O{opt}",
        "-fno-asynchronous-unwind-tables",
        "-fno-unwind-tables",
        "-fno-exceptions",
        "-fno-stack-protector",
        "-fno-ident",
        "-g0",
        "-o",
        asm_path,
        c_path,
    ]
    run(cmd)
    with open(asm_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return count_in_function(lines, func_names)


def main() -> None:
    os.makedirs("build", exist_ok=True)
    c_path = os.path.join("build", "generated_pointer_chase.c")
    func_names = generate_c(c_path)

    rows: List[Tuple[str, str, str, int, Counts]] = []

    for compiler in COMPILERS:
        for opt in OPTS:
            counts = compile_and_count(c_path, func_names, compiler, opt)
            for name in func_names:
                # name pattern: {pattern}_d{depth}
                pattern, depth_str = name.split("_d")
                depth = int(depth_str)
                rows.append((compiler, opt, pattern, depth, counts[name]))

    # Sort for stable output
    rows.sort(key=lambda r: (r[0], r[1], PATTERNS.index(r[2]), r[3]))

    # Write CSV
    csv_path = os.path.join("build", "results_aot.csv")
    with open(csv_path, "w", newline="\n") as f:
        f.write("compiler,opt,pattern,depth,loads,branches,basic_blocks,instructions\n")
        for compiler, opt, pattern, depth, c in rows:
            f.write(
                f"{compiler},O{opt},{pattern},{depth},{c.loads},{c.branches},{c.basic_blocks},{c.instructions}\n"
            )

    # Write Markdown tables per compiler/opt
    md_path = os.path.join("build", "results_aot.md")
    with open(md_path, "w", newline="\n") as f:
        for compiler in COMPILERS:
            for opt in OPTS:
                f.write(f"## {compiler} -O{opt}\n\n")
                f.write("| pattern | depth | loads | branches | basic_blocks | instructions |\n")
                f.write("|---|---:|---:|---:|---:|---:|\n")
                for c2, o2, pattern, depth, c in rows:
                    if c2 == compiler and o2 == opt:
                        f.write(
                            f"| {pattern} | {depth} | {c.loads} | {c.branches} | {c.basic_blocks} | {c.instructions} |\n"
                        )
                f.write("\n")


if __name__ == "__main__":
    main()
