## Why

Legacy code migration is time-consuming, error-prone, and requires deep expertise. This AI-driven code migration system automates the analyze-plan-implement-validate workflow using Claude Code's Agent Mesh architecture, enabling high-quality migrations with minimal human intervention while maintaining full observability and control.

## What Changes

- Implement 6 specialized harness phases (Project Tracking, Test, Code, Benchmark, Evaluation, CI)
- Create 19 reusable skills across all harness phases for specific automation tasks
- Build 7 core agents using Agent Mesh architecture for autonomous workflow orchestration
- Integrate with CI/CD platforms (GitLab/GitHub) and Kanban boards for tracking
- Establish configuration system with `rule.md`, `tasks.md`, and `CLAUDE.md`
- Leverage opencode agent for all code analysis, refactoring, testing, and evaluation operations
- Implement comprehensive monitoring, KPI tracking, and distributed tracing
- Create feedback loops for continuous improvement and automated retry mechanisms

## Capabilities

### New Capabilities
<!-- Capabilities being introduced. Replace <name> with kebab-case identifier (e.g., user-auth, data-export, api-rate-limiting). Each creates specs/<name>/spec.md -->
- `project-tracking-harness`: Analyze codebase, plan migration, generate user story backlog, loop through stories
- `test-harness`: Generate characterization and functional tests, validate coverage requirements
- `code-harness`: Apply automated refactoring rules, generate spec-driven code, validate transformations
- `benchmark-harness`: Build benchmark suite, establish performance baselines, compare results
- `evaluation-harness`: Generate evaluation metrics, calculate test scores, validate quality thresholds
- `ci-harness`: Prepare merge requests, push to CI platform, monitor pipeline, handle results
- `agent-mesh-orchestration`: Distributed collaborative agent network for parallel execution and resilient workflows
- `skills-framework`: Reusable, focused commands for specific actions across all harness phases
- `configuration-management`: Migration rules, task definitions, and project-specific instructions
- `kpi-tracking`: Comprehensive metrics collection, trend analysis, and quality monitoring
- `failure-recovery`: Root cause analysis, automated retry mechanisms, and human escalation

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

**Code Structure**:
- New `.claude/` directory with agents and skills subdirectories
- Configuration files: `rule.md`, `tasks.md`, `CLAUDE.md`
- New directories: `specs/`, `rules/`, `benchmarks/`, `docs/adr/`

**Integrations**:
- CI/CD platforms (GitLab, GitHub) - API access for MR creation, pipeline monitoring
- Kanban boards (Jira, Linear, GitHub Projects) - Ticket management and status updates
- opencode agent - All code operations (analysis, refactoring, testing, evaluation)

**Dependencies**:
- Claude Code CLI or Desktop App
- opencode agent service
- CI platform API access
- Kanban board API access

**Workflows**:
- New automated migration workflow replacing manual processes
- Agent Mesh replaces traditional linear pipelines or CrewAI orchestration
- Feedback loops for continuous improvement and retry mechanisms
