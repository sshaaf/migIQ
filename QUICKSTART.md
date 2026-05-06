# Quick Start Guide - Code Migration System

This guide will help you quickly understand and start using the code migration system.

## What You Have

A complete specification for an **AI-driven code migration system** using the **Agent Mesh architecture** with Claude Code harnesses.

### Core Documentation Files

1. **[README.md](./README.md)** - Project overview and getting started
2. **[SPECIFICATION.md](./SPECIFICATION.md)** - Complete implementation specification
3. **[AGENT-MESH.md](./AGENT-MESH.md)** - Agent mesh architecture details
4. **[skills.md](./skills.md)** - 19 skill definitions across all phases
5. **[agents.md](./agents.md)** - 7 agent definitions with workflows
6. **[vision.md](./vision.md)** - Original vision from diagram

### Template Files

Located in `templates/`:

1. **[rule.md](./templates/rule.md)** - Migration rules and constraints template
2. **[tasks.md](./templates/tasks.md)** - Task tracking template
3. **[CLAUDE.md](./templates/CLAUDE.md)** - Claude Code instructions template

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  PROJECT TRACKING HARNESS               │
│  Plan User Story Backlog → Generate User Story Backlog │
│              (project-tracker-agent)                    │
└────────────────────┬────────────────────────────────────┘
                     │ LOOP for each story
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   TEST HARNESS                          │
│  Generate Characterization Tests + Functional Tests     │
│            (test-generator-agent)                       │
│          Tools: opencode agent                          │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   CODE HARNESS                          │
│         Generate Spec-Driven Refactors                  │
│            (code-refactor-agent)                        │
│      Tools: opencode agent                              │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 BENCHMARK HARNESS                       │
│         Build Benchmark / Test Suite                    │
│          (benchmark-builder-agent)                      │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 EVALUATION HARNESS                      │
│      Generate Evaluation Metrics / Test Scores          │
│          (quality-evaluator-agent)                      │
│         Tools: opencode agent                           │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    CI HARNESS                           │
│              Prepare Merge Request                      │
│           (ci-integration-agent)                        │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  CI PLATFORM                            │
│           RUN CI Pipeline                               │
│      Failed Tests/Specs? → YES → KPIs → Backlog        │
│                      ↓ NO                               │
│                    MERGE                                │
└────────────────────┬────────────────────────────────────┘
                     ↓
              KANBAN BOARDS
                (Done)
```

## Key Concepts

### Agent Mesh
- **Distributed collaboration** of specialized AI agents
- **Parallel execution** where dependencies allow
- **Autonomous decision-making** with human oversight
- **Resilient workflows** with automatic recovery

### Skills (19 total)
Reusable commands that perform specific actions:
- `/analyze-codebase` - Analyze migration needs
- `/generate-characterization-tests` - Capture current behavior
- `/apply-refactor-rules` - Apply automated refactoring
- `/validate-quality` - Validate against thresholds
- [See skills.md for complete list]

### Agents (7 core + 3 support)
Autonomous workflows that orchestrate skills:
- `project-tracker-agent` - Manage overall backlog
- `test-generator-agent` - Generate test coverage
- `code-refactor-agent` - Execute refactoring
- `quality-evaluator-agent` - Validate quality
- [See agents.md for complete list]

## The Workflow Loop

For each user story:

1. **Analyze** → Understand codebase and requirements
2. **Plan** → Break down into tasks
3. **Test** → Generate safety net of tests
4. **Implement** → Refactor with opencode agent + generate new code
5. **Benchmark** → Validate performance
6. **Evaluate** → Check quality gates
7. **Integrate** → Create MR and run CI
8. **Decision**:
   - ✅ **Pass** → Merge → Done
   - ❌ **Fail** → Generate KPIs → Return to backlog → Retry

## How to Get Started

### Step 1: Review Documentation

**Essential Reading** (30 minutes):
1. [README.md](./README.md) - Overall project context
2. [AGENT-MESH.md](./AGENT-MESH.md) - Architecture patterns
3. [skills.md](./skills.md) - Browse available skills

**Deep Dive** (1-2 hours):
1. [SPECIFICATION.md](./SPECIFICATION.md) - Implementation details
2. [agents.md](./agents.md) - Agent workflows
3. Templates in `templates/`

### Step 2: Set Up Configuration

Copy templates to project root:

```bash
cp templates/rule.md ./rule.md
cp templates/tasks.md ./tasks.md
cp templates/CLAUDE.md ./CLAUDE.md
```

Customize for your project:
- Edit `rule.md` with your migration rules
- Edit `tasks.md` with your user stories
- Update `CLAUDE.md` with project specifics

### Step 3: Set Up Infrastructure

Create directory structure:

```bash
mkdir -p .claude/{agents,skills,config}
mkdir -p src/{main,test}
mkdir -p {specs,rules,benchmarks,docs/adr}
```

### Step 4: Configure Tools

Set environment variables:

```bash
# CI Platform
export CI_PLATFORM_TOKEN="your-token"

