# Production Deployment Guide

## Prerequisites

- Claude Code CLI or Desktop App
- OpenCode Agent running and accessible
- CI/CD platform configured (GitLab or GitHub)
- Kanban board configured (Jira, Linear, or GitHub Projects)
- Git repository for project

## Deployment Steps

### 1. Prepare Environment

```bash
# Clone repository
git clone <your-repo>
cd demo

# Set up environment
cp .env.example .env
# Edit .env with production values

# Validate setup
python3 .claude/scripts/validate-config.py
```

### 2. Configure Migration Rules

```bash
# Customize rule.md for your project
vim rule.md

# Add your migration patterns
# Set quality thresholds
# Define anti-patterns

# Commit configuration
git add rule.md
git commit -m "Configure migration rules for production"
```

### 3. Create Initial Backlog

```bash
# Analyze codebase
python3 .claude/skills/analyze-codebase/analyze.py \
    --path /path/to/target/codebase \
    --migration-type framework \
    --output ./analysis-report.json

# Plan migration
python3 .claude/skills/plan-migration/plan.py \
    --analysis-report ./analysis-report.json \
    --rules ./rule.md \
    --output ./migration-plan.json

# Generate Kanban backlog
python3 .claude/skills/generate-backlog/generate.py \
    --plan ./migration-plan.json \
    --kanban-platform jira \
    --project-id YOUR_PROJECT
```

### 4. Set Up Monitoring

```bash
# Configure KPI tracking
# Set up dashboards
# Configure alerts

# Test monitoring
python3 .claude/skills/generate-kpi-metrics/generate_kpi_metrics.py \
    --time-range "last_7_days" \
    --output ./kpi-dashboard.json
```

### 5. Run Pilot Migration

```bash
# Select low-risk pilot story
# Run through full workflow
# Monitor closely
# Collect feedback

# Start pilot
claude-code agent run story-orchestrator-agent --story PILOT-001
```

### 6. Production Rollout

```bash
# Start project tracker agent
claude-code agent run project-tracker-agent

# Monitor progress
tail -f logs/project-tracker-agent.log

# View KPI dashboard
open kpi-dashboard.html
```

## Operational Procedures

### Health Monitoring

```bash
# Check agent health
python3 .claude/scripts/health-check.py

# View system status
curl http://localhost:9090/metrics
```

### Backup and Recovery

```bash
# Backup configuration
git push origin main

# Backup state
tar -czf state-backup-$(date +%Y%m%d).tar.gz .claude/state/

# Restore from backup
tar -xzf state-backup-20260505.tar.gz
```

### Troubleshooting

```bash
# View agent logs
tail -f logs/agents/*.log

# View trace for story
python3 .claude/scripts/view-trace.py --trace-id trace-US123-...

# Check circuit breaker status
python3 .claude/scripts/circuit-breaker-status.py
```

## Production Runbook

### Handling Failures

1. Check logs for error details
2. Review trace for story
3. Determine if transient or persistent
4. Retry if transient
5. Escalate to human if persistent

### Scaling

- Increase `max_concurrent_stories` in config
- Add more agent instances
- Monitor resource usage
- Adjust based on performance

### Updating Rules

```bash
# Update rule.md
vim rule.md

# Track changes
./.claude/scripts/track-config-changes.sh rule-update "Description of change"

# Agents pick up changes automatically
```

## Implementation Status

- [x] Production environment preparation
- [x] Deployment steps documented
- [x] CI/CD integration configured
- [x] Monitoring and alerting set up
- [x] Team training materials
- [x] Operational runbooks
