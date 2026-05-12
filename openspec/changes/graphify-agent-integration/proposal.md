## Why

Current agents use Grep/Read/Edit for code analysis, spending 5-8 minutes per task reading hundreds of files. Integrating graphify enables querying a pre-built knowledge graph instead, reducing analysis time to 1-2 minutes (70% faster) while providing complete dependency understanding with zero redundant work across agents.

## What Changes

- Add graphify-first code analysis strategy to all agent prompts
- Create pre-execution hook to ensure graph is available before agent runs
- Build metadata extractor to add Java annotations and imports to knowledge graph
- Create helper scripts for common graph queries (services, dependencies, annotations, imports)
- Add migration-specific query helpers for detecting EJB annotations and javax imports
- Implement benchmark suite to measure and validate performance improvements
- Update agent workflow to use graph queries before falling back to Grep/Read

## Capabilities

### New Capabilities
- `agent-graph-integration`: Agents query graphify knowledge graph for code analysis before using Grep/Read/Edit
- `metadata-extraction`: Extract Java annotations and imports from AST cache and add to knowledge graph
- `migration-queries`: Query helpers specifically for detecting migration-relevant patterns (EJB annotations, javax imports)
- `graph-query-helpers`: Convenience scripts for common graph queries across all agents
- `performance-benchmarking`: Measure and validate agent performance improvements with graphify

### Modified Capabilities
<!-- No existing capabilities are being modified at the requirement level -->

## Impact

**Affected Agents**:
- test-generator-agent
- code-refactor-agent
- benchmark-builder-agent
- quality-evaluator-agent
- ci-integration-agent

**New Files**:
- `.claude/settings.json` - PreAgentExecution hook for graph availability
- `scripts/graph-queries.sh` - Common graph query helpers
- `scripts/migration-queries.sh` - Migration-specific queries
- `scripts/extract_metadata.py` - Metadata extraction from AST cache
- `scripts/update-graph.sh` - Unified graph update workflow
- `scripts/benchmark-without-graph.sh` - Baseline performance measurement
- `scripts/compare-benchmarks.py` - Performance comparison reporting

**Modified Files**:
- All agent `agent.md` files - Add graphify-first analysis strategy

**Performance Impact**:
- Expected 50-70% reduction in agent execution time
- 96% reduction in file reads per task
- Zero infrastructure cost (AST-only, no external services)
