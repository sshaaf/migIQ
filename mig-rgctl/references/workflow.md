# MigIQ rgctl Workflow

Phase-specific rgctl commands for MigIQ skills. Upstream reference: [rgctl workflows](https://github.com/sshaaf/rgctl/blob/main/skills/rgctl/references/workflows.md).

## Artifact Checklist

Run these after `discover` to confirm the graph is usable:

```bash
# 1. Index exists
rgctl -f json metrics --pagerank

# 2. Communities present (required for subsystem mapping)
rgctl -f json communities list | jq '.communities | length'

# 3. Migration plan (only when --export-migration-hints was used)
test -f .rgctl/migration_plan.json || test -f .rgctl/dashboard/migration_plan.json \
  || ls ~/.rgctl/cache/*/.rgctl/migration_plan.json 2>/dev/null
```

With the default daemon, replace `.rgctl/` paths with the cache path under `~/.rgctl/cache/<reponame>/.rgctl/`.

---

## Phase 1: migiq — Full Migration Analysis

**Goal:** Knowledge graph + migration plan + security/taint for downstream skills.

```bash
cd <app-repo-root>

rgctl discover . --with-cfg --with-security --with-taint \
  --with-dashboard --with-harmonic --export-migration-hints \
  --migration-preset hybrid_default --migration-order scheduled
```

**Validate:**

```bash
rgctl -f json metrics --pagerank --communities | jq '.pagerank.top[:5]'
rgctl -f json communities list
rgctl -f json gql --macro-name all_communities unused
```

**Read:** `migration_plan.json` (or dashboard copy) for package ordering and hints.

| Flag | Why MigIQ needs it |
|------|-------------------|
| `--with-cfg` | CPG slice/flows during mig-execute |
| `--with-security` | Secrets scanning for containerize/deploy |
| `--with-taint` | Data-flow / injection risks |
| `--with-harmonic` | Migration hotspot ranking |
| `--export-migration-hints` | `migration_plan.json` for mig-plan |
| `--with-dashboard` | Human-readable migration dashboard |

---

## Phase 2: mig-prompt-builder — Current-State Summary

**Prerequisite:** Phase 1 discover completed (or equivalent).

**Queries to build the migration prompt:**

```bash
# Stack & scale
rgctl -f json metrics --pagerank --communities

# Subsystems / modules
rgctl -f json communities list

# Framework & dependency signals
rgctl -f json gql "MATCH (n:Function) RETURN n LIMIT 20"
rgctl -f json gql "MATCH (a)-[r:USES|DEPENDSON]->(b) RETURN a,b LIMIT 50"

# Migration plan context (if exported)
cat .rgctl/migration_plan.json   # or daemon cache path
```

**Deduce for migration-prompt.md:**

- Languages, frameworks, build system (from discover language + GQL)
- Monolith vs modular (community count, pagerank distribution)
- Integration points (USES/DEPENDSON edges, external libs)
- Risk hotspots (pagerank top, harmonic if enabled)
- Suggested migration order (`migration_plan.json` packages)
- Technical risks (security findings, taint paths, Kantra violations if `--with-kantra`)

---

## Phase 3: mig-plan — Task & Story Generation

**Prerequisite:** `mig-prompt-workspace/migration-prompt.md` + indexed graph.

```bash
# Confirm communities for task grouping
rgctl -f json communities list

# Per-community scope for task groups
rgctl -f json gql --macro-name all_communities unused

# Blast radius for high-risk tasks
rgctl -f json blast-radius <Symbol> --depth 2

# Migration package order
# read migration_plan.json → map packages to task groups
```

---

## mig-containerize — Containerization Readiness

**Prerequisite:** Graph indexed. Prefer discover with `--with-cfg --with-security --with-taint --with-harmonic` if not already done.

**Step 1 — Verify index + communities:**

```bash
rgctl -f json metrics --pagerank
rgctl -f json communities list    # STOP if empty — re-discover with --with-harmonic
```

**Step 2 — Language, dependencies, blockers:**

```bash
rgctl -f json gql "MATCH (n:Function) RETURN n LIMIT 20"
rgctl -f json metrics --pagerank --communities
rgctl -f json gql "MATCH (a)-[r:USES|DEPENDSON]->(b) RETURN a,b LIMIT 50"
rgctl -f json semantic query "file path upload storage localhost" --limit 10
```

**Map communities → container boundaries:** Each named community is a candidate deployable unit or shared library layer.

| Concern | rgctl command |
|---------|---------------|
| External DB/cache/queue | GQL USES/DEPENDSON |
| Hardcoded paths / localhost | semantic query + source grep |
| Secrets in config | `--with-security` findings |
| Tainted input → filesystem | `--with-taint` paths |
| Shared library coupling | communities list + blast-radius |

---

## mig-execute — During Implementation

```bash
# Before changing a symbol
rgctl -f json blast-radius <Symbol> --depth 2

# Call neighborhood
rgctl -f json gql "MATCH (a:Function)-[:CALLS*1..3]->(b:Function) WHERE a.name = '<fn>' RETURN a,b LIMIT 50"

# Data flow (requires --with-cfg discover)
rgctl -f json cpg flows <file> --line <n> --variable <var> --function <fn> --direction forward
```

---

## mig-test-gen / mig-deploy

```bash
# Test scope — community under test
rgctl -f json gql "MATCH (f:Function) WHERE f.community_id = '<id>' RETURN f LIMIT 20"

# Deploy — external dependencies & ports (from graph + manifests)
rgctl -f json gql "MATCH (a)-[r:USES|DEPENDSON]->(b) RETURN a,b LIMIT 50"
rgctl -f json metrics --pagerank   # prioritize smoke tests on hotspots
```

---

## Discover Flag Cheat Sheet (by MigIQ stage)

| Stage | Recommended discover flags |
|-------|---------------------------|
| migiq Phase 1 | `--with-cfg --with-security --with-taint --with-dashboard --with-harmonic --export-migration-hints` |
| mig-prompt-builder | *(reuse Phase 1 index)* |
| mig-plan | *(reuse Phase 1 index)* + read `migration_plan.json` |
| mig-containerize | `--with-cfg --with-security --with-taint --with-harmonic` (if re-indexing) |
| mig-execute | *(reuse index)*; `--with-cfg` required for CPG slice/flows |
| Java framework migration | add `--with-kantra --kantra-target <target>` |

Full flag reference: [rgctl Migration Feature-Flag Cheat Sheet](https://github.com/sshaaf/rgctl/blob/main/skills/rgctl/references/workflows.md#migration-feature-flag-cheat-sheet).
