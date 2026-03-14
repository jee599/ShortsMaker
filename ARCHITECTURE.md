# Architecture

## Current Shape

The repository starts as a Python package with a lightweight CLI so media-processing workflows can be added incrementally.

## Proposed Flow

1. Collect structured inputs such as scripts, clips, images, or audio references.
2. Normalize them into a job definition.
3. Run a pipeline that prepares timing, assets, and export commands.
4. Write generated artifacts to an ignored output directory.

## Initial Modules

- `shortsmaker.cli`: command-line entry point
- future `shortsmaker.jobs`: job definitions and validation
- future `shortsmaker.pipeline`: orchestration and step execution
- future `shortsmaker.export`: FFmpeg or other renderer integration

## Repository Conventions

- Checked-in assets live in `assets/`.
- Helper automation belongs in `scripts/`.
- Tests should stay lightweight until the first real pipeline exists.
- Generated outputs should never be committed.
