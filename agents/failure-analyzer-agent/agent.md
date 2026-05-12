---
name: failure-analyzer-agent
type: support
model: claude-sonnet-4-6
description: Analyze failures and generate remediation plans
---

# Failure Analyzer Agent

## Purpose

Analyze failures and generate remediation plans

## Skills Used

- `/request-root-cause`
- `/update-documentation`

## Workflow

```
1. Analyze failure
2. Generate root cause
3. Create remediation plan
4. Update documentation
```

## Configuration

```yaml
agent:
  name: failure-analyzer-agent
  type: support
  max_retries: 3
  timeout: 3600
```

## State Management

Maintains local state for current task and outputs for next harness.

## Error Handling

- Retry with exponential backoff
- Escalate after max retries
- Log all failures with trace ID
