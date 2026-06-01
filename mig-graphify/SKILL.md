---
name: mig-graphify
description: Build knowledge graph for code migration analysis. Use when you need to analyze codebase structure, understand dependencies, or prepare for migration. This skill is required before running any code analysis or migration tasks when the user mentions migrating, porting, or moving their codebase to a different language, framework, or platform. Trigger on phrases like "migrate to X", "move my codebase to X", "port to X", or when planning any significant code transformation.
---

# Migration Analysis with Knowledge Graph

This skill helps analyze codebases for migration by first building a comprehensive knowledge graph using graphify CLI, then analyzing that graph to identify dependencies, complexity hotspots, and potential migration blockers.

## When to Use This Skill

Use this skill whenever the user wants to:
- Migrate to a different programming language (Java → Kotlin, Python 2 → 3, etc.)
- Switch frameworks (Spring → Quarkus, Angular → React, etc.)
- Move to a different platform (on-prem → cloud, monolith → microservices, containerization)
- Understand their codebase structure before any major refactoring or transformation

The key insight is that successful migrations require deep understanding of the existing codebase's structure and dependencies. The knowledge graph provides this foundation.

## Workflow

### Step 1: Build Knowledge Graph with Graphify

**CRITICAL FIRST STEP - DO THIS BEFORE ANY ANALYSIS:**

Run the graphify CLI to build a knowledge graph of the codebase. Graphify is pre-installed and available in your PATH.

**Run this command:**

```bash
cd <codebase-directory>
graphify update .
```

**Important notes:**
- Graphify runs **100% offline** for code analysis - it uses tree-sitter for AST extraction with no API calls
- Do NOT pass any API keys or credentials
- Code files (Java, Python, JavaScript, etc.) are processed locally without network access
- The command will create a `graphify-out/` directory with analysis results

**What graphify generates:**

After completion, you'll find these files in `graphify-out/`:
- **`graph.json`** - Complete graph data structure (nodes, edges, communities)
- **`GRAPH_REPORT.md`** - Analysis summary with key insights
- **`graph.html`** - Interactive visualization (optional to view)

Wait for the command to complete before proceeding to Step 2. Typical run time: 10-60 seconds depending on codebase size.

### Step 2: Read and Analyze the Knowledge Graph

Once graphify completes, read the generated outputs to understand the migration landscape.

**Start with the summary report:**

```bash
cat graphify-out/GRAPH_REPORT.md
```

This report highlights:
- **God nodes** - The most-connected files/modules that many others depend on
- **Surprising connections** - Unexpected dependencies between distant modules
- **Communities** - Logical groupings of related code
- **Key statistics** - Total nodes, edges, density metrics

**Then read the full graph data:**

```bash
cat graphify-out/graph.json
```

The JSON contains the complete graph structure:
- `nodes` - Every file, class, function, or module
- `edges` - Relationships between nodes (imports, calls, inheritance)
- `communities` - Detected clusters of related code
- Each edge has a `tag` field: EXTRACTED (certain), INFERRED (likely), or AMBIGUOUS (uncertain)

### Step 3: Identify Migration Insights

Analyze the graph data to answer these critical migration questions:

**Dependency Complexity:**
- Which nodes have the highest **in-degree** (fan-in)? These are critical dependencies that many files rely on - changes here propagate widely
- Which nodes have the highest **out-degree** (fan-out)? These are integration points that depend on many others - complex to migrate
- Are there **circular dependencies** (nodes that depend on each other)? These require coordinated migration
- What **external dependencies** exist? Check if they have equivalents in the target ecosystem

**Architectural Patterns:**
- What **communities** were detected? These represent logical boundaries for phased migration
- Are communities **tightly coupled** (many inter-community edges) or **loosely coupled** (few connections)?
- Do communities align with domain boundaries (users, payments, analytics)?

**Migration Hotspots:**
- **Leaf nodes** (in-degree = 0, no dependencies on them) - Safe to migrate first
- **Root nodes** (out-degree = 0, depend on nothing) - Self-contained, easy to migrate
- **God nodes** (very high degree) - Migration blockers, need special handling
- **Bridge nodes** (connect communities) - Critical for phased migration planning

**Risk Areas:**
- **AMBIGUOUS edges** - Relationships graphify wasn't sure about, need manual verification
- **Surprising connections** - Unexpected dependencies that could cause issues
- **Large files** with high complexity - Expensive to migrate, higher risk
- **Platform-specific code** - May not have direct equivalents in target

### Step 4: Generate Migration Readiness Report

Create a structured report for the user that includes:

**Executive Summary**
- Brief overview of the codebase structure (from graph statistics)
- Overall migration complexity assessment (Low/Medium/High)
- Estimated effort and key challenges

**Dependency Analysis**
- Total count of files, modules, classes, functions (from graph.json nodes)
- Dependency graph statistics:
  - Total edges (dependencies)
  - Average degree (connectivity)
  - Number of communities (logical groupings)
  - Density (how interconnected the code is)
- List of external dependencies with migration notes
- **God nodes** that need special attention
- **Circular dependencies** that complicate phased migration

