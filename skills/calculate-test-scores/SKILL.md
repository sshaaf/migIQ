---
name: calculate-test-scores
description: Calculate test coverage and quality scores. Use when the user wants to measure test quality, calculate coverage metrics, assess test effectiveness, or evaluate testing completeness.
---

Calculate test coverage and quality scores.

## Parameters

- `--test-results` (required): Path to test results file (JUnit XML, coverage JSON, etc.)
- `--source-path` (required): Path to source code
- `--weights` (optional): Path to scoring weights config (JSON)
- `--output` (optional): Path for score report (default: ./test-score-report.json)

## Description

Calculates comprehensive test quality scores by analyzing test coverage, test effectiveness, and critical code coverage. Uses Graphify to weight scores based on code criticality.

## Code Analysis Strategy

**Use Graphify to weight coverage by criticality:**

1. **Identify critical code (should have high coverage):**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # God nodes = critical, need high coverage weight
   ```

2. **Find public APIs (must be tested):**
   ```bash
   /graphify query "Find all public classes"
   /graphify query "Find all @RestController classes"
   # Public surface area needs 100% coverage
   ```

3. **Identify dependency hubs:**
   ```bash
   # High-degree nodes in graph = high impact
   # Missing tests here = higher penalty in score
   ```

4. **Find tested vs untested classes:**
   ```bash
   /graphify query "Find all classes in package X"
   # Cross-reference with coverage report
   ```

5. **Calculate risk-weighted coverage:**
   ```bash
   # God node with 50% coverage = worse than leaf node with 50% coverage
   # Use node degree from graph to weight the score
   ```

**Use Grep/Read only for:**
- Parsing test result files
- Reading coverage reports
- Extracting test metrics

## Scoring Algorithm

Calculates weighted score based on:

1. **Critical Code Coverage (40%):**
   - God nodes (high-degree) coverage: weight × coverage %
   - Public APIs coverage: weight × coverage %
   - Integration paths coverage: weight × coverage %

2. **Test Quality (30%):**
   - Test pass rate
   - Assertion density (assertions per test)
   - Test isolation (mocking ratio)

3. **Breadth Coverage (20%):**
   - Package coverage
   - Class coverage
   - Method coverage

4. **Depth Coverage (10%):**
   - Branch coverage
   - Condition coverage
   - Path coverage

**Graph-based weighting:**
- Node degree 10+ (god nodes) → 3× weight
- Node degree 5-9 (hubs) → 2× weight
- Node degree 1-4 (normal) → 1× weight
- Node degree 0 (leaf) → 0.5× weight

## Actions

1. Ensure Graphify graph exists
2. Parse test results and coverage reports
3. Extract node degrees from graph.json
4. Identify critical classes from GRAPH_REPORT.md
5. Cross-reference tested vs untested classes using graph
6. Calculate coverage for each criticality tier:
   - God nodes coverage
   - Hubs coverage
   - Normal nodes coverage
   - Leaf nodes coverage
7. Calculate test quality metrics
8. Compute weighted final score (0-100)
9. Generate detailed score report with recommendations

## Returns

Test score report containing:
- Overall weighted score (0-100)
- Coverage by criticality tier
- Critical gaps (high-degree nodes with low coverage)
- Test quality metrics
- Recommendations for improvement
- Pass/Fail status based on threshold

## Tools Used

- **graphify** (REQUIRED) - Code criticality analysis and weighting
- Coverage parsers (JaCoCo, Cobertura, etc.)
- Test result parsers (JUnit, TestNG, etc.)
- Statistical analysis tools

## Example

```bash
# Calculate test scores
/calculate-test-scores \
  --test-results ./target/test-results.xml \
  --source-path ./src/main/java

# With custom weights
/calculate-test-scores \
  --test-results ./coverage.json \
  --source-path ./src \
  --weights ./test-weights.json \
  --output ./reports/test-score.json
```

## Sample Output

```json
{
  "overall_score": 78.5,
  "critical_coverage": {
    "god_nodes": 85.0,
    "hubs": 75.0,
    "normal": 80.0,
    "leaves": 65.0
  },
  "test_quality": {
    "pass_rate": 98.5,
    "assertion_density": 4.2,
    "isolation_score": 85.0
  },
  "critical_gaps": [
    {"class": "OrderService", "degree": 15, "coverage": 45.0},
    {"class": "PaymentProcessor", "degree": 12, "coverage": 60.0}
  ],
  "recommendations": [
    "Increase coverage for god node OrderService (currently 45%, target 90%)",
    "Add integration tests for high-degree classes"
  ],
  "status": "PASS"
}
```
