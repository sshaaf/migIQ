## Context

Current agents analyze codebases using Grep/Read/Edit tools, which requires reading hundreds of files for each task (5-8 minutes per task). Graphify already builds AST-based knowledge graphs containing class relationships, dependencies, and structure, but agents aren't leveraging this capability.

**Current workflow:**
1. Agent receives task (e.g., "generate tests for OrderService")
2. Uses Grep to find service classes (~45 grep calls)
3. Reads 200-300 files to understand context
4. Analyzes dependencies manually
5. Generates output

**Constraints:**
- Must work with existing graphify CLI (no external services)
- Must not require Neo4j or other database dependencies
- Must remain AST-only (no API costs)
- Agents must gracefully fall back to Grep/Read if graph unavailable
- Graph updates should be fast (<30 seconds)

**Stakeholders:**
- All migration agent workflows
- Developers running local migrations
- CI/CD pipelines using agents

## Goals / Non-Goals

**Goals:**
- Reduce agent execution time by 50-70%
- Enable automatic dependency discovery via graph queries
- Extract Java metadata (annotations, imports) from AST cache
- Provide migration-specific queries (EJB annotations, javax imports)
- Measure and validate performance improvements
- Make graph queries the primary analysis method, Grep/Read as fallback

**Non-Goals:**
- Neo4j integration (future work)
- Vector search or semantic queries (future work)
- Multi-repo global graph (future work)
- Real-time graph updates during code changes
- Graph visualization UI
- Custom query language beyond graphify CLI

## Decisions

### Decision 1: Graph-First Strategy in Agent Prompts

**Choice:** Update all agent `agent.md` files to check for graph availability and use graphify queries before Grep/Read.

**Rationale:**
- Agents already follow documented strategies in agent.md
- No code changes required, just prompt engineering
- Easy to rollback if it doesn't work
- Maintains backward compatibility (falls back to Grep/Read)

**Alternatives considered:**
- Modify agent runtime code → Too invasive, harder to maintain
- Create wrapper scripts → Agents wouldn't know about graph capability

**Implementation:**
- Add "Code Analysis Strategy" section to each agent.md
- Document when to use graph vs Grep/Read
- Set performance target: <5 file reads per task

### Decision 2: PreAgentExecution Hook for Graph Availability

**Choice:** Use `.claude/settings.json` hook to ensure graph exists before agent runs.

**Rationale:**
- One-time graph build (30s) vs repeated file reads (5-8 min)
- Automatic, no manual intervention
- Hooks run before agent starts, ensuring graph is fresh
- Idempotent: only builds if graph missing

**Alternatives considered:**
- Manual graph build → Users will forget, agents will be slow
- Build during agent execution → Adds latency to every run
- Periodic background updates → Complex, may use stale graph

**Implementation:**
- Hook checks if `graphify-out/graph.json` exists
- If missing: runs `graphify update .`
- If exists: proceeds immediately

### Decision 3: Extract Metadata from AST Cache (Not Re-Parse)

**Choice:** Build metadata extractor that walks existing graphify AST cache to find annotations and imports.

**Rationale:**
- AST cache already parsed (graphify update already ran)
- No additional parsing cost
- Zero API/LLM calls needed
- Consistent with "AST-only" constraint

**Alternatives considered:**
- Re-parse files with tree-sitter → Duplicate work, slower
- Use regex on source code → Unreliable, misses complex patterns
- Store metadata during graphify update → Requires modifying graphify

**Implementation:**
- Python script walks `graphify-out/cache/*.json`
- Extracts annotation nodes (`marker_annotation`, `annotation`)
- Extracts import nodes (`import_declaration`)
- Builds reverse indexes (annotation → files, import → files)
- Enhances graph.json with annotation and import nodes

### Decision 4: Separate Helper Scripts for Common Queries

**Choice:** Create `graph-queries.sh` and `migration-queries.sh` with reusable query functions.

**Rationale:**
- Agents can source these scripts for instant query access
- Standardizes query patterns across all agents
- Makes complex jq queries reusable
- Easier to test and maintain than inline queries

**Alternatives considered:**
- Inline queries in each agent → Duplication, hard to maintain
- Extend graphify CLI → Outside our control, requires upstream changes
- Create separate CLI tool → Overkill, bash functions sufficient

**Implementation:**
- `graph-queries.sh`: Generic helpers (find services, tests, dependencies)
- `migration-queries.sh`: Migration-specific (EJB annotations, javax imports)
- Functions use jq to parse graph-enhanced.json
- Export functions for agent consumption

### Decision 5: Benchmark-Driven Validation

**Choice:** Create benchmark scripts to measure performance before/after graphify integration.

**Rationale:**
- Proof required to justify 2-3 day investment
- Identifies which agents benefit most
- Validates 50-70% speedup claim
- Provides data for future optimizations

**Alternatives considered:**
- Manual observation → Subjective, not reproducible
- Log analysis only → Incomplete picture
- Skip validation → Risk investing time without proof of value

**Implementation:**
- Baseline benchmark: temporarily disable graph, measure agent performance
- With-graph benchmark: ensure graph exists, measure performance
- Comparison script: parse logs, extract metrics, generate report
- Metrics: execution time, grep calls, read calls, graphify queries

## Risks / Trade-offs

### Risk 1: Graphify Graph Quality
**[Risk]** Graphify's AST extraction may miss relationships or produce incomplete graphs for complex codebases.
**→ Mitigation:** Agents fall back to Grep/Read if graph queries return empty results. Test on real migration projects to validate graph completeness.

### Risk 2: Metadata Extraction Accuracy
**[Risk]** AST node types may vary across Java versions or tree-sitter grammar updates.
**→ Mitigation:** Extract samples from test projects, validate node types before production. Document supported Java versions.

### Risk 3: Graph Staleness
**[Risk]** Graph becomes stale after code changes, agents work with outdated information.
**→ Mitigation:** PreAgentExecution hook rebuilds graph if missing. Document recommendation to run `graphify update .` after significant code changes.

### Risk 4: Agent Prompt Complexity
**[Risk]** Adding graph strategy to agent.md may make prompts too complex or confuse agents.
**→ Mitigation:** Keep strategy simple (check, query, fallback). Test with one agent first before rolling out to all.

### Risk 5: Performance Regression
**[Risk]** Graph queries may be slower than expected, negating benefits.
**→ Mitigation:** Benchmark validates performance before rollout. Rollback plan (revert agent.md changes) takes <5 minutes.

### Trade-off 1: AST-Only vs Complete Metadata
**Trade-off:** Extracting only AST-visible metadata (annotations, imports) misses runtime behavior (reflection, dynamic loading).
**Acceptance:** This is acceptable for migration use case. Most migrations involve static code patterns (EJB annotations, javax imports).

### Trade-off 2: Bash Scripts vs Proper Tooling
**Trade-off:** Using bash/jq/python scripts instead of proper CLI tool or service.
**Acceptance:** Acceptable for MVP. If successful, future work can build proper tooling. Scripts are maintainable and sufficient for current needs.

### Trade-off 3: No Real-Time Updates
**Trade-off:** Graph updates require explicit `graphify update .` call, not automatic on file changes.
**Acceptance:** Acceptable. Agents run infrequently enough that pre-execution hook ensures freshness. Real-time updates would add complexity without clear benefit.
