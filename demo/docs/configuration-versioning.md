# Configuration Version Control

## Overview

All configuration files (`rule.md`, `tasks.md`, `CLAUDE.md`) are version-controlled in git. This provides:
- Full change history and audit trail
- Ability to rollback problematic changes
- Collaborative review of configuration updates
- Integration with CI/CD workflows

## Configuration Files

### rule.md
- **Purpose**: Migration rules, patterns, quality thresholds
- **Update Frequency**: As needed when new patterns discovered
- **Review Required**: Yes, for threshold changes

### tasks.md
- **Purpose**: User story backlog and task tracking
- **Update Frequency**: Continuously as tasks progress
- **Review Required**: No, for status updates; Yes, for new stories

### CLAUDE.md
- **Purpose**: Project-specific instructions for Claude Code
- **Update Frequency**: Rarely, only for workflow changes
- **Review Required**: Yes, affects agent behavior

## Version Control Workflow

### Manual Commits

```bash
# Track and commit configuration changes
cd demo
./.claude/scripts/track-config-changes.sh rule-add "Add new refactoring pattern"

# Or commit manually
git add rule.md tasks.md
git commit -m "Update migration rules

- Added pattern for dependency injection migration
- Increased code coverage threshold to 85%

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Automated Tracking (via Agents)

Agents automatically track configuration changes when:
- Updating `rule.md` based on failure analysis
- Marking tasks complete in `tasks.md`
- Documenting lessons learned

## Change Types

### Rule Changes

**When to update `rule.md`:**
- New migration pattern discovered
- Anti-pattern identified
- Quality threshold needs adjustment
- New architectural pattern adopted

**Commit format:**
```
[rule] Add/Update: <description>

Details of what changed and why

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Task Changes

**When to update `tasks.md`:**
- New user story added to backlog
- Task status changes (In Progress, Done, Failed)
- Story priority changes
- Dependencies updated

**Commit format:**
```
[task] <action>: <story-id> <description>

Details of the change

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Claude Instructions

**When to update `CLAUDE.md`:**
- Workflow changes
- New quality gates added
- Testing requirements change
- Tool integration updates

**Commit format:**
```
[claude] Update: <description>

What changed and impact on agent behavior

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Best Practices

### 1. Atomic Commits
- One logical change per commit
- Related changes to multiple files can be in one commit
- Don't mix unrelated changes

### 2. Descriptive Messages
```bash
# Good
git commit -m "Add Spring Boot 3.x migration rule

Added transformation rules for:
- javax.* to jakarta.* package migration
- Security configuration updates
- Deprecated API replacements

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Bad
git commit -m "Updated files"
```

### 3. Review Before Commit
```bash
# Review changes before committing
git diff rule.md
git diff tasks.md

# Use the tracking script for guided commits
./.claude/scripts/track-config-changes.sh
```

### 4. Regular Commits
- Commit after completing a logical unit of work
- Don't wait too long between commits
- Commit before making experimental changes

### 5. Branch for Major Changes
```bash
# Create branch for significant rule updates
git checkout -b update-quality-thresholds
# Make changes to rule.md
git add rule.md
git commit -m "Increase quality thresholds based on pilot results"
git push -u origin update-quality-thresholds
# Create PR for review
```

## Rollback Procedures

### Rollback Latest Commit
```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes (DANGER!)
git reset --hard HEAD~1
```

### Rollback Specific File
```bash
# Restore file from previous commit
git checkout HEAD~1 -- rule.md

# Restore file from specific commit
git checkout <commit-hash> -- rule.md
```

### Rollback to Specific Version
```bash
# View file history
git log --oneline -- rule.md

# Restore from specific commit
git checkout <commit-hash> -- rule.md
git commit -m "Rollback rule.md to working state from <commit-hash>"
```

## Viewing History

### File History
```bash
# See all changes to rule.md
git log --oneline -- rule.md

# See detailed changes
git log -p -- rule.md

# See changes by specific author
git log --author="Claude" -- rule.md
```

### Compare Versions
```bash
# Compare current with previous version
git diff HEAD~1 rule.md

# Compare two specific versions
git diff <commit1> <commit2> rule.md

# Compare with main branch
git diff main rule.md
```

### Blame/Annotate
```bash
# See who changed each line
git blame rule.md

# See when specific section was added
git log -S "Code Coverage" -- rule.md
```

## Integration with Agents

### Automatic Commits by Agents

Agents may automatically commit configuration changes:

```python
# Example: Agent updating tasks.md
def update_task_status(task_id: str, status: str):
    # Update tasks.md
    update_tasks_file(task_id, status)

    # Track change in git
    git_add("tasks.md")
    git_commit(f"[task] Update status: {task_id} -> {status}\n\nAutomated by story-orchestrator-agent\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>")
```

### Review Points for Human

Agents will flag for human review:
- Quality threshold changes
- New architectural patterns
- Security-related rules
- Breaking changes to workflow

## Backup and Recovery

### Regular Backups
```bash
# Configuration files are in git - push regularly
git push origin main

# Create backup branch
git branch backup-$(date +%Y%m%d)
git push origin backup-$(date +%Y%m%d)
```

### Disaster Recovery
```bash
# Clone from remote
git clone <repository-url> migration-system-recovered
cd migration-system-recovered/demo

# Verify configuration
python3 .claude/scripts/validate-config.py
```

## Audit Trail

### Compliance Reporting
```bash
# Generate change log for period
git log --since="2024-01-01" --until="2024-12-31" \
    --pretty=format:"%h %ad %s" --date=short \
    -- rule.md tasks.md CLAUDE.md > config-changelog.txt

# Export full audit trail
git log -p --since="2024-01-01" \
    -- rule.md tasks.md CLAUDE.md > config-audit-trail.txt
```

### Compliance Requirements
- All configuration changes tracked in git
- Change author and timestamp recorded
- Commit message explains rationale
- Ability to rollback any change
- Full audit trail for compliance

## Troubleshooting

### Problem: Configuration out of sync
```bash
# Pull latest from remote
git pull origin main

# If conflicts, resolve manually
git status
# Edit conflicting files
git add <resolved-files>
git commit
```

### Problem: Accidentally committed secrets
```bash
# Remove file from git history (DANGEROUS!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Rotate the exposed credentials immediately!
```

### Problem: Lost uncommitted changes
```bash
# Check reflog for lost commits
git reflog

# Recover lost commit
git checkout <commit-hash>

# Or use git fsck
git fsck --lost-found
```

## References

- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Workflow Strategies](https://www.atlassian.com/git/tutorials/comparing-workflows)
