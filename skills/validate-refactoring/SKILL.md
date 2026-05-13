---
name: validate-refactoring
description: Validate refactoring preserves behavior. Use when the user wants to verify refactoring correctness, ensure behavior preservation, validate transformation accuracy, or confirm refactoring doesn't break functionality.
---

Validate refactored code preserves behavior.

## Parameters

- `--source-path` (required): Path to refactored code
- `--test-results` (required): Path to test results JSON
- `--baseline-graph` (optional): Path to baseline graph.json (pre-refactoring)
- `--output` (optional): Path for validation report (default: ./validation-report.json)

## Description

Validates that refactoring preserves behavior by comparing:
- Test results (before vs after)
- Dependency structure (via Graphify graph comparison)
- Public API surface
- Performance characteristics

## Code Analysis Strategy

**Use Graphify to validate structural integrity:**

1. **Compare dependency graphs:**
   ```bash
   # Compare baseline graph (pre-refactor) with current graph (post-refactor)
   diff <(jq -S '.edges | sort' baseline-graph.json) \
        <(jq -S '.edges | sort' graphify-out/graph.json)
   # Key dependencies should be preserved
   ```

2. **Check for broken dependencies:**
   ```bash
   /graphify query "Find all classes that depend on RefactoredClass"
   # Ensure dependents still work
   ```

3. **Validate public API preservation:**
   ```bash
   /graphify query "Show public methods of RefactoredClass"
   # Compare with baseline - public API should be unchanged
   ```

4. **Check for new dependencies (code smells):**
   ```bash
   # If refactoring introduced new dependencies, flag as potential issue
   jq '.edges | length' baseline-graph.json
   jq '.edges | length' graphify-out/graph.json
   # Edge count should stay same or decrease
   ```

5. **Validate package structure:**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # Check that refactoring didn't break module boundaries
   ```

## Actions

1. Load test results (before and after refactoring)
2. Compare Graphify graphs (baseline vs current)
3. Check dependency preservation
4. Validate public API unchanged
5. Check for new unwanted dependencies
6. Compare test coverage
7. Validate performance metrics
8. Generate validation report

## Validation Checks

- ✅ All tests pass (same or better than baseline)
- ✅ Test coverage maintained or improved
- ✅ Public API preserved (no breaking changes)
- ✅ Key dependencies preserved
- ✅ No new circular dependencies
- ✅ Module boundaries respected
- ✅ Performance maintained or improved
- ✅ No new god classes or god nodes

## Returns

Validation report containing:
- Test comparison (pass/fail, coverage delta)
- Dependency analysis (preserved, added, removed)
- API compatibility check
- Structural integrity assessment
- Performance comparison
- Overall validation status (PASS/FAIL)

## Tools Used

- **graphify** (REQUIRED) - Structural validation via graph comparison
- Test result parsers
- Diff tools for comparison
- Performance metrics tools

## Example

```bash
# Validate refactoring
/validate-refactoring \
  --source-path ./src \
  --test-results ./test-results.json \
  --baseline-graph ./baseline/graph.json

# With custom output
/validate-refactoring \
  --source-path ./src \
  --test-results ./test-results.json \
  --output ./reports/validation.json
```
