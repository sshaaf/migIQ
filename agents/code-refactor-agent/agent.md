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

## Code Analysis Strategy

BEFORE using Grep/Read/Edit, ALWAYS:

1. **Check graph exists:**
   ```bash
   [ -f graphify-out/graph.json ] && echo "Graph available"
   ```

2. **For dependency questions:**
   ```bash
   graphify path "ClassA" "ClassB"
   # Returns: Shortest dependency path
   ```

3. **For code search:**
   ```bash
   graphify query "Find all @MessageDriven classes"
   # Returns: All matching nodes with file locations
   ```

4. **For architecture understanding:**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # Shows: Community structure, god nodes, relationships
   ```

5. **For class context:**
   ```bash
   graphify query "What does OrderServiceMDB do?"
   # Returns: Class purpose and connections
   ```

6. **After making code changes:**
   ```bash
   graphify extract . --update
   # Updates graph (incremental, only changed files, ~10-30s)
   ```

**Use Grep/Read only if:**
- Graph doesn't exist
- Question can't be answered from graph
- Need to see actual code implementation

**Performance Target:** <5 file reads per task

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
