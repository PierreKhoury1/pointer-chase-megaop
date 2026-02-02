import sys

def generate_c_code(depth):
    # Construct the base pointer type (e.g., int***)
    ptr_type = "int" + ("*" * depth)
    
    # Create arbitrary offsets for the constant arithmetic example
    const_offsets = [2, 5, 17, 3, 7, 11, 13][:depth]
    if len(const_offsets) < depth:
        const_offsets += [depth + i for i in range(depth - len(const_offsets))]

    # 1. Simple N-tuple pointer access
    deref_stars = "*" * depth
    access_simple = f"""
static int access_n_tuple_pointer ({ptr_type} p) {{
  int tmp = {deref_stars}p;
  return tmp;
}}
"""

    # 2. Constant pointer arithmetic
    # Build string like *((*((*(p + 2)) + 5)) + 17)
    const_arith = "p"
    for offset in const_offsets:
        const_arith = f"*({const_arith} + {offset})"
    
    access_const = f"""
static int access_with_constant_pointer_arithmetic({ptr_type} p) {{
  int tmp = {const_arith};
  return tmp;
}}
"""

    # 3. Dynamic pointer arithmetic
    offsets_args = ", ".join([f"int offset{i+1}" for i in range(depth)])
    dyn_arith = "p"
    for i in range(depth):
        dyn_arith = f"*({dyn_arith} + offset{i+1})"

    access_dyn = f"""
static int access_with_pointer_arithmetic({ptr_type} p, {offsets_args}) {{
  int tmp = {dyn_arith};
  return tmp;
}}
"""

    # 4. Pointer arithmetic with checks
    check_decls = []
    for i in range(depth, 0, -1):
        stars = "*" * i
        check_decls.append(f"int check_{'p' * i}(int{stars} p);")
    check_decls.append("int check(int p);")
    
    check_decls_str = "\n".join(check_decls)

    check_body_lines = []
    check_body_lines.append(f"  check_{'p' * depth}(p);")
    current_var = "p"
    for i in range(1, depth):
        next_var = f"tmp{i}"
        stars = "*" * (depth - i)
        check_body_lines.append(f"  int{stars} {next_var} = *({current_var} + offset{i});")
        check_body_lines.append(f"  check_{'p' * (depth - i)}({next_var});")
        current_var = next_var
    
    check_body_lines.append(f"  int tmp = *({current_var} + offset{depth});")
    check_body_lines.append(f"  check(tmp);")
    check_body_lines.append(f"  return tmp;")
    
    check_body_str = "\n".join(check_body_lines)

    access_checks = f"""
{check_decls_str}

static int access_with_pointer_arithmetic_and_checks({ptr_type} p, {offsets_args}) {{
{check_body_str}
}}
"""

    # Combine all
    template = f"""#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

{access_simple}
{access_const}
{access_dyn}
{access_checks}

int main(void) {{
  return 0;
}}
"""
    return template

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            d = int(sys.argv[1])
            if d < 1: raise ValueError
            print(generate_c_code(d))
        except ValueError:
            print("Please provide a positive integer for depth.")
    else:
        # Default example depth 3
        print(generate_c_code(3))

