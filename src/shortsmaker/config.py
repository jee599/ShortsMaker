from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepoPaths:
    root: Path
    input_profiles: Path
    output_jobs: Path
    temp: Path
    renderer: Path
    renderer_public_jobs: Path


def repo_paths() -> RepoPaths:
    root = Path(__file__).resolve().parents[2]
    return RepoPaths(
        root=root,
        input_profiles=root / "input" / "profiles",
        output_jobs=root / "output" / "jobs",
        temp=root / "temp",
        renderer=root / "renderer",
        renderer_public_jobs=root / "renderer" / "public" / "jobs",
    )


def ensure_runtime_directories() -> RepoPaths:
    paths = repo_paths()
    for directory in (
        paths.input_profiles,
        paths.output_jobs,
        paths.temp,
        paths.renderer_public_jobs,
    ):
        directory.mkdir(parents=True, exist_ok=True)
    return paths
