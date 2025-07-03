import ast
import pathlib
import subprocess

PACKAGE_DIR = pathlib.Path("src/mooch/enhancers")
INIT_FILE = PACKAGE_DIR / "__init__.py"


def get_public_functions_from_file(py_file: pathlib.Path) -> list[str]:
    """Return public function names from a Python file."""
    source = py_file.read_text()
    tree = ast.parse(source)
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")]


def get_module_name(py_file: pathlib.Path) -> str:
    """Return module name relative to PACKAGE_DIR, without .py"""  # noqa: D400, D415
    return py_file.stem


def generate_init() -> None:
    all_entries = []
    import_lines = []

    for py_file in PACKAGE_DIR.glob("*.py"):
        if py_file.name == "__init__.py" or py_file.name.startswith("_"):
            continue

        module_name = get_module_name(py_file)
        public_funcs = get_public_functions_from_file(py_file)

        if public_funcs:
            import_lines.append(f"from .{module_name} import {', '.join(public_funcs)}")
            all_entries.extend(public_funcs)

    content = "\n".join(import_lines) + "\n\n__all__ = " + repr(all_entries) + "\n"
    INIT_FILE.write_text(content)
    print(f"✅ Generated {INIT_FILE} with {len(all_entries)} functions.")  # noqa: T201


def run_ruff() -> None:
    print("🧹 Running ruff format...")  # noqa: T201
    subprocess.run(["ruff", "format", str(INIT_FILE)], check=True)  # noqa: S603 S607

    print("🔀 Running ruff check --fix (may return non-zero exit)...")  # noqa: T201
    subprocess.run(["ruff", "check", "--fix", str(INIT_FILE)], check=False)  # noqa: S603 S607

    print("✅ Ruff finished (even if lint warnings exist).")  # noqa: T201


if __name__ == "__main__":
    generate_init()
    run_ruff()
