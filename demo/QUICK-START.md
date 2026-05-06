# Quick Start Guide

Get up and running with the Code Migration System in minutes.

## Prerequisites

- Python 3.8+
- Git
- Claude Code (CLI or Desktop)
- OpenCode Agent (running and accessible)
- CI/CD platform account (GitLab or GitHub)
- Kanban board account (Jira, Linear, or GitHub Projects)

## 5-Minute Setup

### 1. Environment Configuration (2 min)

```bash
cd demo

# Copy and edit environment file
cp .env.example .env
vi .env  # or nano .env

# Required variables:
# - CI_PLATFORM_TYPE=gitlab (or github)
# - GITLAB_TOKEN=your-token (or GITHUB_TOKEN)
# - KANBAN_PLATFORM=jira (or linear, github-projects)
# - KANBAN_API_TOKEN=your-token
# - OPENCODE_AGENT_API=http://localhost:8080
# - OPENCODE_AGENT_API_KEY=your-key
```

### 2. Initialize Project (1 min)

```bash
# Run automated setup
chmod +x .claude/scripts/setup-project.sh
./.claude/scripts/setup-project.sh

# This will:
# - Create rule.md, tasks.md, CLAUDE.md from templates
# - Validate directory structure
# - Check configuration
```

### 3. Customize Configuration (2 min)

Edit configuration files for your specific migration:

```bash
# Migration rules and patterns
vi rule.md

# Add your specific rules:
# - Framework migration patterns
# - Anti-patterns to detect
# - Quality thresholds
# - Testing requirements

# Project instructions for Claude Code
vi CLAUDE.md

# Customize:
# - Coding standards
# - Testing requirements
# - CI/CD workflow
# - Review process
```

## First Migration

### Analyze Your Codebase

```bash
# Run codebase analysis
python3 .claude/skills/analyze-codebase/analyze.py \
    --path /path/to/your/codebase \
    --migration-type framework \
    --output ./analysis-report.json

# Review the report
cat analysis-report.json | jq '.'

# Key metrics:
# - migrationScore: 0-100 (higher = easier)
# - antiPatterns: Issues detected
# - complexity: Code complexity metrics
# - recommendations: Prioritized actions
```

### Create Migration Plan

```bash
# Generate migration plan
python3 .claude/skills/plan-migration/plan.py \
    --analysis-report ./analysis-report.json \
    --rules ./rule.md \
    --strategy risk \
    --output ./migration-plan.json

# Review the plan
cat migration-plan.json | jq '.stories'

# This creates user stories with:
# - Story ID and title
# - Priority ranking
# - Task breakdown
# - Dependencies
```

### Generate Backlog

```bash
# Create Kanban tickets
python3 .claude/skills/generate-backlog/generate.py \
    --plan ./migration-plan.json \
    --kanban-platform jira \
    --project-id YOUR_PROJECT_KEY

# This creates:
# - One ticket per user story
# - Labels and priorities set
# - Dependencies linked
# - Ready to track progress
```

## Running Migrations

### Option 1: Manual Skill Invocation

Run each skill manually for full control:

```bash
# 1. Generate tests
python3 .claude/skills/generate-characterization-tests/generate_characterization_tests.py \
    --source-path ./src/main

# 2. Apply refactoring
python3 .claude/skills/apply-refactor-rules/apply_refactor_rules.py \
    --source-path ./src \
    --rules-path ./rules/refactoring.yml

# 3. Validate coverage
python3 .claude/skills/validate-coverage/validate_coverage.py \
    --coverage-report ./coverage.json \
    --threshold 80

# 4. Run benchmarks
python3 .claude/skills/run-benchmarks/run_benchmarks.py \
    --benchmark-suite ./benchmarks/suite.json \
    --baseline ./benchmarks/baseline.json

# 5. Validate quality
python3 .claude/skills/validate-quality/validate_quality.py \
    --metrics ./metrics.json \
    --thresholds-path ./rule.md
```

### Option 2: Agent Mesh Automation (Future)

Once Claude Code agents are deployed:

```bash
# Run full automated workflow
claude-code agent run project-tracker-agent

# This will:
# - Process all stories in backlog
# - Run all harnesses automatically
# - Create MRs and monitor CI
# - Handle failures and retry
# - Track KPIs and report progress
```

