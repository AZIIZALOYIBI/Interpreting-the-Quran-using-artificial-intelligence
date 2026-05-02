---
name: update-frontend-dependencies
description: Workflow command scaffold for update-frontend-dependencies in Interpreting-the-Quran-using-artificial-intelligence.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /update-frontend-dependencies

Use this workflow when working on **update-frontend-dependencies** in `Interpreting-the-Quran-using-artificial-intelligence`.

## Goal

Updates or fixes frontend dependencies, often to address security vulnerabilities or sync issues.

## Common Files

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Modify frontend/package.json to update dependency versions.
- Regenerate frontend/package-lock.json to reflect dependency changes.
- Optionally update frontend/tsconfig.json if required by dependency changes.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.