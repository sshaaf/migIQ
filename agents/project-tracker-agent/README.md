# Project Tracker Agent

Main coordinator for the migration workflow. Receives context from `/migration` skill and orchestrates the complete migration process.

## Overview

The project tracker agent:
1. Executes three initial tasks (analyze, plan, generate backlog)
2. Manages the tasks.md file with all migration tasks and stories
3. Processes user stories by invoking story-orchestrator-agent
4. Integrates with Kanban boards for external tracking
5. Monitors progress and handles failures

## Usage

**Invoked by /migration skill:**
```bash
/migration --project-path ./my-app --migration-type framework
```

**Manual invocation (advanced):**
```bash
python3 project_tracker.py --context '{
  "sessionId": "mig-20260512-abc123",
  "traceId": "migration-session-abc123",
  "projectPath": "/path/to/project",
  "migrationType": "framework",
  "rulesPath": "./rule.md",
  "tasksPath": "./tasks.md",
  "mode": "interactive",
  "kanban": {
    "platform": "jira",
    "project": "PROJ-123"
  }
}'
```

## Workflow

### Phase 1: Initial Tasks

Executes three foundational tasks:

**TASK-001: Analyze Codebase**
- Skill: `/analyze-codebase`
- Output: `analysis-report.json`
- Updates tasks.md with analysis results

**TASK-002: Create Migration Plan**
- Skill: `/plan-migration`
- Input: `analysis-report.json`, `rule.md`
- Output: `migration-plan.json`
- Updates tasks.md with plan details

**TASK-003: Generate Backlog**
- Skill: `/generate-backlog`
- Input: `migration-plan.json`
- Output: User stories added to `tasks.md`
- Syncs with Kanban board if configured

### Phase 2: Process User Stories

For each user story in the backlog:

1. **Select next story** - Priority-based (P0 > P1 > P2 > P3)
2. **Update status** - Backlog → In Progress
3. **Invoke story-orchestrator-agent** - Passes story context
4. **Monitor progress** - Tracks execution through harnesses
5. **Handle result** - Update tasks.md and Kanban
6. **Continue to next** - Loop until all stories complete

## Tasks.md Management

The agent reads and writes tasks.md following this structure:

```markdown
## Initial Tasks

### TASK-001: Analyze Codebase
- **Status**: completed
- **Assignee**: project-tracker-agent
- **Outcome**: analysis-report.json
- **Started**: 2026-05-12T10:00:05Z
- **Completed**: 2026-05-12T10:02:30Z
- **Result**: ✓ Analysis complete, 150 files analyzed

## User Stories

### [US-001] Migrate Authentication Service
**Priority**: P0
**Status**: In Progress
**Story Points**: 8
...
```

### Task Status Values

- `pending` - Not started
- `in_progress` - Currently executing
- `completed` - Successfully finished
- `failed` - Execution failed

### Story Status Values

- `Backlog` - Not started
- `In Progress` - Currently being processed
- `Done` - Successfully completed
- `Failed` - Processing failed

## Kanban Integration

When Kanban configuration is provided, the agent:

1. **Creates tickets** - One per user story
2. **Syncs status** - Updates ticket status as stories progress
3. **Links artifacts** - Adds MR/PR links to tickets
4. **Updates fields** - Story points, assignee, labels

### Supported Platforms

- **Jira** - REST API integration
- **Linear** - GraphQL API integration
- **GitHub Projects** - GitHub API integration

## Error Handling

**Initial Task Failure:**
- Updates task status to `failed`
- Records error message in tasks.md
- Stops execution
- Returns failure status

**Story Failure:**
- Updates story status to `Failed`
- Invokes `failure-analyzer-agent` for root cause analysis
- In `autonomous` mode: Retries or continues
- In `interactive` mode: Pauses for human intervention

## Modes

**Interactive Mode (default):**
- Prompts before critical actions
- Pauses on story failures
- Better for first-time migrations

**Autonomous Mode:**
- Runs end-to-end without intervention
- Auto-retries on failures
- Only escalates on critical errors
- Better for trusted migrations

## Implementation Details

### Key Components

