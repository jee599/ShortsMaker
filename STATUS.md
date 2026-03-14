# Status

## Current Task

Implement the first automated ShortsMaker pipeline for saju-based copy, multilingual TTS, and Remotion rendering prep.

## Working Session

- Agent: gpt-5-codex
- Date: 2026-03-14
- Branch: main
- Focus: Generate a fresh sample English short artifact for user validation.

## Done

- Created the initial repository structure and handoff docs.
- Added a minimal Python package and smoke test baseline.
- Reframed the product around saju-based short generation for TikTok, Instagram Reels, and Facebook Reels.
- Added a profile schema, multilingual hook-generation pipeline, and a sample input profile.
- Added pluggable TTS providers with `edge-tts` as the working default and Azure Speech as the upgrade path.
- Added a Remotion renderer project and Python render-prep / render execution helpers.
- Verified unit tests, a real English TTS run, Remotion prop generation, and one successful MP4 render.
- Hardened CLI path handling so relative `--profile` and `--plan` paths resolve from either the current working directory or the repo root.
- Increased job timestamp precision to reduce accidental output folder collisions.
- Generated another sample English short end-to-end at `output/jobs/metal-water-money-20260314T065549380207Z/` for quick user review.

## Next

- Improve locale copy quality for each supported language with market-specific phrasing.
- Add provider selection for higher-quality commercial TTS such as Azure Speech once credentials are available.
- Add richer scene logic such as timed caption chunks, B-roll assets, and per-platform visual presets.

## Blocked

- No hard blocker yet.
- Production-quality Azure Speech usage needs `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`.
- Full publishing automation still needs platform credential strategy and rate-limit handling.

## Notes for Next Agent

- Current product direction is fixed around saju-based shorts for TikTok, Instagram Reels, and Facebook Reels.
- Target locale coverage for the MVP is `en`, `ko`, `ja`, `id`, `th`, `vi`, and `hi`.
- Prefer pluggable providers instead of baking vendor assumptions into the core planning logic.
- `python -m shortsmaker run --profile input\profiles\sample_saju.json --language en` is already verified.
- The same `run` command is now also verified from one directory above the repo, so repo-relative paths are no longer fragile.
- `python -m shortsmaker render --plan output\jobs\<job-id>\plan.json --language en --execute` is also verified after `npm install` inside `renderer/`.
- Latest validation artifact: `output/jobs/metal-water-money-20260314T065549380207Z/videos/en.mp4`.
- Non-ASCII text displays garbled in some terminal outputs, but the JSON files themselves are stored correctly in UTF-8.

## Agent Contribution

- gpt-5-codex: bootstrapped the repository with workflow docs, a package skeleton, and a quick verification path.
- gpt-5-codex: implemented the first end-to-end saju short pipeline with multilingual copy planning, TTS, and Remotion rendering.
- gpt-5-codex: fixed repo-relative CLI path handling and reduced job folder collisions.
- gpt-5-codex: generated a fresh sample English short artifact for validation.
