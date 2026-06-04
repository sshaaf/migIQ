#!/usr/bin/env python3
"""Grade mig-execute outputs."""
import json, os, sys
from pathlib import Path

def check(filepath, patterns):
    if not os.path.exists(filepath): return False, "Not found"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()
        found = [p for p in patterns if p.lower() in content]
        return (True, f"Found: {','.join(found[:2])}") if found else (False, "Not found")

def check_dir(d, patterns):
    for fn in os.listdir(d) if os.path.exists(d) else []:
        try:
            with open(os.path.join(d, fn), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                found = [p for p in patterns if p.lower() in content]
                if found: return True, f"In {fn}"
        except: pass
    return False, "Not found"

def grade_full(d):
    r = Path(d)
    return [
        {"name": "execution_report_exists", **dict(zip(['passed','evidence'], [check(r/'EXECUTION_REPORT.md', ['summary','report'])[0], "EXECUTION_REPORT.md exists" if (r/'EXECUTION_REPORT.md').exists() else "Not found"]))},
        {"name": "execution_log_exists", **dict(zip(['passed','evidence'], [check(r/'execution-log.md', ['log','task'])[0], "execution-log.md exists" if (r/'execution-log.md').exists() else "Not found"]))},
        {"name": "addresses_user_stories", **dict(zip(['passed','evidence'], check_dir(d, ['user story 1', 'user story 2', 'user story 3'])))},
        {"name": "tasks_updated", **dict(zip(['passed','evidence'], check_dir(d, ['- [x]', 'checked', 'completed'])))},
        {"name": "includes_statistics", **dict(zip(['passed','evidence'], check_dir(d, ['completed', 'failed', 'skipped', 'count', 'statistics'])))},
        {"name": "mentions_parallel_execution", **dict(zip(['passed','evidence'], check_dir(d, ['parallel', 'concurrent', 'sub-agent', 'simultaneously'])))},
        {"name": "includes_next_steps", **dict(zip(['passed','evidence'], check_dir(d, ['next steps', 'recommendations', 'follow-up'])))},
    ]

GRADERS = {'full-execution': grade_full}

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
            print(f"{eval_name}/{config}: {sum(1 for r in results if r['passed'])}/{len(results)} passed")

if __name__ == '__main__': main()
