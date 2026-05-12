## ADDED Requirements

### Requirement: Apply automated refactoring rules
The system SHALL apply refactoring transformations using opencode agent based on rules defined in YAML.

#### Scenario: Dry-run mode
- **WHEN** user invokes `/apply-refactor-rules` with dry-run flag
- **THEN** system generates transformation plan without applying changes

#### Scenario: Apply transformations
- **WHEN** user invokes `/apply-refactor-rules` without dry-run flag
- **THEN** system applies transformations using opencode agent and generates diff report

### Requirement: Generate spec-driven code
The system SHALL generate new code implementations from specifications using opencode agent.

#### Scenario: Generate from specifications
- **WHEN** code-refactor-agent invokes `/generate-spec-driven-code` with spec path
- **THEN** system generates implementation code that satisfies specifications

#### Scenario: Use code templates
- **WHEN** template path provided
- **THEN** system uses templates as starting point for code generation

### Requirement: Validate refactored code
The system SHALL validate that refactored code preserves behavior and meets specifications.

#### Scenario: Characterization tests pass
- **WHEN** system runs characterization tests against refactored code
- **THEN** all characterization tests MUST pass (behavior preserved)

#### Scenario: Functional tests pass
- **WHEN** system runs functional tests against refactored code
- **THEN** all functional tests MUST pass (new behavior correct)

#### Scenario: Spec validation
- **WHEN** system validates refactored code against specifications using opencode agent
- **THEN** code MUST satisfy all specification requirements

### Requirement: Handle validation failures
The code-refactor-agent SHALL attempt fixes for validation failures with limited retries before escalation.

#### Scenario: Automatic fix attempt
- **WHEN** validation fails
- **THEN** agent analyzes failure, attempts fix, and re-validates (max 3 retries)

#### Scenario: Escalate after retries
- **WHEN** validation still fails after max retries
- **THEN** agent escalates to human with detailed failure analysis
