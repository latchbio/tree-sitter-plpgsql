from pathlib import Path
import time
from tree_sitter import Language, Node, Parser

print("compiling")
start = time.monotonic()
Language.build_library(
  'build/python.so',
  [
    '.',
  ]
)
print(f"done {time.monotonic() - start:.3f}s")

plpgsql = Language('build/python.so', 'plpgsql')

parser = Parser()
parser.set_language(plpgsql)

ansi_green = "\x1b[32m"
ansi_red = "\x1b[31m"
ansi_reset = "\x1b[0m"

good_marker = f"{ansi_green}✓{ansi_reset}"
bad_marker = f"{ansi_red}✗{ansi_reset}"

parse_time = 0
total_count = 0
total_size = 0
errored: list[Path] = []

def render(cur: Node, indent=""):
    indent += "  "
    for i, x in enumerate(cur.children):
        name = cur.field_name_for_child(i)
        if name is not None:
            name = f" ({name})"
        else:
            name = ""

        prefix = f"{indent}{i}{name} {x.type}"
        if len(x.children) == 0:
            print(f"{prefix}: {x.text}")
        else:
            print(prefix)
            render(x, indent + "  ")

root = Path("../vacuole/schema")

ignore = {".DS_Store"}
def try_parse(cur: Path, indent=""):
    for x in cur.iterdir():
        if x.name in ignore:
            continue

        if x.is_dir():
            print(f"{indent}{x.name}:")
            try_parse(x, indent + "  ")
        elif x.is_file():
            global total_count
            total_count += 1

            data = x.read_bytes()

            global parse_time
            start = time.monotonic()
            ast = parser.parse(data).root_node
            parse_time += time.monotonic() - start

            global total_size
            total_size += len(data)

            marker = good_marker
            if ast.has_error:
                marker = bad_marker
                errored.append(x)

            print(f"{indent}{x.name}: {marker}")

            # print(f"{indent}{ast.type}:")
            # render(ast, indent)

try_parse(root)

print(
    f"\nTotal: {parse_time:.3f}s (avg {total_size/parse_time/1000/1000:.1f}MB/s)"
    f"\n{good_marker} {total_count - len(errored)} + "
    f"{bad_marker} {len(errored)} = {total_count}"
)

print("\nErrors in:")
for x in errored:
    print(x.relative_to(root))
