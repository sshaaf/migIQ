---
name: migration
trigger: /migration
description: Main orchestrator command to initiate and manage the complete code migration workflow. Use when the user wants to start a migration, migrate a codebase, run a full migration project, or coordinate end-to-end migration work. This is the primary entry point for all migration tasks.
---

Main orchestrator command to initiate and manage the complete code migration workflow.

## Parameters

- `--project-path` (required): Path to the project to migrate
- `--migration-type` (required): Type of migration (framework, language, platform, custom)
- `--rules` (optional): Path to rule.md file (default: ./rule.md)
- `--tasks` (optional): Path to tasks.md file (default: ./tasks.md)
- `--kanban-platform` (optional): Kanban platform (jira, linear, github-projects)
- `--kanban-project` (optional): Kanban project/board ID
- `--ci-platform` (optional): CI platform (gitlab, github)
- `--mode` (optional): Execution mode (interactive, autonomous, default: interactive)

## Description

The primary entry point for code migration workflows. This skill orchestrates the entire migration process by:

1. **Initializing the migration context** - Validates inputs and prepares the environment
2. **Delegating to project-tracker-agent** - Passes control to the main coordination agent
3. **Creating initial tasks** - Sets up the task structure in tasks.md
4. **Monitoring progress** - Tracks overall migration progress

The project-tracker-agent will create and manage tasks for each phase:
- Analysis task → analysis-report.json
- Planning task → migration-plan.json
- Backlog generation task → tasks.md + Kanban sync
- Story processing tasks → Per-story execution through harnesses

## Workflow

```
┌──────────────────────────────────────────────────┐
│ /migration command invoked                       │
├──────────────────────────────────────────────────┤
│ 1. Validate parameters                           │
│ 2. Build knowledge graph with Graphify (REQUIRED)│
│ 3. Initialize migration context                  │
│ 4. Create/update configuration files             │
│ 5. Invoke project-tracker-agent                  │
│ 6. Monitor and report progress                   │
└──────────────────────────────────────────────────┘
```

## Actions

1. **Validate Input**
   - Check project path exists
   - Validate migration type
   - Verify required tools are available
   - Note: /mig-graphify skill will check if graphify CLI is installed

2. **Build Knowledge Graph (REQUIRED)**
   ```bash
   # ALWAYS run this FIRST before any code analysis
   /mig-graphify <project-path>
   ```
   - Creates `graphify-out/graph.json` knowledge graph (~30s for most projects)
   - Generates `graphify-out/GRAPH_REPORT.md` with architecture overview
   - Enables 50-70% faster migration execution
   - Required by all downstream agents for code analysis

   **Why Graphify is mandatory:**
   - Reduces file reads by 96% compared to Grep/Read approach
   - Provides complete dependency understanding instantly
   - Extracts Java annotations and imports via tree-sitter AST (local, no API calls)
   - Zero infrastructure cost - all analysis is local
   - Migration agents **will fail** without graphify graph

3. **Initialize Context**
   - Load configuration from project's .env file (if exists)
   - Create/update rule.md if needed
   - Create/update tasks.md if needed
   - Set up environment variables
   - Configure integrations (Kanban, CI)

3. **Delegate to Project Tracker**
   - Invoke `project-tracker-agent` with context
   - Pass migration parameters
   - Provide trace ID for observability

4. **Monitor Progress**
   - Listen for task updates
   - Display progress summary
   - Report KPIs
   - Handle human intervention requests

## Outputs

The skill itself returns a migration session ID and monitoring URL. The project-tracker-agent creates tasks with outcomes:

**Initial Tasks Created:**
- `TASK-001`: Analyze codebase → analysis-report.json
- `TASK-002`: Create migration plan → migration-plan.json
- `TASK-003`: Generate backlog → tasks.md updated + Kanban synced
- `TASK-004+`: Process user stories → Per-story execution

Each task includes:
- Task ID
- Description
- Status (pending, in_progress, completed, failed)
- Outcome (file paths, metrics, results)
- Dependencies
- Assignee (agent)

## Interactive vs Autonomous Mode

**Interactive Mode (default):**
- Pauses for human intervention when user stories fail
- Allows manual review and remediation
- Continues to next story after manual fix

**Autonomous Mode:**
- Automatically invokes failure-analyzer-agent when stories fail
- Attempts automatic remediation and retry
- Continues processing without human intervention
- Set via `--mode autonomous` or `MODE=autonomous` in .env

**How to enable:**
```bash
# Option 1: Command-line flag
/migration --project-path ./my-app --migration-type framework --mode autonomous

# Option 2: Environment variable in project's .env
echo "MODE=autonomous" >> ./my-app/.env
/migration --project-path ./my-app --migration-type framework
```

## Configuration Files

### .env (Project Configuration)
The migration automatically loads configuration from `<project-path>/.env` if it exists.

