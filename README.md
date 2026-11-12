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
```

## License

[MIT](LICENSE).
