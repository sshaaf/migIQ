## ADDED Requirements

### Requirement: Provide .env.example template file
The system SHALL provide a .env.example file in the project root with all available configuration options.

#### Scenario: File exists in project root
- **WHEN** user clones repository
- **THEN** .env.example file MUST be present in root directory

#### Scenario: File is tracked in git
- **WHEN** .env.example is committed to repository
- **THEN** git MUST track the file for version control

### Requirement: Document all configuration variables
The system SHALL document all available environment variables in .env.example.

#### Scenario: Tracker configuration variables
- **WHEN** .env.example is opened
- **THEN** file MUST include TRACKER_TYPE, TRACKER_GITHUB_*, and TRACKER_LOCAL_* variables

#### Scenario: Agent configuration variables
- **WHEN** .env.example is opened
- **THEN** file MUST include variables for all configurable agents

#### Scenario: System configuration variables
- **WHEN** .env.example is opened
- **THEN** file MUST include SESSION_ID, MODE, and other system variables

### Requirement: Use comments to explain each variable
The system SHALL provide inline comments explaining purpose and valid values for each variable.

#### Scenario: Variable with comment
- **WHEN** viewing configuration variable in .env.example
- **THEN** variable MUST have comment explaining its purpose

#### Scenario: Valid values documented
- **WHEN** variable has limited valid values
- **THEN** comment MUST list valid options

#### Scenario: Example values provided
- **WHEN** variable requires specific format
- **THEN** comment MUST include example value

### Requirement: Comment out sensitive variables
The system SHALL comment out variables containing credentials or tokens by default.

#### Scenario: GitHub token commented
- **WHEN** .env.example contains TRACKER_GITHUB_TOKEN
- **THEN** line MUST be commented with # prefix

#### Scenario: API keys commented
- **WHEN** .env.example contains API keys
- **THEN** lines MUST be commented with # prefix

### Requirement: Group variables by component
The system SHALL organize variables into logical groups with section headers.

#### Scenario: Tracker section
- **WHEN** viewing .env.example
- **THEN** tracker variables MUST be under "# Tracker Configuration" header

#### Scenario: Agent sections
- **WHEN** viewing .env.example
- **THEN** each agent's variables MUST be under dedicated section header

#### Scenario: General section
- **WHEN** viewing .env.example
- **THEN** general variables MUST be under "# General Configuration" header

### Requirement: Provide safe default values
The system SHALL provide safe, non-sensitive default values where applicable.

#### Scenario: Tracker type default
- **WHEN** no .env file is created
- **THEN** .env.example MUST show TRACKER_TYPE=local as default

#### Scenario: Mode default
- **WHEN** no .env file is created
- **THEN** .env.example MUST show MODE=interactive as default

#### Scenario: No credentials in defaults
- **WHEN** viewing .env.example defaults
- **THEN** file MUST NOT contain actual credentials

### Requirement: Include setup instructions
The system SHALL include brief setup instructions at the top of .env.example.

#### Scenario: Copy instructions
- **WHEN** viewing .env.example header
- **THEN** file MUST include instruction to copy to .env

#### Scenario: Customization guidance
- **WHEN** viewing .env.example header
- **THEN** file MUST include guidance to customize values

#### Scenario: Security warning
- **WHEN** viewing .env.example header
- **THEN** file MUST warn never to commit .env file
