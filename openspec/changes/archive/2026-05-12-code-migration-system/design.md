## Context

**Current State**: Manual code migration is slow, error-prone, and requires deep expertise. Traditional automation tools use linear pipelines that cannot adapt to failures or optimize for parallel execution.

**Background**: The Red Hat blog post "Refactoring at the speed of mission" describes an agent mesh approach to legacy system modernization. This architecture uses distributed, collaborative AI agents instead of monolithic orchestration frameworks.

**Constraints**:
- Must achieve >80% automation rate without human intervention
- Must integrate with existing CI/CD platforms (GitLab/GitHub) and Kanban boards
- Must maintain or improve code quality and test coverage
- No performance regressions beyond acceptable thresholds
- Full audit trail and observability required

**Stakeholders**:
- Development teams performing migrations
- Architecture teams defining migration patterns
- DevOps teams managing CI/CD infrastructure
- Management tracking migration velocity and quality

## Goals / Non-Goals

**Goals:**
- Automate the analyze-plan-implement-validate workflow for code migrations
- Enable parallel execution of independent tasks using Agent Mesh architecture
- Provide comprehensive quality gates and feedback loops
- Integrate seamlessly with existing developer workflows and tools
- Support multiple migration types (framework, language, platform)
- Achieve high automation rate (>80%) with minimal human intervention
- Maintain full observability through distributed tracing and KPI tracking

**Non-Goals:**
- Supporting non-code migrations (database schema, infrastructure)
- Real-time migration (system remains available during migration)
- Automated architecture redesign (humans define patterns in rule.md)
- Supporting all programming languages (focus on Java, Python, JavaScript initially)
- Replacing human code review (system prepares MRs for review)

## Decisions

### Decision 1: Agent Mesh Architecture over CrewAI

**Choice**: Implement using Claude Code's native Agent Mesh architecture instead of CrewAI framework.

**Rationale**:
- **Native Integration**: Claude Code harnesses provide better integration with development tools (git, CI/CD, file system)
- **Flexibility**: Agent Mesh allows dynamic, parallel collaboration vs. CrewAI's predefined sequential crews
- **Performance**: Parallel execution without Python framework overhead
- **Simplicity**: Skills and agents pattern is simpler to maintain and extend
- **Scalability**: Distributed architecture scales horizontally with agent instances

**Alternatives Considered**:
- CrewAI: More opinionated framework but less flexible, Python overhead, sequential workflows
- Custom orchestration: More control but higher implementation cost and maintenance burden
- Linear pipeline (Jenkins/GitHub Actions): Simpler but no adaptive behavior or parallel optimization

### Decision 2: Six Harness Phases with Specialized Agents

**Choice**: Decompose workflow into 6 specialized harness phases, each with dedicated agents and skills.

**Rationale**:
- **Separation of Concerns**: Each harness has clear responsibility and can evolve independently
- **Parallel Execution**: Test generation, benchmarking, and quality evaluation can run in parallel where dependencies allow
- **Isolated Failures**: Failure in one harness doesn't cascade to others
- **Reusability**: Skills can be invoked by agents or directly by users
- **Observability**: Clear boundaries for tracing and metrics

**Harness Phases**:
1. Project Tracking - Backlog management and story orchestration
2. Test - Generate characterization and functional tests
3. Code - Apply refactoring and generate new code
4. Benchmark - Performance validation
5. Evaluation - Quality gates and scoring
6. CI - Integration with CI/CD platforms

**Alternatives Considered**:
- Fewer phases (combine test/code): Reduces modularity and makes parallel execution harder
- More phases (split evaluation into multiple): Over-engineering, adds coordination overhead

### Decision 3: opencode Agent for All Code Operations

**Choice**: Delegate all code analysis, refactoring, testing, and evaluation to opencode agent.

