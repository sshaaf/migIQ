# analyze-codebase

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

The skill delegates to opencode agent for deep code analysis.

## Actions

1. Validate input parameters
2. Invoke opencode agent for codebase analysis
3. Collect metrics (LOC, complexity, dependencies)
4. Identify anti-patterns from rule.md
5. Generate structured analysis report
6. Calculate migration complexity score

## Outputs

Returns JSON analysis report with:
- `structure`: Codebase organization
- `dependencies`: List of dependencies with versions
- `antiPatterns`: Detected anti-patterns
- `complexity`: Complexity metrics
- `migrationScore`: 0-100 score indicating migration difficulty
- `recommendations`: Prioritized recommendations

## Tools Used

- opencode agent (code analysis)
- Language-specific analyzers (optional)
- Dependency scanners

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
