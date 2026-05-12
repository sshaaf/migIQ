---
name: quality-evaluator-agent
type: harness
model: claude-sonnet-4-6
description: Evaluate code quality and enforce gates
---

# Quality Evaluator Agent

## Purpose

Evaluate code quality and enforce gates

## Skills Used

- `/generate-evaluation-metrics`
- `/calculate-test-scores`
- `/validate-quality`

## Workflow

```
1. Generate metrics
2. Calculate scores
3. Validate thresholds
4. Return go/no-go decision
```

## Configuration

```yaml
agent:
  name: quality-evaluator-agent
  type: harness
  max_retries: 3
  timeout: 3600
```

## State Management

Maintains local state for current task and outputs for next harness.

## Error Handling

- Retry with exponential backoff
- Escalate after max retries
- Log all failures with trace ID
