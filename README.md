# Code Migration System - Agent Mesh Implementation

An AI-driven code migration system using Claude Code's Agent Mesh architecture to automate the analyze-plan-implement-validate workflow.

> **📁 Demo Implementation**: A complete, working implementation is being built in the [`demo/`](./demo/) directory. See [demo/README.md](./demo/README.md) for setup and usage instructions.

## Overview

This project implements a comprehensive code migration system that leverages:
- **Agent Mesh Architecture** - Distributed, collaborative AI agents
- **Claude Code Harnesses** - Skills and agents for autonomous execution
- **CI/CD Integration** - Automated testing and deployment
- **Human-in-the-Loop** - Supervised automation with escalation

## Architecture

The system uses a recursive workflow: **Analyze → Plan → Implement → Validate**

### Key Components

1. **Harness Agents** - Specialized AI agents for each phase
2. **Skills** - Reusable, focused commands
3. **CI Platform** - DevOps infrastructure (GitLab/GitHub)
4. **Kanban Boards** - Visual project tracking
5. **Human Supervisor** - Oversight and intervention

## Documentation

### Core Documents

- **[SPECIFICATION.md](./SPECIFICATION.md)** - Complete implementation specification
- **[AGENT-MESH.md](./AGENT-MESH.md)** - Agent Mesh architecture details
- **[skills.md](./skills.md)** - All skill definitions and usage
- **[agents.md](./agents.md)** - All agent definitions and workflows
- **[vision.md](./vision.md)** - Original vision and workflow description

### Configuration Files (To Be Created)

- **rule.md** - Migration rules, patterns, and constraints
- **tasks.md** - Task definitions and backlog
- **CLAUDE.md** - Project-specific instructions for Claude Code

## Workflow Phases

### 1. Project Tracking HARNESS
- Analyze codebase for migration needs
- Plan user stories
- Generate and maintain backlog
- Loop through each story

**Agent**: `project-tracker-agent`

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

The system provides **19 specialized skills** across all harness phases:

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
- CI Platform (GitLab or GitHub)
- Kanban Board (Jira, Linear, or GitHub Projects)
- **opencode agent** (all code operations)

### Installation

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd app-mod-demo
   ```

2. **Verify Directory Structure**

   The following directories should already exist:
   ```
   .claude/
   ├── agents/          # Agent definitions
   └── skills/          # Skill implementations
   templates/           # Configuration templates
   specs/              # Specifications
   rules/              # Refactoring rules
   benchmarks/         # Performance benchmarks
   docs/
   └── adr/            # Architecture Decision Records
   ```

3. **Configure Environment Variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and fill in your actual values
   # At minimum, configure:
   # - CI_PLATFORM_TYPE and credentials (GitLab or GitHub)
   # - KANBAN_PLATFORM and credentials (Jira, Linear, or GitHub Projects)
   # - OPENCODE_AGENT_API and API key
   ```

4. **Initialize Configuration Files**
   ```bash
   # Copy configuration templates to your project
   cp templates/CLAUDE.md ./CLAUDE.md
   cp templates/rule.md ./rule.md
   cp templates/tasks.md ./tasks.md

   # Customize these files for your specific migration project
   ```

5. **Set Up Agents**
   ```bash
   # Agent definitions will be created in .claude/agents/
   # Each agent gets its own subdirectory with:
   # - agent.md (agent definition)
   # - config.yaml (agent configuration)
   # - workflows/ (agent workflows)
   ```

6. **Set Up Skills**
   ```bash
   # Skill implementations will be created in .claude/skills/
   # Each skill gets its own subdirectory with implementation
   ```

