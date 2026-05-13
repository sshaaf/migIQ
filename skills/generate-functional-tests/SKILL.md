---
name: generate-functional-tests
trigger: /generate-functional-tests
description: Generate functional tests for migrated code. Use when the user wants to create functional tests, validate migrated functionality, test business logic, or verify feature correctness after migration.
---

Generate functional tests for migrated code.

## Parameters

- `--spec-path` (required): Path to specification file (user story, requirements doc)
- `--source-path` (required): Path to source code under test
- `--output` (optional): Path for generated test files (default: ./tests/functional/)
- `--test-framework` (optional): Test framework to use (junit, testng, default: auto-detect)

## Description

Generates functional tests based on specifications to validate that migrated code meets requirements. Uses Graphify to understand code structure and ensure tests cover the right functionality.

## Code Analysis Strategy

**Use Graphify to map specs to code:**

1. **Find classes that implement the spec:**
   ```bash
   /mig-graphify query "Find all classes with @RestController annotation"
   /mig-graphify query "Find all classes with @Service annotation"
   # Match spec requirements to actual implementation classes
   ```

2. **Understand end-to-end flows:**
   ```bash
   /mig-graphify path "UserController" "UserRepository"
   # Map entire flow from API to data layer
   ```

3. **Identify dependencies for test setup:**
   ```bash
   /mig-graphify query "What does UserService depend on?"
   # Know what mocks/stubs are needed
   ```

4. **Find similar existing tests:**
   ```bash
   /mig-graphify query "Find all test classes"
   # Learn patterns from existing tests
   ```

5. **Check for integration points:**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # Identify module boundaries for integration test scope
   ```

**Use Grep/Read only for:**
- Reading spec details for test case generation
- Reading actual method signatures
- Analyzing existing test patterns
- Understanding business logic implementation

**Performance Target:** <10 file reads per functional test suite

## Actions

1. Ensure Graphify graph exists
2. Parse specification file for requirements
3. Use graph to map requirements to implementation classes
4. For each requirement:
   - Query graph to find implementing classes
   - Identify dependency path from entry point to exit point
   - Determine test scope (unit vs integration)
5. Generate test cases:
   - Happy path tests
   - Error condition tests
   - Edge case tests
   - Integration tests for end-to-end flows
6. Generate test data and fixtures based on graph understanding
7. Write tests to output directory
8. Generate test execution report

## Test Coverage Strategy

Based on graph analysis:
- **Entry points** (Controllers/APIs) → Full request/response tests
- **Business logic** (Services) → Behavior verification tests
- **Integration paths** → End-to-end scenario tests from graph paths
- **Data layer** (Repositories) → Data validation tests

## Returns

Functional test suite containing:
- Happy path tests for all spec requirements
- Error condition and edge case tests
- Integration tests for complete flows
- Test data fixtures
- Test execution report
- Coverage mapping (spec requirement → test cases)

## Tools Used

- **graphify** (REQUIRED) - Mapping specs to code, understanding flows
- Test framework (JUnit/TestNG/etc.)
- Test data generation tools
- API testing tools (RestAssured/MockMvc/etc.)
- Assertion libraries

## Example

```bash
# Generate functional tests from spec
/generate-functional-tests \
  --spec-path ./specs/user-registration.md \
  --source-path ./src/main/java

# With custom output
/generate-functional-tests \
  --spec-path ./specs/api-requirements.yaml \
  --source-path ./src \
  --output ./tests/functional \
  --test-framework junit
```
