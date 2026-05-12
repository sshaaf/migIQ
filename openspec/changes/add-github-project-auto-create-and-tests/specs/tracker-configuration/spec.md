## ADDED Requirements

### Requirement: Support optional project number configuration
The system SHALL allow project_number to be optional for GitHub tracker configuration.

#### Scenario: Project number provided
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER is set
- **THEN** system MUST validate it is an integer

#### Scenario: Project number omitted
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER is not set
- **THEN** system MUST NOT raise validation error

#### Scenario: Project number None
- **WHEN** TRACKER_GITHUB_PROJECT_NUMBER is explicitly None
- **THEN** system MUST treat as omitted and allow auto-creation

### Requirement: Support project creation configuration
The system SHALL support configuration fields for project auto-creation.

#### Scenario: Project name configuration
- **WHEN** TRACKER_GITHUB_PROJECT_NAME is set
- **THEN** system MUST use that as project name

#### Scenario: Default project name
- **WHEN** TRACKER_GITHUB_PROJECT_NAME is not set
- **THEN** system MUST generate name from organization and timestamp

#### Scenario: Project description
- **WHEN** TRACKER_GITHUB_PROJECT_DESCRIPTION is set
- **THEN** system MUST include description in created project

### Requirement: Validate configuration for auto-creation
The system SHALL validate GitHub configuration has required fields for project creation.

#### Scenario: Token required for creation
- **WHEN** project auto-creation is triggered
- **THEN** TRACKER_GITHUB_TOKEN MUST be set

#### Scenario: Organization required for creation
- **WHEN** project auto-creation is triggered
- **THEN** TRACKER_GITHUB_ORGANIZATION MUST be set

#### Scenario: Token has project permissions
- **WHEN** validating GitHub config
- **THEN** system SHOULD warn if token lacks 'project' scope
