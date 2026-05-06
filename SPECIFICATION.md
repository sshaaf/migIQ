# Code Migration System - Implementation Specification

## Overview

This specification defines an automated, AI-driven **Code Migration** workflow using Claude Code harnesses (skills and agents) to orchestrate migration from planning through validation.

The architecture is based on the **Agent Mesh** approach, inspired by Red Hat's blog post on "Refactoring at the speed of mission" - a distributed, collaborative network of specialized AI agents working together to accomplish complex migration tasks.

**Reference**: [Agent Mesh Architecture Details](./AGENT-MESH.md)

## Architecture

The system follows a recursive loop: **Analyze → Plan → Implement → Validate**

### Core Components

1. **Harnesses** - Specialized workflow stages powered by Claude Code agents and skills
2. **CI Platform** - DevOps infrastructure (GitLab/GitHub) for verification
3. **Kanban Boards** - Visual tracking of user stories and progress
4. **Human Supervisor** - Developer/architect oversight and intervention

## Workflow Phases

### Phase 1: Project Tracking HARNESS
**Purpose**: Initiate and manage the migration backlog

**Inputs**:
- Migration requirements
- Codebase analysis
- Business rules (`rule.md`)
- Task definitions (`tasks.md`)

**Outputs**:
- User story backlog
- Prioritized migration tasks
- Updated task tracking

**Process**:
1. Analyze codebase for migration needs
2. Plan user stories based on migration scope
3. Generate backlog with priority ordering
4. Loop through each story for processing

### Phase 2: Test HARNESS
**Purpose**: Create comprehensive test coverage as safety net

**Inputs**:
- User story from backlog
- Existing codebase
- Current test coverage

**Outputs**:
- Characterization tests (capture current behavior)
- Functional tests for new behavior
- Code coverage reports

**Tools**:
- opencode agent (all test generation and analysis)

**Process**:
1. Generate characterization tests for existing code using opencode agent
2. Generate functional tests for expected behavior using opencode agent
3. Validate test coverage meets thresholds using opencode agent

### Phase 3: Code HARNESS
**Purpose**: Execute spec-driven refactoring and code transformation

**Inputs**:
- Generated specifications
- Test suite
- Refactoring rules

**Outputs**:
- Refactored code
- Migration artifacts
- Transformation logs

**Tools**:
- opencode agent (all refactoring and code generation)

**Process**:
1. Parse specifications from Test HARNESS using opencode agent
2. Apply refactoring rules using opencode agent
3. Generate new code based on specs using opencode agent
4. Validate against specifications using opencode agent

### Phase 4: Benchmark HARNESS
**Purpose**: Build formal benchmark and test suite

**Inputs**:
- Refactored code
- Test results
- Performance baselines

**Outputs**:
- Benchmark test suite
- Performance metrics
- Regression test suite

**Process**:
1. Compile successful code changes
2. Build benchmark suite from tests
3. Establish performance baselines
4. Package for evaluation

### Phase 5: Evaluation HARNESS
**Purpose**: Validate quality and correctness of migration

**Inputs**:
- Refactored code
- Test results
- Benchmark metrics

**Outputs**:
- Evaluation scores
- Quality metrics
- Pass/fail determination

**Tools**:
- opencode agent (all evaluation and validation)

**Process**:
1. Run evaluation metrics using opencode agent
2. Calculate test scores using opencode agent
3. Validate against quality thresholds using opencode agent
4. Generate evaluation report using opencode agent

### Phase 6: CI HARNESS
**Purpose**: Prepare and submit code for CI pipeline

**Inputs**:
- Validated code changes
- Test results
- Evaluation metrics

**Outputs**:
- Merge request
- CI pipeline trigger
- Integration metadata

**Process**:
1. Prepare merge request with all artifacts
2. Push to CI platform
3. Monitor CI pipeline execution

## CI Platform Integration

### Pipeline Flow
1. **RUN CI Pipeline**
2. **Decision Point**: Failed Tests / Failed Specs / Human Required?
   - **YES** → Close MR → Generate KPI Metrics (opencode agent) → Return to backlog
   - **NO** → Merge → Update Kanban

### KPI Tracking (using opencode agent)
- Test pass/fail rates
- Code coverage deltas
- Performance metrics
- Human intervention frequency

## Human Interaction Points

1. **Update Documentation**
   - `rule.md` - Migration rules and patterns
   - `tasks.md` - Task definitions and priorities

2. **Root Cause Analysis** (Optional)
   - Request deep analysis on failures
   - Add to tasks.md for retry

3. **Backlog Management**
   - Return issues to backlog
   - Adjust priorities
   - Refine specifications

## Feedback Loops

### Success Path
Project Tracking → Test → Code → Benchmark → Evaluation → CI → Merge → Kanban (Done)

### Failure Path
CI Platform → KPI Metrics → Kanban (Backlog) → Project Tracking (Retry)

## Data Flow

```
[Project Tracking HARNESS]
        ↓
[Test HARNESS] → [Code HARNESS] → [Evaluation HARNESS]
                        ↓                ↓
                [Benchmark HARNESS] -----+
                        ↓
                [CI HARNESS]
                        ↓
                [CI Platform]
                        ↓
                [Kanban Boards] ← [Human Supervisor]
                        ↓
            (loop back if needed)
```

## Implementation Approach

### Using Claude Code Agent Mesh

Replace CrewAI orchestration with **Agent Mesh** architecture:

1. **Skills** - Reusable, focused commands for specific actions (see `skills.md`)
2. **Agents** - Autonomous task executors for complex workflows (see `agents.md`)
3. **Agent Mesh** - Distributed, collaborative network of agents (see `AGENT-MESH.md`)

#### Why Agent Mesh Instead of CrewAI?

1. **Native Integration** - Claude Code harnesses provide better integration with development tools
2. **Flexibility** - Agent Mesh allows dynamic, parallel collaboration vs. CrewAI's sequential crews
3. **Performance** - Parallel execution without Python/framework overhead
4. **Tooling** - Direct access to git, CI/CD, and development tools
5. **Simplicity** - Skills and agents pattern is simpler to maintain and extend
6. **Scalability** - Distributed architecture scales horizontally

See [AGENT-MESH.md](./AGENT-MESH.md) for complete architecture details.

### Configuration Files

- `rule.md` - Migration rules, patterns, and constraints
- `tasks.md` - Task definitions and backlog
- `CLAUDE.md` - Project-specific instructions for Claude Code
- `.claude/` - Agent and skill definitions

## Success Criteria

1. **Automation Rate**: >80% of migrations complete without human intervention
2. **Quality**: All tests pass, code coverage maintained/improved
3. **Performance**: No regression in benchmark metrics
4. **Reliability**: Consistent feedback loop handling
5. **Traceability**: Full audit trail from story to merge

## Technical Stack

- **Claude Code** - Orchestration and AI agents
- **opencode agent** - All code analysis, generation, refactoring, testing, and evaluation
- **GitLab/GitHub** - CI platform
- **Kanban** - Project tracking

## Next Steps

1. Review and refine `skills.md` for each harness phase
2. Review and refine `agents.md` for orchestration logic
3. Create initial `rule.md` and `tasks.md` templates
4. Build skill implementations in `.claude/skills/`
5. Build agent definitions in `.claude/agents/`
6. Set up CI platform integration
7. Configure Kanban board automation