**Migration Strategy Recommendations**
- **Suggested migration order** based on graph analysis:
  - Start with leaf nodes (nothing depends on them)
  - Then migrate one community at a time (least coupled first)
  - God nodes last (after everything else is stable)
- **Phasing approach** - All-at-once vs incremental based on:
  - Community structure (strong communities → incremental migration)
  - Coupling density (low coupling → easier phasing)
  - Number of external dependencies
- **Critical path items** - God nodes and bridge nodes that block other work

**Risk Assessment**
- **High-risk areas:**
  - God nodes with high fan-in
  - Circular dependencies
  - Platform-specific code
  - Large, complex files
- **Potential blockers:**
  - External dependencies without target equivalents
  - Surprising connections not caught in initial design
  - Ambiguous relationships needing verification

**Next Steps**
- Specific, actionable items for starting the migration
- Recommended tools or libraries for the target ecosystem
- Testing strategy recommendations
- Validation checkpoints

## Output Format

Structure your migration analysis report like this:

```markdown
# Migration Analysis: [Source] → [Target]

## Executive Summary
[2-3 sentence overview based on graph analysis]

**Migration Complexity**: [Low/Medium/High]
**Estimated Effort**: [X weeks/months based on graph size and complexity]

## Codebase Structure (from Knowledge Graph)
- **Total Files**: [count from graph.json nodes]
- **Total Dependencies**: [count from graph.json edges]
- **Communities Detected**: [count from graph.json communities]
- **Average Connectivity**: [avg degree]
- **God Nodes**: [list top 5 highest-degree nodes]

## Dependency Analysis

### Critical Dependencies (High Fan-In)
[List nodes with most incoming edges - many files depend on these]

### Integration Points (High Fan-Out)
[List nodes with most outgoing edges - these depend on many others]

### Circular Dependencies
[List cycles detected in the graph]

### Community Structure
[Describe the detected communities and their coupling]

### External Dependencies
[List external libs/frameworks with notes on target equivalents]

## Migration Complexity Assessment

**Overall**: [Low/Medium/High]

**Reasoning**: [Explain based on graph metrics - density, god nodes, circular deps, etc.]

## Recommended Migration Strategy

### Phase 1: [Community/Layer Name]
[Which nodes to migrate first and why - based on graph structure]

### Phase 2: [Community/Layer Name]
[Next layer after foundation is stable]

### Phase 3: [Community/Layer Name]
[Final integration and cutover]

## Risk Areas
- **[Risk Category]**: [Specific nodes/edges from graph that pose risk]
- **[Risk Category]**: [Description and mitigation approach]

## Next Steps
1. [Specific actionable item based on graph insights]
2. [Specific actionable item]
3. [Specific actionable item]
```

## Key Principles

**Start with the Graph**: Don't jump straight to recommendations. First thoroughly understand the codebase structure from the knowledge graph. The quality of your migration analysis depends on how well you understand the graph data.

**Be Data-Driven**: Ground every recommendation in specific graph metrics. Don't say "X is complex" - say "X has in-degree of 47 and is in 3 circular dependency cycles."

**Use Graph Terminology**: Refer to specific nodes, edges, communities by their IDs or names from the graph. This makes the analysis concrete and verifiable.

**Prioritize Safety**: When recommending migration order, prioritize approaches that minimize risk based on graph structure:
- Leaf nodes first (nothing depends on them)
- Low-degree nodes before high-degree (simpler dependencies)
- Single community before multi-community (contained changes)
- Low-coupling edges before high-coupling (fewer ripple effects)

**Acknowledge Ambiguity**: The graph tags edges as EXTRACTED, INFERRED, or AMBIGUOUS. Call out AMBIGUOUS relationships that need manual verification before migration.

**Consider the Target**: Your recommendations should be informed by both the source codebase structure (from graph) AND the target ecosystem's idioms.

## Example: Analyzing God Nodes

From `GRAPH_REPORT.md`, you might see:

```
## God Nodes (Top 5)
1. src/users/models.py (degree: 47)
2. src/config/database.py (degree: 38)
3. src/payments/services.py (degree: 31)
```

In your report, explain:
- **What this means**: `users/models.py` has 47 connections - nearly every module touches it
- **Migration impact**: Changes here affect 47+ files, high risk of breaking things
- **Recommendation**: Migrate this LAST after everything else is stable, or use Strangler Fig pattern

## Example: Using Community Structure

From `graph.json`, you might find:

```json
"communities": [
  {"id": 0, "nodes": ["users/models.py", "users/services.py", "users/views.py"]},
  {"id": 1, "nodes": ["payments/models.py", "payments/stripe.py"]},
  {"id": 2, "nodes": ["analytics/tracker.py", "analytics/reports.py"]}
]
```

In your report, explain:
- **Community 1 (payments)** has only 2 nodes, minimal external connections → migrate first
- **Community 0 (users)** has 3 nodes but many external edges → migrate last
- **Community 2 (analytics)** is downstream (only incoming edges) → migrate early

---

Remember: The knowledge graph is your source of truth. Every migration recommendation should trace back to specific graph structure (nodes, edges, communities, metrics). Your job is to translate graph data into actionable migration guidance.
