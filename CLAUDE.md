Emulator Fidelity: public website showing how faithfully AWS Emulator reproduces
each AWS service, refreshed after every `aws/aws-emulator` release.

## Rules

- Every repo artifact is in English (code, comments, docs, commits). Spanish only
  in the Spanish UI strings of the website.
- Ask the user before taking design decisions (stack, scope, visual design).
- Python: minimalist, classes preferred, type hints, no custom error handling
  unless needed, files around 25-40 lines, lines under 79 characters.
- Never commit raw downloads (`scores.json`, api-models); only derived JSON in `data/`.
- Branches: `feat/*` / `fix/*` with a PR to `main`.

## Layout

- `pipeline/` Python + uv data pipeline, entry point `pipeline/main.py`.
- `tests/` mirrors `pipeline/` (pytest, fixtures, no network in unit tests).
- `data/` derived JSON consumed by the website.
- `web/` Astro + React islands + TanStack Table + Apache ECharts + Tailwind (pnpm).
