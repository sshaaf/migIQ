---
name: mig-graphify
trigger: /mig-graphify
description: Build knowledge graph for code migration analysis. Use when you need to analyze codebase structure, understand dependencies, or prepare for migration. This is required before running any code analysis or migration tasks.
---

Build knowledge graph for fast code analysis during migration.

## Parameters

- `<path>` (optional): Path to analyze (default: current directory)
- `--update` (optional): Incremental update (re-analyze only changed files)
- `--mode deep` (optional): Thorough extraction with richer edges

## Description

Creates a knowledge graph of your codebase that enables 50-70% faster migration execution by reducing file reads by 96%. Required for all migration agents to work properly.

## What it does

1. Analyzes code structure via tree-sitter AST
2. Extracts dependencies, imports, and annotations
3. Builds knowledge graph with community detection
4. Generates outputs:
   - `graphify-out/graph.json` - Complete graph data
   - `graphify-out/GRAPH_REPORT.md` - Architecture summary
   - `graphify-out/graph.html` - Interactive visualization

## Usage

```bash
# Analyze current directory (offline, no API key)
/mig-graphify

# Analyze specific path
/mig-graphify ./my-project

# Force rebuild after major refactoring
/mig-graphify --force

# Skip HTML visualization for large codebases
/mig-graphify --no-viz
```

## Actions

1. **Check if graphify CLI is installed**
   ```bash
   graphify --version
   ```

   If not found, display installation instructions and exit:
   ```
   ⚠️  Graphify tool not found

   Install graphify to enable fast code analysis:

   # Option A: Using uv (recommended)
   uv tool install graphifyy

   # Option B: Using pipx
   pipx install graphifyy

   # Option C: Using pip
   pip install graphifyy

   # Verify installation
   graphify --version

   After installation, run this command again.
   ```

2. **Build knowledge graph (offline mode - no API key required)**

   Use the `update` command for pure AST extraction without LLM:
   ```bash
   graphify update <path>
   ```

   This performs local-only tree-sitter AST extraction and does not require any API key.

   Optional flags:
   - `--force` - overwrite graph.json even if rebuild has fewer nodes
   - `--no-viz` - skip graph.html generation (useful for large graphs)

3. **Verify outputs**
   - Check `graphify-out/graph.json` exists
   - Check `graphify-out/GRAPH_REPORT.md` exists
   - Report graph statistics (nodes, edges, communities)

## Query Operations

After building the graph, you can query it (requires LLM API for semantic queries):

```bash
# Find dependency paths (no API key needed)
graphify path "ClassA" "ClassB"

# Explain a node (requires API key)
graphify explain "ServiceClassName"

# Natural language queries (requires API key)
graphify query "Find all service classes"
graphify query "Find classes with @Stateless annotation"
graphify query "Find files importing javax.*"
```

**Note:** Query operations require an LLM API key. For migration analysis, the graph structure itself (graph.json) is sufficient and built offline.

## Outputs

**graphify-out/graph.json:**
- Complete graph structure
- Nodes: classes, files, packages
- Edges: dependencies, imports, calls
- Metadata: annotations, community assignments

**graphify-out/GRAPH_REPORT.md:**
- Architecture overview
- God nodes (high-degree classes that need attention)
- Community structure
- Key connections and patterns

**graphify-out/graph.html:**
- Interactive visualization
- Filterable by community
- Click nodes to see details

## Performance Impact

- **50-70% faster** agent execution
- **96% reduction** in file reads
- **Complete dependency understanding** instantly available
- **Zero API costs** - graph building uses local tree-sitter AST (no LLM required)
- **Fully offline** - runs without internet connection

## Integration with Migration

This skill is automatically invoked by `/migration` as Step 2. All downstream agents (test-generator, code-refactor, etc.) expect the graph to exist.

**Migration workflow:**
```
/migration
  ↓
/mig-graphify  ← builds graph (~30s)
  ↓
analyze-codebase, plan-migration, etc. ← query graph
```

## Tools Used

- **graphify CLI** (required) - Python package `graphifyy`
- tree-sitter - AST parsing (bundled with graphify)
- File system operations

## Example Output

```
Building knowledge graph for ./my-project...
Running offline mode (AST-only, no API required)

✓ Extracted 150 files
✓ Found 8 communities
✓ Identified 5 god nodes
✓ Created 1,247 edges

Outputs:
  - graphify-out/graph.json (425 KB)
  - graphify-out/GRAPH_REPORT.md
  - graphify-out/graph.html

Graph statistics:
  - Nodes: 150
  - Edges: 1,247
  - Communities: 8
  - God nodes: 5 (degree ≥ 10)

Time: 28.3s (tree-sitter AST extraction)
```

## Error Handling

**Tool not found:**
```
Error: graphify command not found
Run: uv tool install graphifyy
```

**Invalid path:**
```
Error: Path './nonexistent' does not exist
```

**Graph build failed:**
```
Error: Graph extraction failed
Check that the path contains valid source code files
```

## Notes

- Graph persists across sessions - only rebuild when code changes significantly
- Use `--update` for incremental changes (faster than full rebuild)
- Graph is required for migration agents - they will fail without it
- All code analysis is local (no API calls for source code)
