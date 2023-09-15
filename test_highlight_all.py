from pathlib import Path
import subprocess
from textwrap import dedent

root_out = Path("./test_highlighted")
root = Path("../vacuole/schema")

ignore = {".DS_Store"}


def highlight_all(cur: Path, out_p: Path, indent=""):
    index_entries: list[str] = []
    for x in cur.iterdir():
        if x.name in ignore:
            continue

        if x.is_dir():
            print(f"{indent}{x.name}:")

            index_entries.append(f"{x.name}/index.html")
            highlight_all(x, out_p / x.name, indent + "  ")
        elif x.is_file():
            out_p.mkdir(parents=True, exist_ok=True)

            out_file = (out_p / x.name).with_suffix(".html")
            index_entries.append(out_file.name)

            with out_file.open("w") as f:
                subprocess.run(
                    ["./node_modules/.bin/tree-sitter", "highlight", x, "--html"],
                    stdout=f,
                )
            print(f"{indent}{x.name}")

    index_html = "\n".join(f'<li><a href="{x}">{x}</a></li>' for x in index_entries)
    (out_p / "index.html").write_text(dedent(f"""
        <ul>
        {index_html}
        </ul>
    """))


highlight_all(root, root_out)
