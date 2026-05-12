## ADDED Requirements

### Requirement: Test configuration must include project name
The integration test system SHALL require TRACKER_GITHUB_PROJECT_NAME to be set in .env.test before test execution.

#### Scenario: Project name is set in .env.test
- **WHEN** .env.test contains TRACKER_GITHUB_PROJECT_NAME with a non-empty value
- **THEN** validation MUST pass and tests MUST proceed with configured project name

#### Scenario: Project name is missing from .env.test
- **WHEN** .env.test does not contain TRACKER_GITHUB_PROJECT_NAME variable
- **THEN** validation MUST fail with error message explaining TRACKER_GITHUB_PROJECT_NAME is required

#### Scenario: Project name is empty in .env.test
- **WHEN** .env.test contains TRACKER_GITHUB_PROJECT_NAME with empty value
- **THEN** validation MUST fail with error message explaining project name cannot be empty

#### Scenario: Project name is placeholder value
- **WHEN** .env.test contains TRACKER_GITHUB_PROJECT_NAME with placeholder like "your-project-name"
- **THEN** validation SHOULD warn that placeholder value should be replaced with actual project name

### Requirement: Validation must fail fast before GitHub API calls
The system SHALL validate test configuration before making any GitHub API calls.

#### Scenario: Validation runs before project creation
- **WHEN** integration test starts
- **THEN** configuration validation MUST run before calling GitHub API

#### Scenario: Validation failure prevents test execution
- **WHEN** configuration validation fails
- **THEN** test MUST exit with non-zero status code without creating any GitHub resources

#### Scenario: Clear error message on validation failure
- **WHEN** validation fails due to missing project name
- **THEN** error message MUST include:
  - Which field is missing (TRACKER_GITHUB_PROJECT_NAME)
  - Where to set it (.env.test file)
  - Example value or link to documentation

### Requirement: Auto-generation fallback must be removed
The system SHALL NOT auto-generate project names for integration tests.

#### Scenario: No project name triggers validation error
- **WHEN** TRACKER_GITHUB_PROJECT_NAME is not set
- **THEN** system MUST fail validation rather than auto-generating a project name

#### Scenario: Generate test project name function is not called
- **WHEN** test executes with valid project name
- **THEN** generate_test_project_name() function MUST NOT be called

### Requirement: Makefile validation must check project name
The Makefile env-check target SHALL validate TRACKER_GITHUB_PROJECT_NAME is configured.

#### Scenario: make env-check validates project name
- **WHEN** user runs make env-check
- **THEN** command MUST verify TRACKER_GITHUB_PROJECT_NAME is set in .env.test

#### Scenario: make env-check fails on missing project name
- **WHEN** make env-check runs and TRACKER_GITHUB_PROJECT_NAME is not set
- **THEN** command MUST exit with non-zero status and display error message

#### Scenario: make test-integration depends on validation
- **WHEN** user runs make test-integration
- **THEN** env-check validation MUST run before executing tests

### Requirement: Documentation must reflect required field
Test documentation SHALL clearly indicate TRACKER_GITHUB_PROJECT_NAME is required, not optional.

#### Scenario: .env.test.example marks field as required
- **WHEN** viewing .env.test.example
- **THEN** TRACKER_GITHUB_PROJECT_NAME MUST be marked as required with uncommented example value

#### Scenario: README.md documents required field
- **WHEN** reading integration test section in README.md
- **THEN** documentation MUST state TRACKER_GITHUB_PROJECT_NAME is required

#### Scenario: TESTING.md includes project name requirement
- **WHEN** reading test configuration in TESTING.md
- **THEN** TRACKER_GITHUB_PROJECT_NAME MUST be listed in required variables section

#### Scenario: SETUP_TESTING.md includes project name in setup steps
- **WHEN** following setup guide in SETUP_TESTING.md
- **THEN** setting TRACKER_GITHUB_PROJECT_NAME MUST be included as required step
