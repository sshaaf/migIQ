---
name: benchmark-builder-agent
type: harness
model: claude-sonnet-4-6
description: Build and run performance benchmarks
---

# Benchmark Builder Agent

## Purpose

Build and run performance benchmarks

## Skills Used

- `/build-benchmark-suite`
- `/establish-baseline`
- `/run-benchmarks`

## Workflow

```
1. Build benchmark suite
2. Establish baseline
3. Run benchmarks
4. Return performance report
```

## Configuration

```yaml
agent:
  name: benchmark-builder-agent
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
