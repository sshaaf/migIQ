# MigIQ Release Notes

## Version 0.1.0 - 2026-05-13

### 🎯 Major Features

#### Tracker-First Workflow
- **Initial tasks now tracked as issues**: Analysis, planning, and backlog generation are created as tracker issues before execution
- **Output attachment**: Task outputs (analysis-report.json, migration-plan.json) are automatically attached to their tracker issues
- **Status tracking**: Task status updates from Backlog → In Progress → Done/Failed in real-time
- **Applies to all trackers**: Works for both GitHub Projects and Local tracker (tasks.md)

#### Autonomous Mode
- **Fully automated execution**: Process all user stories without stopping on failures
- **Failure documentation**: Failed stories are marked and documented as GitHub issue comments
- **Continue on failure**: Migration continues processing remaining stories instead of halting
- **Enable via**: `MODE=autonomous` in .env or `--mode autonomous` flag
- **Use cases**: Overnight runs, CI/CD pipelines, large-scale migrations

#### GitHub Repository Integration
- **Auto-detection**: Automatically detects repository from `git remote` URL
- **Real GitHub issues**: Creates actual issues in the repository (not just draft issues)
- **Issue visibility**: Issues appear in `https://github.com/owner/repo/issues`
- **Auto-linking**: Issues are automatically linked to GitHub Projects v2
- **Manual override**: Optional `TRACKER_GITHUB_REPOSITORY` for custom configuration

### 🔧 Configuration Management

#### Project-Specific .env Loading
- **Automatic discovery**: Migration loads `.env` from project directory
- **Priority system**: Command-line > project .env > agent .env > environment > defaults
- **Token management**: Store GitHub tokens in project .env instead of passing on command-line
- **Configuration isolation**: Each project can have its own tracker settings

**Example:**
```bash
# In your-project/.env
MODE=autonomous
TRACKER_TYPE=github
TRACKER_GITHUB_TOKEN=ghp_xxxxx
TRACKER_GITHUB_ORGANIZATION=my-org
```

Then run:
```bash
/migration --project-path ./your-project --migration-type framework
# Automatically picks up configuration from ./your-project/.env
```

### 📊 Knowledge Graph Integration

#### Graphify Offline Mode
- **No API key required**: Uses `graphify update` command for pure AST extraction
- **Fully offline**: Runs without internet connection using tree-sitter
- **Zero API costs**: All graph building is local
- **Simplified skill**: `/mig-graphify` skill now uses offline-first approach
- **Clear instructions**: Skill provides installation guide if graphify not found

### 🐛 Bug Fixes

#### GitHub Projects v2 Status Updates
- **Fixed**: Status field updates now actually execute (was previously a stub)
- **Implementation**: Uses GraphQL `updateProjectV2ItemFieldValue` mutation
- **Field resolution**: Automatically finds Status field and option IDs
- **Real-time updates**: Issues show correct status in GitHub Projects board

#### Tracker Interface
- **Added**: `add_comment()` method for issue commenting
- **Added**: `attach_output()` method for attaching task outputs
- **Implemented for GitHub**: Comments with collapsible markdown sections
- **Implemented for Local**: File references and summaries in tasks.md

### 📝 Documentation Updates

#### Skills
- **skills/mig-graphify/SKILL.md**: Updated to use offline `graphify update` command
- **skills/migration/SKILL.md**: Added autonomous mode documentation and .env configuration guide
- **.env.example**: Comprehensive configuration template with comments

#### Examples
- **README.md**: Updated with project .env usage examples
- **Configuration priority**: Documented multi-layer configuration system
- **Repository auto-detection**: Explained git remote parsing

### 🔄 Breaking Changes

**None** - All changes are backward compatible. Existing configurations continue to work.

### ⚡ Performance & Reliability

- **Better error handling**: Replaced silent failures (`except: pass`) with proper logging
- **Status confirmation**: Visual feedback when tracker status updates succeed
- **Failure recovery**: Autonomous mode continues processing instead of halting
- **Concurrent operations**: Tracker operations use proper exception handling

### 🛠️ Technical Improvements

#### Project Tracker Agent
- **File**: `agents/project-tracker-agent/project_tracker.py`
- Added `_create_initial_task_issues()` method
- Restructured `execute_initial_tasks()` for tracker-first workflow
- Improved status update logging and error handling
- Added `story_to_issue_map` for tracking story-to-issue relationships

#### GitHub Tracker
- **File**: `agents/project-tracker-agent/trackers/github_tracker.py`
- Implemented `_update_status_field()` with GraphQL field resolution
- Implemented `add_comment()` using GitHub Issues API
- Implemented `attach_output()` with collapsible markdown formatting
- Added `_detect_repository_from_git()` for auto-detection
- Split issue creation into `_create_repository_issue()` and `_create_draft_issue()`

#### Local Tracker
- **File**: `agents/project-tracker-agent/trackers/local_tracker.py`
- Implemented `add_comment()` with timestamps
- Implemented `attach_output()` with file references and JSON summaries
- Enhanced tasks.md formatting

#### Tracker Interface
- **File**: `agents/project-tracker-agent/trackers/interface.py`
- Added `add_comment()` abstract method
- Added `attach_output()` abstract method
- Updated documentation for all methods

### 📦 Dependencies

No new dependencies added. All features use existing libraries:
- `python-dotenv` (already required)
- `requests` (already required for GitHub API)
- `graphify` CLI (optional, for knowledge graph features)

### 🚀 Getting Started

The current install method is to use the install-local.sh which creates a .claude directory in the current project where its invoked from.

#### Quick Start with Autonomous Mode

1. **Copy .env.example to your project**:
```bash
cp .env.example /path/to/your-project/.env
```

2. **Configure your project's .env**:
```bash
# /path/to/your-project/.env
MODE=autonomous
TRACKER_TYPE=github
TRACKER_GITHUB_TOKEN=ghp_your_token_here
TRACKER_GITHUB_ORGANIZATION=your-org
```

3. **Run migration**:
```bash
/migration --project-path /path/to/your-project --migration-type framework
```

4. **Monitor progress**:
- Watch GitHub Projects board for real-time status updates
- Check GitHub issues for detailed task outputs
- Failed stories documented with error details in issue comments

### 📋 Migration Guide

No migration needed. Existing setups continue to work:
- Local tracker (tasks.md) works as before
- GitHub tracker with manual configuration works as before
- New features are opt-in via .env configuration

### 🔮 Future Improvements

- D3.js interactive graph visualization (deferred)
- Additional tracker integrations (GitLab, Jira)
- Story points and custom field updates
- Merge request automation
- CI/CD pipeline with Tekton integration
- Backstage integration
- OpenShift deployment

### 🙏 Acknowledgments

This release focuses on production readiness, automation, and better integration with GitHub Projects for enterprise-scale code migrations.
