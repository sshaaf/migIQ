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

## Code Analysis Strategy

BEFORE using Grep/Read/Edit, ALWAYS:

1. **Check graph exists:**
   ```bash
   [ -f graphify-out/graph.json ] && echo "Graph available"
   ```

2. **For dependency questions:**
   ```bash
   /graphify path "ClassA" "ClassB"
   # Returns: Shortest dependency path
   ```

3. **For code search:**
   ```bash
   /graphify query "Find all @MessageDriven classes"
   # Returns: All matching nodes with file locations
   ```

4. **For architecture understanding:**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # Shows: Community structure, god nodes, relationships
   ```

5. **For class context:**
   ```bash
   /graphify query "What does OrderServiceMDB do?"
   # Returns: Class purpose and connections
   ```

6. **After making code changes:**
   ```bash
   /graphify .
   # Rebuilds graph (incremental if unchanged files, ~10-30s)
   ```

**Use Grep/Read only if:**
- Graph doesn't exist
- Question can't be answered from graph
- Need to see actual code implementation

**Performance Target:** <5 file reads per task

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
