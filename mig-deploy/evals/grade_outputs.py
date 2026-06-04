#!/usr/bin/env python3
"""Grade mig-deploy outputs."""
import json, os, sys
from pathlib import Path

def chk(d, patterns):
    for fn in os.listdir(d) if os.path.exists(d) else []:
        try:
            with open(os.path.join(d, fn), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                if any(p.lower() in content for p in patterns):
                    return True, f"In {fn}"
        except: pass
    return False, "Not found"

def grade_1(d):
    return [
        {"name": "detected_dependencies", **dict(zip(['passed','evidence'], chk(d, ['postgresql', 'database', 'dependency'])))},
        {"name": "deployed_app_and_db", **dict(zip(['passed','evidence'], chk(d, ['deployed', 'deployment', 'applied'])))},
        {"name": "verified_pods", **dict(zip(['passed','evidence'], chk(d, ['pod', 'running', 'ready'])))},
        {"name": "tested_endpoints", **dict(zip(['passed','evidence'], chk(d, ['endpoint', 'curl', 'http', 'test'])))},
        {"name": "deployment_report", **dict(zip(['passed','evidence'], chk(d, ['report', 'summary', 'url'])))},
    ]

GRADERS = {'eval-1': grade_1, 'eval-2': grade_1, 'eval-3': grade_1}

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
