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

## Tracker Integration

The project tracker agent supports multiple tracker backends for managing migration user stories and tasks.

### Supported Trackers

- **Local Tracker** (default): tasks.md file-based tracking
- **GitHub Projects**: GitHub Projects v2 integration via GraphQL API
- **GitLab** (planned): GitLab Issues integration
- **Jira** (planned): Jira integration

### Configuration

#### Local Tracker (Default)

If no tracker configuration is provided, the agent uses the local tasks.md file:

```json
{
  "tracker": {
    "type": "local",
    "config": {
      "tasks_path": "./tasks.md"
    }
  }
}
```

Or simply omit the `tracker` field to use defaults.

#### GitHub Projects Tracker

To sync stories with GitHub Projects v2:

```json
{
  "tracker": {
    "type": "github",
    "config": {
      "token": "$GITHUB_TOKEN",
      "organization": "my-org",
      "project_number": 5,
      "labels": ["migration", "automated"],
      "default_assignee": "migration-bot"
    }
  }
}
```

**Required fields:**
- `token`: GitHub Personal Access Token (use `$ENV_VAR` for environment variable)
- `organization`: GitHub organization or username
- `project_number`: Project number (visible in project URL)

**Optional fields:**
- `labels`: List of labels to apply to created issues
- `default_assignee`: Default assignee for created issues

**Environment variable setup:**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

**Required GitHub token permissions:**
- `repo` (for organization projects)
- `project` (for managing projects)

#### GitHub Project Auto-Creation

**New in this version:** The `project_number` field is now **optional**. If not specified, the tracker will automatically create a new GitHub Project for you!

**Auto-creation workflow:**
1. Omit `project_number` from configuration
2. Agent creates a new project with name: `Migration Agent - {org} - {timestamp}`
3. Project number is printed to console
4. Add `TRACKER_GITHUB_PROJECT_NUMBER=<number>` to your .env to persist

**Example - Let the agent create a project:**
```bash
# .env file (no project_number specified)
TRACKER_TYPE=github
TRACKER_GITHUB_TOKEN=$GITHUB_TOKEN
TRACKER_GITHUB_ORGANIZATION=my-org
# TRACKER_GITHUB_PROJECT_NUMBER not set - will auto-create!
```

**Output:**
```
✓ Created GitHub Project #5: Migration Agent - my-org - 20260512-143022
  URL: https://github.com/orgs/my-org/projects/5

To persist this project, add to your .env file:
  TRACKER_GITHUB_PROJECT_NUMBER=5
```

**Custom project name:**
```bash
TRACKER_GITHUB_PROJECT_NAME=Java Migration Q2 2026
TRACKER_GITHUB_PROJECT_DESCRIPTION=Migration from Java 8 to Java 17
```

**Requirements for auto-creation:**
- GitHub token must have `project` scope
- Organization/user must exist and be accessible
- Sufficient API rate limit (creates ~3-5 API calls)

**Disable auto-creation:**
```json
{
  "tracker": {
    "type": "github",
    "config": {
      "token": "$GITHUB_TOKEN",
      "organization": "my-org",
      "auto_create": false
    }
  }
}
```

#### Configuration via .env File (Recommended)

Instead of JSON context, use .env file for easier configuration management:

**1. Create .env from template:**
```bash
cp .env.example .env
```

**2. Edit .env for local tracker:**
```bash
# Local Tracker
TRACKER_TYPE=local
TRACKER_LOCAL_TASKS_PATH=./tasks.md
```

**3. Edit .env for GitHub tracker:**
```bash
# GitHub Tracker
TRACKER_TYPE=github
TRACKER_GITHUB_TOKEN=$GITHUB_TOKEN
TRACKER_GITHUB_ORGANIZATION=my-org

# Optional: Specify existing project number, or omit to auto-create
TRACKER_GITHUB_PROJECT_NUMBER=5

# Optional: Customize project name and description (for auto-creation)
# TRACKER_GITHUB_PROJECT_NAME=My Migration Project
# TRACKER_GITHUB_PROJECT_DESCRIPTION=Java 8 to 17 migration

# Optional: Additional settings
TRACKER_GITHUB_LABELS=migration,automated
TRACKER_GITHUB_DEFAULT_ASSIGNEE=migration-bot
```

**4. Set sensitive credentials in system environment:**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

