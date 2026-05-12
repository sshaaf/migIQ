# skills-framework Specification

## Purpose
TBD - created by archiving change code-migration-system. Update Purpose after archive.
## Requirements
### Requirement: Define skill interface
All skills SHALL follow standard interface with parameters, actions, outputs, and tools.

#### Scenario: Skill invocation by agent
- **WHEN** agent invokes skill with valid parameters
- **THEN** skill executes actions and returns outputs with status

#### Scenario: Skill invocation by user
- **WHEN** user invokes skill directly via command line
- **THEN** skill executes with same behavior as agent invocation

### Requirement: Implement 19 specialized skills
The system SHALL provide 19 skills across all harness phases (3 project tracking, 3 test, 3 code, 3 benchmark, 3 evaluation, 4 CI, 3 cross-cutting).

#### Scenario: Project tracking skills
- **WHEN** project-tracker-agent needs to analyze, plan, or generate backlog
- **THEN** skills `/analyze-codebase`, `/plan-migration`, `/generate-backlog` are available

#### Scenario: Test harness skills
- **WHEN** test-generator-agent needs to generate tests or validate coverage
- **THEN** skills `/generate-characterization-tests`, `/generate-functional-tests`, `/validate-coverage` are available

#### Scenario: Code harness skills
- **WHEN** code-refactor-agent needs to refactor or generate code
- **THEN** skills `/apply-refactor-rules`, `/generate-spec-driven-code`, `/validate-refactoring` are available

#### Scenario: Cross-cutting skills
- **WHEN** any agent needs KPI metrics, documentation updates, or root cause analysis
- **THEN** skills `/generate-kpi-metrics`, `/update-documentation`, `/request-root-cause` are available

### Requirement: Handle skill errors
Skills SHALL implement error handling with clear error messages and rollback capabilities.

#### Scenario: Validation error
- **WHEN** skill receives invalid parameters
- **THEN** skill returns error status with validation message

#### Scenario: Execution error
- **WHEN** skill execution fails
- **THEN** skill rolls back changes (if applicable) and returns error status with details

### Requirement: Log skill execution
Skills SHALL log invocations, parameters, and outcomes for observability.

#### Scenario: Structured logging
- **WHEN** skill executes
- **THEN** skill logs invocation with timestamp, parameters, outcome, and duration in structured format

### Requirement: Support skill composition
Skills SHALL support composition where one skill can invoke another skill.

#### Scenario: Skill calls another skill
- **WHEN** skill needs functionality from another skill
- **THEN** skill MAY invoke other skill and use its output

