# MigIQ - Intelligent Application Migration Platform

**AI-powered application migration orchestrator for modernizing legacy applications to cloud-native platforms.**

[![Status](https://img.shields.io/badge/status-ready--for--testing-green)]()
[![Migration Success](https://img.shields.io/badge/migration-5--phase--orchestration-blue)]()
[![Platform](https://img.shields.io/badge/platform-OpenShift-red)]()
[![npm version](https://img.shields.io/npm/v/@sshaaf/migiq)]()

---

## 🚀 Quick Start

Install MigIQ for Claude Code with a single command:

```bash
# Install to local project .claude directory (recommended)
npx @sshaaf/migiq

# Or install globally to ~/.claude
npx @sshaaf/migiq -g
```

Then in Claude Code:
```
/migiq
"Migrate this Spring Boot app to Quarkus"
```

Or for autonomous migration:
```
Agent({
  description: "Spring Boot to Quarkus migration",
  prompt: "Follow AGENT.md. Migrate this Spring Boot application to Quarkus...",
  subagent_type: "general-purpose"
})
```

---

## Overview

MigIQ is a comprehensive migration solution that combines knowledge graph analysis, intelligent planning, and autonomous execution to migrate applications across platforms, frameworks, and languages.

## Two Execution Modes

### Interactive Mode (`/migiq` skill)

**Best for:**
- Learning how migrations work
- Migrations < 1 hour
- Active participation desired
- Approving each phase

**Usage:**
```bash
cd my-app
# In Claude Code:
/migiq
"Migrate to [target technology]"
```

---

### Autonomous Mode (Migrator Agent)

**Best for:**
- Migrations > 1 hour
- Background/overnight work
- Parallel multi-app migrations
- When you trust the process

**Usage:**
```
Follow AGENT.md. Migrate from Spring Boot to Quarkus...

```

See [AGENT_EXAMPLES.md](./AGENT_EXAMPLES.md) for 6 complete example prompts.


---

## 🏗️ Architecture

### The MigIQ Ecosystem

```
                  ┌─────────────────────────────────────────────────────────────┐
                  │                      MigIQ Platform                         │
                  ├─────────────────────────────────────────────────────────────┤
                  │                                                             │
                  │  ┌──────────────┐              ┌─────────────────────┐      │
                  │  │   /migiq     │              │  Migrator Agent     │      │
                  │  │   Skill      │◄────────────►│  (AGENT.md)         │      │
                  │  │              │              │                     │      │
                  │  │ Interactive  │              │  Autonomous         │      │
                  │  │ Orchestration│              │  Long-running       │      │
                  │  └──────┬───────┘              └──────────┬──────────┘      │
                  │         │                                 │                 │
                  │         └─────────────┬───────────────────┘                 │
                  │                       │                                     │
                  │         ┌─────────────▼────────────────┐                    │
                  │         │   Core Migration Skills      │                    │
                  │         ├──────────────────────────────┤                    │
                  │         │                              │                    │
                  │         │  1. mig-graphify             │ ← Analysis         │
                  │         │  2. mig-prompt-builder       │ ← Requirements     │
                  │         │  3. mig-plan                 │ ← Planning         │
                  │         │  4. mig-execute              │ ← Execution        │
                  │         │  5. mig-test-gen             │ ← Testing          │
                  │         │  6. mig-containerize         │ ← Containers       │
                  │         │  7. mig-deploy               │ ← Deployment       │
                  │         │                              │                    │
                  │         └──────────────────────────────┘                    │
                  │                                                             │
                  └───────────────────────────────────────────────────────────--┘
```

### 5-Phase Migration Workflow

```
Phase 1: Analysis          Phase 2: Requirements      Phase 3: Planning
                  ┌──────────────-┐         ┌──────────────────┐       ┌─────────────┐
                  │ mig-graphify  │         │ mig-prompt-      │       │  mig-plan   │
                  │               │         │ builder          │       │             │
                  │ • Code graph  │ ────►   │                  │ ────► │ • tasks.md  │
                  │ • Dependencies│         │ • Source tech    │       │ • stories   │
                  │ • Architecture│         │ • Target tech    │       │             │
                  │ • Complexity  │         │ • Constraints    │       │ (uses       │
                  └──────────────-┘         │ • migration-     │       │ migration-  │
                                            │   prompt.md      │       │ prompt.md)  │
                                            └──────────────────┘       └─────────────┘
                                                                              │
                                                                              ▼
                  Phase 5: Reporting        Phase 4: Execution
                  ┌──────────────┐          ┌─────────────────────────┐
                  │ Final Report │  ◄────   │    mig-execute          │
                  │              │          │                         │
                  │ • Summary    │          │ • Code changes          │
                  │ • Metrics    │          │ • Tests (mig-test-gen)  │
                  │ • Next steps │          │ • Containers            │
                  │              │          │ • OpenShift manifests   │
                  └──────────────┘          └─────────────────────────┘
```

## 🎯 Many Use Cases (supports 31 languages)

### 1. Platform Migrations
- Java EE → Spring Boot → Quarkus
- .NET Framework → .NET 8
- Node.js 12 → Node.js 20
- Rails → Node.js/Python

### 2. Cloud Migrations
- On-prem → OpenShift
- Traditional VMs → Containers
- Monolith → Microservices

### 3. Modernization
- Legacy patterns → Modern idioms
- Callbacks → async/await
- Old dependencies → Latest versions
- Manual deployment → CI/CD

### 4. Language Migrations
- Java → Kotlin
- JavaScript → TypeScript
- Python 2 → Python 3


### 5. Target Platforms
- Quarkus, Spring Boot, Micronaut (Java/JVM)
- Node.js (modern), Next.js, Remix (JavaScript/TypeScript)
- FastAPI, Django 4+ (Python)
- .NET 8 (C#)

### 6. Deployment Targets
- Red Hat OpenShift (primary)
- Kubernetes
- Container platforms (Docker, Podman)
---

## 📊 What You Get

After a migration, you'll have:

```
your-project/
├── graphify-out/              # Phase 1: Analysis
│   ├── graph.json            # Knowledge graph
│   ├── GRAPH_REPORT.md       # Analysis report
│   └── graph.html            # Interactive visualization
│
├── mig-prompt-workspace/      # Phase 2: Requirements
│   └── migration-prompt.md   # Standardized prompt
│
├── mig-plan-workspace/        # Phase 3: Planning
│   ├── tasks.md             # Detailed task breakdown
│   └── UserStory.md         # User stories
│   # Note: spec/design in migration-prompt.md (Phase 2)
│
├── mig-execute-workspace/     # Phase 4: Execution
│   ├── EXECUTION_REPORT.md  # Execution results
│   ├── execution-log.md     # Detailed timeline
│   └── outputs/
│       ├── tests/           # Generated tests
│       ├── containers/      # Dockerfiles
│       └── deployments/     # OpenShift YAMLs
│
└── migiq-workspace/           # Phase 5: Orchestration
    ├── orchestration-log.md # Full orchestration log
    └── MIGRATION_REPORT.md  # ⭐ Share with stakeholders
```

## 📚 Documentation

### Getting Started
- [migiq/README.md](./migiq/README.md) - Skill quick start
- [AGENT_EXAMPLES.md](./AGENT_EXAMPLES.md) - Agent usage examples

### Deep Dives
- [migiq/SKILL.md](./migiq/SKILL.md) - Complete orchestration workflow
- [AGENT.md](./AGENT.md) - Autonomous agent definition
- [migiq/TEST_PLAN.md](./migiq/TEST_PLAN.md) - Testing strategy

### Individual Skills
- [mig-graphify/SKILL.md](./mig-graphify/SKILL.md) - Code analysis
- [mig-prompt-builder/SKILL.md](./mig-prompt-builder/SKILL.md) - Requirements
- [mig-plan/SKILL.md](./mig-plan/SKILL.md) - Planning
- [mig-execute/SKILL.md](./mig-execute/SKILL.md) - Execution

---

## 🎓 Examples

### Example 1: Spring Boot to Quarkus
```
User: "Migrate this Spring Boot app to Quarkus"

MigIQ:
✅ Analyzed: 42 classes, 15 REST endpoints
✅ Plan: 47 tasks across 8 user stories
✅ Executed: 45/47 tasks successful
✅ Result: Containerized Quarkus app ready for OpenShift

Time: 38 minutes
Report: migiq-workspace/MIGRATION_REPORT.md
```

### Example 2: Overnight Java EE Migration
```
User: Agent({ ... migrate Java EE to Spring Boot overnight })

Agent (6 hours later):
✅ Migrated: 80K LOC from Java EE to Spring Boot
✅ Converted: 52 EJBs to Spring beans
✅ Tests: 87% coverage
⚠️ Manual review: 3 stateful EJBs (see report)

Report: migiq-workspace/MIGRATION_REPORT.md
```

### Example 3: Parallel Microservices Upgrade
```
User: [Spawns 5 agents for 5 microservices]

All agents (30 min later):
✅ user-service: Node 12 → 20 ✅
✅ product-service: Node 12 → 20 ✅
✅ order-service: Node 12 → 20 ✅
✅ notification-service: Node 12 → 20 ✅
✅ analytics-service: Node 12 → 20 ✅

Total time: 30 minutes (parallel)
Sequential would take: 2.5 hours
```

---

## 🛡️ Best Practices

### Before Migration
1. ✅ Commit all changes (git status clean)
2. ✅ Run existing tests (establish baseline)
3. ✅ Backup database if applicable
4. ✅ Review current architecture

### During Migration
1. ✅ Monitor progress logs
2. ✅ Review generated plan before execution
3. ✅ Don't interrupt long-running operations
4. ✅ Save checkpoints frequently

### After Migration
1. ✅ Review migration report
2. ✅ Run full test suite
3. ✅ Compare performance (before/after)
4. ✅ Deploy to dev/staging first
5. ✅ Monitor for issues

---



### Documentation
- [Full skill documentation](./migiq/SKILL.md)
- [Agent guide](./AGENT.md)
- [Testing procedures](./migiq/TEST_PLAN.md)

### Debugging
- Check `orchestration-log.md` for workflow trace
- Review `execution-log.md` for detailed timeline
- Validate outputs with `test-validator.sh`

### Issues
For bugs or feature requests, document:
1. Source and target technologies
2. Migration phase that failed
3. Error messages from logs
4. Steps to reproduce

---

**Ready to migrate?** Start with [migiq/README.md](./migiq/README.md) or [AGENT_EXAMPLES.md](./AGENT_EXAMPLES.md)
