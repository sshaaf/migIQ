# migration-context-builder Specification

## Purpose
Build a complete migration context object from auto-detected project information and parsed natural language intent, creating the internal command structure needed by the orchestrator.

## ADDED Requirements

### Requirement: Build migration context from inputs
The system SHALL combine auto-detected project data and parsed intent into a structured migration context.

#### Scenario: Simple framework migration context
- **WHEN** user says "Migrate to Quarkus" and project is detected at ./my-app
- **THEN** system builds context with: {project_path: "./my-app", migration_type: "framework", target: "Quarkus"}

#### Scenario: Include project metadata
- **WHEN** building migration context
- **THEN** context includes project name, build system, dependencies, source directories

#### Scenario: Preserve user overrides
- **WHEN** user explicitly provides --project-path flag
- **THEN** context uses user-specified path instead of auto-detected path

### Requirement: Generate equivalent /migration command
The system SHALL generate the equivalent explicit /migration command that would produce the same result.

#### Scenario: Display equivalent command
- **WHEN** migration context is built
- **THEN** system displays: "Running: /migration --project-path ./my-app --migration-type framework --target Quarkus"

#### Scenario: Log command for reproducibility
- **WHEN** migration starts
- **THEN** system logs the equivalent command for future reference and debugging

### Requirement: Validate complete migration context
The system SHALL validate that the migration context has all required fields before proceeding.

#### Scenario: Complete context validation
- **WHEN** context has project_path, migration_type, and required parameters
- **THEN** system proceeds to orchestrator

#### Scenario: Missing required fields
- **WHEN** context is missing required fields (e.g., no target framework specified)
- **THEN** system returns error listing missing fields

### Requirement: Enrich context with project analysis
The system SHALL analyze the source project and add relevant metadata to the context.

#### Scenario: Detect current framework
- **WHEN** analyzing Java EE project
- **THEN** context includes current_framework: "Java EE", current_version: "8", detected_dependencies: [...]

#### Scenario: Identify migration scope
- **WHEN** analyzing project structure
- **THEN** context includes estimated migration scope (number of files, modules, dependencies to update)

#### Scenario: Flag potential issues
- **WHEN** detecting incompatible patterns or deprecated APIs
- **THEN** context includes warnings list for user review