**Supported variables:**
```bash
# Execution Mode
MODE=autonomous                             # 'interactive' (default) or 'autonomous'

# Tracker Configuration
TRACKER_TYPE=github                         # or 'local'
TRACKER_GITHUB_TOKEN=ghp_xxxxx              # GitHub PAT (required for github tracker)
TRACKER_GITHUB_ORGANIZATION=my-org          # GitHub org name
TRACKER_GITHUB_REPOSITORY=my-org/my-repo    # Optional: overrides auto-detection
TRACKER_GITHUB_PROJECT_NUMBER=5             # Optional, auto-creates if missing

# Local Tracker (default)
TRACKER_LOCAL_TASKS_PATH=./tasks.md
```

**Note:** `TRACKER_GITHUB_REPOSITORY` is auto-detected from git remote. Only set manually if needed to override.

**GitHub Tracker modes:**
- **Auto-detected repository** (default): Automatically detects repository from git remote in project directory. Creates real GitHub issues and links them to the project.
- **Manual repository** (`TRACKER_GITHUB_REPOSITORY=owner/repo`): Override auto-detection with explicit repository.
- **No repository**: If auto-detection fails and no manual config, creates draft issues (project-only items).

**Priority order:**
1. Command-line arguments (highest)
2. Project's .env file (`<project-path>/.env`)
3. Agent's .env file (current directory)
4. Defaults (lowest)

This allows you to store GitHub tokens and tracker config in your project's .env file without passing them on the command line.

### rule.md
If not provided, creates template with:
- Default transformation rules
- Quality thresholds
- Anti-patterns to detect
- Security requirements

### tasks.md
If not provided, creates empty backlog file that will be populated during execution.

## Tools Used

- **graphify** (REQUIRED) - Knowledge graph for fast code analysis
- **project-tracker-agent** - Main coordination
- File system operations (validation, setup)
- Configuration management
- Distributed tracing setup

## Example Usage

```bash
# Basic migration (interactive mode)
/migration --project-path ./my-app --migration-type framework

# Full configuration
/migration \
  --project-path ./my-app \
  --migration-type framework \
  --rules ./custom-rules.md \
  --tasks ./backlog.md \
  --kanban-platform jira \
  --kanban-project PROJ-123 \
  --ci-platform gitlab

# Autonomous mode
/migration \
  --project-path ./my-app \
  --migration-type framework \
  --mode autonomous
```

## Success Response

```json
{
  "sessionId": "mig-20260512-abc123",
  "traceId": "migration-session-abc123",
  "status": "initiated",
  "projectTrackerAgent": "running",
  "dashboardUrl": "http://localhost:3000/migrations/abc123",
  "tasks": {
    "total": 3,
    "pending": 3,
    "in_progress": 0,
    "completed": 0
  },
  "message": "Migration initiated. Project tracker agent is running."
}
```

## Error Handling

- **Invalid project path**: Returns error with valid path requirements
- **Missing dependencies**: Lists required tools/agents
- **Configuration error**: Returns detailed error with fix suggestions
- **Agent unavailable**: Retries with exponential backoff, escalates after max retries

## Integration with Project Tracker

The skill creates initial task structure in tasks.md:

```markdown
# Migration Tasks

## Session: mig-20260512-abc123
**Project**: ./my-app
**Type**: framework
**Started**: 2026-05-12T10:00:00Z

## Tasks

### TASK-001: Analyze Codebase
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Outcome**: analysis-report.json
- **Started**: -
- **Completed**: -

### TASK-002: Create Migration Plan
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Blocked by**: TASK-001
- **Outcome**: migration-plan.json
- **Started**: -
- **Completed**: -

### TASK-003: Generate Backlog
- **Status**: pending
- **Assignee**: project-tracker-agent
- **Blocked by**: TASK-002
- **Outcome**: tasks.md updated, Kanban synced
- **Started**: -
- **Completed**: -
```

## Human Intervention Points

The skill can pause and request human input at:
1. After analysis - Review findings before planning
2. After planning - Approve story breakdown
3. After backlog generation - Confirm priorities
4. On critical failures - Decide on retry strategy

## Observability

- Creates distributed trace with trace ID
- Logs all major events
- Updates tasks.md in real-time
- Syncs with Kanban board
- Provides progress webhooks (optional)

## Performance with Graphify

This migration system is **optimized for speed** through Graphify knowledge graphs:

- **50-70% faster** overall execution time
- **96% reduction** in file reads
- **Complete dependency understanding** without scanning code
- **Local AST parsing** - no external API calls, zero infrastructure cost

**CRITICAL:** All migration agents depend on the knowledge graph. The `/mig-graphify` command MUST run before delegating to project-tracker-agent, or downstream agents will fail.

## Notes

- This is the **recommended entry point** for all migrations
- Replaces manual invocation of project-tracker-agent
- Provides better user experience with setup automation
- Supports both quick starts and advanced configurations
- **ALWAYS runs Graphify first** - this is non-negotiable for performance
