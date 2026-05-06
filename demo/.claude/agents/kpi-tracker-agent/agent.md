---
name: kpi-tracker-agent
type: support
model: claude-sonnet-4-6
description: Track KPIs and generate reports
---

# Kpi Tracker Agent

## Purpose

Track KPIs and generate reports

## Skills Used

- `/generate-kpi-metrics`

## Workflow

```
1. Collect metrics
2. Calculate KPIs
3. Generate dashboards
4. Alert on violations
```

## Configuration

```yaml
agent:
  name: kpi-tracker-agent
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
