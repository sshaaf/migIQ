## ADDED Requirements

### Requirement: Support .env.test configuration file
The system SHALL support loading test configuration from .env.test file separate from production .env.

#### Scenario: Load .env.test for integration tests
- **WHEN** integration test runs
- **THEN** system MUST load configuration from .env.test

#### Scenario: .env.test does not affect production
- **WHEN** .env.test exists
- **THEN** production code MUST NOT load .env.test

#### Scenario: .env.test not found handled gracefully
- **WHEN** .env.test is missing
- **THEN** test MUST provide helpful error message with setup instructions

### Requirement: Provide .env.test.example template
The system SHALL provide .env.test.example file documenting test configuration.

#### Scenario: Template exists in repository
- **WHEN** user clones repository
- **THEN** .env.test.example MUST be present

#### Scenario: Template documents all test variables
- **WHEN** viewing .env.test.example
- **THEN** file MUST include all variables needed for integration testing

#### Scenario: Template includes setup instructions
- **WHEN** viewing .env.test.example
- **THEN** file MUST include comments explaining how to configure for testing

### Requirement: Prevent committing test credentials
The system SHALL ensure .env.test is not committed to version control.

#### Scenario: .env.test in .gitignore
- **WHEN** .env.test is created
- **THEN** git MUST ignore it per .gitignore

#### Scenario: .env.test.example is tracked
- **WHEN** .env.test.example exists
- **THEN** git MUST track it for documentation

### Requirement: Test configuration uses safe defaults
The system SHALL provide safe default values for test configuration where possible.

#### Scenario: Default to creating temporary project
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER not set in .env.test
- **THEN** test MUST create temporary project and delete after

#### Scenario: Warn about existing project number
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER is set in .env.test
- **THEN** test MUST warn before modifying existing project

### Requirement: Validate test configuration before running
The system SHALL validate test configuration has required fields.

#### Scenario: Check required GitHub fields
- **WHEN** test starts
- **THEN** system MUST validate TRACKER_GITHUB_TOKEN and TRACKER_GITHUB_ORGANIZATION are set

#### Scenario: Helpful error for missing fields
- **WHEN** required field is missing
- **THEN** error message MUST indicate which field and suggest fixing .env.test
