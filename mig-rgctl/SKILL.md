---
name: mig-rgctl
description: MigIQ-specific code knowledge graph analysis using rgctl. Use during MigIQ migrations when you need to index a codebase, validate graph artifacts, or query structure for prompt-building, planning, containerization, or execution. Prefer this over the generic rgctl skill inside MigIQ workflows — it documents MigIQ phase commands, required artifacts (.rgctl/, communities, migration_plan.json), and discover flags per stage. Trigger when migiq, mig-prompt-builder, mig-plan, mig-containerize, or mig-execute need graph analysis.
---

# MigIQ rgctl Analysis

MigIQ wraps the [rgctl](https://github.com/sshaaf/rgctl) CLI with phase-specific discover flags, artifact checks, and query recipes. For full CLI reference, also see the upstream **rgctl** skill (`rgctl install --skill`).

**Workflow reference (read for phase-specific commands):** [references/workflow.md](references/workflow.md)

## Quick Start

From the **application repo root** (not `migiq-workspace/`):

```bash
# MigIQ Phase 1 — full migration analysis
rgctl discover . --with-cfg --with-security --with-taint \
  --with-dashboard --with-harmonic --export-migration-hints
```

Do **not** use `rgctl -r PATH discover .` — the trailing `.` ignores `-r`.

## Validate Index Exists

Before any MigIQ skill queries the graph:

```bash
rgctl -f json metrics --pagerank
```

If this fails, run `discover` (see workflow.md for flags by phase) and STOP.

### Artifact locations

| Mode | Where artifacts live |
|------|----------------------|
| Default (daemon) | `~/.rgctl/cache/<reponame>/.rgctl/` |
| `--no-daemon` | `{repo}/.rgctl/` |

An in-repo `.rgctl/` directory is **not** required with the default daemon — check with `metrics`, not only `ls .rgctl`.

### Communities (subsystem mapping)

Communities are required for subsystem mapping in prompt-builder and containerize:

```bash
rgctl -f json communities list
rgctl -f json gql --macro-name all_communities unused
```

If `communities list` is empty, re-run discover with `--with-harmonic` (included in Phase 1 recipe above).

### Migration plan (when exported)

After discover with `--export-migration-hints`:

- `{artifact-root}/migration_plan.json`, or
- `{artifact-root}/dashboard/migration_plan.json`

## What MigIQ Skills Deduce from rgctl

| Capability | rgctl feature | Used by |
|------------|---------------|---------|
| Languages, frameworks, build tools | discover + GQL on modules/functions | mig-prompt-builder, mig-plan |
| Architecture (monolith vs modules) | communities list, pagerank | mig-prompt-builder, mig-plan |
| Hotspots / god nodes | metrics `--pagerank`, `--harmonic` | mig-prompt-builder, mig-plan, mig-execute |
| External dependencies | GQL USES/DEPENDSON, semantic search | mig-prompt-builder, mig-containerize |
| Migration ordering | `migration_plan.json`, Kantra (`--with-kantra`) | migiq, mig-plan |
| Security / secrets | `--with-security` | mig-containerize, mig-deploy |
| Containerization blockers | semantic query + taint (`--with-taint`) | mig-containerize |
| Refactor blast radius | `blast-radius`, CPG slice/flows | mig-execute |

See [references/workflow.md](references/workflow.md) for exact commands per MigIQ phase.

## Lighter Discover Profiles

Not every phase needs the full Phase 1 recipe:

```bash
# Containerization / deploy readiness (no migration plan)
rgctl discover . --with-cfg --with-security --with-taint --with-harmonic

# Quick re-index after small changes
rgctl discover .

# Java framework migration rules (Quarkus, Spring Boot 3+)
rgctl discover . -l java --with-kantra --kantra-target quarkus
```

## When to Use mig-rgctl vs rgctl

| Situation | Skill |
|-----------|-------|
| Inside `/migiq` or any MigIQ skill | **mig-rgctl** (this skill) |
| General codebase questions outside MigIQ | **rgctl** (upstream) |
| MCP / ad-hoc structural queries | **rgctl** |
