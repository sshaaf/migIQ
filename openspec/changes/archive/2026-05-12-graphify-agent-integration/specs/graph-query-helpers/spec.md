## ADDED Requirements

### Requirement: Find all service classes

The system SHALL provide helper function to find all service classes in the codebase.

#### Scenario: Query for services
- **WHEN** user calls `graph_find_services`
- **THEN** system executes `graphify query "Find all service classes"`

#### Scenario: Return file paths
- **WHEN** services are found
- **THEN** system returns file paths using jq to extract `.nodes[].file`

### Requirement: Find all test classes

The system SHALL provide helper function to find all test classes.

#### Scenario: Query for tests
- **WHEN** user calls `graph_find_tests`
- **THEN** system executes `graphify query "Find all test classes"`

#### Scenario: Return test file paths
- **WHEN** tests are found
- **THEN** system returns file paths using jq

### Requirement: Find dependencies of a class

The system SHALL provide helper function to find dependencies of a specific class.

#### Scenario: Query dependencies
- **WHEN** user calls `graph_find_dependencies "<ClassName>"`
- **THEN** system executes `graphify path "<ClassName>" "*"`

#### Scenario: Filter path output
- **WHEN** path results are returned
- **THEN** system filters using grep for dependency lines

### Requirement: Find classes with specific annotation

The system SHALL provide helper function to find classes using a given annotation.

#### Scenario: Query by annotation
- **WHEN** user calls `graph_find_annotations "<AnnotationName>"`
- **THEN** system queries enhanced graph for annotation matches

#### Scenario: Placeholder for future implementation
- **WHEN** metadata extraction is not yet complete
- **THEN** function includes comment "After metadata extraction, this will work"

### Requirement: Find files importing specific package

The system SHALL provide helper function to find files importing from a package prefix.

#### Scenario: Query by import prefix
- **WHEN** user calls `graph_find_imports "<PackagePrefix>"`
- **THEN** system queries enhanced graph for import matches

#### Scenario: Placeholder for future implementation
- **WHEN** metadata extraction is not yet complete
- **THEN** function includes comment indicating future availability

### Requirement: Export functions for agent use

The system SHALL export all helper functions for use in shell environments.

#### Scenario: Source graph-queries script
- **WHEN** user sources `scripts/graph-queries.sh`
- **THEN** all functions are exported and available

#### Scenario: Functions work in subshells
- **WHEN** agent spawns subshell
- **THEN** exported functions remain available via `export -f`

### Requirement: Handle missing graph gracefully

Helper functions SHALL handle missing graph files without crashing.

#### Scenario: Graph file missing
- **WHEN** graph file does not exist
- **THEN** graphify commands return empty results gracefully

#### Scenario: Query returns no results
- **WHEN** query finds no matches
- **THEN** function returns empty output without error
