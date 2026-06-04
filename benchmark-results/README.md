# Benchmark Results

This directory contains benchmark results exported in GitHub Action format for visualization on GitHub Pages.

## Structure

```
benchmark-results/
├── README.md
├── {skill-name}-pass-rate.json
├── {skill-name}-duration.json
└── {skill-name}-tokens.json
```

## Files

Each skill has three benchmark files:

- **{skill}-pass-rate.json** - Test pass rates (higher is better)
- **{skill}-duration.json** - Execution time in seconds (lower is better)  
- **{skill}-tokens.json** - Token usage (lower is better)

## Format

Files use the `github-action-benchmark` custom JSON format:

```json
[
  {
    "name": "skill-name/configuration",
    "unit": "percent|seconds|tokens",
    "value": 95.5,
    "range": 2.3,
    "extra": "Iteration: 1\nConfiguration: with_skill"
  }
]
```

## Workflow

1. Run evals in workspace directories
2. Use `aggregate_benchmark.py` to generate these files
3. Commit to git
4. GitHub Actions publishes to Pages automatically

## View Results

After pushing to GitHub, view the benchmark dashboard at:

**https://YOUR_USERNAME.github.io/migIQ/dev/bench/**

Historical trends and comparisons will be available once multiple iterations are published.

## Manual Generation

```bash
cd mig-prompt-builder/evals
python aggregate_benchmark.py \
  ../../mig-prompt-builder-workspace/iteration-1 \
  1 \
  ../../benchmark-results
```

This exports the three JSON files to this directory.
