from __future__ import annotations

from pathlib import Path

from shortsmaker.config import ensure_runtime_directories, repo_paths
from shortsmaker.hooks import generate_hook_variants
from shortsmaker.languages import get_language_pack
from shortsmaker.models import DEFAULT_LANGUAGES, DEFAULT_PLATFORMS, SajuProfile
from shortsmaker.render.remotion import prepare_render_jobs, render_from_plan
from shortsmaker.tts.providers import create_tts_provider, voice_catalog
from shortsmaker.utils import read_json, slugify, utc_timestamp, write_json


SAMPLE_PROFILE = {
    "profile_id": "metal-water-money",
    "display_name": "Metal strong chart with weak wood",
    "day_master": "water",
    "five_elements": {
        "wood": 14,
        "fire": 18,
        "earth": 21,
        "metal": 32,
        "water": 27,
    },
    "dominant_element": "metal",
    "lacking_element": "wood",
    "energy_flow": "metal-supports-water",
    "yin_yang_balance": "yang-heavy",
    "season": "autumn",
    "focus_themes": ["money", "career", "luck"],
    "special_traits": ["sharp judgment", "slow trust"],
    "target_languages": ["en", "ko", "ja", "id", "th", "vi", "hi"],
    "target_platforms": ["tiktok", "instagram_reels", "facebook_reels"],
    "brand_label": "Saju Signal",
}


def create_sample_profile(output_path: Path | None = None) -> Path:
    paths = ensure_runtime_directories()
    target = (
        resolve_workspace_path(output_path)
        if output_path is not None
        else paths.input_profiles / "sample_saju.json"
    )
    write_json(target, SAMPLE_PROFILE)
    return target


def load_profile(path: Path) -> SajuProfile:
    return SajuProfile.from_dict(read_json(resolve_workspace_path(path)))


def create_plan(
    profile_path: Path,
    languages: list[str] | None = None,
    platforms: list[str] | None = None,
) -> tuple[dict[str, object], Path]:
    paths = ensure_runtime_directories()
    profile = load_profile(profile_path)
    selected_languages = languages or profile.target_languages or list(DEFAULT_LANGUAGES)
    selected_platforms = platforms or profile.target_platforms or list(DEFAULT_PLATFORMS)

    job_id = f"{slugify(profile.profile_id)}-{utc_timestamp()}"
    job_dir = paths.output_jobs / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "job_id": job_id,
        "created_at": utc_timestamp(),
        "profile_source": str(profile_path),
        "profile": profile.to_dict(),
        "targets": {
            "languages": selected_languages,
            "platforms": selected_platforms,
        },
        "tooling": {
            "default_tts_provider": "edge",
            "recommended_tts_provider": "azure",
            "default_renderer": "remotion",
        },
        "languages": [],
    }

    for language_code in selected_languages:
        pack = get_language_pack(language_code)
        variants = generate_hook_variants(profile, language_code)
        selected_variant = variants[0]
        estimated_duration_seconds = max(
            9.0,
            round(len(selected_variant.narration.split()) * 0.42, 2),
        )
        manifest["languages"].append(
            {
                "language_code": language_code,
                "language_name": pack.label,
                "voice_catalog": voice_catalog(language_code),
                "selected_variant": selected_variant.to_dict(),
                "variants": [variant.to_dict() for variant in variants],
                "narration_text": selected_variant.narration,
                "estimated_duration_seconds": estimated_duration_seconds,
            }
        )

    plan_path = job_dir / "plan.json"
    write_json(plan_path, manifest)
    return manifest, plan_path


def load_plan(plan_path: Path) -> dict[str, object]:
    return read_json(resolve_workspace_path(plan_path))


def synthesize_plan(
    plan_path: Path,
    tts_provider_name: str = "edge",
    selected_language: str | None = None,
) -> dict[str, object]:
    plan = load_plan(plan_path)
    provider = create_tts_provider(tts_provider_name)
    audio_dir = plan_path.parent / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    for locale_entry in plan["languages"]:
        language_code = locale_entry["language_code"]
        if selected_language and language_code != selected_language:
            continue

        output_path = audio_dir / f"{language_code}.mp3"
        artifact = provider.synthesize(
            text=locale_entry["narration_text"],
            language_code=language_code,
            output_path=output_path,
        )
        locale_entry["narration_artifact"] = artifact.to_dict()

    write_json(plan_path, plan)
    return plan


def prepare_renders(
    plan_path: Path,
    selected_language: str | None = None,
) -> dict[str, object]:
    plan = load_plan(plan_path)
    prepare_render_jobs(plan, plan_path, selected_language=selected_language)
    return load_plan(plan_path)


def execute_render(
    plan_path: Path,
    selected_language: str | None = None,
    install_dependencies: bool = True,
) -> dict[str, object]:
    plan = load_plan(plan_path)
    render_from_plan(
        plan,
        plan_path,
        selected_language=selected_language,
        install_dependencies=install_dependencies,
    )
    return load_plan(plan_path)


def run_pipeline(
    profile_path: Path,
    tts_provider_name: str = "edge",
    selected_language: str | None = None,
    execute_renderer: bool = False,
    install_renderer_dependencies: bool = True,
) -> tuple[dict[str, object], Path]:
    plan, plan_path = create_plan(profile_path)
    plan = synthesize_plan(
        plan_path,
        tts_provider_name=tts_provider_name,
        selected_language=selected_language,
    )
    if execute_renderer:
        render_from_plan(
            plan,
            plan_path,
            selected_language=selected_language,
            install_dependencies=install_renderer_dependencies,
        )
    else:
        prepare_render_jobs(plan, plan_path, selected_language=selected_language)
    return load_plan(plan_path), plan_path


def resolve_workspace_path(path: Path) -> Path:
    if path.is_absolute():
        return path

    cwd_candidate = (Path.cwd() / path).resolve()
    if cwd_candidate.exists():
        return cwd_candidate

    repo_candidate = (repo_paths().root / path).resolve()
    if repo_candidate.exists():
        return repo_candidate

    return cwd_candidate
