# Emulator Fidelity

How faithfully does [AWS Emulator](https://github.com/aws/aws-emulator) reproduce
each AWS service? This project turns the fidelity results that AWS publishes with
every emulator release into an explorable website, refreshed automatically after
each release.

> Not affiliated with Amazon Web Services. Fidelity results are published by AWS
> under CC0; the per-service aggregation is computed by this project.

## How it works

1. A scheduled GitHub Actions workflow polls the `aws/aws-emulator` releases.
2. When a release ships a `scores.json.gz` asset, the Python pipeline (`pipeline/`)
   joins it with [`aws/api-models-aws`](https://github.com/aws/api-models-aws) and the
   [`aws/aws-emulator-evaluation-suite`](https://github.com/aws/aws-emulator-evaluation-suite)
   manifest, and writes small JSON files to `data/`.
3. The Astro site (`web/`) is rebuilt from `data/` and deployed to GitHub Pages.

## Project structure

- `pipeline/`: Python data pipeline (uv).
- `tests/`: pipeline tests (pytest).
- `data/`: derived fidelity data, committed by the workflow.
- `web/`: Astro + React website (pnpm).

## Development

Tools are installed with [mise](https://mise.jdx.dev/):

```bash
mise install
uv sync
```

Process every release that is not in `data/` yet (needs an authenticated
[GitHub CLI](https://cli.github.com/), `gh auth login`):

```bash
uv run python -m pipeline.main
```

Run the tests:

```bash
uv run pytest
```

## Data files

- `data/releases/<tag>.json`: per-service summary of one release. Counters
  are `[passed, total]` behavioral tests; `control` / `data` split them by plane
  (a test asserting on both planes counts in both).
- `data/latest/catalog.json`: every service with an API model, flagged when it
  has fidelity tests.
- `data/latest/services/<slug>.json`: latest detail of one service: tests per
  operation and the failing tests with their path in the evaluation suite.

## License

[MIT](LICENSE).
