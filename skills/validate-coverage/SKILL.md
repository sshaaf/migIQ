---
name: validate-coverage
trigger: /validate-coverage
description: Validate test coverage meets requirements. Use when the user wants to check test coverage, ensure coverage thresholds, validate testing completeness, or verify coverage requirements are met.
---

Validate test coverage meets requirements.

## Parameters

- `--coverage-report` (required): Path to coverage report (XML, JSON, or HTML)
- `--source-path` (required): Path to source code
- `--threshold` (optional): Overall coverage threshold percentage (default: 80%)
- `--critical-threshold` (optional): Critical code coverage threshold (default: 90%)
- `--output` (optional): Path for validation report (default: ./coverage-validation.json)

## Description

Validates that test coverage meets thresholds, with special attention to critical code identified via Graphify. Ensures that high-impact classes have higher coverage requirements.

## Code Analysis Strategy

**Use Graphify to apply tiered coverage requirements:**

1. **Identify critical code (higher threshold):**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # God nodes must meet critical-threshold (90%+)
   ```

2. **Find all classes and their criticality:**
   ```bash
   jq '.nodes[] | {name: .name, degree: .degree}' graphify-out/graph.json
   # Degree determines coverage requirement tier
   ```

3. **Map coverage to classes:**
   ```bash
   /graphify query "Find all classes in package com.example"
   # Cross-reference with coverage report
   ```

4. **Check public API coverage:**
   ```bash
   /graphify query "Find all @RestController classes"
   /graphify query "Find all @Service classes"
   # Public APIs must have 100% coverage
   ```

5. **Identify coverage gaps:**
   ```bash
   # Classes in graph without corresponding coverage data
   # High-degree classes with below-threshold coverage
   ```

**Use Grep/Read only for:**
- Parsing coverage report files
- Reading threshold configuration
- Extracting coverage percentages

## Validation Rules

**Tiered coverage requirements based on graph criticality:**

1. **God Nodes** (degree ≥ 10):
   - Required coverage: `critical-threshold` (default 90%)
   - Justification: High impact, many dependents

2. **Hub Nodes** (degree 5-9):
   - Required coverage: 85%
   - Justification: Moderate impact

3. **Normal Nodes** (degree 2-4):
   - Required coverage: `threshold` (default 80%)
   - Justification: Standard requirement

4. **Leaf Nodes** (degree 0-1):
   - Required coverage: 70%
   - Justification: Low impact, fewer dependents

5. **Public APIs** (Controllers, Services):
   - Required coverage: 95%+
   - Justification: External contract, must be reliable

## Actions

1. Ensure Graphify graph exists
2. Parse coverage report
3. Extract node degrees from graph.json
4. Identify criticality tier for each class
5. For each class:
   - Get current coverage from report
   - Determine required coverage based on tier
   - Check if coverage meets requirement
6. Identify critical gaps:
   - God nodes below 90%
   - Public APIs below 95%
   - Any class below minimum threshold
7. Generate validation report
8. Return PASS/FAIL status

## Validation Report

```json
{
  "status": "FAIL",
  "overall_coverage": 82.5,
  "threshold": 80.0,
  "critical_threshold": 90.0,
  "by_tier": {
    "god_nodes": {"required": 90.0, "actual": 75.0, "status": "FAIL"},
    "hubs": {"required": 85.0, "actual": 88.0, "status": "PASS"},
    "normal": {"required": 80.0, "actual": 85.0, "status": "PASS"},
    "leaves": {"required": 70.0, "actual": 78.0, "status": "PASS"}
  },
  "critical_gaps": [
    {
      "class": "OrderService",
      "tier": "god_node",
      "degree": 15,
      "required": 90.0,
      "actual": 65.0,
      "gap": 25.0
    },
    {
      "class": "PaymentController",
      "tier": "public_api",
      "degree": 8,
      "required": 95.0,
      "actual": 80.0,
      "gap": 15.0
    }
  ],
  "recommendations": [
    "CRITICAL: OrderService is a god node (15 dependents) with only 65% coverage - needs 90%+",
    "Add integration tests for PaymentController to reach 95% coverage",
    "Overall status FAIL due to critical gaps"
  ]
}
```

## Returns

Validation report containing:
- Overall PASS/FAIL status
- Coverage by criticality tier
- Critical gaps (high-priority classes below threshold)
- Detailed recommendations
- List of all classes below their tier requirement

## Tools Used

- **graphify** (REQUIRED) - Criticality analysis and tiered thresholds
- Coverage parsers (JaCoCo XML, Cobertura, etc.)
- JSON/XML processing tools

## Example

```bash
# Validate coverage with defaults
/validate-coverage \
  --coverage-report ./target/site/jacoco/jacoco.xml \
  --source-path ./src/main/java

# With custom thresholds
/validate-coverage \
  --coverage-report ./coverage.json \
  --source-path ./src \
  --threshold 75 \
  --critical-threshold 95 \
  --output ./reports/coverage-validation.json
```

## Exit Codes

- `0` - PASS: All coverage requirements met
- `1` - FAIL: Critical gaps found (god nodes or public APIs below threshold)
- `2` - WARNING: Overall threshold met but some classes below tier requirements
