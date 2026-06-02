"""Command line interface for stratified certificate projects."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .model import PROJECT_FILE, load_project, resolve_project_file, validate_project
from .report import build_markdown_report
from .templates import new_toy_project


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        return _init_project(Path(args.path), force=args.force)
    if args.command == "validate":
        return _validate(Path(args.path))
    if args.command == "report":
        return _report(Path(args.path), Path(args.out))

    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stratcert",
        description="Manage source-agnostic stratified certificate classification projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a generic starter project")
    init_parser.add_argument("path", help="project directory to create")
    init_parser.add_argument("--force", action="store_true", help="overwrite an existing classification file")

    validate_parser = subparsers.add_parser("validate", help="validate a project file or directory")
    validate_parser.add_argument("path", help="project directory or classification JSON file")

    report_parser = subparsers.add_parser("report", help="compile a markdown report")
    report_parser.add_argument("path", help="project directory or classification JSON file")
    report_parser.add_argument("--out", required=True, help="markdown output path")

    return parser


def _init_project(path: Path, force: bool = False) -> int:
    path.mkdir(parents=True, exist_ok=True)
    (path / "certificates").mkdir(exist_ok=True)
    (path / "reports").mkdir(exist_ok=True)

    project_file = path / PROJECT_FILE
    if project_file.exists() and not force:
        print(f"{project_file} already exists; pass --force to overwrite", file=sys.stderr)
        return 1

    project_file.write_text(
        json.dumps(new_toy_project(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"created {project_file}")
    return 0


def _validate(path: Path) -> int:
    project = load_project(path)
    errors = validate_project(project)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"valid: {resolve_project_file(path)}")
    return 0


def _report(path: Path, out: Path) -> int:
    project = load_project(path)
    errors = validate_project(project)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_markdown_report(project), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
