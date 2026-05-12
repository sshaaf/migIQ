# Migration Workflow - Complete Flow

This document describes the complete migration workflow starting from the `/migration` command.

## Entry Point

**Command**: `/migration --project-path ./my-app --migration-type framework`

This is the recommended way to start any migration.

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ USER INVOKES                                                 │
├─────────────────────────────────────────────────────────────┤
│ /migration --project-path ./app --migration-type framework  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ MIGRATION SKILL (Orchestrator)                              │
├─────────────────────────────────────────────────────────────┤
│ 1. Validate inputs (path, migration type, etc.)            │
│ 2. Initialize context (create rule.md, tasks.md)           │
│ 3. Create initial task structure in tasks.md:              │
│    - TASK-001: Analyze codebase                            │
│    - TASK-002: Create migration plan                       │
│    - TASK-003: Generate backlog                            │
│ 4. Generate session ID and trace ID                        │
│ 5. Delegate to project-tracker-agent                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ PROJECT-TRACKER-AGENT (Main Coordinator)                    │
├─────────────────────────────────────────────────────────────┤
│ Receives context from /migration skill                      │
│                                                             │
│ PHASE 1: Execute Initial Tasks                             │
│ ────────────────────────────────────────                   │
│ TASK-001: /analyze-codebase                                │
│   → Output: analysis-report.json                           │
│   → Updates tasks.md with outcome                          │
│                                                             │
│ TASK-002: /plan-migration                                  │
│   → Input: analysis-report.json, rule.md                   │
│   → Output: migration-plan.json                            │
│   → Updates tasks.md with outcome                          │
│                                                             │
│ TASK-003: /generate-backlog                                │
│   → Input: migration-plan.json                             │
│   → Output: tasks.md updated with user stories             │
│   → Syncs with Kanban board                                │
│   → Updates tasks.md with outcome                          │
│                                                             │
│ PHASE 2: Process User Stories (Loop)                       │
│ ────────────────────────────────────────                   │
│ 1. Load user stories from tasks.md                         │
│ 2. Select next high-priority story                         │
│ 3. Invoke story-orchestrator-agent → per story             │
│ 4. Monitor story progress                                  │
│ 5. Handle completion/failure                               │
│ 6. Update tasks.md and Kanban                              │
│ 7. Loop to next story                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │ STORY-ORCHESTRATOR-AGENT (Per Story)  │
        │                                       │
        │ Receives story context from           │
        │ project-tracker-agent                 │
        └───────────────────────────────────────┘
                            ↓
    ┌───────────────────────────────────────────────┐
    │ HARNESS SEQUENCE (Sequential Execution)       │
    ├───────────────────────────────────────────────┤
    │                                               │
    │  ┌─────────────────────────────────────┐     │
    │  │ 1. TEST-GENERATOR-AGENT             │     │
    │  ├─────────────────────────────────────┤     │
    │  │ Skills:                             │     │
    │  │ ▸ /generate-characterization-tests  │     │
    │  │ ▸ /generate-functional-tests        │     │
    │  │ ▸ /validate-coverage                │     │
    │  │                                     │     │
    │  │ Outcome: Test suite created         │     │
    │  │ Updates: tasks.md with task result  │     │
    │  └─────────────────────────────────────┘     │
    │              ↓                                │
    │  ┌─────────────────────────────────────┐     │
    │  │ 2. CODE-REFACTOR-AGENT              │     │
    │  ├─────────────────────────────────────┤     │
    │  │ Skills:                             │     │
    │  │ ▸ /apply-refactor-rules             │     │
    │  │ ▸ /generate-spec-driven-code        │     │
    │  │ ▸ /validate-refactoring             │     │
    │  │                                     │     │
    │  │ Outcome: Refactored code            │     │
    │  │ Updates: tasks.md with task result  │     │
    │  └─────────────────────────────────────┘     │
    │              ↓                                │
    │  ┌─────────────────────────────────────┐     │
    │  │ 3. BENCHMARK-BUILDER-AGENT          │     │
    │  ├─────────────────────────────────────┤     │
    │  │ Skills:                             │     │
    │  │ ▸ /build-benchmark-suite            │     │
    │  │ ▸ /establish-baseline               │     │
    │  │ ▸ /run-benchmarks                   │     │
    │  │                                     │     │
    │  │ Outcome: Performance metrics        │     │
    │  │ Updates: tasks.md with task result  │     │
    │  └─────────────────────────────────────┘     │
    │              ↓                                │
    │  ┌─────────────────────────────────────┐     │
    │  │ 4. QUALITY-EVALUATOR-AGENT          │     │
    │  ├─────────────────────────────────────┤     │
    │  │ Skills:                             │     │
    │  │ ▸ /generate-evaluation-metrics      │     │
    │  │ ▸ /calculate-test-scores            │     │
    │  │ ▸ /validate-quality                 │     │
    │  │                                     │     │
    │  │ Outcome: Quality report             │     │
    │  │ Updates: tasks.md with task result  │     │
    │  └─────────────────────────────────────┘     │
    │              ↓                                │
    │  ┌─────────────────────────────────────┐     │
    │  │ 5. CI-INTEGRATION-AGENT             │     │
    │  ├─────────────────────────────────────┤     │
    │  │ Skills:                             │     │
    │  │ ▸ /prepare-merge-request            │     │
    │  │ ▸ /push-merge-request               │     │
    │  │ ▸ /monitor-pipeline                 │     │
    │  │ ▸ /handle-pipeline-result           │     │
    │  │                                     │     │
    │  │ Outcome: CI pipeline result         │     │
    │  │ Updates: tasks.md, Kanban           │     │
    │  └─────────────────────────────────────┘     │
    │                                               │
    └───────────────────────────────────────────────┘
                            ↓
                ┌──────────────────┐
                │  SUCCESS PATH    │
                ├──────────────────┤
                │ Story Complete   │
                │ Update tasks.md  │
                │ Update Kanban    │
                │ Next Story       │
                └──────────────────┘
                            ↓
            Return to project-tracker-agent
            (Loop to next story)

                ┌──────────────────┐
                │  FAILURE PATH    │
                ├──────────────────┤
                │ failure-analyzer │
                │ /request-root    │
                │ -cause           │
                │ Update tasks.md  │
                │ Retry or Escalate│
                └──────────────────┘
