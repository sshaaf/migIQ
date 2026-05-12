# project-tracking-harness Specification

## Purpose
TBD - created by archiving change code-migration-system. Update Purpose after archive.
## Requirements
### Requirement: Analyze codebase for migration needs
The system SHALL analyze target codebase to identify migration requirements, dependencies, complexity, and generate structured analysis report.

#### Scenario: Successful codebase analysis
- **WHEN** user invokes `/analyze-codebase` with valid codebase path and migration type
- **THEN** system generates analysis report with codebase structure, dependencies, anti-patterns, and complexity score

#### Scenario: Incremental analysis
- **WHEN** user specifies incremental scope instead of full analysis
- **THEN** system analyzes only changed modules since last analysis

### Requirement: Plan migration from analysis
The system SHALL create migration plan from analysis report by applying rules from rule.md and generating prioritized user stories.

#### Scenario: Generate migration plan
- **WHEN** user invokes `/plan-migration` with analysis report and rule file
- **THEN** system generates migration plan with user stories, task breakdown, and priority ordering

#### Scenario: Apply prioritization strategy
- **WHEN** user specifies prioritization strategy (risk, complexity, or business-value)
- **THEN** system orders user stories according to selected strategy

### Requirement: Generate and maintain Kanban backlog
The system SHALL generate Kanban tickets from user stories and maintain synchronization between tasks.md and Kanban board.

#### Scenario: Create Kanban tickets
- **WHEN** user invokes `/generate-backlog` with user stories
- **THEN** system creates tickets on Kanban board with labels, priorities, and dependencies

#### Scenario: Update ticket status
- **WHEN** story status changes in workflow
- **THEN** system updates corresponding Kanban ticket status automatically

### Requirement: Loop through user stories
The project-tracker-agent SHALL continuously process user stories from backlog until complete or human intervention required.

#### Scenario: Process story from backlog
- **WHEN** agent selects next story from backlog
- **THEN** agent invokes story-orchestrator-agent with story context and monitors progress

#### Scenario: Handle story completion
- **WHEN** story completes successfully
- **THEN** agent updates tasks.md, moves Kanban ticket to Done, and processes next story

#### Scenario: Handle story failure
- **WHEN** story fails after retries
- **THEN** agent generates KPI metrics, requests root cause analysis, and returns story to backlog

## ADDED Requirements

### Requirement: Load configuration from .env file on startup
The system SHALL load .env file when ProjectTrackerAgent initializes.

#### Scenario: .env exists in project root
- **WHEN** ProjectTrackerAgent is initialized
- **THEN** system MUST call load_dotenv() before loading configuration

#### Scenario: .env does not exist
- **WHEN** ProjectTrackerAgent is initialized without .env file
- **THEN** system MUST continue without error using system env vars

### Requirement: Merge environment and context configuration
The system SHALL merge configuration from environment variables and JSON context.

#### Scenario: Tracker in env, other config in context
- **WHEN** tracker config in environment but sessionId in context
- **THEN** system MUST use tracker from env and sessionId from context

#### Scenario: Complete config in env
- **WHEN** all configuration in environment variables
- **THEN** system MUST build config entirely from environment

#### Scenario: Complete config in context
- **WHEN** complete context JSON provided
- **THEN** system MUST use context and ignore environment

### Requirement: Log configuration source
The system SHALL log where configuration was loaded from.

#### Scenario: Config from environment
- **WHEN** configuration loaded from environment variables
- **THEN** system MUST log "Configuration loaded from environment"

#### Scenario: Config from context
- **WHEN** configuration loaded from JSON context
- **THEN** system MUST log "Configuration loaded from context"

#### Scenario: Config from mixed sources
- **WHEN** configuration loaded from both sources
- **THEN** system MUST log "Configuration merged from environment and context"

### Requirement: Validate .env.example exists
The system SHALL check for .env.example and warn if .env is missing.

#### Scenario: .env.example exists but .env missing
- **WHEN** .env.example exists but .env file missing
- **THEN** system MUST print helpful message referencing .env.example

#### Scenario: Neither file exists
- **WHEN** neither .env nor .env.example exists
- **THEN** system MUST continue without warning

### Requirement: Support environment-specific .env files
The system SHALL support loading .env.local for local overrides.

#### Scenario: Both .env and .env.local exist
- **WHEN** both files are present
- **THEN** system MUST load .env first then .env.local (override)

#### Scenario: Only .env.local exists
- **WHEN** only .env.local exists
- **THEN** system MUST load .env.local

### Requirement: Maintain backward compatibility
The system SHALL maintain full backward compatibility with existing context-based configuration.

#### Scenario: Legacy context-only usage
- **WHEN** no environment variables or .env file present
- **THEN** system MUST work exactly as before with context JSON

#### Scenario: Existing scripts unchanged
- **WHEN** existing invocation scripts use --context argument
- **THEN** system MUST work without requiring .env file
