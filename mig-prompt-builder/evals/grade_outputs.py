#!/usr/bin/env python3
"""Grade mig-prompt-builder outputs against assertions.

This script evaluates skill outputs from a workspace directory against
the assertions defined in evals.json.

Usage:
    python grade_outputs.py <workspace_dir> <eval_id>

Example:
    python grade_outputs.py ../../mig-prompt-builder-workspace/iteration-1 eval-1-vague-java
"""

import json
import os
import sys
import re
from pathlib import Path


def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)


def check_file_contains(file_path, patterns, require_all=False):
    """Check if file contains certain patterns (case-insensitive)."""
    if not os.path.exists(file_path):
        return False, "File not found"

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()

    matches = [p.lower() in content for p in patterns]

    if require_all:
        if all(matches):
            return True, "Found all required patterns"
        else:
            missing = [patterns[i] for i, m in enumerate(matches) if not m]
            return False, f"Missing patterns: {', '.join(missing)}"
    else:
        if any(matches):
            found = [patterns[i] for i, m in enumerate(matches) if m]
            return True, f"Found patterns: {', '.join(found[:2])}"
        else:
            return False, "No patterns found"


def check_not_contains(file_path, patterns):
    """Check that file does NOT contain certain patterns (word boundaries)."""
    if not os.path.exists(file_path):
        return False, "File not found"

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()

    found_patterns = []
    for p in patterns:
        if re.search(r'\b' + re.escape(p.lower()) + r'\b', content):
            found_patterns.append(p)

    if not found_patterns:
        return True, "None of the forbidden patterns found"
    else:
        return False, f"Found forbidden patterns: {', '.join(found_patterns)}"


