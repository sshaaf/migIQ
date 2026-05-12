## MODIFIED Requirements

### Requirement: Agents check for graph availability

Agents SHALL check if graphify knowledge graph exists before performing code analysis.

#### Scenario: Graph exists
- **WHEN** agent starts code analysis task
- **THEN** agent checks for `graphify-out/graph.json` file existence

#### Scenario: Graph missing
- **WHEN** graph file does not exist
- **THEN** agent falls back to Grep/Read/Edit tools for analysis

### Requirement: Agents use correct graphify command for building graph

Agents SHALL use `/graphify .` skill command (in IDE context) or `graphify extract .` CLI command to build knowledge graph.

#### Scenario: Build graph in IDE context
- **WHEN** agent needs to build graph in Claude Code IDE
- **THEN** agent executes `/graphify .` skill command

#### Scenario: Build graph in CLI context
- **WHEN** agent runs in headless/CLI environment
- **THEN** agent executes `graphify extract .` command

#### Scenario: Incremental graph update
- **WHEN** agent needs to update graph after code changes
- **THEN** agent executes `graphify extract . --update` to re-extract only changed files

### Requirement: Agents query graph using correct CLI syntax

Agents SHALL use `graphify query "<question>"` for natural language queries and `graphify path "Node1" "Node2"` for dependency discovery.

#### Scenario: Natural language query
- **WHEN** agent needs to find code patterns
- **THEN** agent executes `graphify query "Find all service classes"`

#### Scenario: Dependency discovery
- **WHEN** agent needs to understand dependencies
- **THEN** agent executes `graphify path "ClassA" "ClassB"` to find connection

#### Scenario: Architecture overview
- **WHEN** agent needs architectural context
- **THEN** agent reads `graphify-out/GRAPH_REPORT.md` file

### Requirement: Agents reference correct output files

Agents SHALL expect graphify output in `graphify-out/` directory with files: `graph.html`, `GRAPH_REPORT.md`, and `graph.json`.

#### Scenario: Check report location
- **WHEN** agent looks for graph summary
- **THEN** agent reads `graphify-out/GRAPH_REPORT.md`

#### Scenario: Check graph data
- **WHEN** agent needs structured graph data
- **THEN** agent parses `graphify-out/graph.json`

#### Scenario: View visualization
- **WHEN** user wants to explore graph visually
- **THEN** user opens `graphify-out/graph.html` in browser

## REMOVED Requirements

### Requirement: Agents update graph after code changes

**Reason**: Replaced with `graphify extract . --update` command for incremental updates. The old `graphify update .` command does not exist in the Python graphify tool.

**Migration**: Use `graphify extract . --update` instead of `graphify update .`. The `--update` flag tells graphify to re-extract only files that have changed since last extraction.
