# Implementation Guide

This document describes the implemented components of the Agent Mesh for Code Migration.

## Prerequisites

**CRITICAL**: Before using this migration system, you MUST install graphify:

```bash
uv tool install graphifyy && graphify install
```

**Why this is required:**
- Agents use `/graphify` skill (installed by `graphify install`) for code analysis
- PreAgentExecution hook depends on `/graphify .` command
- Java EE migration requires semantic extraction to detect:
  - EJB annotations (@Stateless, @MessageDriven, @Stateful)
  - javax.* imports
  - Migration patterns
- Without graphify, agents will fail during execution

**Verification:**
```bash
/graphify --help  # Should show usage information
ls ~/.claude/skills/graphify/  # Should show SKILL.md
```

## Overview

The migration system is triggered by the `/migration` command which delegates to the `project-tracker-agent` to orchestrate the complete workflow.

## Implemented Components

### 1. `/migration` Skill (Main Entry Point)

**Location**: `skills/migration/`

**Files**:
- `skill.md` - Skill specification
- `migration.py` - Python implementation
- `tasks.md.template` - Template for tasks.md file

**What it does**:
1. Validates input parameters (project path, migration type, etc.)
2. Creates/initializes `rule.md` if missing
3. Creates `tasks.md` with initial task structure:
   - TASK-001: Analyze codebase
   - TASK-002: Create migration plan
   - TASK-003: Generate backlog
4. Generates session ID and trace ID
5. Invokes `project-tracker-agent` with context

**Usage**:
```bash
/migration --project-path ./my-app --migration-type framework

# With Kanban integration
/migration \
  --project-path ./my-app \
  --migration-type framework \
  --kanban-platform jira \
  --kanban-project PROJ-123

# Autonomous mode
/migration --project-path ./my-app --migration-type framework --mode autonomous
```

### 2. Project Tracker Agent (Main Coordinator)

**Location**: `agents/project-tracker-agent/`

**Files**:
- `agent.md` - Agent specification
- `project_tracker.py` - Python implementation
- `README.md` - Detailed implementation guide

**What it does**:

**Phase 1: Execute Initial Tasks**
- TASK-001: Invokes `/analyze-codebase` → produces `analysis-report.json`
- TASK-002: Invokes `/plan-migration` → produces `migration-plan.json`
- TASK-003: Invokes `/generate-backlog` → updates `tasks.md` with user stories

**Phase 2: Process User Stories**
- Reads user stories from `tasks.md`
- Selects next high-priority story (P0 > P1 > P2 > P3)
- Updates story status: Backlog → In Progress
- Invokes `story-orchestrator-agent` for each story
- Handles results and updates `tasks.md`
- Syncs with Kanban board if configured

**Key Features**:
- **TasksFileManager class**: Reads/writes/parses tasks.md
  - `read_tasks()` - Read entire file
  - `parse_user_stories()` - Extract user stories using regex
  - `update_task_status()` - Update individual task status
  - `update_story_status()` - Update user story status
  - `add_user_stories_from_plan()` - Add stories from migration plan

- **ProjectTrackerAgent class**: Main coordinator
  - `execute_skill()` - Invoke skills (analyze, plan, generate-backlog)
  - `execute_initial_tasks()` - Run TASK-001, TASK-002, TASK-003
  - `process_user_stories()` - Loop through backlog
  - `invoke_story_orchestrator()` - Delegate to story-orchestrator-agent

**Usage**:
```bash
# Automatically invoked by /migration skill
/migration --project-path ./my-app --migration-type framework

# Manual invocation (advanced)
python3 agents/project-tracker-agent/project_tracker.py --context '{
  "sessionId": "mig-20260512-abc123",
  "traceId": "migration-session-abc123",
  "projectPath": "/path/to/project",
  "migrationType": "framework",
  "rulesPath": "./rule.md",
  "tasksPath": "./tasks.md",
  "mode": "interactive"
}'
```

### 3. Tasks.md Structure

The agent uses a structured tasks.md format based on the template from `/Users/sshaaf/git/java/app-mod-demo/templates/tasks.md`.

**Key Sections**:

```markdown
# Migration Tasks

## Session: mig-YYYYMMDD-xxxxxxxx
**Project**: ./project-path
**Type**: framework
**Started**: ISO timestamp
**Trace ID**: migration-session-xxxxxxxx

## Initial Tasks

### TASK-001: Analyze Codebase
- **Status**: pending|in_progress|completed|failed
- **Assignee**: project-tracker-agent
- **Outcome**: analysis-report.json
- **Started**: timestamp or -
- **Completed**: timestamp or -
- **Result**: outcome message

### TASK-002: Create Migration Plan
...

### TASK-003: Generate Backlog
...

## User Stories

### [US-001] Story Title
**Priority**: P0|P1|P2|P3
**Status**: Backlog|In Progress|Done|Failed
**Story Points**: N
**Assigned To**: agent-name

**Description**: ...
**Acceptance Criteria**: ...
**Technical Details**: ...
**Tasks**: ...
**Notes**: ...
**Links**: ...

## Backlog Overview
| Status | Count | % |

## Metrics
Velocity, quality metrics, cycle time, automation metrics

## Risk Register
Risk tracking table
```

### 4. Integration Points

**Kanban Integration** (Simulated):
- Creates tickets for each user story
- Syncs status updates
- Supports: Jira, Linear, GitHub Projects

**CI/CD Integration** (Future):
- GitLab and GitHub support
- MR/PR creation and monitoring

