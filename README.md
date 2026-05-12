# Agent Mesh for Code Migration

A reusable Agent Mesh package providing specialized agents and skills for AI-driven code migration using Claude Code's Agent Mesh architecture.

## Overview

This package provides a complete set of mesh components for code migration:
- **10 Specialized Agents** - Collaborative AI agents for migration workflows
- **26 Skills** - Reusable, focused commands across all migration phases
- **Agent Mesh Architecture** - Distributed, autonomous execution patterns
- **OpenSpec Tracking** - Structured proposals and specifications

## Architecture

The system uses a recursive workflow: **Analyze → Plan → Implement → Validate**

### Key Components

1. **Harness Agents** - Specialized AI agents for each phase
2. **Skills** - Reusable, focused commands
3. **CI Platform** - DevOps infrastructure (GitLab/GitHub)
4. **Kanban Boards** - Visual project tracking
5. **Human Supervisor** - Oversight and intervention

## Package Structure

```
/agents/              # 10 specialized mesh agents
/skills/              # 26 migration skills
/openspec/            # Proposals and specifications
/docs/                # Core mesh documentation
  ├─ agent-mesh-infrastructure.md
  ├─ testing-guide.md
  ├─ distributed-tracing.md
  ├─ failure-recovery.md
  └─ kpi-tracking.md
README.md             # This file
```

## Documentation

### Implementation
- **[IMPLEMENTATION.md](./IMPLEMENTATION.md)** - Complete implementation guide for project-tracker-agent
- **[Migration Flow](./docs/migration-flow.md)** - Detailed workflow and task structure

### Architecture
- **[Agent Mesh Infrastructure](./docs/agent-mesh-infrastructure.md)** - Core architecture and patterns
- **[Testing Guide](./docs/testing-guide.md)** - How to test the mesh
- **[Distributed Tracing](./docs/distributed-tracing.md)** - Mesh observability
- **[Failure Recovery](./docs/failure-recovery.md)** - Error handling and recovery
- **[KPI Tracking](./docs/kpi-tracking.md)** - Metrics and reporting

## Getting Started - Quick Command

To start a migration, use the main `/migration` command:

```bash
/migration --project-path ./my-app --migration-type framework
```

This command:
1. Validates inputs and initializes the migration context
2. Creates `rule.md` and `tasks.md` if they don't exist
3. Delegates to `project-tracker-agent` which creates and executes tasks
4. Returns a session ID and trace ID for monitoring

## Workflow Phases

### 1. Project Tracking HARNESS
- Analyze codebase for migration needs
- Plan user stories
- Generate and maintain backlog
- Loop through each story

**Agent**: `project-tracker-agent`
**Triggered by**: `/migration` skill

### 2. Test HARNESS
- Generate characterization tests (capture current behavior)
- Generate functional tests (define expected behavior)
- Validate test coverage

**Agent**: `test-generator-agent`
**Tools**: opencode agent

### 3. Code HARNESS
- Apply automated refactoring
- Generate spec-driven code
- Validate transformations

**Agent**: `code-refactor-agent`
**Tools**: opencode agent

### 4. Benchmark HARNESS
- Build benchmark test suite
- Establish performance baselines
- Run benchmarks and compare

**Agent**: `benchmark-builder-agent`

### 5. Evaluation HARNESS
- Generate comprehensive evaluation metrics
- Calculate test scores
- Validate quality thresholds

**Agent**: `quality-evaluator-agent`
**Tools**: opencode agent

### 6. CI HARNESS
- Prepare merge requests
- Push to CI platform
- Monitor pipeline execution
- Handle results and feedback

**Agent**: `ci-integration-agent`
**Tools**: GitLab/GitHub API, opencode agent (KPI metrics)

## Agent Mesh Architecture

The system uses a **distributed mesh of specialized agents** that collaborate autonomously:

```
project-tracker-agent (Coordination Layer)
    ↓
story-orchestrator-agent (Per-story orchestration)
    ↓
    ├─ test-generator-agent ──────┐
    ├─ code-refactor-agent        ├── Parallel execution
    ├─ benchmark-builder-agent    │   where possible
    └─ quality-evaluator-agent ───┘
          ↓
    ci-integration-agent (Integration)
          ↓
    CI Platform → Kanban → (loop if needed)
```

**Supporting Agents**:
- `failure-analyzer-agent` - Root cause analysis
- `documentation-manager-agent` - Knowledge management
- `kpi-tracker-agent` - Metrics and reporting

See [AGENT-MESH.md](./AGENT-MESH.md) for detailed architecture.

## Skills Overview

The system provides **27 specialized skills** across all harness phases:

### Main Orchestration (1 skill)
- `/migration` - Main entry point to start migration workflow

