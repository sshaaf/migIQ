---
name: generate-characterization-tests
trigger: /generate-characterization-tests
description: Generate characterization tests to capture current behavior. Use when the user wants to create safety net tests, capture existing behavior, establish regression detection, or document current functionality through tests.
---

Generate characterization tests to capture current behavior.

## Parameters

- `--source-path` (required): Path to source code to test
- `--output` (optional): Path for generated test files (default: ./tests/characterization/)
- `--test-framework` (optional): Test framework to use (junit, testng, default: auto-detect)
- `--coverage-target` (optional): Target coverage percentage (default: 80%)

## Description

Generates characterization tests that capture existing behavior of the codebase. These tests act as a safety net during migration, ensuring that refactoring doesn't break functionality.

Uses Graphify to understand code structure, dependencies, and critical paths that need test coverage.

## Code Analysis Strategy

**Use Graphify to identify what needs testing:**

1. **Find critical classes (high-degree nodes):**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # Look for "God Nodes" - these are critical and need comprehensive tests
   ```

2. **Identify public APIs to test:**
   ```bash
   /mig-graphify query "Find all public classes"
   /mig-graphify query "Find all classes with @Service annotation"
   /mig-graphify query "Find all classes with @RestController annotation"
   # Public APIs are the surface area that needs characterization
   ```

3. **Find dependency chains to cover:**
   ```bash
   /mig-graphify path "ServiceClass" "RepositoryClass"
   # Understand call paths to ensure integration tests cover flows
   ```

4. **Identify untested areas:**
   ```bash
   /mig-graphify query "Find all classes in package com.example.core"
   # Cross-reference with existing tests to find gaps
   ```

5. **Find complex classes (need more tests):**
   ```bash
   # Classes with high degree in GRAPH_REPORT.md need thorough testing
   ```

**Use Grep/Read only for:**
- Reading actual method implementations to capture behavior
- Analyzing existing tests to avoid duplication
- Understanding method signatures for test generation

**Performance Target:** <5 file reads per class tested

## Actions

1. Ensure Graphify graph exists
2. Identify critical classes via GRAPH_REPORT.md (god nodes)
3. Query graph for public APIs and service classes
4. Analyze dependency paths to plan integration tests
5. For each class to test:
   - Read actual implementation (only when necessary)
   - Generate tests that capture current behavior
   - Include dependency mocking based on graph
6. Generate test files in output directory
7. Generate coverage report showing what's characterized

## Test Generation Strategy

- **God nodes** → Comprehensive test suites (high priority)
- **Service/Controller classes** → API contract tests
- **Leaf nodes** → Unit tests
- **Integration paths** → End-to-end flow tests based on graph paths

## Returns

Test suite containing:
- Unit tests for critical classes
- Integration tests for key dependency paths
- Mock setups based on actual dependencies from graph
- Coverage report showing characterized vs. total code
- Test execution report

## Tools Used

- **graphify** (REQUIRED) - Identifying critical code and dependencies
- Test framework (JUnit/TestNG/etc.)
- Mocking frameworks (Mockito/EasyMock/etc.)
- Coverage tools (JaCoCo/Cobertura/etc.)

## Example

```bash
# Generate characterization tests
/generate-characterization-tests --source-path ./src/main/java

# With custom output and framework
/generate-characterization-tests \
  --source-path ./src/main/java \
  --output ./tests/characterization \
  --test-framework junit \
  --coverage-target 85
```
