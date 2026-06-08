#!/usr/bin/env python3
"""Aggregate grading results and timing into benchmark outputs.

This script processes grading.json and timing.json files from workspace
directories and produces:
1. benchmark.json - Internal format with detailed statistics
2. GitHub Action format files for visualization on GitHub Pages

Usage:
    python aggregate_benchmark.py <workspace_dir> <iteration_number> [output_dir]

Example:
    python aggregate_benchmark.py ../../mig-prompt-builder-workspace/iteration-1 1
    python aggregate_benchmark.py ../../mig-prompt-builder-workspace/iteration-1 1 ../../benchmark-results
"""

import json
import statistics
import sys
from pathlib import Path
from datetime import datetime


def load_grading(grading_path):
    """Load grading results."""
    with open(grading_path) as f:
        data = json.load(f)
    expectations = data['expectations']
    passed = sum(1 for e in expectations if e['passed'])
    total = len(expectations)
    return passed, total


def load_timing(timing_path):
    """Load timing data."""
    with open(timing_path) as f:
        return json.load(f)


def export_github_action_format(skill_name, iteration, configurations, output_dir):
    """Export benchmark data in github-action-benchmark format.

    Creates separate files for different metric types:
    - pass-rate.json (bigger is better)
    - duration.json (smaller is better)
    - tokens.json (smaller is better)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Pass rate entries (bigger is better)
    pass_rate_entries = []
    # Duration entries (smaller is better)
    duration_entries = []
    # Token entries (smaller is better)
    token_entries = []

    for config in configurations:
        config_name = config['name']

        # Pass rate
        pass_rate_entries.append({
            "name": f"{skill_name}/{config_name}",
            "unit": "percent",
            "value": config['pass_rate']['mean'] * 100,
            "range": config['pass_rate']['stddev'] * 100 if config['pass_rate']['stddev'] > 0 else 0,
            "extra": f"Iteration: {iteration}\nConfiguration: {config_name}"
        })

        # Duration
        duration_entries.append({
            "name": f"{skill_name}/{config_name}",
            "unit": "seconds",
            "value": config['duration_seconds']['mean'],
            "range": config['duration_seconds']['stddev'],
            "extra": f"Iteration: {iteration}\nConfiguration: {config_name}"
        })

        # Tokens
        token_entries.append({
            "name": f"{skill_name}/{config_name}",
            "unit": "tokens",
            "value": config['total_tokens']['mean'],
            "range": config['total_tokens']['stddev'],
            "extra": f"Iteration: {iteration}\nConfiguration: {config_name}"
        })

    # Write separate files
    with open(output_dir / f'{skill_name}-pass-rate.json', 'w') as f:
        json.dump(pass_rate_entries, f, indent=2)

    with open(output_dir / f'{skill_name}-duration.json', 'w') as f:
        json.dump(duration_entries, f, indent=2)

    with open(output_dir / f'{skill_name}-tokens.json', 'w') as f:
        json.dump(token_entries, f, indent=2)

    return {
        'pass_rate': output_dir / f'{skill_name}-pass-rate.json',
        'duration': output_dir / f'{skill_name}-duration.json',
        'tokens': output_dir / f'{skill_name}-tokens.json'
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python aggregate_benchmark.py <workspace_dir> <iteration> [output_dir]")
        print("Example: python aggregate_benchmark.py ../../mig-prompt-builder-workspace/iteration-1 1")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    iteration = int(sys.argv[2])
    output_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    # Detect skill name from parent directory
    skill_name = workspace.parent.name.replace('-workspace', '')

    # Find all eval directories
    eval_dirs = [d for d in workspace.iterdir() if d.is_dir() and d.name.startswith('eval-')]

    if not eval_dirs:
        print(f"No eval directories found in {workspace}")
        sys.exit(1)

    configurations = []

    # Process with_skill configuration
    with_skill_results = []
    for eval_dir in eval_dirs:
        eval_name = eval_dir.name
        config_dir = eval_dir / 'with_skill'
        grading_file = config_dir / 'grading.json'
        timing_file = config_dir / 'timing.json'

        if grading_file.exists() and timing_file.exists():
            passed, total = load_grading(grading_file)
            timing = load_timing(timing_file)

            with_skill_results.append({
                'eval_id': eval_name,
                'pass_rate': passed / total if total > 0 else 0,
                'duration_seconds': timing.get('total_duration_seconds', 0),
                'total_tokens': timing.get('total_tokens', 0)
            })

    # Calculate aggregates for with_skill
    if with_skill_results:
        configurations.append({
            'name': 'with_skill',
            'pass_rate': {
                'mean': statistics.mean([r['pass_rate'] for r in with_skill_results]),
                'stddev': statistics.stdev([r['pass_rate'] for r in with_skill_results]) if len(with_skill_results) > 1 else 0
            },
            'duration_seconds': {
                'mean': statistics.mean([r['duration_seconds'] for r in with_skill_results]),
                'stddev': statistics.stdev([r['duration_seconds'] for r in with_skill_results]) if len(with_skill_results) > 1 else 0
            },
            'total_tokens': {
                'mean': statistics.mean([r['total_tokens'] for r in with_skill_results]),
                'stddev': statistics.stdev([r['total_tokens'] for r in with_skill_results]) if len(with_skill_results) > 1 else 0
            },
            'per_eval': with_skill_results
        })

    # Process without_skill configuration
    without_skill_results = []
    for eval_dir in eval_dirs:
        eval_name = eval_dir.name
        config_dir = eval_dir / 'without_skill'
        grading_file = config_dir / 'grading.json'
        timing_file = config_dir / 'timing.json'

        if grading_file.exists() and timing_file.exists():
            passed, total = load_grading(grading_file)
            timing = load_timing(timing_file)

            without_skill_results.append({
                'eval_id': eval_name,
                'pass_rate': passed / total if total > 0 else 0,
                'duration_seconds': timing.get('total_duration_seconds', 0),
                'total_tokens': timing.get('total_tokens', 0)
            })

    # Calculate aggregates for without_skill
    if without_skill_results:
        configurations.append({
            'name': 'without_skill',
            'pass_rate': {
                'mean': statistics.mean([r['pass_rate'] for r in without_skill_results]),
                'stddev': statistics.stdev([r['pass_rate'] for r in without_skill_results]) if len(without_skill_results) > 1 else 0
            },
            'duration_seconds': {
                'mean': statistics.mean([r['duration_seconds'] for r in without_skill_results]),
                'stddev': statistics.stdev([r['duration_seconds'] for r in without_skill_results]) if len(without_skill_results) > 1 else 0
            },
            'total_tokens': {
                'mean': statistics.mean([r['total_tokens'] for r in without_skill_results]),
                'stddev': statistics.stdev([r['total_tokens'] for r in without_skill_results]) if len(without_skill_results) > 1 else 0
            },
            'per_eval': without_skill_results
        })

    # Create benchmark output
    benchmark = {
        'skill_name': skill_name,
        'iteration': iteration,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'configurations': configurations
    }

    # Save internal benchmark.json
    with open(workspace / 'benchmark.json', 'w') as f:
        json.dump(benchmark, f, indent=2)
    print(f"✓ Created {workspace / 'benchmark.json'}")

    # Create benchmark.md
    md_lines = [
        f'# Benchmark Results - {skill_name} Iteration {iteration}',
        '',
        f'**Generated:** {benchmark["timestamp"]}',
        '',
        '## Summary',
        ''
    ]

    for config in configurations:
        md_lines.append(f"### {config['name']}")
        md_lines.append(f"- **Pass Rate**: {config['pass_rate']['mean']:.1%} ± {config['pass_rate']['stddev']:.1%}")
        md_lines.append(f"- **Duration**: {config['duration_seconds']['mean']:.1f}s ± {config['duration_seconds']['stddev']:.1f}s")
        md_lines.append(f"- **Tokens**: {config['total_tokens']['mean']:.0f} ± {config['total_tokens']['stddev']:.0f}")
        md_lines.append('')

    # Calculate deltas if both configurations exist
    if len(configurations) == 2:
        with_skill = configurations[0]
        without_skill = configurations[1]

        md_lines.append('## Delta (with_skill vs without_skill)')
        md_lines.append(f"- **Pass Rate**: {(with_skill['pass_rate']['mean'] - without_skill['pass_rate']['mean']):+.1%}")
        md_lines.append(f"- **Duration**: {with_skill['duration_seconds']['mean'] - without_skill['duration_seconds']['mean']:+.1f}s")
        md_lines.append(f"- **Tokens**: {with_skill['total_tokens']['mean'] - without_skill['total_tokens']['mean']:+.0f}")
        md_lines.append('')

    md_lines.append('## Per-Eval Results')
    md_lines.append('')

    for config in configurations:
        md_lines.append(f"### {config['name']}")
        md_lines.append('| Eval | Pass Rate | Duration (s) | Tokens |')
        md_lines.append('|------|-----------|--------------|--------|')
        for result in config['per_eval']:
            md_lines.append(f"| {result['eval_id']} | {result['pass_rate']:.1%} | {result['duration_seconds']:.1f} | {result['total_tokens']} |")
        md_lines.append('')

    with open(workspace / 'benchmark.md', 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"✓ Created {workspace / 'benchmark.md'}")

    # Export GitHub Action format if output_dir specified
    if output_dir:
        exported = export_github_action_format(skill_name, iteration, configurations, output_dir)
        print(f"\n✓ Exported GitHub Action format to {output_dir}:")
        for metric, path in exported.items():
            print(f"  - {metric}: {path}")

    print("\n✅ Benchmark aggregation complete!")


if __name__ == '__main__':
    main()
