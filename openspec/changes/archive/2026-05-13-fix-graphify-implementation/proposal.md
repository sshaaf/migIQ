## Why

The current graphify integration uses incorrect installation, commands, and output expectations based on a different tool (ThoughtWorks graphify). The actual graphify (https://github.com/safishamsi/graphify) is a Python tool with different CLI commands, output structure, and workflow. Agents are trying to use non-existent commands and expect wrong output files.

## What Changes

- **BREAKING**: Change installation from npm to Python package (`graphifyy`)
- **BREAKING**: Replace `graphify update .` with `/graphify .` skill command
- **BREAKING**: Update output file expectations (graph.html, GRAPH_REPORT.md location, graph.json structure)
- **BREAKING**: Fix query commands (graphify query, graphify path with correct syntax)
- Add `--update` flag for incremental graph updates
- Update PreAgentExecution hook to use correct graphify command
- Fix agent.md prompts to use correct graphify CLI
- Update all helper scripts to use correct commands and output files
- Remove metadata extraction script (graphify handles this via AST parsing)
- Update benchmark scripts to use correct commands

## Capabilities

### New Capabilities
<!-- No new capabilities, just fixing existing implementation -->

### Modified Capabilities
- `agent-graph-integration`: Change from incorrect graphify commands to correct Python CLI
- `graph-query-helpers`: Update to use correct graphify query syntax and output files
- `metadata-extraction`: Remove custom extraction (graphify does this automatically)

## Impact

**Breaking Changes:**
- Existing graphify installations won't work (npm vs Python)
- All graphify commands in agent.md files are incorrect
- PreAgentExecution hook uses wrong command
- Helper scripts reference non-existent files
- Benchmark scripts won't work

**Affected Files:**
- `.claude/settings.json` - PreAgentExecution hook command
- All 5 agent `agent.md` files - graphify command examples
- `scripts/graph-queries.sh` - Query helpers using wrong commands
- `scripts/migration-queries.sh` - Wrong output file references
- `scripts/extract_metadata.py` - **DELETE** (not needed, graphify does this)
- `scripts/update-graph.sh` - Wrong commands
- `scripts/benchmark-*.sh` - Wrong graphify commands
- `README.md` - Installation and usage instructions

**Correct Implementation:**
- Install: `uv tool install graphifyy` or `pipx install graphifyy`, then `graphify install`
- Main command: `/graphify .` (as IDE skill) or `graphify extract .` (CLI)
- Output: `graphify-out/graph.html`, `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`
- Query: `graphify query "question"` and `graphify path "Node1" "Node2"`
- Update: Add `--update` flag to re-extract only changed files
- Local AST: Uses tree-sitter locally (no API calls for code)

**Migration Path:**
- Uninstall npm graphify (if installed)
- Install Python graphifyy package
- Run `graphify install` to set up
- Update all scripts and agent prompts
- Delete custom metadata extraction script