# Kanban Board
export KANBAN_API_URL="your-kanban-url"
export KANBAN_API_TOKEN="your-kanban-token"

# Migration Tools
export OPENCODE_API="http://localhost:8080"
export OPENSPEC_API="http://localhost:8081"
```

### Step 5: Implement Skills

Start with the most critical skills:

1. **Priority 1**: Core workflow skills
   - `/analyze-codebase`
   - `/generate-characterization-tests`
   - `/apply-refactor-rules`

2. **Priority 2**: Validation skills
   - `/validate-coverage`
   - `/validate-quality`

3. **Priority 3**: Integration skills
   - `/prepare-merge-request`
   - `/push-merge-request`

Place implementations in `.claude/skills/`

### Step 6: Implement Agents

Start with the orchestrator:

1. **Start here**: `story-orchestrator-agent`
   - Coordinates entire story lifecycle
   - Integrates all harnesses

2. **Then add**: Individual harness agents
   - `test-generator-agent`
   - `code-refactor-agent`
   - `quality-evaluator-agent`

3. **Finally**: Supporting agents
   - `failure-analyzer-agent`
   - `kpi-tracker-agent`

Place implementations in `.claude/agents/`

### Step 7: Run Your First Migration

Start with a small, low-risk migration:

```bash
# 1. Define a simple user story in tasks.md
# Example: US-001 - Update a single Java file to Java 17

# 2. Run the story orchestrator
claude-code agent run story-orchestrator-agent --story US-001

# 3. Monitor progress
# - Check logs in logs/agents/
# - View KPI dashboard
# - Track Kanban board

# 4. Review results
# - Check generated tests
# - Review refactored code
# - Validate quality metrics

