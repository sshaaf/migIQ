#!/usr/bin/env python3
"""Compare agent performance with/without graphify.

This script analyzes benchmark logs from baseline (without graph) and
graphify (with graph) runs, then generates a comparison report.

Usage:
    python scripts/compare-benchmarks.py

Input files:
    - benchmark-without-graph.log
    - benchmark-with-graph.log

Output:
    Markdown-formatted comparison report to stdout
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional


def parse_log(log_file: str) -> Dict:
    """Extract metrics from agent benchmark log.

    Args:
        log_file: Path to benchmark log file

    Returns:
        Dictionary with metrics:
        - grep_calls: Number of Grep tool calls
        - read_calls: Number of Read tool calls
        - graphify_queries: Number of graphify queries (0 for baseline)
        - execution_time: Total execution time in seconds
    """
    if not Path(log_file).exists():
        print(f"Error: Log file not found: {log_file}", file=sys.stderr)
        return {
            "grep_calls": 0,
            "read_calls": 0,
            "graphify_queries": 0,
            "execution_time": 0
        }

    with open(log_file) as f:
        content = f.read()

    # Count tool calls
    grep_calls = content.count('"tool": "Grep"')
    read_calls = content.count('"tool": "Read"')

    # Count graphify queries (query, path)
    graphify_queries = len(re.findall(r'graphify (query|path)', content))

    # Extract execution time
    execution_time = extract_time(content)

    return {
        "grep_calls": grep_calls,
        "read_calls": read_calls,
        "graphify_queries": graphify_queries,
        "execution_time": execution_time
    }


def extract_time(content: str) -> float:
    """Extract execution time from benchmark output.

    Parses "real XmYs" format from time command output.

    Args:
        content: Log file content

    Returns:
        Execution time in seconds
    """
    # Match "real 5m23.456s" format
    match = re.search(r'real\s+(\d+)m([\d.]+)s', content)
    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        return minutes * 60 + seconds

    return 0.0


def calculate_improvement(baseline: float, optimized: float) -> float:
    """Calculate percentage improvement.

    Args:
        baseline: Baseline value
        optimized: Optimized value

    Returns:
        Percentage improvement (positive means faster/fewer)
    """
    if baseline == 0:
        return 0.0

    improvement = (1 - optimized / baseline) * 100
    return improvement


def generate_report(without_graph: Dict, with_graph: Dict) -> None:
    """Generate markdown comparison report.

    Args:
        without_graph: Metrics from baseline run
        with_graph: Metrics from graphify run
    """
    print("# Agent Performance Comparison")
    print()
    print("| Metric | Without Graph | With Graph | Improvement |")
    print("|--------|---------------|------------|-------------|")

    # Execution time
    time_improvement = calculate_improvement(
        without_graph["execution_time"],
        with_graph["execution_time"]
    )
    print(f"| Execution Time | {without_graph['execution_time']:.1f}s | "
          f"{with_graph['execution_time']:.1f}s | "
          f"**{time_improvement:.0f}% faster** |")

    # Grep calls
    grep_reduction = calculate_improvement(
        without_graph["grep_calls"],
        with_graph["grep_calls"]
    )
    print(f"| Grep Calls | {without_graph['grep_calls']} | "
          f"{with_graph['grep_calls']} | "
          f"**{grep_reduction:.0f}% fewer** |")

    # Read calls
    read_reduction = calculate_improvement(
        without_graph["read_calls"],
        with_graph["read_calls"]
    )
    print(f"| Read Calls | {without_graph['read_calls']} | "
          f"{with_graph['read_calls']} | "
          f"**{read_reduction:.0f}% fewer** |")

    # Graphify queries (new capability)
    print(f"| Graphify Queries | 0 | "
          f"{with_graph['graphify_queries']} | "
          f"**New capability** |")

    print()
    print("## Summary")
    print()
    print(f"**Overall speedup**: {time_improvement:.0f}%")
    print(f"**I/O reduction**: {read_reduction:.0f}% fewer file reads")
    print(f"**New capabilities**: {with_graph['graphify_queries']} graph queries enabled")
    print()

    # Success criteria
    print("## Success Criteria")
    print()

    success_criteria = []

    # Check 50% speedup target
    if time_improvement >= 50:
        success_criteria.append("✅ Execution time improved by >50%")
    else:
        success_criteria.append(f"❌ Execution time improved by {time_improvement:.0f}% (target: 50%)")

    # Check 90% I/O reduction target
    if read_reduction >= 90:
        success_criteria.append("✅ File reads reduced by >90%")
    else:
        success_criteria.append(f"⚠️  File reads reduced by {read_reduction:.0f}% (target: 90%)")

    # Check graph usage
    if with_graph['graphify_queries'] > 10:
        success_criteria.append("✅ Agent uses graph queries (>10 queries)")
    elif with_graph['graphify_queries'] > 0:
        success_criteria.append(f"⚠️  Agent uses {with_graph['graphify_queries']} graph queries (expected: >10)")
    else:
        success_criteria.append("❌ Agent not using graph queries")

    for criterion in success_criteria:
        print(f"- {criterion}")

    print()


def main():
    """Main entry point for benchmark comparison."""
    baseline_log = "benchmark-without-graph.log"
    graphify_log = "benchmark-with-graph.log"

    # Check if log files exist
    if not Path(baseline_log).exists():
        print(f"Error: Baseline log not found: {baseline_log}", file=sys.stderr)
        print("Run: ./scripts/benchmark-without-graph.sh <agent> <story>", file=sys.stderr)
        sys.exit(1)

    if not Path(graphify_log).exists():
        print(f"Error: Graphify log not found: {graphify_log}", file=sys.stderr)
        print("Run: ./scripts/benchmark-with-graph.sh <agent> <story>", file=sys.stderr)
        sys.exit(1)

    # Parse logs
    without_graph = parse_log(baseline_log)
    with_graph = parse_log(graphify_log)

    # Generate report
    generate_report(without_graph, with_graph)


if __name__ == "__main__":
    main()