## Validation

### Validate Configuration

```bash
# Check all configuration files
python3 .claude/scripts/validate-config.py

# Run with strict mode (warnings as errors)
python3 .claude/scripts/validate-config.py --strict
```

### Check Integration Health

```bash
# Test CI platform connection
python3 -c "
import os, requests
token = os.getenv('GITLAB_TOKEN') or os.getenv('GITHUB_TOKEN')
url = os.getenv('GITLAB_URL') or 'https://api.github.com'
headers = {'PRIVATE-TOKEN': token} if 'gitlab' in url else {'Authorization': f'token {token}'}
r = requests.get(f'{url}/api/v4/user' if 'gitlab' in url else f'{url}/user', headers=headers)
print('✅ CI connection OK' if r.status_code == 200 else f'❌ CI connection failed: {r.status_code}')
"

# Test Kanban connection (Jira example)
python3 -c "
import os, requests
from requests.auth import HTTPBasicAuth
url = os.getenv('JIRA_URL')
email = os.getenv('JIRA_EMAIL')
token = os.getenv('JIRA_API_TOKEN')
auth = HTTPBasicAuth(email, token)
r = requests.get(f'{url}/rest/api/2/myself', auth=auth)
print('✅ Kanban connection OK' if r.status_code == 200 else f'❌ Kanban connection failed: {r.status_code}')
"
```

## Common Commands

### Configuration Management

```bash
# Update migration rules and commit
vi rule.md
./.claude/scripts/track-config-changes.sh rule-update "Added Spring Boot 3.x pattern"

# Update task status
vi tasks.md
./.claude/scripts/track-config-changes.sh task-update "Completed US-001"
```

### Viewing Results

```bash
# View analysis report
cat analysis-report.json | jq '{score: .migrationScore, recommendations: .recommendations}'

# View migration plan
cat migration-plan.json | jq '.stories[] | {id, title, priority}'

# View KPI metrics (if generated)
cat kpi-dashboard.json | jq '{velocity, automation_rate, quality_score}'
```

### Troubleshooting

```bash
# Check logs
ls -lah logs/

# View recent errors
grep ERROR logs/*.log | tail -20

# Validate environment
source .env && env | grep -E "CI_PLATFORM|KANBAN|OPENCODE"
```

## Next Steps

### For a Pilot Project

1. **Select Low-Risk Target**: Choose a small, non-critical module
2. **Customize Rules**: Add patterns specific to your tech stack
3. **Run Analysis**: Analyze and create plan
4. **Manual First Story**: Do one story manually to validate
5. **Iterate**: Refine rules based on learnings
6. **Scale Up**: Gradually increase automation

### For Production Deployment

1. **Review Security**: See [docs/security-compliance.md](./docs/security-compliance.md)
2. **Set Up Monitoring**: See [docs/kpi-tracking.md](./docs/kpi-tracking.md)
3. **Train Team**: Share documentation and run workshops
4. **Deploy Agents**: Set up Claude Code agent infrastructure
5. **Monitor & Tune**: Track KPIs and adjust thresholds

## Getting Help

- **Documentation**: See [docs/](./docs/) directory
- **Examples**: See [IMPLEMENTATION-SUMMARY.md](./IMPLEMENTATION-SUMMARY.md)
- **Issues**: Check troubleshooting guide
- **Support**: Open issue in repository

## Key Files Reference

| File | Purpose |
|------|---------|
| `.env` | Environment configuration and secrets |
| `rule.md` | Migration rules and quality thresholds |
| `tasks.md` | User story backlog and status |
| `CLAUDE.md` | Project instructions for Claude Code |
| `analysis-report.json` | Codebase analysis results |
| `migration-plan.json` | Generated migration plan |

## Validation Checklist

Before starting migrations:

- [ ] `.env` configured with all credentials
- [ ] `rule.md` customized for your migration type
- [ ] `tasks.md` initialized (or generated from plan)
- [ ] `CLAUDE.md` updated with project details
- [ ] Configuration validation passes
- [ ] CI platform connection works
- [ ] Kanban board connection works
- [ ] OpenCode Agent accessible (if using)

---

**Ready to migrate!** Start with analysis and proceed step by step.
