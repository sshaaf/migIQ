---
name: story-orchestrator-agent
type: orchestrator
model: claude-sonnet-4-6
description: Orchestrates single user story through all harness phases
---

# Story Orchestrator Agent

## Purpose

Manages a single user story through the complete migration workflow across all harness phases.

## Workflow

```
┌──────────────────────────────────────┐
│ 1. Receive story from project-tracker│
├──────────────────────────────────────┤
│ 2. Test Harness (test-generator)    │
├──────────────────────────────────────┤
│ 3. Code Harness (code-refactor)     │
├──────────────────────────────────────┤
│ 4. Benchmark Harness (benchmark)    │
├──────────────────────────────────────┤
│ 5. Evaluation Harness (evaluator)   │
├──────────────────────────────────────┤
│ 6. CI Harness (ci-integration)      │
├──────────────────────────────────────┤
│ 7. Return result to project-tracker │
└──────────────────────────────────────┘
```

## Harness Invocation

Invokes harnesses sequentially, passing context between them:

1. **test-generator-agent** → Generates tests
2. **code-refactor-agent** → Applies transformations
3. **benchmark-builder-agent** → Performance validation
4. **quality-evaluator-agent** → Quality gates
5. **ci-integration-agent** → CI/CD integration

## Context Passing

Each harness receives:
- Story ID and description
- Previous harness outputs
- Trace ID for distributed tracing
- Configuration from rule.md

## Parallel Execution

Where dependencies allow:
- Test generation || Benchmark preparation
- Independent transformation rules

## Failure Handling

- **Harness Failure**: Retry with exponential backoff (max 3)
- **Persistent Failure**: Invoke failure-analyzer-agent
- **Human Escalation**: After max retries or critical failures

## State Management

**Story Context:**
- Story ID and metadata
- Test suite artifacts
- Refactored code
- Benchmark results
- Evaluation metrics
- CI pipeline results

## Configuration

```yaml
agent:
  name: story-orchestrator-agent
  sequential_harnesses:
    - test-generator-agent
    - code-refactor-agent
    - benchmark-builder-agent
    - quality-evaluator-agent
    - ci-integration-agent
  max_retries: 3
  retry_backoff_base: 1000  # ms
```
