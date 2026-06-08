#!/usr/bin/env python3
"""Grade mig-graphify outputs against assertions.

Usage:
    python grade_outputs.py <workspace_dir> <eval_name>
"""

import json
import os
import sys
from pathlib import Path


def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)


def check_patterns_in_files(directory, patterns, filenames=None):
    """Check if patterns appear in any files in directory."""
    if not os.path.exists(directory):
        return False, "Directory not found"

    search_files = filenames if filenames else os.listdir(directory)

    for filename in search_files:
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            continue

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
                found = [p for p in patterns if p.lower() in content]
                if found:
                    return True, f"Found in {filename}: {', '.join(found[:2])}"
        except:
            continue

    return False, "Patterns not found in any file"


def grade_eval(run_dir, eval_id):
    """Grade an eval based on its ID."""
    results = []
    run_path = Path(run_dir)

    # Common grading for all mig-graphify evals
    common_checks = [
        {
            "name": "ran_graphify_cli",
            "check": lambda: check_patterns_in_files(run_dir, ['graphify update', 'graphify extract', 'graph.json', 'graphify-out'])
        },
        {
            "name": "references_graph_output",
            "check": lambda: check_patterns_in_files(run_dir, ['graph.json', 'GRAPH_REPORT.md', 'graphify-out', 'graph output'])
        },
        {
            "name": "mentions_god_nodes",
            "check": lambda: check_patterns_in_files(run_dir, ['god node', 'high-degree node', 'high degree', 'highest degree', 'most connected'])
        },
        {
            "name": "uses_graph_metrics",
            "check": lambda: check_patterns_in_files(run_dir, ['degree', 'edges', 'nodes', 'connectivity', 'coupling'])
        },
    ]

    # Eval-specific checks
    eval_specific = {
        'eval-1': [
            {
                "name": "mentions_communities",
                "check": lambda: check_patterns_in_files(run_dir, ['communities', 'community detection', 'logical groupings', 'clusters'])
            },
            {
                "name": "identifies_spring_dependencies",
                "check": lambda: check_patterns_in_files(run_dir, ['spring boot', 'spring data', 'spring security'])
            },
            {
                "name": "suggests_migration_strategy",
                "check": lambda: check_patterns_in_files(run_dir, ['phased', 'migration strategy', 'migration approach', 'migration plan'])
            },
        ],
        'eval-2': [
            {
                "name": "mentions_communities",
                "check": lambda: check_patterns_in_files(run_dir, ['communities', 'community', 'microservices', 'service boundaries'])
            },
            {
                "name": "identifies_circular_dependencies",
                "check": lambda: check_patterns_in_files(run_dir, ['circular', 'cycle', 'circular dependency'])
            },
            {
                "name": "recommends_extraction_order",
                "check": lambda: check_patterns_in_files(run_dir, ['extraction order', 'leaf', 'migration order', 'start with'])
            },
        ],
        'eval-3': [
            {
                "name": "identifies_file_system_dependencies",
                "check": lambda: check_patterns_in_files(run_dir, ['file system', 'file path', 'local storage', 'file upload'])
            },
            {
                "name": "identifies_oracle_dependency",
                "check": lambda: check_patterns_in_files(run_dir, ['oracle', 'database'])
            },
            {
                "name": "identifies_platform_specific_code",
                "check": lambda: check_patterns_in_files(run_dir, ['platform-specific', 'on-prem', 'on-premises'])
            },
            {
                "name": "discusses_containerization",
                "check": lambda: check_patterns_in_files(run_dir, ['containerization', 'docker', 'podman', 'container image'])
            },
            {
                "name": "provides_migration_phases",
                "check": lambda: check_patterns_in_files(run_dir, ['phase', 'migration strategy', 'migration plan'])
            },
        ],
        'eval-4': [
            {
                "name": "identifies_service_dependencies",
                "check": lambda: check_patterns_in_files(run_dir, ['mongodb', 'redis', 'database', 'file storage'])
            },
            {
                "name": "discusses_configuration_management",
                "check": lambda: check_patterns_in_files(run_dir, ['configmap', 'secret', 'environment variable', 'configuration'])
            },
            {
                "name": "provides_dockerfile_guidance",
                "check": lambda: check_patterns_in_files(run_dir, ['dockerfile', 'container image', 'build'])
            },
            {
                "name": "addresses_multi_service_coordination",
                "check": lambda: check_patterns_in_files(run_dir, ['coordinate', 'multiple services', 'service communication'])
            },
            {
                "name": "provides_openshift_deployment_plan",
                "check": lambda: check_patterns_in_files(run_dir, ['openshift', 'deployment', 'kubernetes'])
            },
        ],
    }

    # Run common checks
    for check in common_checks:
        passed, evidence = check['check']()
        results.append({
            "name": check['name'],
            "passed": passed,
            "evidence": evidence
        })

    # Run eval-specific checks
    specific_checks = eval_specific.get(eval_id, [])
    for check in specific_checks:
        passed, evidence = check['check']()
        results.append({
            "name": check['name'],
            "passed": passed,
            "evidence": evidence
        })

    return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python grade_outputs.py <workspace_dir> <eval_name>")
        sys.exit(1)

    workspace_dir = Path(sys.argv[1])
    eval_name = sys.argv[2]

    # Check for with_skill/without_skill subdirs
    for config in ['with_skill', 'without_skill']:
        outputs_dir = workspace_dir / eval_name / config / 'outputs'
        if outputs_dir.exists():
            results = grade_eval(outputs_dir, eval_name)
            grading_file = workspace_dir / eval_name / config / 'grading.json'
            grading_file.parent.mkdir(parents=True, exist_ok=True)

            with open(grading_file, 'w') as f:
                json.dump({'expectations': results}, f, indent=2)

            passed = sum(1 for r in results if r['passed'])
            total = len(results)
            print(f"{eval_name}/{config}: {passed}/{total} passed")


if __name__ == '__main__':
    main()