7. **Configure External Integrations**

   Ensure the following services are accessible:

   - **OpenCode Agent**: Running at configured endpoint (default: http://localhost:8080)
   - **CI Platform**: GitLab or GitHub with API access
   - **Kanban Board**: Jira, Linear, or GitHub Projects with API access

8. **Verify Installation**
   ```bash
   # Test environment configuration
   source .env && env | grep -E "CI_PLATFORM|KANBAN|OPENCODE"

   # Verify Claude Code is available
   claude-code --version

   # Test connectivity (once agents are implemented)
   # claude-code agent list
   ```

### Running the System

#### Start the Agent Mesh

```bash
# Start the project tracker agent (main loop)
claude-code agent run project-tracker-agent
```

#### Process a Single User Story

```bash
# Run story orchestrator for specific story
claude-code agent run story-orchestrator-agent --story US-123
```

#### Execute Individual Harness

```bash
# Run test harness
claude-code agent run test-generator-agent --story US-123

# Run code harness
claude-code agent run code-refactor-agent --story US-123

# Run evaluation harness
claude-code agent run quality-evaluator-agent --story US-123
```

#### Invoke Skills Directly

```bash
# Analyze codebase
claude-code skill /analyze-codebase --path ./src --migration-type framework

# Generate tests
claude-code skill /generate-characterization-tests --source-path ./src/main

# Apply refactoring using opencode agent
claude-code skill /apply-refactor-rules --source-path ./src --rules-path ./refactor-rules.yml
```

## Configuration

### rule.md
Defines migration rules, patterns, and constraints:
- Code transformation rules
- Architectural patterns
- Anti-patterns to avoid
- Quality thresholds
- Security requirements

### tasks.md
Defines task backlog and priorities:
- User stories
- Task breakdown
- Dependencies
- Priority ordering
- Assignment and status

### CLAUDE.md
Project-specific instructions for Claude Code:
- Coding standards
- Testing requirements
- CI/CD workflows
- Review processes

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

## Integration Points

### CI/CD Platforms

Supported platforms:
- **GitLab** - Full integration via API and webhooks
- **GitHub** - Full integration via API and webhooks

Features:
- Automatic MR/PR creation
- Pipeline triggering and monitoring
- Status checks and quality gates
- Artifact management

### Kanban Boards

Supported platforms:
- **Jira** - REST API integration
- **Linear** - GraphQL API integration
- **GitHub Projects** - GitHub API integration

Features:
- Automatic ticket creation
- Status synchronization
- Linking and dependencies
- Progress tracking

### Migration Tool

**opencode agent**:
- Code analysis and understanding
- Automated refactoring
- Code generation
- Test generation (characterization and functional)
- Specification validation
- Quality metrics and evaluation
- KPI tracking and reporting
- Multi-language support

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

## Project Status

**Current Phase**: Specification and Design

**Completed**:
- ✅ Vision and requirements
- ✅ Agent Mesh architecture design
- ✅ Skills definition (19 skills)
- ✅ Agents definition (7 agents)
- ✅ Specification document

**Next Steps**:
1. ✅ Create directory structure and templates
2. ✅ Set up environment configuration
3. Implement skills in `.claude/skills/` (19 skills)
4. Implement agents in `.claude/agents/` (7+ agents)
5. Set up CI platform integration (GitLab/GitHub)
6. Configure Kanban board automation (Jira/Linear/GitHub Projects)
7. Build monitoring and observability (distributed tracing, KPI dashboards)
8. Create example migration project
9. End-to-end testing
10. Production deployment

## Contributing

This project is in the design and specification phase. Contributions welcome for:
- Skill implementations
- Agent implementations
- Integration connectors
- Documentation improvements
- Example migrations

## References

- **Red Hat Blog**: [Refactoring at the speed of mission](https://www.redhat.com/en/blog/refactoring-speed-mission-agent-mesh-approach-legacy-system-modernization-red-hat-ai)
- **Claude Code**: [Documentation](https://claude.com/claude-code)

## License

[To be determined]

## Authors

- Vision and Architecture: Based on Red Hat Agent Mesh approach
- Implementation: Claude Code harness architecture

## Support

For questions and support:
- Open an issue in the repository
- Review the documentation in `docs/`
- Check the vision document: `vision.md`
- Review the Agent Mesh architecture: `AGENT-MESH.md`
