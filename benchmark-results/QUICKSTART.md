# Benchmarking Quick Start

## Run Your First Benchmark

### Step 1: Run an eval and create timing data

```bash
# Create workspace directory
mkdir -p mig-prompt-builder-workspace/iteration-1/eval-1-vague-java/with_skill/outputs

# Run your eval in Claude Code
# Outputs should go to the outputs/ directory above

# After completion, create timing.json
cat > mig-prompt-builder-workspace/iteration-1/eval-1-vague-java/with_skill/timing.json <<EOF
{
  "total_duration_seconds": 285.2,
  "total_tokens": 29966
}
EOF
```

### Step 2: Grade outputs

```bash
cd mig-prompt-builder/evals
python grade_outputs.py ../../mig-prompt-builder-workspace/iteration-1 eval-1-vague-java
# Output: eval-1-vague-java/with_skill: 8/8 passed
```

### Step 3: Aggregate and export

```bash
python aggregate_benchmark.py \
  ../../mig-prompt-builder-workspace/iteration-1 \
  1 \
  ../../benchmark-results

# Output:
# ✓ Created benchmark.json
# ✓ Created benchmark.md
# ✓ Exported GitHub Action format to benchmark-results/
```

### Step 4: Commit and push

```bash
git add benchmark-results/
git commit -m "Add mig-prompt-builder iteration 1 benchmarks"
git push
```

### Step 5: View on GitHub Pages

Visit: `https://YOUR_USERNAME.github.io/migIQ/dev/bench/`

## Expected Files

After step 3, you should have:

```
mig-prompt-builder-workspace/iteration-1/
├── eval-1-vague-java/
│   └── with_skill/
│       ├── outputs/              # Your eval outputs
│       ├── grading.json          # ← Created by step 2
│       └── timing.json           # ← Created by step 1
├── benchmark.json                # ← Created by step 3
└── benchmark.md                  # ← Created by step 3

benchmark-results/
├── mig-prompt-builder-pass-rate.json   # ← Created by step 3
├── mig-prompt-builder-duration.json    # ← Created by step 3
└── mig-prompt-builder-tokens.json      # ← Created by step 3
```

## Need Help?

- Full guide: [BENCHMARKING.md](../BENCHMARKING.md)
- Skill-specific guide: [mig-prompt-builder/evals/README.md](../mig-prompt-builder/evals/README.md)
