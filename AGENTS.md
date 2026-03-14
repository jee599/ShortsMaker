# Agent Workflow Rules

This repository is used by GPT and Claude working sequentially on the same `main` branch.
Do not run concurrent work in the same branch.

## Read Order

Start every task in this order:

1. Read `AGENTS.md`
2. Read `PROJECT_BRIEF.md`
3. Read `STATUS.md`
4. Read `ARCHITECTURE.md` if needed

## Working Rules

1. Work on one small task at a time.
2. Do not start work that is not listed in `STATUS.md`.
3. Before coding, review `Current Task` and `Notes for Next Agent` in `STATUS.md`.
4. At task start, update the `Working Session` section in `STATUS.md`.
5. If structure, folders, dependencies, or core design change, update `ARCHITECTURE.md`.
6. If goals, scope, or success criteria change, update `PROJECT_BRIEF.md`.
7. At task end, update `STATUS.md` with completed work, next work, remaining work, blockers, and contribution data.

## Git Rules

1. The default branch is `main`.
2. Commit once per task unit.
3. Push after every commit with `git push origin main`.
4. Use commit messages in the form `agent-version: change summary`.

## Handoff Rules

At the end of each task, these sections must be current:

- `Done`
- `Next`
- `Blocked`
- `Notes for Next Agent`
- `Agent Contribution`

The next agent must be able to continue from the docs and latest commit only.