**TasksFileManager:**
- Reads/writes tasks.md
- Parses user stories using regex
- Updates task and story status
- Adds user stories from migration plan

**ProjectTrackerAgent:**
- Main coordinator class
- Executes initial tasks
- Processes user stories
- Invokes skills and agents
- Manages workflow state

### Skill Invocation

Skills are invoked via `execute_skill()` method:

```python
result = self.execute_skill('analyze-codebase', {
    'path': self.project_path,
    'migration_type': self.migration_type,
    'output': './analysis-report.json'
})
```

### Agent Invocation

Story-orchestrator-agent is invoked per story:

```python
story_result = self.invoke_story_orchestrator(story)
```

In production, this would use Claude Code agent invocation.

## Files Created

During execution, the agent creates:

- `analysis-report.json` - Codebase analysis results
- `migration-plan.json` - User stories and task breakdown
- Updates `tasks.md` - With stories, status, outcomes

## Monitoring

**Console Output:**
- Real-time progress updates
- Task status changes
- Skill execution results
- Error messages

**tasks.md:**
- Persistent task tracking
- Timestamped updates
- Outcome documentation
- Change history

**Kanban Board:**
- External visibility
- Team collaboration
- Status synchronization

## Example Output

```
============================================================
PROJECT TRACKER AGENT INITIALIZED
============================================================
Session ID: mig-20260512-abc123
Trace ID: migration-session-abc123
Project: /path/to/project
Migration Type: framework
Mode: interactive

============================================================
EXECUTING INITIAL TASKS
============================================================

[TASK-001] Analyze Codebase

→ Executing skill: analyze-codebase
  Args: {
    "path": "/path/to/project",
    "migration_type": "framework",
    "output": "./analysis-report.json"
  }
  ✓ Analysis complete: ./analysis-report.json
  Status: ✓ Completed

[TASK-002] Create Migration Plan

→ Executing skill: plan-migration
  Args: {
    "analysis_report": "./analysis-report.json",
    "rules": "./rule.md",
    "output": "./migration-plan.json"
  }
  ✓ Migration plan created: ./migration-plan.json
  Status: ✓ Completed

[TASK-003] Generate Backlog

→ Executing skill: generate-backlog
  Args: {
    "plan": "./migration-plan.json",
    "kanban_platform": "jira"
  }
  → Syncing with jira board...
    ✓ Created ticket: JIRA-001 - Migrate Authentication Service
    ✓ Created ticket: JIRA-002 - Update Shared Library Dependencies
    ✓ Created ticket: JIRA-003 - Migrate User Service
  ✓ Backlog generated: 3 stories added to ./tasks.md
  Status: ✓ Completed

============================================================
INITIAL TASKS COMPLETED SUCCESSFULLY
============================================================

============================================================
PROCESSING USER STORIES
============================================================

Found 3 stories in backlog

────────────────────────────────────────────────────────────
Story: [US-001] Migrate Authentication Service
Priority: P0, Points: 8
────────────────────────────────────────────────────────────

  → Invoking story-orchestrator-agent for US-001
    Command: claude-code agent run story-orchestrator-agent --story US-001
    → Story orchestrator would execute harness sequence
    → Test → Code → Benchmark → Evaluation → CI
  ✓ Story US-001 completed successfully

...
```

## Dependencies

- Python 3.7+
- Access to skills directory
- Write permissions for tasks.md and output files
- Optional: Kanban platform API credentials

## Testing

Test the agent with a sample context:

```bash
# Create test context
cat > test-context.json <<EOF
{
  "sessionId": "test-session-001",
  "traceId": "test-trace-001",
  "projectPath": "./sample-project",
  "migrationType": "framework",
  "rulesPath": "./rule.md",
  "tasksPath": "./tasks.md",
  "mode": "interactive"
}
EOF

# Run agent
python3 project_tracker.py --context "$(cat test-context.json)"
```

## Future Enhancements

- Real skill invocation via Claude Code API
- Real agent invocation for story-orchestrator
- Actual Kanban API integration
- Distributed tracing integration
- Webhook notifications
- Progress dashboard
