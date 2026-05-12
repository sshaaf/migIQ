---
name: documentation-manager-agent
type: support
model: claude-sonnet-4-6
description: Manage and update configuration documentation
---

# Documentation Manager Agent

## Purpose

Manage and update configuration documentation

## Skills Used

- `/update-documentation`

## Workflow

```
1. Receive update request
2. Validate changes
3. Update files
4. Commit to git
```

## Configuration

```yaml
agent:
  name: documentation-manager-agent
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
