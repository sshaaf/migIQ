#!/usr/bin/env python3
"""Generate agent definition stubs"""

from pathlib import Path

AGENTS = {
    "test-generator-agent": {
        "type": "harness",
        "purpose": "Generate characterization and functional tests",
        "skills": ["generate-characterization-tests", "generate-functional-tests", "validate-coverage"],
        "workflow": "1. Generate characterization tests\n2. Generate functional tests\n3. Validate coverage\n4. Return test suite"
    },
    "code-refactor-agent": {
        "type": "harness",
        "purpose": "Apply refactoring rules and generate code",
        "skills": ["apply-refactor-rules", "generate-spec-driven-code", "validate-refactoring"],
        "workflow": "1. Apply refactoring rules\n2. Generate new code from specs\n3. Validate transformations\n4. Return refactored code"
    },
    "benchmark-builder-agent": {
        "type": "harness",
        "purpose": "Build and run performance benchmarks",
        "skills": ["build-benchmark-suite", "establish-baseline", "run-benchmarks"],
        "workflow": "1. Build benchmark suite\n2. Establish baseline\n3. Run benchmarks\n4. Return performance report"
    },
    "quality-evaluator-agent": {
        "type": "harness",
        "purpose": "Evaluate code quality and enforce gates",
        "skills": ["generate-evaluation-metrics", "calculate-test-scores", "validate-quality"],
        "workflow": "1. Generate metrics\n2. Calculate scores\n3. Validate thresholds\n4. Return go/no-go decision"
    },
    "ci-integration-agent": {
        "type": "harness",
        "purpose": "Integrate with CI/CD platform",
        "skills": ["prepare-merge-request", "push-merge-request", "monitor-pipeline", "handle-pipeline-result"],
        "workflow": "1. Prepare MR\n2. Push to platform\n3. Monitor pipeline\n4. Handle result"
    },
    "failure-analyzer-agent": {
        "type": "support",
        "purpose": "Analyze failures and generate remediation plans",
        "skills": ["request-root-cause", "update-documentation"],
        "workflow": "1. Analyze failure\n2. Generate root cause\n3. Create remediation plan\n4. Update documentation"
    },
    "documentation-manager-agent": {
        "type": "support",
        "purpose": "Manage and update configuration documentation",
        "skills": ["update-documentation"],
        "workflow": "1. Receive update request\n2. Validate changes\n3. Update files\n4. Commit to git"
    },
    "kpi-tracker-agent": {
        "type": "support",
        "purpose": "Track KPIs and generate reports",
        "skills": ["generate-kpi-metrics"],
        "workflow": "1. Collect metrics\n2. Calculate KPIs\n3. Generate dashboards\n4. Alert on violations"
    }
}

def create_agent(name, info):
    """Create agent definition"""
    base = Path(f".claude/agents/{name}")
    base.mkdir(exist_ok=True)

    content = f"""---
name: {name}
type: {info['type']}
model: claude-sonnet-4-6
description: {info['purpose']}
---

# {name.title().replace('-', ' ')}

## Purpose

{info['purpose']}

## Skills Used

{chr(10).join(f'- `/{skill}`' for skill in info['skills'])}

## Workflow

```
{info['workflow']}
```

## Configuration

```yaml
agent:
  name: {name}
  type: {info['type']}
  max_retries: 3
  timeout: 3600
```

## State Management

Maintains local state for current task and outputs for next harness.

## Error Handling

- Retry with exponential backoff
- Escalate after max retries
- Log all failures with trace ID
"""
    (base / "agent.md").write_text(content)
    print(f"✓ Created {name}")

if __name__ == "__main__":
    for name, info in AGENTS.items():
        create_agent(name, info)

    print(f"\n✅ Created {len(AGENTS)} agents")