**Skills Invoked**:
- `/analyze-codebase` - TASK-001
- `/plan-migration` - TASK-002
- `/generate-backlog` - TASK-003

**Agents Invoked**:
- `story-orchestrator-agent` - Per user story

## Workflow Example

```
┌─────────────────────────────────────────────────────────────┐
│ USER                                                         │
├─────────────────────────────────────────────────────────────┤
│ /migration --project-path ./app --migration-type framework  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ /migration SKILL                                            │
├─────────────────────────────────────────────────────────────┤
│ 1. Validate inputs                                          │
│ 2. Create rule.md (if missing)                              │
│ 3. Create tasks.md with TASK-001, 002, 003                 │
│ 4. Generate session ID: mig-20260512-abc123                │
│ 5. Generate trace ID: migration-session-abc123             │
│ 6. Invoke project-tracker-agent ↓                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PROJECT-TRACKER-AGENT                                       │
├─────────────────────────────────────────────────────────────┤
│ PHASE 1: Initial Tasks                                      │
│                                                             │
│ TASK-001: /analyze-codebase                                │
│   → analysis-report.json created                           │
│   → tasks.md updated: TASK-001 = completed                 │
│                                                             │
│ TASK-002: /plan-migration                                  │
│   → migration-plan.json created                            │
│   → tasks.md updated: TASK-002 = completed                 │
│                                                             │
│ TASK-003: /generate-backlog                                │
│   → User stories added to tasks.md                         │
│   → Kanban tickets created (if configured)                 │
│   → tasks.md updated: TASK-003 = completed                 │
│                                                             │
│ PHASE 2: Process User Stories                              │
│                                                             │
│ For each story in backlog (by priority):                   │
│   1. Update status: Backlog → In Progress                  │
│   2. Invoke story-orchestrator-agent                       │
│   3. Monitor execution                                     │
│   4. Update status: In Progress → Done/Failed              │
│   5. Update tasks.md and Kanban                            │
│   6. Continue to next story                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (Story processing continues
                     via story-orchestrator-agent)
```

## Files Created During Execution

1. **rule.md** - Migration rules and patterns (if not exists)
2. **tasks.md** - Task tracking and user stories
3. **analysis-report.json** - Codebase analysis results
4. **migration-plan.json** - User stories and priorities

## Current Implementation Status

✅ **Implemented**:
- `/migration` skill - Entry point
- `project-tracker-agent` - Main coordinator
- TasksFileManager - tasks.md parsing and updating
- Initial tasks execution (analyze, plan, generate-backlog)
- User story processing loop
- Kanban integration (simulated)
- Session and trace ID generation
- Error handling and status updates

⏳ **Simulated** (Ready for Real Integration):
- Skill invocation (uses placeholder implementations)
- Agent invocation (uses placeholder for story-orchestrator)
- Kanban API calls (shows what would be created)

🔜 **Future Enhancements**:
- Real Claude Code skill invocation via API
- Real agent invocation for story-orchestrator
- Actual Kanban API integration (Jira, Linear, GitHub)
- CI/CD integration
- Distributed tracing integration
- Progress webhooks and notifications

## Testing the Implementation

### Quick Test

```bash
# Navigate to the mesh repo
cd /path/to/mig-agent-mesh

# Run the migration command
python3 skills/migration/migration.py \
  --project-path ./sample-project \
  --migration-type framework

# This will:
# 1. Create rule.md and tasks.md
# 2. Invoke project-tracker-agent
# 3. Execute initial tasks (simulated)
# 4. Process user stories (simulated)
```

### With Kanban

```bash
python3 skills/migration/migration.py \
  --project-path ./sample-project \
  --migration-type framework \
  --kanban-platform jira \
  --kanban-project PROJ-123
```

### Check Results

After execution, check:
- `rule.md` - Migration rules template created
- `tasks.md` - Initial tasks + user stories added
- `analysis-report.json` - Analysis results
- `migration-plan.json` - Migration plan with user stories

## Integration with Other Agents

The project-tracker-agent is designed to work with:

1. **story-orchestrator-agent** - Processes individual stories
2. **failure-analyzer-agent** - Analyzes failures
3. **kpi-tracker-agent** - Generates metrics
4. **documentation-manager-agent** - Updates documentation

These agents are invoked as needed during story processing.

## Next Steps

To complete the implementation:

1. **Implement remaining agents**:
   - story-orchestrator-agent
   - test-generator-agent
   - code-refactor-agent
   - benchmark-builder-agent
   - quality-evaluator-agent
   - ci-integration-agent
   - failure-analyzer-agent
   - kpi-tracker-agent
   - documentation-manager-agent

2. **Implement remaining skills**:
   - All 26 skills need real implementations
   - Currently using simulated/placeholder logic

3. **Real integrations**:
   - Kanban API integration (Jira, Linear, GitHub)
   - CI/CD integration (GitLab, GitHub)
   - Distributed tracing setup
   - Webhook notifications

4. **Testing**:
   - End-to-end testing with real projects
   - Integration testing with external services
   - Error handling and recovery scenarios

## Documentation

- **Main README**: Overview and quick start
- **Migration Flow**: Complete workflow diagram (`docs/migration-flow.md`)
- **Agent Documentation**: Per-agent specs in `agents/*/agent.md`
- **Skill Documentation**: Per-skill specs in `skills/*/skill.md`
- **This Document**: Implementation guide
