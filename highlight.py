from pathlib import Path
import sys
import time
from tree_sitter import Language, Node, Parser

print("compiling")
start = time.monotonic()
Language.build_library(
    "build/python.so",
    [
        ".",
    ],
)
print(f"done {time.monotonic() - start:.3f}s")

plpgsql = Language("build/python.so", "plpgsql")

parser = Parser()
parser.set_language(plpgsql)


def render(cur: Node):
    if cur.child_count == 0:
        sys.stdout.write(cur.text.decode())
        return

    for x in cur.children:
        render(x)


file = Path("../vacuole/schema/accounts/accounts.sql")
ast = parser.parse(file.read_bytes())
r = ast.root_node
# render(ast.root_node)
