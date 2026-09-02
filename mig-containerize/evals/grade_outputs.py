#!/usr/bin/env python3
"""Grade mig-containerize outputs."""
import json, os, sys
from pathlib import Path

def chk(d, patterns):
    for fn in os.listdir(d) if os.path.exists(d) else []:
        try:
            with open(os.path.join(d, fn), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                found = [p for p in patterns if p.lower() in content]
                if found: return True, f"In {fn}"
        except: pass
    return False, "Not found"

def grade_1(d):
    return [
        {"name": "queried_rgctl_graph", **dict(zip(['passed','evidence'], chk(d, ['rgctl', 'pagerank', 'communities', 'metrics'])))},
        {"name": "selected_ubi_image", **dict(zip(['passed','evidence'], chk(d, ['ubi', 'red hat', 'openjdk'])))},
        {"name": "generated_dockerfile", **dict(zip(['passed','evidence'], chk(d, ['dockerfile', 'FROM'])))},
        {"name": "dockerfile_multistage", **dict(zip(['passed','evidence'], chk(d, ['multi-stage', 'FROM.*AS'])))},
        {"name": "dockerfile_nonroot", **dict(zip(['passed','evidence'], chk(d, ['non-root', 'USER 1001', 'USER'])))},
        {"name": "generated_deployment", **dict(zip(['passed','evidence'], chk(d, ['deployment', 'kind: deployment'])))},
        {"name": "generated_service", **dict(zip(['passed','evidence'], chk(d, ['service', 'kind: service'])))},
        {"name": "generated_route", **dict(zip(['passed','evidence'], chk(d, ['route', 'kind: route'])))},
        {"name": "generated_configmap", **dict(zip(['passed','evidence'], chk(d, ['configmap', 'kind: configmap'])))},
        {"name": "generated_secret", **dict(zip(['passed','evidence'], chk(d, ['secret', 'kind: secret'])))},
        {"name": "generated_pvc_or_statefulset", **dict(zip(['passed','evidence'], chk(d, ['pvc', 'persistentvolumeclaim', 'statefulset'])))},
    ]

GRADERS = {'eval-1': grade_1}

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
