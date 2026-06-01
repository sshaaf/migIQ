# MigIQ - Intelligent Application Migration Platform

**AI-powered application migration orchestrator for modernizing legacy applications to cloud-native platforms.**

[![Status](https://img.shields.io/badge/status-ready--for--testing-green)]()
[![Migration Success](https://img.shields.io/badge/migration-5--phase--orchestration-blue)]()
[![Platform](https://img.shields.io/badge/platform-OpenShift-red)]()

---

## Overview

MigIQ is a comprehensive migration solution that combines knowledge graph analysis, intelligent planning, and autonomous execution to migrate applications across platforms, frameworks, and languages.

### What Makes MigIQ Different

**Traditional Migrations**:
- Manual analysis of codebase
- Manually create migration plan
- Manually execute tasks
- Hope you didn't miss anything

**MigIQ Migrations**:
```bash
cd my-spring-app
/migiq
"Migrate this to Quarkus for OpenShift"
# → Complete migration with analysis, plan, execution, and deployment artifacts
```

---

## 🚀 Quick Start

### Interactive Migration (30-60 minutes)
```bash
cd /path/to/your/app
# In Claude Code, type:
/migiq
"Migrate this Spring Boot app to Quarkus"
```

### Autonomous Migration (background, multi-hour)
```javascript
Agent({
  description: "Migrate to Quarkus",
  prompt: `Follow AGENT.md at /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: Migrate this application from Spring Boot to Quarkus.
  Working Directory: /path/to/your/app
  
  Requirements:
  - Target: Quarkus 3.x
  - Deployment: Red Hat OpenShift
  - Approach: Phased migration
  
  Follow the 5-phase migiq workflow. Update me at major milestones.`
})
```

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
│ • Code graph  │ ────►   │                  │ ────► │ • spec.md   │
│ • Dependencies│         │ • Source tech    │       │ • design.md │
│ • Architecture│         │ • Target tech    │       │ • tasks.md  │
│ • Complexity  │         │ • Constraints    │       │ • stories   │
└──────────────-┘         └──────────────────┘       └─────────────┘
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

---

## 📦 Project Structure

```
migIQ/
├── README.md                   # This file - project overview
├── AGENT.md                    # Autonomous migrator agent definition
├── AGENT_EXAMPLES.md           # 6 example agent prompts
├── SESSION_SUMMARY.md          # Development session log
│
├── migiq/                      # Main orchestration skill
│   ├── README.md              # Skill documentation
│   ├── SKILL.md               # Skill definition (5-phase workflow)
│   ├── TEST_PLAN.md           # Testing strategy
│   ├── test-validator.sh      # Output validation script
│   └── evals/
│       └── evals.json         # Test case definitions
│
├── mig-graphify/              # Phase 1: Codebase analysis
│   └── SKILL.md
│
├── mig-prompt-builder/         # Phase 2: Requirements gathering
│   └── SKILL.md
│
├── mig-plan/                   # Phase 3: Migration planning
│   └── SKILL.md
│
├── mig-execute/                # Phase 4: Migration execution
│   └── SKILL.md
│
├── mig-test-gen/               # Testing integration
│   └── SKILL.md
│
├── mig-containerize/           # Containerization integration
│   └── SKILL.md
│
└── mig-deploy/                 # OpenShift deployment
    └── SKILL.md
```

---

## 🎯 Use Cases

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

---

## 💡 Two Execution Modes

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
```javascript
Agent({
  description: "Migrate to Quarkus",
  prompt: `Follow AGENT.md. Migrate from Spring Boot to Quarkus...`
})
```

See [AGENT_EXAMPLES.md](./AGENT_EXAMPLES.md) for 6 complete example prompts.

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
│   ├── spec.md              # Current state + target state
│   ├── design.md            # Architecture design
│   ├── tasks.md             # Detailed task breakdown
│   └── UserStory.md         # User stories
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

---

## 🔧 Supported Technologies

### Source Platforms
- Java EE, Spring Boot, Play Framework
- Node.js, Express, NestJS
- Python Django, Flask, FastAPI
- Ruby on Rails
- .NET Framework, ASP.NET

### Target Platforms
- Quarkus, Spring Boot, Micronaut (Java/JVM)
- Node.js (modern), Next.js, Remix (JavaScript/TypeScript)
- FastAPI, Django 4+ (Python)
- .NET 8 (C#)

### Deployment Targets
- Red Hat OpenShift (primary)
- Kubernetes
- Container platforms (Docker, Podman)

---

## 📈 Migration Success Metrics

Typical migration outcomes:

| Metric | Target | Typical Result |
|--------|--------|----------------|
| Code Coverage | 80%+ | 85-95% |
| Task Success Rate | 90%+ | 85-100% |
| Manual Intervention | < 10% | 5-15% |
| Deployment Ready | Yes | Yes (with containers + manifests) |

---

## 🧪 Testing

### Quick Validation
```bash
# After migration:
cd your-migrated-app
bash /path/to/migiq/test-validator.sh
```

### Comprehensive Testing
See [migiq/TEST_PLAN.md](./migiq/TEST_PLAN.md) for full testing procedures.

### Example Test Cases
1. Spring Boot → Quarkus (~35 min)
2. Node.js Express Modernization (~25 min)
3. Java EE → Spring Boot (~50 min)

---

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

## 🤝 Contributing

### Improving Skills
1. Test existing skills on new codebases
2. Document edge cases and solutions
3. Add new migration patterns
4. Improve error handling

### Adding Test Cases
1. Add to `migiq/evals/evals.json`
2. Run with test-validator.sh
3. Document results
4. Submit improvements

### Extending Platforms
1. Add new source/target platform support
2. Update skill definitions
3. Add example migrations
4. Document platform-specific patterns

---

## 🔍 Troubleshooting

### Migration Fails at Phase 1 (Analysis)
**Issue**: Graphify can't analyze codebase  
**Fix**: Check that graphify CLI is installed and accessible

### Migration Fails at Phase 4 (Execution)
**Issue**: Some tasks fail during execution  
**Expected**: This is normal for complex migrations  
**Action**: Review EXECUTION_REPORT.md for specific failures and remediation options

### Agent Doesn't Respond
**Issue**: Agent spawned but no updates  
**Check**: Agent might be waiting for permissions  
**Fix**: Check permission prompts, approve necessary actions

### Final Report Missing
**Issue**: Migration completes but no report  
**Fix**: Check `migiq-workspace/` directory, may be in different location

---

## 📞 Support

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

## 📄 License

Part of the Konveyor project.

---

## 🎯 Roadmap

### Current (v1.0)
- ✅ 5-phase orchestration workflow
- ✅ Interactive and autonomous modes
- ✅ 7 core migration skills
- ✅ OpenShift deployment integration
- ✅ Comprehensive reporting

### Planned (v1.1)
- [ ] Multi-stage migrations (incremental modernization)
- [ ] Rollback and recovery features
- [ ] Migration telemetry dashboard
- [ ] Pre-migration cost estimation
- [ ] Post-migration performance comparison

### Future (v2.0)
- [ ] AI-powered migration strategy recommendations
- [ ] Cross-cloud platform support
- [ ] Migration pattern library
- [ ] Automated post-migration optimization
- [ ] Integration with CI/CD pipelines

---

**Ready to migrate?** Start with [migiq/README.md](./migiq/README.md) or [AGENT_EXAMPLES.md](./AGENT_EXAMPLES.md)

**Questions?** Check the [troubleshooting](#-troubleshooting) section or review the [documentation](#-documentation)