### Project Tracking (3 skills)
- `/analyze-codebase` - Analyze codebase for migration needs
- `/plan-migration` - Create migration plan from analysis
- `/generate-backlog` - Generate and update Kanban backlog

### Testing (3 skills)
- `/generate-characterization-tests` - Capture current behavior
- `/generate-functional-tests` - Define expected behavior
- `/validate-coverage` - Validate coverage meets requirements

### Code (3 skills)
- `/apply-refactor-rules` - Apply refactoring using opencode agent
- `/generate-spec-driven-code` - Generate code from specifications
- `/validate-refactoring` - Validate refactored code

### Benchmarking (3 skills)
- `/build-benchmark-suite` - Compile benchmark suite
- `/establish-baseline` - Establish performance baseline
- `/run-benchmarks` - Execute and compare benchmarks

### Evaluation (3 skills)
- `/generate-evaluation-metrics` - Generate quality metrics
- `/calculate-test-scores` - Calculate test scores
- `/validate-quality` - Validate quality thresholds

### CI Integration (4 skills)
- `/prepare-merge-request` - Prepare MR with artifacts
- `/push-merge-request` - Push to CI platform
- `/monitor-pipeline` - Monitor CI pipeline
- `/handle-pipeline-result` - Handle pipeline results

### Cross-Cutting (3 skills)
- `/generate-kpi-metrics` - Generate KPI metrics
- `/update-documentation` - Update rule.md and tasks.md
- `/request-root-cause` - Root cause analysis for failures

See [skills.md](./skills.md) for complete skill documentation.

## Feedback Loops

### Success Path
```
Project Tracking → Test → Code → Benchmark → Evaluation → CI → Merge → Done
```

### Failure Path
```
CI Platform → KPI Metrics → Root Cause Analysis → Backlog → Retry
```

### Human Intervention Points

1. **Update Documentation** - Refine `rule.md` and `tasks.md`
2. **Root Cause Analysis** - Deep analysis on failures
3. **Backlog Management** - Adjust priorities and refinements

## Getting Started

### Prerequisites

- Claude Code CLI or Desktop App
- Target project using this mesh for code migration

### Using This Mesh

This is a **reusable mesh package** meant to be integrated into your migration project:

1. **Clone or Install the Mesh**
   ```bash
   git clone <repository-url>
   cd mig-agent-mesh
   ```

2. **Review Agents**

   Explore the 10 specialized agents in `/agents/`:
   - `project-tracker-agent` - Main coordination loop
   - `story-orchestrator-agent` - Per-story orchestration
   - `test-generator-agent` - Test creation harness
   - `code-refactor-agent` - Code transformation harness
   - `benchmark-builder-agent` - Performance benchmarking
   - `quality-evaluator-agent` - Quality validation
   - `ci-integration-agent` - CI/CD integration
   - `failure-analyzer-agent` - Root cause analysis
   - `documentation-manager-agent` - Knowledge management
   - `kpi-tracker-agent` - Metrics and reporting

3. **Review Skills**

   Browse the 26 skills in `/skills/` organized by phase:
   - Project Tracking: analyze, plan, generate backlog
   - Testing: characterization tests, functional tests, coverage
   - Code: refactoring, spec-driven generation, validation
   - Benchmarking: build suite, baseline, run benchmarks
   - Evaluation: metrics, scoring, quality validation
   - CI Integration: MR preparation, pipeline monitoring
   - Cross-Cutting: KPI metrics, documentation, root cause

4. **Review OpenSpec Proposals**

   Check `/openspec/` for structured specifications and proposals

5. **Integration**

   Copy or reference agents and skills from your migration project's `.claude/` directory

### Using the Migration System

**Start a Migration (Recommended):**
```bash
# Basic migration
/migration --project-path ./my-app --migration-type framework

# With full configuration
/migration \
  --project-path ./my-app \
  --migration-type framework \
  --kanban-platform jira \
  --kanban-project PROJ-123 \
  --ci-platform gitlab

# Autonomous mode (no prompts)
/migration --project-path ./my-app --migration-type framework --mode autonomous
```

**Advanced: Run Agents Directly:**
```bash
# Start project tracker manually
claude-code agent run project-tracker-agent --context '{"sessionId":"...","traceId":"..."}'

# Run specific harness
claude-code agent run test-generator-agent --story US-123
```

**Invoke Individual Skills:**
```bash
# Analyze codebase
/analyze-codebase --path ./src --migration-type framework

# Generate tests
/generate-characterization-tests --source-path ./src/main

# Apply refactoring
/apply-refactor-rules --source-path ./src --rules-path ./rules.yml
```

## Configuration for Your Project

