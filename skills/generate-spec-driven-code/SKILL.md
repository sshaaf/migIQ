---
name: generate-spec-driven-code
trigger: /generate-spec-driven-code
description: Generate code from specifications. Use when the user wants to generate implementation from specs, create code from design documents, implement based on specifications, or automate code generation from requirements.
---

Generate code from specifications.

## Parameters

- `--spec-path` (required): Path to specification file (markdown, JSON, or YAML)
- `--output-path` (required): Path where generated code should be written
- `--template` (optional): Code template to use (default: auto-detect from spec)
- `--context` (optional): Additional context files for understanding existing patterns

## Description

Generates implementation code from specifications. Uses Graphify to understand existing codebase patterns and ensure generated code fits the architecture.

## Code Analysis Strategy

**Use Graphify to understand existing patterns:**

1. **Analyze existing similar code:**
   ```bash
   /graphify query "Find all service classes"
   /graphify query "Find all repository classes"
   # Understand patterns to replicate in generated code
   ```

2. **Check for naming conflicts:**
   ```bash
   /graphify query "Find class named X"
   # Ensure generated class names don't conflict
   ```

3. **Understand dependencies:**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # See architectural layers and how classes are organized
   ```

4. **Find similar implementations:**
   ```bash
   /graphify query "Find classes with @RestController annotation"
   # Use as reference for code generation patterns
   ```

5. **After generating code:**
   ```bash
   /graphify .
   # Update graph with newly generated files
   ```

## Actions

1. Parse specification file
2. Use Graphify to understand existing code patterns
3. Extract template or pattern from existing code
4. Generate code following existing patterns
5. Validate generated code (syntax, imports, patterns)
6. Write generated files
7. Update Graphify graph

## Returns

Generated code files with:
- Proper imports based on existing patterns
- Consistent naming conventions from codebase
- Matching architectural patterns
- Complete implementations

## Tools Used

- **graphify** (REQUIRED) - Understanding existing patterns
- Code generation templates
- Language-specific formatters
- Write tool for creating files

## Example

```bash
# Generate service from spec
/generate-spec-driven-code \
  --spec-path ./specs/user-service.md \
  --output-path ./src/main/java/com/example/UserService.java

# Generate with custom template
/generate-spec-driven-code \
  --spec-path ./specs/api.yaml \
  --output-path ./src/controllers/ \
  --template rest-controller
```
