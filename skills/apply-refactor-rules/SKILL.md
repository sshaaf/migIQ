---
name: apply-refactor-rules
trigger: /apply-refactor-rules
description: Apply refactoring rules from rule.md to transform code. Use when the user wants to refactor code, apply transformation rules, modernize code patterns, or implement code changes based on migration rules.
---

Apply refactoring rules from rule.md to transform code.

## Parameters

- `--source-path` (required): Path to source code to refactor
- `--rules-path` (required): Path to rule.md file with transformation rules
- `--dry-run` (optional): Preview changes without applying (default: false)
- `--output` (optional): Path for transformation report (default: ./refactor-report.json)

## Description

Applies refactoring rules to transform code based on migration requirements. Uses Graphify to understand code structure and dependencies before making changes.

## Code Analysis Strategy

**BEFORE refactoring, use Graphify to understand the code:**

1. **Check graph exists:**
   ```bash
   [ -f graphify-out/graph.json ] && echo "Graph available"
   ```

2. **Find files to refactor:**
   ```bash
   /graphify query "Find all classes matching pattern X"
   # Returns: All matching files with locations
   ```

3. **Check dependencies before refactoring:**
   ```bash
   /graphify path "SourceClass" "DependentClass"
   # Returns: Dependency path - critical for understanding impact
   ```

4. **Understand class relationships:**
   ```bash
   /graphify query "What does ClassX depend on?"
   /graphify query "What depends on ClassX?"
   ```

5. **After making changes:**
   ```bash
   /graphify .
   # Rebuilds graph to reflect refactored code (~10-30s)
   ```

**Use Grep/Read only for:**
- Reading actual code to refactor
- Applying transformations
- Generating diffs

**Performance Target:** <5 file reads per refactoring task

## Actions

1. Validate input parameters
2. Load refactoring rules from rule.md
3. Use Graphify to identify target files and dependencies
4. For each file to refactor:
   - Read file content
   - Apply transformation rules
   - Validate syntax
   - Generate diff
5. Create transformation report
6. If not dry-run: Apply changes
7. Rebuild Graphify graph with changes

## Returns

Transformation report containing:
- Files modified
- Rules applied per file
- Diffs for each transformation
- Validation results
- Updated graph reference

## Tools Used

- **graphify** (REQUIRED) - Understanding code structure and dependencies
- Edit tool for applying transformations
- Language-specific parsers for validation

## Example

```bash
# Preview changes
/apply-refactor-rules --source-path ./src --rules-path ./rule.md --dry-run

# Apply refactoring
/apply-refactor-rules --source-path ./src --rules-path ./rule.md
```
