from pathlib import Path
from typing import Literal, NotRequired, TypedDict
import json5
import json

src = Path(__file__).parent / "vscode_themes" / "dark_plus.json"


def load(x: Path):
    data = json5.loads(x.read_text())
    assert isinstance(data, dict)

    tokenColors = data["tokenColors"]
    assert isinstance(tokenColors, list)

    include = data.get("include")
    if include is not None:
        tokenColors.extend(load(x.parent / include))

    return tokenColors


class Settings(TypedDict):
    foreground: NotRequired[str]
    fontStyle: NotRequired[
        Literal["italic"]
        | Literal["bold"]
        | Literal["underline"]
        | Literal["strikethrough"]
    ]


class TokenColor(TypedDict):
    scope: str | list[str]
    settings: Settings


def to_tree_sitter(data: list[TokenColor]):
    res = {}
    for x in data:
        scope = x["scope"]
        if isinstance(scope, str):
            scope = [scope]

        s = x["settings"]
        tree_sitter_data = {}
        if "foreground" in s:
            tree_sitter_data["color"] = s["foreground"]
        if s.get("fontStyle") == "italic":
            tree_sitter_data["italic"] = True
        if s.get("fontStyle") == "bold":
            tree_sitter_data["bold"] = True
        if s.get("fontStyle") == "underline":
            tree_sitter_data["underline"] = True

        for cur in scope:
            res[cur] = tree_sitter_data

    return res


data = load(src)
res = to_tree_sitter(data)
print(json.dumps(res, sort_keys=True))
