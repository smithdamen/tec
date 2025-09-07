#!/usr/bin/env python3
"""Generate Google-style docstring stubs (docstrings only) for symbols missing them.

Usage:
    python tools/gen_docstring_stubs.py src/tec > docs/assets/docstring_stubs.md

This script is READ-ONLY: it prints Markdown with copy/pastable triple-quoted docstrings
and tells you exactly where to paste them (file path + line number).
"""

from __future__ import annotations

import ast
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import cast


def _ann(node: ast.AST | None) -> str:
    """Return a best-effort string for a type annotation AST node."""
    if node is None:
        return "Any"
    try:
        return ast.unparse(node)
    except Exception:
        return "Any"


def _format_args(a: ast.arguments) -> list[str]:
    """Return argument strings with annotations, excluding implicit self/cls."""
    items: list[str] = []
    posonly = getattr(a, "posonlyargs", [])
    for arg in [*posonly, *a.args]:
        items.append(f"{arg.arg}: {_ann(arg.annotation)}")
    if a.vararg is not None:
        items.append(f"*{a.vararg.arg}: {_ann(a.vararg.annotation)}")
    for arg in a.kwonlyargs:
        items.append(f"{arg.arg}: {_ann(arg.annotation)}")
    if a.kwarg is not None:
        items.append(f"**{a.kwarg.arg}: {_ann(a.kwarg.annotation)}")
    # Skip leading self/cls in docs
    return [s for s in items if not s.startswith(("self:", "cls:"))]


def _func_doc(name: str, fn: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Build a Google-style function/method docstring stub."""
    args = _format_args(fn.args)
    returns = _ann(getattr(fn, "returns", None)) if getattr(fn, "returns", None) else "None"
    lines = [f'"""TODO: Summary for `{name}`.', "", "Args:"]
    if args:
        lines += [f"    {a}: TODO." for a in args]
    else:
        lines.append("    (none)")
    lines += [
        "",
        "Returns:",
        f"    {returns}: TODO.",
        "",
        "Raises:",
        "    (none)",
        "",
        '"""',
    ]
    return "\n".join(lines)


def _class_doc(name: str) -> str:
    """Build a Google-style class docstring stub."""
    return "\n".join(
        [
            f'"""TODO: Summary for `{name}`.',
            "",
            "Attributes:",
            "    TODO",
            '"""',
        ]
    )


def _module_doc(module_path: str) -> str:
    """Build a module docstring stub."""
    return "\n".join(
        [
            f'"""TODO: Module summary for {module_path}.',
            "",
            "Key concepts:",
            "- TODO",
            '"""',
        ]
    )


def _rel_paths(root: Path) -> list[Path]:
    """Return Python files under root, excluding tests directory."""
    return [p for p in root.rglob("*.py") if "/tests/" not in p.as_posix()]


def _emit_header(title: str) -> None:
    """Print a Markdown section header."""
    print(f"\n## {title}\n")


def _emit_block(desc: str, code: str) -> None:
    """Print a Markdown description + code block."""
    print(desc)
    print("\n```python")
    print(code)
    print("```")
    print()


def _iter_toplevel(tree: ast.AST) -> Iterable[ast.AST]:
    """Yield top-level nodes from a parsed module tree."""
    body = getattr(tree, "body", [])
    return cast(Iterable[ast.AST], body)


def main() -> None:
    """Entry point."""
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/tec")
    files = _rel_paths(root)
    if not files:
        print(f"# No Python files found under {root}")
        return

    print("# Docstring stubs (auto-generated)")
    print("_Paste these inside the indicated module/class/function as the first statement._")

    for path in sorted(files):
        try:
            src = path.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except Exception:
            continue

        emitted_any = False

        # Module docstring
        if not ast.get_docstring(tree):
            if not emitted_any:
                _emit_header(path.as_posix())
                emitted_any = True
            _emit_block("**Module docstring (paste at very top):**", _module_doc(path.as_posix()))

        # Classes and functions
        for node in _iter_toplevel(tree):
            if isinstance(node, ast.ClassDef):
                if (not node.name.startswith("_")) and (not ast.get_docstring(node)):
                    if not emitted_any:
                        _emit_header(path.as_posix())
                        emitted_any = True
                    desc = (
                        f"**Class `{node.name}` docstring "
                        f"(paste inside class at line {node.lineno}):**"
                    )
                    _emit_block(desc, _class_doc(node.name))

                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef | ast.AsyncFunctionDef):
                        if sub.name.startswith("_"):
                            continue
                        if not ast.get_docstring(sub):
                            if not emitted_any:
                                _emit_header(path.as_posix())
                                emitted_any = True
                            desc = (
                                f"**Method `{node.name}.{sub.name}` docstring "
                                f"(paste inside method at line {sub.lineno}):**"
                            )
                            _emit_block(desc, _func_doc(sub.name, sub))

            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                if node.name.startswith("_"):
                    continue
                if not ast.get_docstring(node):
                    if not emitted_any:
                        _emit_header(path.as_posix())
                        emitted_any = True
                    desc = (
                        f"**Function `{node.name}` docstring "
                        f"(paste inside function at line {node.lineno}):**"
                    )
                    _emit_block(desc, _func_doc(node.name, node))


if __name__ == "__main__":
    main()