**Rationale**:
- **Expertise**: opencode agent specializes in code understanding and transformation
- **Consistency**: Single tool for all code operations reduces integration complexity
- **Multi-language**: Supports multiple programming languages without custom tooling per language
- **Spec-driven**: Aligns with specification-driven refactoring approach

**Operations Delegated**:
- Code analysis and understanding
- Automated refactoring (AST transformations)
- Test generation (characterization and functional)
- Code generation from specifications
- Quality evaluation and metrics
- KPI tracking and reporting

**Alternatives Considered**:
- Language-specific tools (openrewrite for Java, etc.): More fragmentation, harder to maintain
- Manual refactoring: Not scalable, defeats automation goal
- AST manipulation libraries: Lower-level, requires more implementation effort

### Decision 4: Configuration as Code (rule.md, tasks.md, CLAUDE.md)

**Choice**: Use markdown files for migration rules, tasks, and project instructions instead of databases or proprietary formats.

**Rationale**:
- **Version Control**: Configuration changes tracked in git with full history
- **Human Readable**: Easy for humans to review and update
- **Agent Readable**: Structured markdown is easy for AI agents to parse and understand
- **Collaborative**: Teams can review configuration changes via pull requests
- **Portable**: Works across different environments without database setup

**Configuration Files**:
- `rule.md`: Migration rules, patterns, anti-patterns, quality thresholds
- `tasks.md`: User stories, task breakdown, dependencies, priorities
- `CLAUDE.md`: Project-specific instructions for Claude Code agents

**Alternatives Considered**:
- YAML/JSON: Less human-readable, harder to write descriptive rules
- Database: Adds operational complexity, harder to version control
- API configuration: Requires additional service, less transparent

### Decision 5: Feedback Loops with Automated Retry

**Choice**: Implement feedback loops where CI failures automatically return to backlog with KPI metrics and root cause analysis.

**Rationale**:
- **Continuous Improvement**: Failures inform future migrations through updated rules
- **Resilience**: Transient failures don't require human intervention
- **Learning**: KPI metrics help identify patterns and improve success rates
- **Transparency**: Full audit trail from failure to resolution

**Feedback Flow**:
```
CI Pipeline FAIL → Close MR → Generate KPI Metrics → Root Cause Analysis →
Update tasks.md → Return to Backlog → Retry with Updated Context
```

**Retry Strategy**:
- Limited retries (max 3) to prevent infinite loops
- Exponential backoff between retries
- Human escalation after max retries
- Context preservation across retries

**Alternatives Considered**:
- Manual retry: Slower, requires human attention for every failure
- No retry: Wastes successful intermediate work
- Infinite retry: Risk of infinite loops, resource waste

### Decision 6: Distributed Tracing and KPI Tracking

**Choice**: Implement comprehensive observability with distributed tracing, structured logging, and KPI dashboards.

**Rationale**:
- **Debugging**: Trace each story through all agents for root cause analysis
- **Performance**: Identify bottlenecks and optimize parallel execution
- **Business Metrics**: Track migration velocity, quality trends, automation rate
- **Compliance**: Full audit trail for regulated environments

**Observability Components**:
- Trace ID for each story flowing through all agents
- Structured JSON logs for searchability
- Real-time KPI dashboard (velocity, quality, automation rate)
- Historical trend analysis

**Alternatives Considered**:
- Basic logging: Insufficient for distributed debugging
- No metrics: Cannot measure success or identify improvement opportunities
- External APM tools: Additional cost and integration complexity

## Risks / Trade-offs

### Risk: Complexity of Distributed System
**Impact**: Agent coordination, state management, and failure handling are more complex than linear pipelines.

**Mitigation**:
- Clear agent contracts and message protocols
- Comprehensive testing of failure scenarios
- Circuit breakers to prevent cascade failures
- Detailed documentation and examples

### Risk: Dependency on External Services
**Impact**: System depends on opencode agent, CI platforms, and Kanban APIs. Service outages block migrations.

