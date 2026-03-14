from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from shortsmaker.config import repo_paths
from shortsmaker.job import (
    create_plan,
    create_sample_profile,
    execute_render,
    prepare_renders,
    run_pipeline,
    synthesize_plan,
)
from shortsmaker.languages import LANGUAGE_PACKS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shortsmaker",
        description="Automate saju-based short generation across copy, TTS, and Remotion.",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser("info", help="Show workspace and provider information.")

    init_profile = subparsers.add_parser(
        "init-profile",
        help="Create a sample saju profile JSON.",
    )
    init_profile.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional custom output path for the sample profile.",
    )

    plan = subparsers.add_parser(
        "plan",
        help="Generate hook variants and a plan manifest from a saju profile.",
    )
    plan.add_argument("--profile", type=Path, required=True)
    plan.add_argument("--languages", nargs="*", default=None)
    plan.add_argument("--platforms", nargs="*", default=None)

    tts = subparsers.add_parser(
        "tts",
        help="Synthesize narration audio for a plan manifest.",
    )
    tts.add_argument("--plan", type=Path, required=True)
    tts.add_argument("--tts-provider", default="edge", choices=["edge", "azure"])
    tts.add_argument("--language", default=None)

    render = subparsers.add_parser(
        "render",
        help="Prepare Remotion props or render MP4 files from a plan manifest.",
    )
    render.add_argument("--plan", type=Path, required=True)
    render.add_argument("--language", default=None)
    render.add_argument("--execute", action="store_true")
    render.add_argument("--skip-install", action="store_true")

    run = subparsers.add_parser(
        "run",
        help="Execute the end-to-end planning, TTS, and render-prep pipeline.",
    )
    run.add_argument("--profile", type=Path, required=True)
    run.add_argument("--tts-provider", default="edge", choices=["edge", "azure"])
    run.add_argument("--language", default=None)
    run.add_argument("--execute-render", action="store_true")
    run.add_argument("--skip-install", action="store_true")

    return parser


def handle_info() -> None:
    root = repo_paths().root
    print("ShortsMaker workspace is ready.")
    print(f"Repository root: {root}")
    print(f"Supported languages: {', '.join(sorted(LANGUAGE_PACKS))}")
    print("Default TTS provider: edge")
    print("Recommended production TTS provider: azure")
    print("Default renderer: remotion")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    if argv is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(argv or ["info"])

    command = args.command or "info"

    if command == "info":
        handle_info()
        return 0

    if command == "init-profile":
        target = create_sample_profile(args.output)
        print(f"Sample profile created at: {target}")
        return 0

    if command == "plan":
        _, plan_path = create_plan(
            profile_path=args.profile,
            languages=args.languages,
            platforms=args.platforms,
        )
        print(f"Plan created at: {plan_path}")
        return 0

    if command == "tts":
        synthesize_plan(
            plan_path=args.plan,
            tts_provider_name=args.tts_provider,
            selected_language=args.language,
        )
        print(f"TTS artifacts updated in: {args.plan}")
        return 0

    if command == "render":
        if args.execute:
            execute_render(
                plan_path=args.plan,
                selected_language=args.language,
                install_dependencies=not args.skip_install,
            )
            print(f"Rendered videos from: {args.plan}")
            return 0

        prepare_renders(
            plan_path=args.plan,
            selected_language=args.language,
        )
        print(f"Render props prepared from: {args.plan}")
        return 0

    if command == "run":
        _, plan_path = run_pipeline(
            profile_path=args.profile,
            tts_provider_name=args.tts_provider,
            selected_language=args.language,
            execute_renderer=args.execute_render,
            install_renderer_dependencies=not args.skip_install,
        )
        print(f"Pipeline finished. Plan: {plan_path}")
        return 0

    parser.error(f"Unsupported command: {command}")
    return 2
