---
name: code-refactor-agent
type: harness
model: claude-sonnet-4-6
description: Apply refactoring rules and generate code
---

# Code Refactor Agent

## Purpose

Apply refactoring rules and generate code

## Skills Used

- `/apply-refactor-rules`
- `/generate-spec-driven-code`
- `/validate-refactoring`

## Workflow

```
1. Apply refactoring rules
2. Generate new code from specs
3. Validate transformations
4. Return refactored code
```

## Configuration

```yaml
agent:
  name: code-refactor-agent
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
