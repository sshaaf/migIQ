---
name: ci-integration-agent
type: harness
model: claude-sonnet-4-6
description: Integrate with CI/CD platform
---

# Ci Integration Agent

## Purpose

Integrate with CI/CD platform

## Skills Used

- `/prepare-merge-request`
- `/push-merge-request`
- `/monitor-pipeline`
- `/handle-pipeline-result`

## Workflow

```
1. Prepare MR
2. Push to platform
3. Monitor pipeline
4. Handle result
```

## Configuration

```yaml
agent:
  name: ci-integration-agent
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
