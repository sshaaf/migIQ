## Context

The current graphify integration was implemented based on the wrong tool (ThoughtWorks graphify, an npm package). The actual graphify (https://github.com/safishamsi/graphify) is a Python package with completely different:
- Installation method (Python vs npm)
- CLI commands (`/graphify .` vs `graphify update .`)
- Output structure (`graph.html`, `GRAPH_REPORT.md` in root vs different locations)
- Query syntax and capabilities
- Workflow (uses tree-sitter AST locally, no custom metadata extraction needed)

**Current broken state:**
- PreAgentExecution hook runs non-existent `graphify update .` command
- Agents reference wrong commands in prompts
- Helper scripts expect non-existent files
- Custom metadata extraction duplicates graphify's built-in functionality
- Installation instructions point to npm package

**Stakeholders:**
- All 5 agents using graphify integration
- Developers following setup documentation
- Benchmark scripts measuring performance

## Goals / Non-Goals

**Goals:**
- Correct all graphify commands to match actual Python CLI
- Update installation to Python package (`graphifyy`)
- Fix output file references (`graph.html`, `GRAPH_REPORT.md`, `graph.json`)
- Remove redundant metadata extraction (graphify does this)
- Update PreAgentExecution hook to use correct command
- Maintain benchmark capabilities with corrected implementation
- Preserve agent-first strategy (check graph before Grep/Read)

**Non-Goals:**
- Change overall architecture (agents still use graph-first approach)
- Add new graphify features beyond fixing current implementation
- Support both old and new graphify (breaking change is acceptable)
- Build custom visualization (graphify provides graph.html)

## Decisions

### Decision 1: Use `/graphify .` Skill Command in Hook

**Choice:** PreAgentExecution hook uses `/graphify .` (IDE skill command) instead of CLI `graphify extract .`

**Rationale:**
- Agents run in Claude Code IDE context where `/graphify .` is available as skill
- Skill command integrates better with IDE environment
- Fallback to `graphify extract .` if skill unavailable
- Consistent with how agents invoke commands

**Alternatives considered:**
- Use CLI `graphify extract .` → Less integrated with IDE context
- Use `graphify extract . --update` → Correct for incremental updates but doesn't work in IDE skill context

**Implementation:**
```json
{
  "hooks": {
    "PreAgentExecution": [
      {
        "matcher": "*-agent",
        "hooks": [
          {
            "type": "command",
            "command": "[ -d .git ] && [ ! -f graphify-out/graph.json ] && /graphify . || echo 'Graph exists'"
          }
        ]
      }
    ]
  }
}
```

### Decision 2: Delete Custom Metadata Extraction Script

**Choice:** Remove `scripts/extract_metadata.py` entirely.

**Rationale:**
- Graphify already extracts annotations and imports via tree-sitter AST
- Graphify output includes all metadata in `graph.json`
- Custom extraction duplicates work and creates maintenance burden
- Graphify's extraction is more complete (handles 29 languages)
- No need for `graph-enhanced.json` - graphify's `graph.json` has everything

**Alternatives considered:**
- Keep extraction as post-processing → Unnecessary complexity
- Enhance graphify's extraction → Out of scope, should contribute upstream

**Impact:**
- Remove `scripts/extract_metadata.py`
- Remove `scripts/update-graph.sh` (replaced with simple `/graphify .` or `graphify extract .`)
- Update migration queries to read from `graphify-out/graph.json` directly

### Decision 3: Simplify Query Helpers to Use Graphify CLI

**Choice:** Update helper scripts to use `graphify query` and `graphify path` commands instead of parsing JSON.

**Rationale:**
- Graphify has built-in query capabilities
- `graphify query "question"` returns natural language answers
- `graphify path "Node1" "Node2"` finds connections
- Simpler than parsing JSON with jq
- More maintainable (graphify handles query logic)

**Alternatives considered:**
- Keep jq-based JSON parsing → More fragile, harder to maintain
- Build custom query language → Reinventing graphify's capabilities

**Implementation:**
```bash
graph_find_services() {
    graphify query "Find all service classes"
}

graph_find_dependencies() {
    local class=$1
    graphify path "$class" "*"
}
```

### Decision 4: Update Agent Prompts for Correct Commands

**Choice:** Update all agent.md files with correct graphify syntax.

**Rationale:**
- Agents need to know correct commands to use graph
- Examples must match actual CLI behavior
- Fallback strategy still applies (use Grep/Read if graph fails)

**Changes:**
- `/graphify .` instead of `graphify update .`
- `graphify query "question"` instead of parsing graph.json
- `graphify path "Node1" "Node2"` for dependency discovery
- Reference `graphify-out/GRAPH_REPORT.md` for architecture overview
- `graphify extract . --update` for incremental updates after code changes

### Decision 5: Update Installation to Python Package

**Choice:** Document installation as Python package with multiple options.

**Rationale:**
- Package name is `graphifyy` (double-y) on PyPI
- CLI command is still `graphify` after installation
- Multiple installation methods (uv, pipx, pip) for flexibility
- Requires `graphify install` post-installation setup

**Documentation:**
```bash
# Option 1: uv (recommended)
uv tool install graphifyy && graphify install

# Option 2: pipx
pipx install graphifyy && graphify install

# Option 3: pip
pip install graphifyy && graphify install
```

## Risks / Trade-offs

### Risk 1: Breaking Change for Existing Users
**[Risk]** Anyone who followed previous graphify setup will have non-functional installation.
**→ Mitigation:** Clear migration guide in documentation. Uninstall npm package, install Python package, update scripts.

### Risk 2: `/graphify .` Skill May Not Work in All Contexts
**[Risk]** PreAgentExecution hook using `/graphify .` may fail outside IDE context.
**→ Mitigation:** Add fallback to `graphify extract .` if skill command fails. Document both approaches.

### Risk 3: Query Syntax Differences
**[Risk]** Natural language queries via `graphify query` may return different formats than jq parsing.
**→ Mitigation:** Test queries with real codebase. Document expected output formats. Keep some jq fallbacks if needed.

### Risk 4: Graph Output Structure Changes
**[Risk]** `graph.json` structure from Python graphify may differ from expected format.
**→ Mitigation:** Inspect actual output structure. Update migration queries to match real schema.

### Trade-off 1: Losing Custom Metadata Extraction
**Trade-off:** Deleting `extract_metadata.py` means we rely entirely on graphify's extraction.
**Acceptance:** Graphify's extraction is more complete and maintained. If we need custom processing, contribute to graphify or post-process its output.

### Trade-off 2: Natural Language Queries vs Structured JSON
**Trade-off:** `graphify query` returns natural language vs structured data from JSON parsing.
**Acceptance:** Natural language is more flexible for agents. Can use graph.json directly if structured data needed.

## Migration Plan

### Step 1: Update Installation Documentation
- Remove npm installation instructions
- Add Python package installation (uv/pipx/pip)
- Document `graphify install` post-installation step

### Step 2: Fix Agent Prompts
- Update all 5 agent.md files with correct commands
- Replace `graphify update .` with `/graphify .` or `graphify extract .`
- Update query examples to use `graphify query` and `graphify path`

### Step 3: Update Helper Scripts
- Rewrite `graph-queries.sh` to use graphify CLI
- Rewrite `migration-queries.sh` to use graphify CLI or parse graph.json correctly
- Delete `extract_metadata.py` (no longer needed)
- Delete or rewrite `update-graph.sh` to simple wrapper

### Step 4: Fix PreAgentExecution Hook
- Update hook command to `/graphify .`
- Add fallback for CLI context

### Step 5: Update Benchmark Scripts
- Fix commands in `benchmark-with-graph.sh`
- Ensure correct timing measurement

### Step 6: Test with Real Codebase
- Run `/graphify .` on actual Java project
- Verify `graphify-out/` contains expected files
- Test queries work as expected
- Validate migration queries find EJB classes and javax imports

### Rollback Strategy
If new implementation doesn't work:
1. Revert all command changes
2. Document that graphify integration is experimental
3. Recommend manual graph building until stable
4. Option: Fork graphify and customize if needed

## Open Questions

1. **Does `/graphify .` work in PreAgentExecution hooks?**
   - Need to test if skill commands work in hook context
   - May need CLI fallback: `graphify extract .`

2. **What is the exact structure of graph.json from Python graphify?**
   - Need to inspect actual output to update migration queries
   - May need different jq selectors

3. **How do incremental updates work?**
   - `--update` flag documented, but need to test behavior
   - Does it detect changed files automatically?

4. **Can we query annotations and imports via graphify query?**
   - Test: `graphify query "Find classes with @Stateless"`
   - Test: `graphify query "Find files importing javax.*"`
   - May need to parse graph.json if queries insufficient