**Mitigation**:
- Graceful degradation where possible
- Retry mechanisms for transient failures
- Health checks and service monitoring
- Fallback to manual operations for critical migrations

### Risk: Quality Gate False Positives/Negatives
**Impact**: Too strict gates block valid migrations; too lenient gates allow low-quality code.

**Mitigation**:
- Configurable thresholds in rule.md
- Human override capability
- Continuous tuning based on historical data
- Multiple quality dimensions (not just single metric)

### Risk: Agent Mesh Learning Curve
**Impact**: Teams unfamiliar with agent-based architecture may struggle with debugging and extending.

**Mitigation**:
- Comprehensive documentation and examples
- Clear separation between skills (simple) and agents (complex)
- Progressive disclosure (start with basic skills, advance to agents)
- Observability tooling for understanding agent behavior

### Trade-off: Automation vs. Control
**Decision**: Optimize for automation (>80% rate) while preserving human oversight.

**Implications**:
- Human intervention points are well-defined (documentation updates, complex failures)
- Agents escalate rather than make risky decisions
- Full audit trail allows human review of automated decisions

### Trade-off: Generalization vs. Specificity
**Decision**: Start with common migration patterns, extend for specific cases via rule.md.

**Implications**:
- Initial implementation focuses on framework/language migrations
- Custom patterns configured via rules rather than code changes
- Some edge cases may require manual handling initially

## Migration Plan

### Phase 1: Foundation (Weeks 1-2)
1. Create `.claude/` directory structure
2. Implement configuration files (rule.md, tasks.md, CLAUDE.md templates)
3. Set up CI/CD and Kanban integrations
4. Establish observability infrastructure

### Phase 2: Skills Implementation (Weeks 3-4)
1. Implement Priority 1 skills (analyze-codebase, generate-tests, apply-refactor)
2. Implement Priority 2 skills (validation and quality gates)
3. Implement Priority 3 skills (CI integration and KPI tracking)
4. Test each skill independently

### Phase 3: Agents Implementation (Weeks 5-6)
1. Implement story-orchestrator-agent (core coordination)
2. Implement harness agents (test, code, benchmark, evaluation, CI)
3. Implement support agents (failure-analyzer, kpi-tracker)
4. Test agent collaboration and message passing

### Phase 4: Integration Testing (Week 7)
1. End-to-end testing with sample migration
2. Failure scenario testing
3. Performance and scalability testing
4. Security and compliance validation

### Phase 5: Pilot (Week 8)
1. Select low-risk migration project
2. Run full workflow with monitoring
3. Collect feedback and metrics
4. Tune thresholds and rules

### Rollback Strategy
- All changes in version control (git)
- Agents can be disabled individually
- Skills can be invoked manually as fallback
- Configuration rollback via git revert
- No database migrations required (file-based config)

## Open Questions

1. **Multi-repository Support**: How to handle migrations spanning multiple repositories?
   - Option A: Run separate agent mesh per repository
   - Option B: Coordinate across repositories with super-orchestrator
   - Decision needed: Depends on cross-repo dependency patterns

2. **Baseline Establishment**: When to re-establish performance baselines?
   - Option A: Per migration story
   - Option B: Fixed schedule (quarterly)
   - Decision needed: Depends on how frequently performance characteristics change

3. **Human Review Trigger**: What conditions require mandatory human review vs. optional?
   - Current: Escalate after 3 failed retries
   - Open: Should certain migration types (security-related, public APIs) always require review?

4. **Concurrent Story Limit**: How many stories should agent mesh process in parallel?
   - Trade-off: More parallelism = faster throughput but higher resource usage
   - Decision needed: Based on resource capacity and contention testing

5. **Historical Data Retention**: How long to keep KPI metrics and trace data?
   - Option A: Keep all data indefinitely (audit trail)
   - Option B: Aggregate and archive after N days
   - Decision needed: Based on compliance requirements and storage costs
