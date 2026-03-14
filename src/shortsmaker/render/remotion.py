from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path

from shortsmaker.config import ensure_runtime_directories
from shortsmaker.languages import get_language_pack
from shortsmaker.models import SajuProfile
from shortsmaker.utils import write_json


ELEMENT_PALETTES = {
    "wood": {"start": "#16352c", "end": "#3e9f65", "accent": "#d5ff8a"},
    "fire": {"start": "#381512", "end": "#c34d1f", "accent": "#ffd166"},
    "earth": {"start": "#2f241f", "end": "#8f6a43", "accent": "#ffe7bd"},
    "metal": {"start": "#121c2c", "end": "#5f7da9", "accent": "#f4fbff"},
    "water": {"start": "#0f1b34", "end": "#245ea8", "accent": "#87e0ff"},
}


def prepare_render_jobs(
    plan: dict[str, object],
    plan_path: Path,
    selected_language: str | None = None,
) -> list[Path]:
    ensure_runtime_directories()
    job_dir = plan_path.parent
    render_dir = job_dir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)

    profile = SajuProfile.from_dict(plan["profile"])
    props_files: list[Path] = []

    for locale_entry in plan["languages"]:
        language_code = locale_entry["language_code"]
        if selected_language and language_code != selected_language:
            continue

        public_audio_src = None
        narration_artifact = locale_entry.get("narration_artifact")
        duration_seconds = locale_entry.get("estimated_duration_seconds", 12.0)
        if narration_artifact:
            duration_seconds = narration_artifact["duration_seconds"]
            audio_path = Path(narration_artifact["output_path"])
            public_audio_src = _copy_audio_to_public(audio_path, plan["job_id"], language_code)

        pack = get_language_pack(language_code)
        voice_name = (
            narration_artifact["voice"]
            if narration_artifact
            else locale_entry["voice_catalog"]["edge"]
        )
        props = {
            "compositionId": "ShortsMakerVertical",
            "jobId": plan["job_id"],
            "language": {
                "code": language_code,
                "label": locale_entry["language_name"],
            },
            "platforms": plan["targets"]["platforms"],
            "video": {
                "width": 1080,
                "height": 1920,
                "fps": 30,
                "durationInFrames": _duration_to_frames(duration_seconds),
            },
            "theme": {
                "brandLabel": profile.brand_label,
                "badge": pack.badge_label,
                "fontFamily": pack.font_family,
                **ELEMENT_PALETTES[profile.dominant_element],
            },
            "hook": {
                "title": locale_entry["selected_variant"]["title"],
                "support": locale_entry["selected_variant"]["support"],
                "cta": locale_entry["selected_variant"]["cta"],
                "keywords": locale_entry["selected_variant"]["keywords"],
                "visualMotifs": locale_entry["selected_variant"]["visual_motifs"],
                "traits": profile.special_traits,
            },
            "captions": locale_entry["selected_variant"]["caption_lines"],
            "narration": {
                "audioSrc": public_audio_src,
                "durationSeconds": duration_seconds,
                "voice": voice_name,
            },
        }

        props_path = render_dir / f"{language_code}.json"
        write_json(props_path, props)
        locale_entry["render_artifact"] = {
            "props_path": str(props_path),
            "video_output_path": str(job_dir / "videos" / f"{language_code}.mp4"),
        }
        props_files.append(props_path)

    write_json(plan_path, plan)
    return props_files


def render_from_plan(
    plan: dict[str, object],
    plan_path: Path,
    selected_language: str | None = None,
    install_dependencies: bool = True,
) -> list[Path]:
    props_files = prepare_render_jobs(plan, plan_path, selected_language=selected_language)
    renderer_dir = ensure_runtime_directories().renderer
    npm_command = _npm_command()

    if install_dependencies and not (renderer_dir / "node_modules").exists():
        subprocess.run([npm_command, "install"], cwd=renderer_dir, check=True)

    video_paths: list[Path] = []
    for props_path in props_files:
        output_path = (plan_path.parent / "videos" / f"{props_path.stem}.mp4").resolve()
        resolved_props_path = props_path.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                npm_command,
                "run",
                "render",
                "--",
                "--props",
                str(resolved_props_path),
                "--out",
                str(output_path),
            ],
            cwd=renderer_dir,
            check=True,
        )
        video_paths.append(output_path)

    return video_paths


def _copy_audio_to_public(audio_path: Path, job_id: str, language_code: str) -> str:
    paths = ensure_runtime_directories()
    public_audio_dir = paths.renderer_public_jobs / job_id / "audio"
    public_audio_dir.mkdir(parents=True, exist_ok=True)
    target = public_audio_dir / f"{language_code}{audio_path.suffix}"
    shutil.copy2(audio_path, target)
    return f"/public/jobs/{job_id}/audio/{target.name}"


def _duration_to_frames(duration_seconds: float) -> int:
    return max(270, math.ceil((duration_seconds + 1.4) * 30))


def _npm_command() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"