```

## Task-Driven Workflow

The `/migration` command creates a task-driven workflow where:

1. **Each task has an outcome** - Every task in tasks.md specifies what it produces
2. **Outcomes feed next tasks** - Task outputs become inputs for subsequent tasks
3. **Tasks.md is the source of truth** - All task status and outcomes tracked in tasks.md
4. **Kanban sync** - Tasks.md syncs with external Kanban board for visibility

## Example tasks.md Structure

After `/migration` runs:

```markdown
# Migration Tasks

## Session: mig-20260512-abc123
**Project**: ./my-app
**Type**: framework
**Started**: 2026-05-12T10:00:00Z
**Trace ID**: migration-session-abc123

## Initial Tasks

### TASK-001: Analyze Codebase
- **Status**: completed
- **Assignee**: project-tracker-agent
- **Outcome**: analysis-report.json
- **Started**: 2026-05-12T10:00:05Z
- **Completed**: 2026-05-12T10:02:30Z
- **Result**: ✓ Analysis complete, 150 files analyzed

### TASK-002: Create Migration Plan
- **Status**: completed
- **Assignee**: project-tracker-agent
- **Outcome**: migration-plan.json
- **Started**: 2026-05-12T10:02:35Z
- **Completed**: 2026-05-12T10:05:00Z
- **Result**: ✓ Plan created, 12 user stories identified

### TASK-003: Generate Backlog
- **Status**: completed
- **Assignee**: project-tracker-agent
- **Outcome**: tasks.md updated, Kanban synced
- **Started**: 2026-05-12T10:05:05Z
- **Completed**: 2026-05-12T10:06:00Z
- **Result**: ✓ Backlog generated, 12 tickets created in Jira

## User Stories

### US-001: Migrate authentication module
- **Status**: in_progress
- **Priority**: High
- **Story Points**: 8
- **Assignee**: story-orchestrator-agent
- **Started**: 2026-05-12T10:06:10Z
- **Tasks**:
  - TASK-004: Generate tests for auth module (completed)
  - TASK-005: Refactor auth module (in_progress)
  - TASK-006: Run benchmarks (pending)
  - TASK-007: Validate quality (pending)
  - TASK-008: Create MR (pending)

### US-002: Migrate data access layer
- **Status**: pending
- **Priority**: High
- **Story Points**: 13
...
```

## Supporting Agents

**Invoked as needed during workflow:**

- **kpi-tracker-agent** - Via `/generate-kpi-metrics` - Track progress metrics
- **documentation-manager-agent** - Via `/update-documentation` - Maintain rule.md, tasks.md
- **failure-analyzer-agent** - Via `/request-root-cause` - Analyze failures

## Human Intervention Points

The workflow can pause for human input at:

1. **After TASK-001 (Analysis)** - Review findings before planning
2. **After TASK-002 (Planning)** - Approve story breakdown
3. **After TASK-003 (Backlog)** - Confirm priorities
4. **On critical failures** - Decide on retry strategy
5. **Before CI push** - Final review before merge request

## Monitoring Progress

**Via tasks.md:**
- Real-time task status updates
- Outcome tracking for each task
- Session and trace IDs for correlation

**Via Kanban board:**
- Visual story progress
- Team collaboration
- Status synchronization

**Via KPI metrics:**
- Migration velocity
- Automation rate
- Quality scores
- Cycle time

## Modes

**Interactive Mode (default):**
```bash
/migration --project-path ./app --migration-type framework
```
- Prompts for confirmation at critical points
- Pauses for human review
- Better for first-time migrations

**Autonomous Mode:**
```bash
/migration --project-path ./app --migration-type framework --mode autonomous
```
- Runs end-to-end without intervention
- Only escalates on critical failures
- Better for trusted, repeatable migrations
