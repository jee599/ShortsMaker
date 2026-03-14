# ShortsMaker

ShortsMaker automates short-form astrology videos for TikTok, Instagram Reels, and Facebook Reels.

The current pipeline is designed around this flow:

1. Read a structured `saju` profile JSON.
2. Generate hook-heavy copy in multiple languages from five-element and chart traits.
3. Convert the chosen narration into speech with pluggable TTS providers.
4. Prepare or render a vertical short with Remotion.

## Current Tooling Decision

- Default TTS: `edge-tts`
- Production-ready upgrade path: Azure Speech
- Default renderer: Remotion

This balance keeps local automation simple while preserving a clean path to better voice quality and stronger production controls.

## Supported Language Targets

The MVP ships with these presets:

- English (`en`)
- Korean (`ko`)
- Japanese (`ja`)
- Indonesian (`id`)
- Thai (`th`)
- Vietnamese (`vi`)
- Hindi (`hi`)

The structure is designed so more locales can be added without changing the pipeline shape.

## Quick Start

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install -e .
$env:PYTHONPATH = "src"
python -m shortsmaker info
python -m shortsmaker init-profile
python -m shortsmaker run --profile input\profiles\sample_saju.json --tts-provider edge
```

To render MP4 output with Remotion, install the Node renderer once:

```powershell
cd renderer
npm install
cd ..
python -m shortsmaker render --plan output\jobs\<job-id>\plan.json --execute
```

To switch the narration provider to Azure Speech later, set the variables from [.env.example](C:/Users/jee59/OneDrive/문서/GitHub/ShortsMaker/.env.example) and run `--tts-provider azure`.

## Repository Layout

- `input/profiles/`: committed sample or curated source profiles
- `output/jobs/`: generated manifests, audio, props, and videos
- `renderer/`: Remotion project used for vertical shorts
- `src/shortsmaker/`: orchestration, copy, TTS, and render preparation
- `tests/`: unit tests for the planning pipeline

## Sample Workflow

1. Edit [input/profiles/sample_saju.json](C:/Users/jee59/OneDrive/문서/GitHub/ShortsMaker/input/profiles/sample_saju.json).
2. Run `python -m shortsmaker run --profile input\profiles\sample_saju.json --tts-provider edge`.
3. Review the generated job folder under `output/jobs/`.
4. If renderer dependencies are installed, run the `render` command with `--execute`.
