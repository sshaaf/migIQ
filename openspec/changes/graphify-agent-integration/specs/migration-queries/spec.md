## ADDED Requirements

### Requirement: Query for EJB annotations

The system SHALL provide query functions to find classes with EJB annotations.

#### Scenario: Find Stateless beans
- **WHEN** user queries for EJB classes
- **THEN** system finds all classes with `@Stateless` annotation

#### Scenario: Find MessageDriven beans
- **WHEN** user queries for EJB classes
- **THEN** system finds all classes with `@MessageDriven` annotation

#### Scenario: Find Stateful beans
- **WHEN** user queries for EJB classes
- **THEN** system finds all classes with `@Stateful` annotation

### Requirement: Query for javax imports

The system SHALL provide query functions to find files importing javax packages.

#### Scenario: Find javax imports
- **WHEN** user queries for legacy imports
- **THEN** system returns all unique `javax.*` import statements

#### Scenario: Group by import prefix
- **WHEN** querying javax imports
- **THEN** system filters by `import_prefix == "javax"`

#### Scenario: Sort imports uniquely
- **WHEN** displaying javax imports
- **THEN** system returns unique sorted list

### Requirement: Find files using specific annotation

The system SHALL provide query to find all files using a given annotation.

#### Scenario: Query by annotation name
- **WHEN** user provides annotation name
- **THEN** system finds all files with `has_annotation` relationship to that annotation

#### Scenario: Return file paths
- **WHEN** files are found
- **THEN** system returns source file paths for matching nodes

### Requirement: Display migration status summary

The system SHALL provide summary function showing migration-relevant metrics.

#### Scenario: Count EJB annotations
- **WHEN** user requests migration status
- **THEN** system displays count of EJB annotation usage

#### Scenario: Count javax imports
- **WHEN** user requests migration status
- **THEN** system displays count of javax import usage

#### Scenario: Count files needing migration
- **WHEN** user requests migration status
- **THEN** system displays count of files with either javax imports OR EJB annotations

### Requirement: Export query functions for shell use

The system SHALL export migration query functions for use in shell scripts and agents.

#### Scenario: Source migration-queries script
- **WHEN** user sources `scripts/migration-queries.sh`
- **THEN** all query functions are available in current shell

#### Scenario: Call from agent
- **WHEN** agent sources migration-queries script
- **THEN** agent can call functions like `find_ejb_classes` and `find_javax_imports`
