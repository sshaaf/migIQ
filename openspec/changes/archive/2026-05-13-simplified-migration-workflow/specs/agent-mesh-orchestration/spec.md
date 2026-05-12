# agent-mesh-orchestration Specification (Delta)

## ADDED Requirements

### Requirement: Accept natural language migration input
The story-orchestrator-agent SHALL accept natural language migration requests and auto-construct migration commands.

#### Scenario: Parse natural language and build context
- **WHEN** orchestrator receives natural language input like "Migrate this app to Quarkus"
- **THEN** orchestrator invokes parser to extract intent and detector to find project path

#### Scenario: Validate context before processing
- **WHEN** migration context is built from natural language
- **THEN** orchestrator validates project exists and intent is clear before starting harness workflow

#### Scenario: Auto-run migration command
- **WHEN** context is validated
- **THEN** orchestrator automatically executes equivalent of /migration command without user having to type explicit flags

#### Scenario: Fallback to explicit command mode
- **WHEN** natural language parsing fails or is ambiguous
- **THEN** orchestrator prompts user to use explicit /migration command or clarify intent

### Requirement: Display migration context confirmation
The orchestrator SHALL display the detected migration context for user confirmation before proceeding.

#### Scenario: Show auto-detected parameters
- **WHEN** migration context is built from natural language
- **THEN** orchestrator displays: project path, migration type, target framework, and asks for confirmation

#### Scenario: Allow user to proceed or abort
- **WHEN** confirmation prompt is shown
- **THEN** user can confirm to proceed, or abort to modify parameters

#### Scenario: Skip confirmation in autonomous mode
- **WHEN** system is running in autonomous mode (MODE=autonomous)
- **THEN** orchestrator skips confirmation and proceeds directly
