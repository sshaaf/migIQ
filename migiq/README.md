# MigIQ - Complete Application Migration Orchestrator

**Version**: 1.0  
**Status**: Ready for Testing  
**Author**: Created for Konveyor MigIQ Project

## Overview

MigIQ is an end-to-end orchestration skill that automates complete application migration workflows. It chains together all mig-* skills in the correct sequence to deliver a comprehensive migration from analysis to deployment.

## What It Does

When you say **"migrate this app to Quarkus"** (or any target technology), MigIQ automatically:

1. **Analyzes** your codebase using [rgctl](https://github.com/sshaaf/rgctl) knowledge graphs
2. **Gathers** migration requirements through interactive prompts
3. **Plans** the migration with detailed tasks and user stories
4. **Executes** the migration plan with automated implementation
5. **Reports** comprehensive results in a stakeholder-ready document

All automatically. No need to invoke each skill separately.

## Quick Start

```bash
# Navigate to your project
cd /path/to/your/app

# Invoke the skill in Claude Code
/migiq
```

Then provide your migration goal:
```
Migrate this Spring Boot app to Quarkus and deploy it to OpenShift
```

The orchestrator handles the rest.

## Example Use Cases

- **"Migrate this app to Quarkus"** - Java EE/Spring Boot → Quarkus migration
- **"Modernize this Node.js application"** - Legacy Node.js → modern patterns
- **"Port this to microservices on OpenShift"** - Monolith decomposition + cloud deployment
- **"Migrate from Rails to Node.js"** - Cross-language migration

## What You Get

After the orchestration completes, you'll have:

```
your-project/
├── rgctl index                # Phase 1: Analysis
│   ├── graph.json
│   ├── rgctl metrics / migration plan
│   └── graph.html
│
├── mig-prompt-workspace/      # Migration requirements
│   └── migration-prompt.md
│
├── mig-plan-workspace/        # Detailed planning
│   ├── tasks.md
│   └── UserStory.md
│   # Note: spec/design in migration-prompt.md (Phase 2)
│
├── mig-execute-workspace/     # Implementation results
│   ├── EXECUTION_REPORT.md
│   ├── execution-log.md
│   └── outputs/
│       ├── tests/
│       ├── containers/
│       └── deployments/
│
└── migiq-workspace/           # Orchestration summary
    ├── orchestration-log.md
    └── MIGRATION_REPORT.md    ⭐ Share this with stakeholders
```

## Key Features

### 🔄 Full Automation
Runs all 5 phases automatically. Only pauses if errors occur or clarification is needed.

### 🛡️ Failure Recovery
Handles errors gracefully. Stops on critical failures, presents options, waits for your decision.

### 📊 Comprehensive Reporting
Generates stakeholder-ready migration reports that synthesize all phases.

### 🚀 OpenShift Ready
Always includes containerization and OpenShift deployment artifacts.

### ✅ Actionable Deliverables
Produces real code changes, tests, containers, and deployment configs - not just plans.

## File Structure

```
migiq/
├── README.md                  # This file
├── SKILL.md                   # Skill definition and workflow
├── TEST_PLAN.md              # Testing strategy and procedures
├── test-validator.sh          # Automated output validation
└── evals/
    └── evals.json            # Test case definitions
```

## Testing

See [TEST_PLAN.md](./TEST_PLAN.md) for comprehensive testing instructions.

**Quick validation**:

```bash
# After running migiq, validate outputs
cd your-project
bash /path/to/migiq/test-validator.sh
```

## Time Expectations

| Project Size | Expected Duration |
|--------------|-------------------|
| Small (<10K LOC) | 15-30 minutes |
| Medium (10-50K LOC) | 30-60 minutes |
| Large (>50K LOC) | 60-120 minutes |

Duration depends on codebase complexity, migration scope, and target technology.

## Dependencies

**Required:**
- **rgctl** CLI + skill ([rgctl](https://github.com/sshaaf/rgctl)) — codebase analysis
- **Cursor** or **Claude Code** with skills

**Installed by MigIQ:**
- **mig-prompt-builder** - Migration requirements gathering
- **mig-plan** - Comprehensive migration planning
- **mig-execute** - Automated migration execution

**Optional (later phases):** OpenShift CLI (`oc`), Podman/Docker for containerize/deploy.

## Limitations

1. **Interactive requirements**: Phase 2 may ask clarifying questions - this is expected
2. **Execution failures**: Complex migrations may have partial execution success - the skill reports failures clearly
3. **Time intensive**: Full migrations take 30-90 minutes - plan accordingly
4. **Permission prompts**: May pause for file/command permissions if not pre-configured

## When NOT to Use This Skill

Use individual skills instead if you:
- Only want code analysis → use **rgctl** directly
- Only want to create a plan → use **mig-plan** directly
- Only want to execute an existing plan → use **mig-execute** directly
- Want to explore migration options → use **mig-prompt-builder** directly

MigIQ is for **"I want to migrate this app, make it happen"** workflows.

## Examples

### Example 1: Spring Boot to Quarkus

**Input**:
```
/migiq

"Migrate this Spring Boot REST API to Quarkus. We have Spring Data JPA, 
Spring Security, and about 15 controllers. Need it running on OpenShift."
```

**What happens**:
1. Graphify analyzes Spring components
2. Prompt builder captures Quarkus target, OpenShift platform
3. Planner creates migration tasks (Spring → Quarkus annotations, dependency updates)
4. Executor implements changes, generates tests, creates Dockerfile, produces OpenShift YAMLs
5. Reporter synthesizes comprehensive migration summary

**Time**: ~35-45 minutes

---

### Example 2: Node.js Modernization

**Input**:
```
/migiq

"This Node.js app is from 2016. Help me modernize it and get it ready for OpenShift."
```

**What happens**:
1. Graphify analyzes Node.js structure
2. Prompt builder asks about target Node version, patterns to adopt
3. Planner creates modernization tasks (async/await, error handling, dependency updates)
4. Executor implements improvements, adds containerization
5. Reporter provides modernization summary

**Time**: ~25-35 minutes

---

### Example 3: Java EE to Spring Boot

**Input**:
```
/migiq

"Migrate this old Java EE app to Spring Boot. It has lots of EJBs."
```

**What happens**:
1. Graphify identifies EJB structure, entity beans, deployment descriptors
2. Prompt builder captures Spring Boot version, decomposition approach
3. Planner creates EJB → Spring conversion tasks
4. Executor implements migration (may have partial success on complex EJBs)
5. Reporter documents what succeeded, what needs manual attention

**Time**: ~50-70 minutes

## Contributing

To improve this skill:

1. Run test cases and document results
2. Identify workflow issues or missing features
3. Update SKILL.md with improvements
4. Add new test cases to evals/evals.json
5. Re-validate with test-validator.sh

## Support

For issues or questions:
- Review TEST_PLAN.md for troubleshooting guidance
- Check orchestration-log.md for detailed workflow traces
- Examine individual skill outputs for phase-specific issues

## License

Part of the Konveyor MigIQ project.
