#!/usr/bin/env python3
"""Grade mig-plan outputs against assertions."""

import json
import os
import sys
from pathlib import Path


def check_file_exists(file_path):
    return os.path.exists(file_path)


def check_patterns(filepath, patterns):
    if not os.path.exists(filepath):
        return False, "File not found"
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()
        found = [p for p in patterns if p.lower() in content]
        if found:
            return True, f"Found: {', '.join(found[:2])}"
    return False, "Patterns not found"


def grade_eval_1(run_dir):
    """Grade eval-1."""
    results = []
    run_path = Path(run_dir)

    # Check required documents exist (tasks.md and UserStory.md)
    files = ['tasks.md', 'UserStory.md']
    all_exist = all((run_path / f).exists() for f in files)
    results.append({"name": "required_documents_generated", "passed": all_exist,
                   "evidence": f"{sum(1 for f in files if (run_path/f).exists())}/{len(files)} files exist"})

    # tasks_address_specific_migration_patterns (e.g., EJB to Spring)
    passed, evidence = check_patterns(run_path / 'tasks.md', ['ejb', 'spring', 'component', 'service', 'migrate'])
    results.append({"name": "tasks_address_migration_patterns", "passed": passed, "evidence": evidence})

    # tasks_have_integration_hooks
    passed, evidence = check_patterns(run_path / 'tasks.md', ['mig-test-gen', 'mig-containerize', 'mig-deploy'])
    results.append({"name": "tasks_have_integration_hooks", "passed": passed, "evidence": evidence})

    # tasks_are_actionable
    passed, evidence = check_patterns(run_path / 'tasks.md', ['- [ ]', 'subtask', 'checkbox'])
    results.append({"name": "tasks_are_actionable", "passed": passed, "evidence": evidence})

    # userstory_links_to_tasks
    passed, evidence = check_patterns(run_path / 'UserStory.md', ['task', 'tasks.md', 'refer'])
    results.append({"name": "userstory_links_to_tasks", "passed": passed, "evidence": evidence})

    # userstory_has_acceptance_criteria
    passed, evidence = check_patterns(run_path / 'UserStory.md', ['acceptance', 'criteria', 'testable'])
    results.append({"name": "userstory_has_acceptance_criteria", "passed": passed, "evidence": evidence})

    # addresses_openshift_deployment
    passed, evidence = check_patterns(run_path / 'tasks.md', ['openshift', 'kubernetes', 'deployment'])
    results.append({"name": "addresses_openshift_deployment", "passed": passed, "evidence": evidence})

    return results


GRADERS = {'eval-1': grade_eval_1}


def main():
    if len(sys.argv) < 3:
        print("Usage: python grade_outputs.py <workspace_dir> <eval_name>")
        sys.exit(1)

    workspace_dir = Path(sys.argv[1])
    eval_name = sys.argv[2]

    grader = GRADERS.get(eval_name)
    if not grader:
        print(f"Unknown eval: {eval_name}")
        sys.exit(1)

    for config in ['with_skill', 'without_skill']:
        outputs_dir = workspace_dir / eval_name / config / 'outputs'
        if outputs_dir.exists():
            results = grader(outputs_dir)
            grading_file = workspace_dir / eval_name / config / 'grading.json'
            grading_file.parent.mkdir(parents=True, exist_ok=True)

            with open(grading_file, 'w') as f:
                json.dump({'expectations': results}, f, indent=2)

            passed = sum(1 for r in results if r['passed'])
            print(f"{eval_name}/{config}: {passed}/{len(results)} passed")


if __name__ == '__main__':
    main()
