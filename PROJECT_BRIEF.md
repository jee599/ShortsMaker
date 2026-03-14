# Project Brief

## Vision

Build an automated short-form video factory that turns structured `saju` data into multilingual, hook-driven shorts for TikTok, Instagram Reels, and Facebook Reels.

## Product Direction

The system should generate emotionally sticky lines from five elements and other chart traits, synthesize narration, and render vertical videos with minimal manual intervention.

## Goals

- Accept a structured `saju` profile as JSON.
- Generate multiple hook variants per target language.
- Support English, Korean, Japanese, Southeast Asian, and Indic target markets through locale presets.
- Automate narration generation with a pluggable TTS layer.
- Automate short rendering with a pluggable video renderer.
- Keep the whole workflow callable from one CLI pipeline.

## Tooling Assumption

- Default TTS remains `edge-tts` for local zero-cost automation.
- Azure Speech is the preferred future production TTS path because of its official API surface and multilingual voice catalog.
- Remotion remains the default renderer because it fits animated, template-driven social shorts better than low-level video scripting alone.

## Non-Goals For This Slice

- Direct publishing to social platforms.
- A full admin UI.
- Fully dynamic caption timing from speech recognition.
- LLM-dependent copy generation that blocks local execution.

## Success Criteria For This Slice

- A user can define a `saju` source profile in JSON.
- One command produces a job folder with localized hook copy.
- The same workflow can synthesize narration for each selected language.
- The workflow can prepare Remotion-ready props and optionally render.
- Core planning behavior is covered by lightweight tests.
