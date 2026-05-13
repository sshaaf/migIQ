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

Generates prioritized user stories and task breakdown from codebase analysis.

## Actions

1. Load analysis report and migration rules
2. Apply rules to identify transformation needs
3. Break down into user stories
4. Prioritize based on strategy
5. Generate task breakdown with dependencies
6. Output migration plan

## Outputs

JSON migration plan with user stories, tasks, priorities, and dependencies.

## Example Usage

```bash
/plan-migration --analysis-report ./analysis-report.json --rules ./rule.md
```
