#!/usr/bin/env python3
"""Grade mig-test-gen outputs."""
import json, os, sys
from pathlib import Path

def check(filepath, patterns):
    if not os.path.exists(filepath): return False, "Not found"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()
        found = [p for p in patterns if p.lower() in content]
        return (True, f"Found: {', '.join(found[:2])}") if found else (False, "Not found")

def check_dir(directory, patterns):
    if not os.path.exists(directory): return False, "Directory not found"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    found = [p for p in patterns if p.lower() in content]
                    if found: return True, f"Found in {filename}"
            except: pass
    return False, "Not found"

def grade_eval_1(d):
    r = Path(d)
    return [
        {"name": "queried_rgctl_graph", **dict(zip(['passed', 'evidence'], check_dir(d, ['rgctl', 'pagerank', 'communities', 'metrics', 'blast-radius'])))},
        {"name": "identified_god_nodes", **dict(zip(['passed', 'evidence'], check_dir(d, ['god node', 'high-degree', 'most connected'])))},
        {"name": "assigned_priority_tiers", **dict(zip(['passed', 'evidence'], check_dir(d, ['priority 1', 'priority 2', 'tier', 'high priority'])))},
        {"name": "set_coverage_targets", **dict(zip(['passed', 'evidence'], check_dir(d, ['coverage', '90%', '80%', 'target'])))},
        {"name": "generated_test_code", **dict(zip(['passed', 'evidence'], check_dir(d, ['@test', 'junit', 'test class', 'def test_'])))},
        {"name": "created_test_report", **dict(zip(['passed', 'evidence'], check_dir(d, ['test report', 'test suite', 'summary'])))},
        {"name": "used_graph_metrics", **dict(zip(['passed', 'evidence'], check_dir(d, ['degree', 'edges', 'connectivity', 'metric'])))},
        {"name": "followed_graph_paths", **dict(zip(['passed', 'evidence'], check_dir(d, ['integration test', 'path', 'controller', 'service'])))},
    ]

GRADERS = {'eval-1': grade_eval_1}

def main():
    if len(sys.argv) < 3: print("Usage: python grade_outputs.py <workspace_dir> <eval_name>"); sys.exit(1)
    workspace_dir, eval_name = Path(sys.argv[1]), sys.argv[2]
    if eval_name not in GRADERS: print(f"Unknown: {eval_name}"); sys.exit(1)
    for config in ['with_skill', 'without_skill']:
        outputs_dir = workspace_dir / eval_name / config / 'outputs'
        if outputs_dir.exists():
            results = GRADERS[eval_name](outputs_dir)
            grading_file = workspace_dir / eval_name / config / 'grading.json'
            grading_file.parent.mkdir(parents=True, exist_ok=True)
            with open(grading_file, 'w') as f: json.dump({'expectations': results}, f, indent=2)
            passed = sum(1 for r in results if r['passed'])
            print(f"{eval_name}/{config}: {passed}/{len(results)} passed")

if __name__ == '__main__': main()
