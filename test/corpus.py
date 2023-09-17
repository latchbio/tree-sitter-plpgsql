from ast import literal_eval
from dataclasses import dataclass
import dataclasses
from pathlib import Path
import re
import time
from tree_sitter import Language, Node, Parser

from .utils import import_module_by_path, good_marker, bad_marker

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


node_data_checked_fields = ["idx", "field", "type", "text"]
node_data_nullable_fields = {"idx"}

word_re = re.compile(r"\w+")


@dataclass
class NodeData:
    idx: int | None = None
    field: str | None = None
    type: str | None = None
    text: bytes | None = None
    children: list["NodeData"] = dataclasses.field(default_factory=list)

    def has_error(self):
        if self.type == "ERROR":
            return True

        return any(x.has_error() for x in self.children)

    def compare(self, that: "NodeData", *, ignore_nulls=False, allow_missing=False):
        for name in node_data_checked_fields:
            a = getattr(self, name)
            b = getattr(that, name)

            if a == b:
                continue

            if name in node_data_nullable_fields and a is None or b is None:
                continue

            if not ignore_nulls:
                return False

            if a is None or b is None:
                continue

            return False

        if allow_missing:
            idx = 0
            for b in that.children:
                if idx >= len(self.children):
                    return False

                a = self.children[idx]

                while not a.compare(
                    b, ignore_nulls=ignore_nulls, allow_missing=allow_missing
                ):
                    idx += 1

                    if idx >= len(self.children):
                        return False
                    a = self.children[idx]

                idx += 1

            return True

        if len(self.children) != len(that.children):
            return False

        return all(
            a.compare(b, ignore_nulls=ignore_nulls, allow_missing=allow_missing)
            for a, b in zip(self.children, that.children)
        )

    def render(self, *, indent="    "):
        res = ""
        if self.idx is not None:
            res += f"{self.idx} "

        if self.field is not None:
            res += f"({self.field}) "

        if self.type is not None:
            if word_re.match(self.type) is None:
                res += f"{repr(self.type)}"
            else:
                res += f"{self.type}"

        if self.text is not None:
            res += f": {repr(self.text)}"

        if len(self.children) > 0:
            children = "\n".join(
                indent + x.render(indent=indent + "    ") for x in self.children
            )
            res += f"\n{children}"

        return res

    def __str__(self):
        return self.render()


rendered_re = re.compile(
    r"""
    ^
    (?P<indent>[ ]*)
    (
        (?P<idx>\d+)
        [ ]+
    )?
    (
        \(
        (?P<name>[^)]*)
        \)
        [ ]*
    )?
    (?P<type>\w+)?
    (?P<raw_type>
        '[^']*' |
        "[^"]*"
    )?
    (
        :
        [ ]+
        (?P<text>
            b'.*' |
            b".*" |
            '.*' |
            ".*"
        )
    )?
    $
    """,
    re.VERBOSE,
)


def read_rendered(data: str):
    stack = []
    indent_stack = []
    for l in data.splitlines():
        if len(l) == 0:
            continue

        if l.lstrip()[0] == "#":
            continue

        match = rendered_re.match(l)
        if match is None:
            raise RuntimeError(f"invalid line: {repr(l)}")

        indent_str: str = match.group("indent")
        idx: str | None = match.group("idx")
        name: str | None = match.group("name")
        type: str | None = match.group("type")
        raw_type: str | None = match.group("raw_type")
        text_str: str | None = match.group("text")

        indent = len(indent_str)
        idx_int = int(idx) if idx is not None else None

        text: str | bytes | None = (
            literal_eval(text_str) if text_str is not None else None
        )
        if isinstance(text, str):
            text = text.encode()

        if type is None and raw_type is not None:
            type = literal_eval(raw_type)

        res = NodeData(idx=idx_int, field=name, type=type, text=text)
        if indent == 0:
            assert len(stack) == 0

            stack = [res]
            indent_stack = [0]

            continue

        parent = stack[-1]
        parent_indent = indent_stack[-1]

        while indent <= parent_indent:
            stack.pop()
            indent_stack.pop()

            parent = stack[-1]
            parent_indent = indent_stack[-1]

        stack.append(res)
        indent_stack.append(indent)

        parent.children.append(res)

    assert len(stack) > 0

    return stack[0]


def load_ast(cur: Node):
    res = NodeData(type=cur.type)

    if len(cur.children) == 0:
        res.text = cur.text

    for idx, x in enumerate(cur.children):
        child = load_ast(x)
        child.idx = idx
        child.field = cur.field_name_for_child(idx)

        res.children.append(child)

    return res


ignored_names = {"__pycache__"}


def walk(cur: Path, out: Path, *, indent=""):
    if cur.name in ignored_names:
        return

    if cur.is_file():
        if cur.suffix != ".py":
            return

        case = import_module_by_path(cur)
        given: str | bytes = case.given
        outline: str = case.outline
        expected: str = case.expected

        given_bytes = given if isinstance(given, bytes) else given.encode()

        ast = parser.parse(given_bytes)
        ast_data = load_ast(ast.root_node)

        outline_data = read_rendered(outline)
        expected_data = read_rendered(expected)

        outline_with_error = outline_data.has_error()

        out.parent.mkdir(parents=True, exist_ok=True)
        out.with_suffix(".txt").write_text(str(ast_data))

        outline_ok = ast_data.compare(
            outline_data, ignore_nulls=True, allow_missing=True
        )
        expected_ok = ast_data.compare(expected_data)
        if not outline_with_error and expected_data.has_error():
            expected_ok = False

        outline_marker = good_marker
        if not outline_ok:
            outline_marker = bad_marker

        expected_marker = good_marker
        if not expected_ok:
            expected_marker = bad_marker

        print(
            f"{indent}{expected_marker} {cur.name}: {outline_marker} {expected_marker}"
        )

        return

    if not cur.is_dir():
        return

    print(f"{indent}{cur.name}:")
    for x in cur.iterdir():
        walk(x, out / x.name, indent=indent + "  ")


root = Path(__file__).parent / "corpus"
out_root = Path(__file__).parent / "out" / "corpus"

walk(root, out_root)
