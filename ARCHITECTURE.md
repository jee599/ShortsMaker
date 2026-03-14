# Architecture

## Current Shape

The project uses Python for orchestration and job planning, with Remotion isolated in a dedicated Node renderer project.

## Pipeline

1. Load a structured `saju` profile JSON.
2. Normalize element balance, day master, and other chart traits into an internal model.
3. Generate hook-first localized copy variants per target language.
4. Synthesize narration through a pluggable TTS provider layer.
5. Build Remotion props and optional render jobs for vertical 9:16 video output.
6. Store everything under `output/jobs/<job-id>/`.

## Core Modules

- `shortsmaker.cli`: top-level commands such as `plan`, `tts`, `render`, and `run`
- `shortsmaker.models`: typed data structures for profiles and hooks
- `shortsmaker.hooks`: hook generation logic driven by five elements and chart traits
- `shortsmaker.job`: job planning and manifest creation
- `shortsmaker.tts.providers`: provider abstraction with `edge-tts` as the default implementation
- `shortsmaker.render.remotion`: Remotion prop generation and render execution helpers

## Tooling Decision

- Default TTS: `edge-tts`
- Recommended future TTS upgrade: Azure Speech
- Default renderer: Remotion

This keeps the MVP locally runnable while preserving a path to higher-quality paid services later.

## Repository Conventions

- Source profiles live in `input/profiles/`.
- Generated artifacts live in `output/jobs/`.
- Temporary files live in `temp/`.
- Renderer runtime assets copied into `renderer/public/jobs/` must stay ignored.
- Tests focus on deterministic planning behavior rather than network-dependent synthesis.
