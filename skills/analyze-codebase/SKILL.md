---
name: analyze-codebase
trigger: /analyze-codebase
description: Analyze target codebase to identify migration requirements, dependencies, and complexity. Use when the user wants to analyze code, understand codebase structure, assess migration readiness, or identify dependencies and anti-patterns before migration.
---

Analyze target codebase to identify migration requirements, dependencies, and complexity.

## Parameters

- `--path` (required): Path to codebase to analyze
- `--migration-type` (required): Type of migration (framework, language, platform, custom)
- `--scope` (optional): Analysis scope (full or incremental, default: full)
- `--output` (optional): Output path for analysis report (default: ./analysis-report.json)

## Description

Analyzes the target codebase and generates a structured report containing:
- Codebase structure and organization
- Dependencies and their versions
- Anti-patterns and code smells
- Complexity metrics
- Migration readiness score

Uses Graphify knowledge graph for fast, comprehensive analysis.

## Code Analysis Strategy

**ALWAYS use Graphify for code analysis:**

1. **Check if graph exists (should exist from /migration trigger):**
   ```bash
   [ -f graphify-out/graph.json ] && echo "Graph available" || /graphify <path>
   ```

2. **Extract codebase structure:**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # Shows: Community structure, god nodes, architecture overview
   ```

3. **Find dependencies:**
   ```bash
   /graphify query "Find all dependencies and their versions"
   ```

4. **Identify anti-patterns:**
   ```bash
   /graphify query "Find all classes with @Stateless annotation"
   /graphify query "Find all classes with @MessageDriven annotation"
   /graphify query "Find classes importing javax.ejb"
   ```

5. **Calculate complexity:**
   ```bash
   jq '.metrics' graphify-out/graph.json
   # Contains: node count, edge count, community metrics
   ```

**Use Grep/Read only for:**
- Reading specific file contents
- Extracting version numbers from pom.xml/build files
- Reading rule.md for anti-pattern definitions

## Actions

1. Validate input parameters
2. Ensure Graphify graph exists (build if missing)
3. Extract structure from GRAPH_REPORT.md
4. Query graph for dependencies and patterns
5. Collect metrics from graph.json
6. Identify anti-patterns using graph queries
7. Generate structured analysis report
8. Calculate migration complexity score

## Outputs

Returns JSON analysis report with:
- `structure`: Codebase organization
- `dependencies`: List of dependencies with versions
- `antiPatterns`: Detected anti-patterns
- `complexity`: Complexity metrics
- `migrationScore`: 0-100 score indicating migration difficulty
- `recommendations`: Prioritized recommendations

## Tools Used

- **graphify** (REQUIRED) - Knowledge graph for fast code analysis
- Graph queries for dependencies and patterns
- GRAPH_REPORT.md for architecture overview
- Language-specific analyzers (optional, for metrics not in graph)

## Example Usage

```bash
# Full analysis
/analyze-codebase --path ./src --migration-type framework

# Incremental analysis
/analyze-codebase --path ./src --migration-type framework --scope incremental
```

## Error Handling

- Invalid path: Returns error with message
- Unsupported migration type: Returns error with supported types
- Analysis failure: Returns partial results with warnings
