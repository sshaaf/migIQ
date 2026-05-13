---
name: plan-migration
description: Create migration plan from analysis report by applying rules. Use when the user wants to plan a migration, create migration strategy, prioritize migration work, generate user stories from analysis, or develop a migration roadmap.
---

Create migration plan from analysis report by applying rules from rule.md.

## Parameters

- `--analysis-report` (required): Path to analysis report JSON
- `--rules` (required): Path to rule.md file
- `--strategy` (optional): Prioritization strategy (risk, complexity, business-value, default: risk)
- `--output` (optional): Output path for migration plan (default: ./migration-plan.json)

## Description

Generates prioritized user stories and task breakdown from codebase analysis. Uses Graphify graph to understand dependencies and prioritize work.

## Code Analysis Strategy

**Use Graphify to enhance planning:**

1. **Review architecture overview:**
   ```bash
   cat graphify-out/GRAPH_REPORT.md
   # Understand god nodes, communities, and architectural layers
   ```

2. **Identify critical dependencies:**
   ```bash
   /graphify query "Find most connected classes"
   # High-degree nodes should be prioritized carefully
   ```

3. **Find dependency clusters:**
   ```bash
   # Communities in GRAPH_REPORT.md show natural work boundaries
   # Use these to group related user stories
   ```

4. **Understand transformation impact:**
   ```bash
   /graphify path "SourceClass" "TargetClass"
   # Long paths = higher risk, plan accordingly
   ```

**Use graph metrics for prioritization:**
- God nodes (high degree) = higher risk, need careful planning
- Leaf nodes (low degree) = lower risk, good early wins
- Community boundaries = natural story boundaries

## Actions

1. Load analysis report and migration rules
2. Review Graphify GRAPH_REPORT.md for architecture insights
3. Use graph metrics to assess risk (node degree, centrality)
4. Apply rules to identify transformation needs
5. Break down into user stories using community structure
6. Prioritize based on strategy + graph metrics
7. Generate task breakdown with dependencies from graph
8. Output migration plan with dependency ordering

## Outputs

JSON migration plan with user stories, tasks, priorities, and dependencies.

## Example Usage

```bash
/plan-migration --analysis-report ./analysis-report.json --rules ./rule.md
```
