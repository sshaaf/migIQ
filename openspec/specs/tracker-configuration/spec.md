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
## ADDED Requirements

### Requirement: Load tracker configuration from environment variables
The system SHALL load tracker configuration from environment variables as primary source.

#### Scenario: Load tracker type from env
- **WHEN** TRACKER_TYPE environment variable is set
- **THEN** system MUST use that value for tracker type

#### Scenario: Load GitHub config from env
- **WHEN** TRACKER_GITHUB_* variables are set
- **THEN** system MUST construct GitHub tracker config from those variables

#### Scenario: Load local config from env
- **WHEN** TRACKER_LOCAL_TASKS_PATH is set
- **THEN** system MUST use that path for local tracker

### Requirement: Fallback to JSON context configuration
The system SHALL fall back to JSON context configuration when environment variables are not set.

#### Scenario: No env vars, context provided
- **WHEN** no TRACKER_* environment variables are set
- **THEN** system MUST use tracker config from context dictionary

#### Scenario: Partial env vars
- **WHEN** some TRACKER_* variables are set but incomplete
- **THEN** system MUST merge env vars with context defaults

### Requirement: Prioritize explicit context over environment
The system SHALL give highest priority to explicit JSON context configuration.

#### Scenario: Both context and env vars present
- **WHEN** tracker config exists in both context and environment
- **THEN** system MUST use context configuration

#### Scenario: Context explicitly set to None
- **WHEN** context tracker is explicitly None or missing
- **THEN** system MUST use environment variable configuration

### Requirement: Validate environment variable configuration
The system SHALL validate configuration loaded from environment variables.

#### Scenario: Missing required GitHub fields
- **WHEN** TRACKER_TYPE=github but TRACKER_GITHUB_TOKEN missing
- **THEN** system MUST raise ConfigurationError with helpful message

#### Scenario: Invalid tracker type
- **WHEN** TRACKER_TYPE has unsupported value
- **THEN** system MUST fall back to local with warning

### Requirement: Support all existing tracker types from environment
The system SHALL support configuring local, GitHub, GitLab, and Jira trackers via environment variables.

#### Scenario: Local tracker from env
- **WHEN** TRACKER_TYPE=local
- **THEN** system MUST create LocalTracker with env config

#### Scenario: GitHub tracker from env
- **WHEN** TRACKER_TYPE=github with valid config
- **THEN** system MUST create GitHubProjectsTracker with env config

#### Scenario: Unsupported tracker from env
- **WHEN** TRACKER_TYPE=gitlab or jira
- **THEN** system MUST log warning and fall back to local

### Requirement: Resolve nested environment variable references
The system SHALL resolve $VAR references in environment variable values.

#### Scenario: Token references another env var
- **WHEN** TRACKER_GITHUB_TOKEN=$GITHUB_TOKEN
- **THEN** system MUST resolve to value of GITHUB_TOKEN

#### Scenario: Recursive resolution
- **WHEN** VAR1=$VAR2 and VAR2=value
- **THEN** system MUST resolve VAR1 to "value"

#### Scenario: Missing referenced var
- **WHEN** TRACKER_GITHUB_TOKEN=$MISSING_VAR
- **THEN** system MUST raise ConfigurationError
