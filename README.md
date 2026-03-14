# ShortsMaker

ShortsMaker is a lightweight starter workspace for building short-form video generation tools.

The repository is currently bootstrapped with:

- project documentation for future agent handoff
- a minimal Python package and CLI entry point
- a small smoke test so the workspace can be verified quickly

## Quick Start

1. Create and activate a virtual environment.
2. Set `PYTHONPATH=src`.
3. Run `python -m shortsmaker`.

On PowerShell:

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
python -m shortsmaker
python -m unittest discover -s tests -p "test_*.py"
```

## Repository Layout

- `src/shortsmaker/`: application package
- `tests/`: smoke and unit tests
- `assets/`: checked-in reference assets and templates
- `scripts/`: local helper scripts
- `PROJECT_BRIEF.md`: goals and scope
- `STATUS.md`: current task, handoff notes, and blockers
- `ARCHITECTURE.md`: evolving technical design

## Current Direction

This bootstrap assumes a Python-first workflow for orchestrating media processing and FFmpeg-based export steps. That can be revisited once the first concrete user flow is chosen.