# 5. Handle outcome
# - If success: Review and merge
# - If failure: Review root cause, update rules, retry
```

## What Makes This Different

### Compared to Traditional Automation

**Traditional**:
- Linear, sequential pipelines
- Single point of failure
- Manual orchestration
- Limited parallelism

**Agent Mesh**:
- Distributed, parallel execution
- Isolated failure domains
- Autonomous coordination
- Maximum parallelism

### Compared to CrewAI

**CrewAI**:
- Python framework
- Predefined crew structures
- Sequential workflows
- Framework overhead

**Agent Mesh with Claude Code**:
- Native harness integration
- Flexible, dynamic collaboration
- Parallel workflows
- Direct tool access

## Key Metrics to Track

### Velocity Metrics
- Stories completed per sprint
- Average cycle time
- Time per harness phase

### Quality Metrics
- Test coverage trends
- Code quality scores
- Security vulnerabilities
- Performance benchmarks

### Automation Metrics
- % stories completed without human intervention
- Human intervention rate
- Agent success rate
- Retry rate

### Business Metrics
- Migration velocity
- Time to production
- Cost per migration
- Risk reduction

## Success Criteria

Your implementation is successful when:

1. **Automation Rate** >80%
   - Most migrations complete without human intervention

2. **Quality** Maintained or Improved
   - All tests pass
   - Coverage ≥80%
   - No quality regressions

3. **Performance** No Regressions
   - Benchmarks maintained
   - No performance degradation >5%

4. **Reliability** Consistent Results
   - Predictable outcomes
   - Clear feedback loops
   - Effective error handling

5. **Traceability** Full Audit Trail
   - Track from story to merge
   - All decisions documented
   - Metrics captured

## Common Patterns

### Pattern 1: Simple Dependency Update

```
Analyze → Identify dependencies → Update pom.xml →
Run tests → Validate → MR
```

**Time**: ~10 minutes
**Automation**: 95%

### Pattern 2: Framework Migration

```
Analyze (opencode agent) → Generate characterization tests (opencode agent) →
Apply refactor rules (opencode agent) → Generate new code (opencode agent) →
Run tests → Benchmark → Validate (opencode agent) → MR
```

**Time**: ~30-60 minutes per module
**Automation**: 70-80%

### Pattern 3: Architectural Refactoring

```
Analyze → Design review (human) → Generate tests →
Iterative refactoring → Benchmark →
Multiple reviews (human) → Validate → MR
```

**Time**: Days to weeks
**Automation**: 40-60%

## Troubleshooting

### Agent Not Progressing?
1. Check agent logs in `logs/agents/`
2. Verify dependencies satisfied
3. Check circuit breaker status
4. Review task prerequisites in `tasks.md`

### Tests Failing?
1. Run characterization tests to identify behavior change
2. Review refactoring rules applied
3. Check for edge cases
4. Use `/request-root-cause` skill

### Quality Gates Failing?
1. Review quality thresholds in `rule.md`
2. Check specific metrics that failed
3. Adjust code or thresholds as appropriate
4. Re-run validation

### CI Pipeline Failing?
1. Check CI platform logs
2. Reproduce failure locally
3. Fix issues
4. Retry pipeline

## Next Steps

### Immediate (Week 1)
- [ ] Review all documentation
- [ ] Set up configuration files
- [ ] Configure development environment
- [ ] Implement first 3 skills

### Short Term (Weeks 2-4)
- [ ] Implement remaining skills
- [ ] Implement core agents
- [ ] Set up CI integration
- [ ] Run first test migration

### Medium Term (Months 2-3)
- [ ] Complete agent mesh implementation
- [ ] Set up monitoring and dashboards
- [ ] Process multiple user stories
- [ ] Tune quality thresholds

### Long Term (Months 4-6)
- [ ] Scale to production use
- [ ] Optimize parallel execution
- [ ] Build knowledge base from learnings
- [ ] Continuous improvement

## Resources

### Documentation
- [README.md](./README.md) - Project overview
- [SPECIFICATION.md](./SPECIFICATION.md) - Full specification
- [AGENT-MESH.md](./AGENT-MESH.md) - Architecture
- [skills.md](./skills.md) - Skills reference
- [agents.md](./agents.md) - Agents reference

### Templates
- [rule.md](./templates/rule.md) - Migration rules
- [tasks.md](./templates/tasks.md) - Task tracking
- [CLAUDE.md](./templates/CLAUDE.md) - Claude instructions

### External References
- [Red Hat Agent Mesh Blog](https://www.redhat.com/en/blog/refactoring-speed-mission-agent-mesh-approach-legacy-system-modernization-red-hat-ai)
- [Claude Code Documentation](https://claude.com/claude-code)

## Getting Help

**Questions?**
- Review documentation first
- Check templates for examples
- Review vision.md for context

**Issues?**
- Check troubleshooting section
- Review agent and skill logs
- Use `/request-root-cause` skill

**Contributions?**
- Follow patterns in specification
- Update documentation
- Add tests
- Submit PR

---

**You now have a complete specification for building an AI-driven code migration system using the Agent Mesh architecture. Start with the immediate next steps and build incrementally!**
