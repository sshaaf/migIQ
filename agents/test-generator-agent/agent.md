---
name: test-generator-agent
type: harness
model: claude-sonnet-4-6
description: Generate characterization and functional tests
---

# Test Generator Agent

## Purpose

Generate characterization and functional tests

## Skills Used

- `/generate-characterization-tests`
- `/generate-functional-tests`
- `/validate-coverage`

## Workflow

```
1. Generate characterization tests
2. Generate functional tests
3. Validate coverage
4. Return test suite
```

## Configuration

```yaml
agent:
  name: test-generator-agent
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
