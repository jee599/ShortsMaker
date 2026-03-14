from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shortsmaker",
        description="Bootstrap CLI for the ShortsMaker workspace.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="info",
        choices=["info"],
        help="Command to run.",
    )
    return parser


def handle_info() -> None:
    root = resolve_repo_root()
    print("ShortsMaker workspace is ready.")
    print(f"Repository root: {root}")
    print("Next step: define the first end-to-end video generation workflow.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "info":
        handle_info()
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2
