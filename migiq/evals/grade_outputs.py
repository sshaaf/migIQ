#!/usr/bin/env python3
"""Grade migiq orchestrator outputs."""
import json, os, sys
from pathlib import Path

def chk(d, patterns):
    for fn in os.listdir(d) if os.path.exists(d) else []:
        try:
            with open(os.path.join(d, fn), 'r', encoding='utf-8', errors='ignore') as f:
                if any(p.lower() in f.read().lower() for p in patterns):
                    return True, f"In {fn}"
        except: pass
    return False, "Not found"

def grade_orchestrator(d):
    return [
        {"name": "graphify_analysis", **dict(zip(['passed','evidence'], chk(d, ['graph', 'analysis', 'graphify'])))},
        {"name": "migration_plan", **dict(zip(['passed','evidence'], chk(d, ['plan', 'tasks', 'user story'])))},
        {"name": "execution_evidence", **dict(zip(['passed','evidence'], chk(d, ['execution', 'completed', 'migrated'])))},
        {"name": "containerization", **dict(zip(['passed','evidence'], chk(d, ['dockerfile', 'container', 'image'])))},
        {"name": "deployment_configs", **dict(zip(['passed','evidence'], chk(d, ['deployment', 'openshift', 'kubernetes'])))},
        {"name": "final_report", **dict(zip(['passed','evidence'], chk(d, ['migration report', 'summary', 'complete'])))},
    ]

GRADERS = {'spring-boot-to-quarkus': grade_orchestrator, 'nodejs-express-modernization': grade_orchestrator, 'java-ee-to-spring-boot': grade_orchestrator}

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
