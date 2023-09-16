from pathlib import Path
import importlib.util as iu

ansi_green = "\x1b[32m"
ansi_red = "\x1b[31m"
ansi_reset = "\x1b[0m"

good_marker = f"{ansi_green}✓{ansi_reset}"
bad_marker = f"{ansi_red}✗{ansi_reset}"


def import_module_by_path(x: Path):
    spec = iu.spec_from_file_location("metadata", x)
    assert spec is not None
    assert spec.loader is not None

    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
