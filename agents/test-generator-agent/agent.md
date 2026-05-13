---
name: test-generator-agent
type: harness
model: claude-sonnet-4-6
description: Generate characterization and functional tests
---

# Test Generator Agent

## Purpose

Generate characterization and functional tests using Graphify-driven analysis to identify critical code and test priorities.

## Skills Used

- `/generate-characterization-tests` - Uses Graphify to identify critical classes
- `/generate-functional-tests` - Uses Graphify to map specs to code
- `/validate-coverage` - Uses Graphify for tiered coverage validation
- `/calculate-test-scores` - Uses Graphify to weight scores by criticality

## Code Analysis Strategy

**CRITICAL:** All test generation is driven by Graphify analysis. The graph MUST exist before this agent runs.

### Test Prioritization via Graphify

1. **Identify critical code requiring tests (God Nodes):**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # God nodes (degree ≥ 10) = highest test priority
   # These classes need comprehensive characterization tests
   ```

2. **Find public APIs (must be tested):**
   ```bash
   /graphify query "Find all @RestController classes"
   /graphify query "Find all @Service classes"
   # Public surface area needs functional tests
   ```

3. **Understand dependency flows for integration tests:**
   ```bash
   /graphify path "UserController" "UserRepository"
   # Map end-to-end flows to generate integration tests
   ```

4. **Identify test coverage gaps:**
   ```bash
   /graphify query "Find all classes in package com.example.core"
   # Cross-reference with existing tests to find untested code
   ```

5. **Determine mock requirements:**
   ```bash
   /graphify query "What does ServiceClass depend on?"
   # Know what dependencies need mocking in tests
   ```

6. **Calculate test quality weights:**
   ```bash
   jq '.nodes[] | {name: .name, degree: .degree}' graphify-out/graph.json
   # Node degree determines coverage requirements
   ```

### Test Generation Workflow

**For Characterization Tests:**
- God nodes (degree ≥ 10) → Comprehensive test suites (3× coverage weight)
- Hubs (degree 5-9) → Standard test coverage (2× weight)
- Normal (degree 2-4) → Basic test coverage (1× weight)
- Leaves (degree 0-1) → Minimal test coverage (0.5× weight)

**For Functional Tests:**
- Map spec requirements to implementation classes via graph
- Use graph paths to understand end-to-end flows
- Generate integration tests based on actual dependency chains

**For Coverage Validation:**
- God nodes must meet 90%+ coverage
- Public APIs must meet 95%+ coverage
- Other classes tiered by criticality (70-85%)

**Use Grep/Read only for:**
- Reading actual method implementations to capture behavior
- Analyzing existing tests to avoid duplication
- Understanding method signatures for test generation

**Performance Target:** <5 file reads per class tested

## Workflow

```
1. Verify Graphify graph exists (REQUIRED)
2. Analyze GRAPH_REPORT.md to identify critical code
3. Generate characterization tests (prioritized by node degree)
4. Generate functional tests (mapped via graph paths)
5. Validate coverage (tiered thresholds by criticality)
6. Calculate test scores (weighted by graph metrics)
7. Return comprehensive test suite
```

## Test Prioritization Strategy

Based on Graphify analysis:

**Priority 1 - God Nodes (degree ≥ 10):**
- Comprehensive characterization tests
- 90%+ coverage requirement
- High test quality standards

**Priority 2 - Public APIs (Controllers/Services):**
- Functional tests for all endpoints
- 95%+ coverage requirement
- Integration test coverage

**Priority 3 - Hubs (degree 5-9):**
- Standard test coverage
- 85%+ coverage requirement

**Priority 4 - Normal/Leaf nodes:**
- Basic test coverage
- 70-80% coverage requirement

This ensures testing effort is focused where it matters most.

## Configuration

```yaml
agent:
  name: test-generator-agent
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