def grade_eval_1(run_dir):
    """Grade eval-1: vague Java migration."""
    results = []
    prompt_path = Path(run_dir) / 'migration-prompt.md'

    # Migration prompt generated
    exists = check_file_exists(prompt_path)
    results.append({
        "name": "migration_prompt_generated",
        "passed": exists,
        "evidence": "migration-prompt.md exists" if exists else "not found"
    })

    if not exists:
        return results

    # Asked clarifying questions
    conversation_files = list(Path(run_dir).glob('*conversation*')) + \
                        list(Path(run_dir).glob('*question*')) + \
                        list(Path(run_dir).glob('*requirements*'))
    asked_questions = len(conversation_files) > 0
    if not asked_questions:
        with open(prompt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            asked_questions = any(word in content for word in ['gather', 'clarify', 'question', 'interview'])

    results.append({
        "name": "asked_clarifying_questions",
        "passed": asked_questions,
        "evidence": f"Found {len(conversation_files)} artifacts" if conversation_files else "Evidence in prompt"
    })

    # Includes OpenShift
    passed, evidence = check_file_contains(prompt_path, ['openshift', 'red hat openshift'])
    results.append({"name": "includes_openshift", "passed": passed, "evidence": evidence})

    # Includes containerization
    passed, evidence = check_file_contains(prompt_path, ['container', 'docker', 'podman'], require_all=False)
    results.append({"name": "includes_containerization", "passed": passed, "evidence": evidence})

    # Includes test coverage
    passed, evidence = check_file_contains(
        prompt_path,
        ['characterization test', 'test coverage', 'unit test', 'integration test'],
        require_all=False
    )
    results.append({"name": "includes_test_coverage", "passed": passed, "evidence": evidence})

    # Includes detailed plan request
    passed, evidence = check_file_contains(
        prompt_path,
        ['detailed migration plan', 'phase', 'task', 'dependencies', 'migration plan'],
        require_all=False
    )
    results.append({"name": "includes_detailed_plan_request", "passed": passed, "evidence": evidence})

    # Current app summary
    passed, evidence = check_file_contains(
        prompt_path,
        ['current application', 'technology stack', 'architecture', 'java'],
        require_all=False
    )
    results.append({"name": "current_app_summary", "passed": passed, "evidence": evidence})

    # Target tech specified
    passed, evidence = check_file_contains(
        prompt_path,
        ['target', 'spring boot', 'migration to', 'modernization'],
        require_all=False
    )
    results.append({"name": "target_tech_specified", "passed": passed, "evidence": evidence})

    return results


def grade_eval_2(run_dir):
    """Grade eval-2: Rails EKS override."""
    results = []
    prompt_path = Path(run_dir) / 'migration-prompt.md'

    exists = check_file_exists(prompt_path)
    results.append({
        "name": "migration_prompt_generated",
        "passed": exists,
        "evidence": "migration-prompt.md exists" if exists else "not found"
    })

    if not exists:
        return results

    # Overrode EKS to OpenShift
    passed, evidence = check_file_contains(prompt_path, ['openshift', 'red hat openshift'])
    results.append({"name": "overrode_eks_to_openshift", "passed": passed, "evidence": evidence})

    # Phased approach specified
    passed, evidence = check_file_contains(
        prompt_path,
        ['phased', 'strangler', 'incremental', 'gradual', 'phase 1'],
        require_all=False
    )
    results.append({"name": "phased_approach_specified", "passed": passed, "evidence": evidence})

    # Rails analysis included
    passed, evidence = check_file_contains(prompt_path, ['rails', '80k', '80,000', 'monolith', 'ruby'], require_all=False)
    results.append({"name": "rails_analysis_included", "passed": passed, "evidence": evidence})

    # Microservices target
    passed, evidence = check_file_contains(prompt_path, ['microservice', 'node.js', 'nodejs', 'node'], require_all=False)
    results.append({"name": "microservices_target", "passed": passed, "evidence": evidence})

    # Includes containerization
    passed, evidence = check_file_contains(prompt_path, ['container', 'docker', 'podman'])
    results.append({"name": "includes_containerization", "passed": passed, "evidence": evidence})

    # Includes test coverage
    passed, evidence = check_file_contains(prompt_path, ['characterization test', 'test coverage', 'test'], require_all=False)
    results.append({"name": "includes_test_coverage", "passed": passed, "evidence": evidence})

    # No explicit EKS mention
    passed, evidence = check_not_contains(prompt_path, ['eks', 'elastic kubernetes service'])
    results.append({"name": "no_explicit_eks_mention", "passed": passed, "evidence": evidence})

    return results


def grade_eval_3(run_dir):
    """Grade eval-3: .NET modernization."""
    results = []
    prompt_path = Path(run_dir) / 'migration-prompt.md'

    exists = check_file_exists(prompt_path)
    results.append({
        "name": "migration_prompt_generated",
        "passed": exists,
        "evidence": "migration-prompt.md exists" if exists else "not found"
    })

    if not exists:
        return results

    # Addresses WCF migration
    passed, evidence = check_file_contains(prompt_path, ['wcf', 'windows communication foundation', 'grpc', 'corewcf'], require_all=False)
    results.append({"name": "addresses_wcf_migration", "passed": passed, "evidence": evidence})

    # Addresses EF6 migration
    passed, evidence = check_file_contains(prompt_path, ['entity framework', 'ef6', 'ef core'], require_all=False)
    results.append({"name": "addresses_ef6_migration", "passed": passed, "evidence": evidence})

    # Addresses ASMX migration
    passed, evidence = check_file_contains(prompt_path, ['asmx', 'web service', 'soap'], require_all=False)
    results.append({"name": "addresses_asmx_migration", "passed": passed, "evidence": evidence})

    # Zero downtime requirement
    passed, evidence = check_file_contains(prompt_path, ['zero downtime', 'no downtime', 'high availability', 'parallel run'], require_all=False)
    results.append({"name": "zero_downtime_requirement", "passed": passed, "evidence": evidence})

    # Includes OpenShift
    passed, evidence = check_file_contains(prompt_path, ['openshift', 'red hat openshift'])
    results.append({"name": "includes_openshift", "passed": passed, "evidence": evidence})

    # Includes containerization
    passed, evidence = check_file_contains(prompt_path, ['container', 'docker', 'podman'])
    results.append({"name": "includes_containerization", "passed": passed, "evidence": evidence})

    # Includes test coverage
    passed, evidence = check_file_contains(prompt_path, ['characterization test', 'test coverage', 'test'], require_all=False)
    results.append({"name": "includes_test_coverage", "passed": passed, "evidence": evidence})

    return results


GRADERS = {
    'eval-1-vague-java': grade_eval_1,
    'eval-2-rails-eks-override': grade_eval_2,
    'eval-3-dotnet-modernization': grade_eval_3,
}


def main():
    if len(sys.argv) < 3:
        print("Usage: python grade_outputs.py <workspace_dir> <eval_id>")
        print("Example: python grade_outputs.py ../../mig-prompt-builder-workspace/iteration-1 eval-1-vague-java")
        sys.exit(1)

    workspace_dir = Path(sys.argv[1])
    eval_id = sys.argv[2]

    if eval_id not in GRADERS:
        print(f"Unknown eval_id: {eval_id}")
        print(f"Available: {', '.join(GRADERS.keys())}")
        sys.exit(1)

    grader = GRADERS[eval_id]

    # Check for with_skill/without_skill subdirs
    for config in ['with_skill', 'without_skill']:
        outputs_dir = workspace_dir / eval_id / config / 'outputs'
        if outputs_dir.exists():
            results = grader(outputs_dir)
            grading_file = workspace_dir / eval_id / config / 'grading.json'
            grading_file.parent.mkdir(parents=True, exist_ok=True)

            with open(grading_file, 'w') as f:
                json.dump({'expectations': results}, f, indent=2)

            passed = sum(1 for r in results if r['passed'])
            total = len(results)
            print(f"{eval_id}/{config}: {passed}/{total} passed")


if __name__ == '__main__':
    main()