**Benefits of .env configuration:**
- ✅ Keep credentials out of command-line history
- ✅ Version control .env.example as documentation
- ✅ Never commit .env (it's in .gitignore)
- ✅ Use .env.local for local overrides
- ✅ Clear reference for all available options

### Field Mappings

#### Priority Mapping (GitHub Projects)

| Migration Priority | GitHub Priority |
|-------------------|----------------|
| P0                | High           |
| P1                | Medium         |
| P2                | Low            |
| P3                | Low            |

#### Status Mapping (GitHub Projects)

| Migration Status | GitHub Status |
|-----------------|---------------|
| Backlog         | Todo          |
| In Progress     | In Progress   |
| Done            | Done          |
| Failed          | Done          |

### Troubleshooting

#### GitHub Authentication Failed

**Error:** "GitHub authentication failed"

**Solution:**
1. Verify your GITHUB_TOKEN environment variable is set:
   ```bash
   echo $GITHUB_TOKEN
   ```
2. Ensure the token has required permissions (repo, project)
3. Check token hasn't expired in GitHub Settings → Developer settings → Personal access tokens

#### GitHub Project Not Found

**Error:** "GitHub project not found"

**Solution:**
1. Verify the organization name is correct
2. Check the project number in the project URL: `https://github.com/orgs/<org>/projects/<number>`
3. Ensure your token has access to the organization

#### Project Auto-Creation Failed

**Error:** "Failed to auto-create GitHub project: ..."

**Common causes:**
1. Token lacks 'project' scope
2. Organization name is incorrect
3. Insufficient permissions for the organization

**Solution:**
1. Verify token has 'project' scope:
   ```bash
   # Check token scopes at https://github.com/settings/tokens
   # Or test with curl:
   curl -H "Authorization: Bearer $TRACKER_GITHUB_TOKEN" \
     https://api.github.com/user
   # Look for 'X-OAuth-Scopes' header
   ```

2. Test organization resolution:
   ```bash
   curl -H "Authorization: Bearer $TRACKER_GITHUB_TOKEN" \
     https://api.github.com/orgs/YOUR_ORG
   ```

3. Manually specify project number if auto-creation fails:
   ```bash
   # Create project manually on GitHub
   # Then add to .env:
   TRACKER_GITHUB_PROJECT_NUMBER=5
   ```

**Error:** "Organization or user 'xyz' not found"

**Solution:**
1. Verify organization/username spelling
2. Check if your token has access to the org
3. For private orgs, ensure token has 'read:org' scope

**Error:** "Please verify your GitHub token has 'project' scope permissions"

**Solution:**
1. Regenerate token with required scopes:
   - Visit https://github.com/settings/tokens
   - Create new token with scopes: `project`, `repo`
   - Update `TRACKER_GITHUB_TOKEN` in .env
2. Or disable auto-creation and use existing project number

#### Rate Limit Exceeded

**Error:** "GitHub rate limit exceeded"

**Solution:**
- Wait for rate limit to reset (visible in error message)
- Use authenticated requests (they have higher limits: 5000/hour vs 60/hour)
- Reduce frequency of operations

#### Environment Variable Not Set

**Error:** "Environment variable 'GITHUB_TOKEN' is not set"

**Solution:**
```bash
export GITHUB_TOKEN="your-token-here"
# Or add to your shell profile (.bashrc, .zshrc, etc.)
```

#### .env File Issues

**Error:** "Configuration loaded from defaults" when you expect .env

**Solution:**
1. Verify .env file exists in project root:
   ```bash
   ls -la .env
   ```
2. Check file format (KEY=value, no spaces around =):
   ```bash
   cat .env
   ```
3. Ensure environment variable names are correct (uppercase with underscores)
4. Check for .env.example hint at startup

**Error:** "Environment variable 'GITHUB_TOKEN' is not set"

**Solution:**
1. Set the environment variable before running:
   ```bash
   export GITHUB_TOKEN="ghp_your_token"
   ```
2. Or reference it in .env:
   ```bash
   TRACKER_GITHUB_TOKEN=$GITHUB_TOKEN
   ```
3. Make sure $VAR syntax matches exactly in .env

**Issue:** Changes to .env not taking effect

**Solution:**
1. Restart the agent (env vars loaded at startup)
2. Check for .env.local overriding your values
3. Verify configuration priority (context > env > defaults)
4. Check agent output for "Config Source:" to see what's being used

**Issue:** Accidentally committed .env with credentials

**Solution:**
1. Remove from git immediately:
   ```bash
   git rm --cached .env
   git commit -m "Remove .env from git"
   ```
2. Rotate compromised credentials (regenerate GitHub token)
3. Verify .env is in .gitignore
4. Use git-secrets or similar tools to prevent future commits

### Example GraphQL Queries

For manual debugging with GitHub Projects:

**Query project details:**
```graphql
query {
  organization(login: "my-org") {
    projectV2(number: 5) {
      id
      title
      items(first: 10) {
        nodes {
          id
          content {
            ... on DraftIssue {
              title
              body
            }
          }
        }
      }
    }
  }
}
```

**Create draft issue:**
```graphql
mutation {
  addProjectV2DraftIssue(input: {
    projectId: "PVT_kwDOABcD12MAAg"
    title: "[US-001] Migration Story"
    body: "Story description"
  }) {
    projectItem {
      id
    }
  }
}
```

Execute queries at: https://docs.github.com/en/graphql/overview/explorer

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

### Unit Tests

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

### Integration Tests

Integration tests validate the GitHub tracker functionality with real API calls.

**Setup:**
1. Create `.env.test` from template:
   ```bash
   cp .env.test.example .env.test
   ```

2. Edit `.env.test` with your credentials:
   ```bash
   # Required
   TRACKER_GITHUB_TOKEN=ghp_your_token_here
   TRACKER_GITHUB_ORGANIZATION=your-org-or-username

   # Optional - will auto-create project if not specified
   # TRACKER_GITHUB_PROJECT_NUMBER=5

   # Optional - customize test behavior
   # TEST_KEEP_PROJECT=false
   # TEST_MIN_RATE_LIMIT=20
   ```

3. Get a GitHub token with 'project' scope:
   - Visit: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `project`, `repo`
   - Copy token to `.env.test`

**Run tests:**

Using the Makefile (recommended):
```bash
# Quick setup
make env-setup              # Create .env.test from template
# Edit .env.test with your credentials

# Run tests
make test-integration       # Run integration tests
make test-integration-json  # Run with JSON output
make test-integration-keep  # Keep test project for debugging

# Other useful commands
make help                   # Show all available commands
make rate-limit            # Check GitHub API rate limit
make validate-token        # Validate GitHub token
make test                  # Run all tests (unit + integration)
```

Or run directly:
```bash
# Run integration tests with pytest
python -m pytest tests/integration/test_github_integration.py -v

# Or run as standalone script
python tests/integration/test_github_integration.py

# Output results in JSON format
python tests/integration/test_github_integration.py --json
```

**What the tests do:**
- ✅ Create a temporary GitHub Project
- ✅ Create test items (3 user stories)
- ✅ Verify items exist with correct fields
- ✅ List all project items
- ✅ Clean up (delete test project)

**Test output:**
```
======================================================================
  TEST: Create GitHub Project
======================================================================
✓ Created project #5: Migration Agent Test - my-org - 20260512-143022
  URL: https://github.com/orgs/my-org/projects/5

======================================================================
  TEST: Create Project Items
======================================================================
✓ Test passed: Created 3 items
  Item 1: PVTI_lADOABc...
  Item 2: PVTI_lADOABc...
  Item 3: PVTI_lADOABc...

======================================================================
  CLEANUP: Delete Test Project
======================================================================
✓ Cleanup complete: Project deleted

======================================================================
  TEST SUMMARY
======================================================================
Total tests: 5
Passed: 5
Failed: 0
======================================================================
```

**Debugging:**
```bash
# Keep test project for inspection
TEST_KEEP_PROJECT=true python tests/integration/test_github_integration.py

# Check API rate limit before testing
curl -H "Authorization: Bearer $TRACKER_GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

**CI/CD integration:**
The test script exits with code 0 on success, 1 on failure, making it suitable for CI/CD pipelines.

```bash
# In GitHub Actions
- name: Run integration tests
  run: python tests/integration/test_github_integration.py
  env:
    TRACKER_GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TRACKER_GITHUB_ORGANIZATION: ${{ github.repository_owner }}
```

## Future Enhancements

- Real skill invocation via Claude Code API
- Real agent invocation for story-orchestrator
- Actual Kanban API integration
- Distributed tracing integration
- Webhook notifications
- Progress dashboard
