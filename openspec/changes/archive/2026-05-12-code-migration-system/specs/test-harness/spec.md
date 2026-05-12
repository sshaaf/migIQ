## ADDED Requirements

### Requirement: Generate characterization tests
The system SHALL generate characterization tests that capture current code behavior using opencode agent.

#### Scenario: Capture current behavior
- **WHEN** test-generator-agent invokes `/generate-characterization-tests` with source path
- **THEN** system generates tests that lock in existing functionality and behavior

#### Scenario: Achieve coverage target
- **WHEN** initial tests have insufficient coverage
- **THEN** system iteratively generates additional tests until coverage target met

### Requirement: Generate functional tests
The system SHALL generate functional tests for expected post-migration behavior using opencode agent based on specifications.

#### Scenario: Generate from specifications
- **WHEN** test-generator-agent invokes `/generate-functional-tests` with spec path
- **THEN** system generates functional test cases that validate expected behavior after migration

#### Scenario: Include edge cases
- **WHEN** generating functional tests
- **THEN** system includes edge cases and error scenarios based on specifications

### Requirement: Validate test coverage
The system SHALL validate that test coverage meets configured minimum threshold.

#### Scenario: Coverage meets threshold
- **WHEN** system invokes `/validate-coverage` and coverage >= minimum threshold
- **THEN** system returns PASS status with coverage report

#### Scenario: Coverage below threshold
- **WHEN** coverage < minimum threshold
- **THEN** system returns FAIL status with coverage gaps report

### Requirement: Package test suite
The test-generator-agent SHALL package generated tests with metadata for downstream harnesses.

#### Scenario: Package test artifacts
- **WHEN** all tests generated and validated
- **THEN** agent packages characterization tests, functional tests, coverage reports, and metadata into artifact bundle
