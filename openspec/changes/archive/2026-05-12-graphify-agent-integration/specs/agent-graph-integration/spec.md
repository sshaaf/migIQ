## ADDED Requirements

### Requirement: Agents check for graph availability

Agents SHALL check if graphify knowledge graph exists before performing code analysis.

#### Scenario: Graph exists
- **WHEN** agent starts code analysis task
- **THEN** agent checks for `graphify-out/graph.json` file existence

#### Scenario: Graph missing
- **WHEN** graph file does not exist
- **THEN** agent falls back to Grep/Read/Edit tools for analysis

### Requirement: Agents query graph for dependencies

Agents SHALL use graphify path queries to discover class dependencies instead of reading multiple files.

#### Scenario: Find dependencies of a class
- **WHEN** agent needs to understand what a class depends on
- **THEN** agent executes `graphify path "<ClassName>" "*"` command

#### Scenario: Find transitive dependencies
- **WHEN** agent needs complete dependency chain
- **THEN** agent receives transitive dependencies from graph path query

### Requirement: Agents query graph for code search

Agents SHALL use graphify query commands to search for code patterns instead of Grep.

#### Scenario: Find service classes
- **WHEN** agent needs to find all service classes
- **THEN** agent executes `graphify query "Find all service classes"`

#### Scenario: Find test classes
- **WHEN** agent needs to locate test files
- **THEN** agent executes `graphify query "Find all test classes"`

### Requirement: Agents explain class context via graph

Agents SHALL use graphify explain command to understand class context and relationships.

#### Scenario: Get class details
- **WHEN** agent needs to understand a specific class
- **THEN** agent executes `graphify explain "<ClassName>"`

#### Scenario: View class connections
- **WHEN** agent needs to see what connects to a class
- **THEN** agent receives all incoming and outgoing relationships from explain command

### Requirement: Agents fall back to traditional tools

Agents SHALL use Grep/Read/Edit tools when graph cannot answer the query.

#### Scenario: Graph query returns empty
- **WHEN** graphify query returns no results
- **THEN** agent falls back to Grep for code search

#### Scenario: Need actual code implementation
- **WHEN** agent needs to see method body or implementation details
- **THEN** agent uses Read tool to view source code

### Requirement: Agent prompts document graph-first strategy

All agent.md files SHALL include a "Code Analysis Strategy" section documenting when to use graph vs traditional tools.

#### Scenario: Agent.md includes graph strategy
- **WHEN** developer reads agent.md file
- **THEN** document includes graphify usage examples before Grep/Read/Edit

#### Scenario: Performance target documented
- **WHEN** agent follows documented strategy
- **THEN** agent achieves <5 file reads per task target

### Requirement: Agents update graph after code changes

Agents SHALL update the knowledge graph after making code modifications.

#### Scenario: Code changes made
- **WHEN** agent modifies source files
- **THEN** agent executes `graphify update .` to refresh graph

#### Scenario: Graph update is fast
- **WHEN** agent updates graph
- **THEN** update completes in under 30 seconds
