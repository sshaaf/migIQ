## MODIFIED Requirements

### Requirement: Find all service classes

The system SHALL provide helper function that uses graphify CLI to find all service classes in the codebase.

#### Scenario: Query for services using graphify
- **WHEN** user calls `graph_find_services`
- **THEN** system executes `graphify query "Find all service classes"`

#### Scenario: Return natural language response
- **WHEN** graphify query completes
- **THEN** system returns graphify's natural language response

### Requirement: Find all test classes

The system SHALL provide helper function that uses graphify CLI to find all test classes.

#### Scenario: Query for tests using graphify
- **WHEN** user calls `graph_find_tests`
- **THEN** system executes `graphify query "Find all test classes"`

#### Scenario: Return test information
- **WHEN** graphify query completes
- **THEN** system returns graphify's response about test classes

### Requirement: Find dependencies of a class

The system SHALL provide helper function that uses graphify path command to find dependencies.

#### Scenario: Query dependencies using graphify path
- **WHEN** user calls `graph_find_dependencies "ClassName"`
- **THEN** system executes `graphify path "ClassName" "*"`

#### Scenario: Show dependency paths
- **WHEN** graphify path completes
- **THEN** system returns all paths from source class to dependencies

### Requirement: Query graph using natural language

The system SHALL provide generic query function that passes questions to graphify CLI.

#### Scenario: Natural language query
- **WHEN** user calls `graph_query "Find all REST endpoints"`
- **THEN** system executes `graphify query "Find all REST endpoints"`

#### Scenario: Return graphify response
- **WHEN** graphify processes query
- **THEN** system returns graphify's natural language answer

## REMOVED Requirements

### Requirement: Find classes with specific annotation

**Reason**: Graphify handles annotation detection automatically via AST parsing. No need for custom placeholder functions waiting for metadata extraction - just use graphify query directly.

**Migration**: Use `graphify query "Find classes with @AnnotationName"` instead of calling `graph_find_annotations`. Graphify's natural language query understands annotation patterns.

### Requirement: Find files importing specific package

**Reason**: Graphify handles import detection automatically via AST parsing. Custom import search functions are redundant.

**Migration**: Use `graphify query "Find files importing package.name.*"` instead of calling `graph_find_imports`. Graphify's query can answer import-related questions directly.

### Requirement: Export functions for agent use

**Reason**: Simplified to use graphify CLI directly instead of bash function wrappers. Agents can call `graphify query` and `graphify path` commands directly.

**Migration**: Agents should use `graphify query "<question>"` and `graphify path "Source" "Target"` commands directly instead of sourcing shell functions. This reduces indirection and makes commands more transparent.
