# Project Brief

## Vision

Build a practical toolkit for creating short-form videos from reusable assets, scripts, and automated media-processing steps.

## Initial Assumption

The bootstrap is intentionally Python-first so the project can move quickly on media orchestration, local automation, and command-line workflows before a UI exists.

## Goals

- Define one clear end-to-end workflow for generating a short video.
- Keep the core pipeline scriptable and testable.
- Separate checked-in source assets from generated outputs.
- Make it easy for the next agent to continue from docs alone.

## Non-Goals

- Full multi-platform publishing automation in the first slice.
- Complex frontend work before the pipeline exists.
- Broad asset management features before a single successful generation path is proven.

## Success Criteria For The First Slice

- A user can place inputs in a known location.
- The tool can run one documented command.
- The command produces a predictable output artifact or a clear placeholder result.
- The workflow can be verified locally with a lightweight test.