When using this mesh in your migration project, you'll need:

**rule.md** - Migration rules, patterns, and constraints:
- Code transformation rules
- Architectural patterns
- Anti-patterns to avoid
- Quality thresholds
- Security requirements

**tasks.md** - Task backlog and priorities:
- User stories
- Task breakdown
- Dependencies
- Priority ordering
- Assignment and status

**CLAUDE.md** - Project-specific instructions for Claude Code:
- Coding standards
- Testing requirements
- CI/CD workflows
- Review processes

**.env** - Environment configuration:
- CI platform credentials (GitLab/GitHub)
- Kanban board credentials (Jira/Linear/GitHub Projects)
- External tool configurations

## Monitoring and Observability

### KPI Dashboard

Track key metrics:
- **Migration Velocity** - Stories completed per day
- **Automation Rate** - % of migrations without human intervention
- **Quality Score** - Aggregate quality metrics
- **Cycle Time** - Time from story start to merge
- **Success Rate** - % of migrations that pass first time

### Distributed Tracing

Each story has a trace ID that flows through all agents:
```
Trace: migration-story-US123
  ├─ project-tracker-agent (10s)
  ├─ story-orchestrator-agent (300s)
  │   ├─ test-generator-agent (120s)
  │   ├─ code-refactor-agent (100s)
  │   ├─ benchmark-builder-agent (50s)
  │   └─ quality-evaluator-agent (30s)
  └─ ci-integration-agent (200s)
```

### Logs and Metrics

All agents produce:
- **Structured logs** - JSON formatted, searchable
- **Metrics** - Prometheus-compatible
- **Traces** - OpenTelemetry compatible
- **Events** - Event stream for real-time monitoring

## Supported Integrations

The mesh agents and skills are designed to integrate with:

**CI/CD Platforms:**
- GitLab - MR creation, pipeline monitoring
- GitHub - PR creation, workflow monitoring

**Kanban Boards:**
- Jira - REST API integration
- Linear - GraphQL API integration
- GitHub Projects - API integration

**Code Operations:**
- opencode agent - All code analysis, refactoring, testing, and evaluation

Your project must configure these integrations for the mesh to function.

## Success Criteria

1. **Automation Rate** - >80% of migrations complete without human intervention
2. **Quality** - All tests pass, code coverage maintained/improved
3. **Performance** - No regression in benchmark metrics
4. **Reliability** - Consistent feedback loop handling
5. **Traceability** - Full audit trail from story to merge

## Technical Stack

- **Orchestration** - Claude Code (Agent Mesh architecture)
- **Languages** - Java, Python, JavaScript (examples)
- **Code Operations** - opencode agent (all analysis, refactoring, testing, evaluation)
- **CI/CD** - GitLab, GitHub
- **Tracking** - Jira, Linear, GitHub Projects

## Package Status

**Current State**: Core mesh components with working implementation

**Included**:
- ✅ 10 Specialized agents (1 implemented: project-tracker-agent)
- ✅ 27 Migration skills (1 implemented: /migration)
- ✅ Agent Mesh architecture documentation
- ✅ OpenSpec proposal tracking
- ✅ Core operational docs
- ✅ Tasks.md template for tracking
- ✅ Working migration orchestration flow

**Implemented & Ready**:
- ✅ `/migration` command - Main entry point
- ✅ `project-tracker-agent` - Full Python implementation
  - Executes initial tasks (analyze, plan, generate-backlog)
  - Parses and updates tasks.md
  - Processes user stories
  - Integrates with Kanban (simulated)
- ✅ TasksFileManager - tasks.md parsing and updates
- ✅ Session and trace ID generation
- ✅ Error handling and status tracking

**Usage**:
This is a **reusable mesh package**. To use it:
1. Clone this repository
2. Run: `/migration --project-path ./your-app --migration-type framework`
3. The system creates rule.md, tasks.md and executes the migration workflow
4. Monitor progress in tasks.md or your Kanban board

## Contributing

Contributions welcome for:
- New or improved agents
- New or improved skills
- Documentation enhancements
- OpenSpec proposals
- Integration examples

## References

- **Red Hat Blog**: [Refactoring at the speed of mission](https://www.redhat.com/en/blog/refactoring-speed-mission-agent-mesh-approach-legacy-system-modernization-red-hat-ai)
- **Claude Code**: [Documentation](https://claude.com/claude-code)

## License

[To be determined]

## Authors

- Architecture: Based on Red Hat Agent Mesh approach
- Implementation: Claude Code Agent Mesh architecture

## Support

For questions and support:
- Open an issue in the repository
- Review the documentation in `/docs/`
- Check OpenSpec proposals in `/openspec/`
