# Evaluation Scripts

This directory contains scripts for evaluating the `mig-plan` skill.

## Files

- **evals.json** - Test case definitions with prompts, expected outputs, and assertions
- **grade_outputs.py** - Grades skill outputs against assertions
- **aggregate_benchmark.py** - Aggregates grading + timing data into benchmark results

## Usage

### 1. Run Evaluations

Run your evals in a workspace directory (e.g., `mig-plan-workspace/iteration-1/`):

```bash
# Your eval run should produce:
# eval-1-vague-java/
#   with_skill/
#     outputs/           # Skill outputs
#     grading.json       # Will be created by grade script
#     timing.json        # You need to create this manually
#   without_skill/       # (optional - for comparison)
#     outputs/
#     grading.json
#     timing.json
```

### 2. Create timing.json

After running an eval, manually create `timing.json` in each configuration directory:

```json
{
  "total_duration_seconds": 285.2,
  "total_tokens": 29966
}
```

### 3. Grade Outputs

```bash
cd mig-plan/evals
python grade_outputs.py ../../mig-plan-workspace/iteration-1 eval-1-vague-java
```

This creates `grading.json` files with pass/fail results.

### 4. Aggregate Benchmarks

```bash
cd mig-plan/evals
python aggregate_benchmark.py ../../mig-plan-workspace/iteration-1 1 ../../benchmark-results
```

This creates:
- `benchmark.json` - Internal format with detailed stats
- `benchmark.md` - Human-readable summary
- GitHub Action format files in `benchmark-results/` (if output_dir specified)

### 5. Commit Results

```bash
git add benchmark-results/
git commit -m "Add benchmark results for mig-plan iteration 1"
git push
```

GitHub Actions will automatically publish to GitHub Pages!

## GitHub Action Format

The `aggregate_benchmark.py` script exports three files per skill:

- `{skill}-pass-rate.json` - Pass rate metrics (bigger is better)
- `{skill}-duration.json` - Execution time metrics (smaller is better)
- `{skill}-tokens.json` - Token usage metrics (smaller is better)

These are consumed by the `github-action-benchmark` workflow for visualization.
