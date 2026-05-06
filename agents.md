# Agents Definition - Code Migration System

## Overview

Agents are autonomous, multi-step task executors that orchestrate skills to accomplish complex workflows. Each harness phase has dedicated agents that manage the end-to-end process.

---

## 1. Project Tracking HARNESS Agents

### `project-tracker-agent`

**Role**: Orchestrate the entire migration planning and backlog management

**Responsibilities**:
1. Trigger codebase analysis
2. Create migration plan
3. Generate and maintain backlog
4. Loop through user stories
5. Coordinate with other harnesses

**Skills Used**:
- `/analyze-codebase`
- `/plan-migration`
- `/generate-backlog`
- `/update-documentation`

**Workflow**:
```
1. Check for new migration requests or updated rule.md
2. Invoke /analyze-codebase for target codebase
3. Invoke /plan-migration with analysis results
4. Invoke /generate-backlog to create Kanban tickets
5. For each user story in backlog:
   a. Check prerequisites (dependencies satisfied)
   b. Invoke test-harness-agent for story
   c. Monitor progress and update Kanban
   d. Handle failures (retry, escalate to human)
6. Update tasks.md with progress
7. Loop continuously
```

**Triggers**:
- New migration request
- Updated `rule.md` or `tasks.md`
- Manual invocation
- Scheduled interval

**Outputs**:
- Maintained backlog
- Updated tasks.md
- Progress reports
- Kanban board updates

---

### `story-orchestrator-agent`

**Role**: Manage individual user story lifecycle

**Responsibilities**:
1. Coordinate harness execution for a single story
2. Pass story context through harnesses
3. Handle failures and retries
4. Update story status

**Skills Used**:
- All harness-specific skills
- `/update-documentation`
- `/generate-kpi-metrics`

**Workflow**:
```
1. Receive user story from project-tracker-agent
2. Invoke test-harness-agent with story context
3. Wait for test completion
4. Invoke code-harness-agent with test artifacts
5. Wait for code completion
6. Invoke benchmark-harness-agent
7. Invoke evaluation-harness-agent
8. If evaluation passes:
   a. Invoke ci-harness-agent
   b. Monitor CI pipeline
9. If evaluation fails:
   a. Generate root cause analysis
   b. Return story to backlog
   c. Update tasks.md
10. Update Kanban status
```

**Triggers**:
- Story selected from backlog
- Retry request
- Manual invocation for specific story

**Outputs**:
- Story completion status
- Artifacts bundle
- Updated Kanban ticket
- KPI metrics

---

## 2. Test HARNESS Agents

### `test-generator-agent`

**Role**: Generate comprehensive test coverage for migration

**Responsibilities**:
1. Analyze code to test
2. Generate characterization tests
3. Generate functional tests
4. Validate coverage
5. Package test suite

**Skills Used**:
- `/generate-characterization-tests`
- `/generate-functional-tests`
- `/validate-coverage`

**Workflow**:
```
1. Receive story and code scope from story-orchestrator-agent
2. Analyze existing code structure
3. Invoke /generate-characterization-tests
   a. Capture current behavior
   b. Lock in existing functionality
4. Invoke /generate-functional-tests
   a. Based on migration specifications
   b. Define expected post-migration behavior
5. Execute all generated tests
6. Invoke /validate-coverage
   a. Check coverage thresholds
   b. If insufficient, generate more tests (iterate)
7. Package test suite with metadata
8. Return test artifacts to story-orchestrator-agent
```

**Triggers**:
- Story-orchestrator-agent request
- Manual test generation request
- Retry after test failures

**Outputs**:
- Characterization test suite
- Functional test suite
- Coverage reports
- Test metadata JSON

**Success Criteria**:
- Coverage >= configured threshold
- All tests pass on current code
- Functional tests defined for expected behavior

---

## 3. Code HARNESS Agents

### `code-refactor-agent`

**Role**: Execute spec-driven code refactoring and transformation

**Responsibilities**:
1. Apply automated refactoring rules
2. Generate new code from specifications
3. Validate transformations
4. Ensure behavior preservation

**Skills Used**:
- `/apply-refactor-rules`
- `/generate-spec-driven-code`
- `/validate-refactoring`

**Workflow**:
```
1. Receive test artifacts and specifications from story-orchestrator-agent
2. Load refactoring rules
3. Invoke /apply-refactor-rules
   a. Run in dry-run mode first using opencode agent
   b. Review transformation plan
   c. Apply transformations using opencode agent
4. For gaps not covered by automated refactoring:
   a. Invoke /generate-spec-driven-code
   b. Generate new implementations
5. Invoke /validate-refactoring
   a. Run characterization tests (should still pass)
   b. Run functional tests (expected behavior)
   c. Validate against specifications
6. If validation fails:
   a. Analyze failures
   b. Attempt fixes (limited retries)
   c. If still failing, escalate to human
7. Package refactored code with metadata
8. Return artifacts to story-orchestrator-agent
```

**Triggers**:
- Story-orchestrator-agent request
- Manual refactoring request
- Retry after validation failures

**Outputs**:
- Refactored source code
- Code generation artifacts
- Validation reports
- Transformation logs

**Success Criteria**:
- All characterization tests pass (behavior preserved)
- All functional tests pass (new behavior correct)
- Code passes validation against specs

---

## 4. Benchmark HARNESS Agents

### `benchmark-builder-agent`

**Role**: Build and execute benchmark test suite

**Responsibilities**:
1. Compile benchmark suite from tests
2. Establish performance baselines
3. Execute benchmarks
4. Compare against baselines

**Skills Used**:
- `/build-benchmark-suite`
- `/establish-baseline`
- `/run-benchmarks`

**Workflow**:
```
1. Receive test artifacts from story-orchestrator-agent
2. Invoke /build-benchmark-suite
   a. Select performance-critical tests
   b. Configure benchmark framework
   c. Package suite
3. Check if baseline exists:
   a. If NO: Invoke /establish-baseline
      - Run benchmarks multiple times
      - Calculate statistical baselines
      - Store for future comparisons
   b. If YES: Load existing baseline
4. Invoke /run-benchmarks
   a. Execute benchmark suite
   b. Collect performance metrics
   c. Compare against baseline
5. Analyze performance deltas
   a. If regression > threshold: FAIL
   b. If improvement or acceptable: PASS
6. Package benchmark results
7. Return artifacts to story-orchestrator-agent
```

**Triggers**:
- Story-orchestrator-agent request
- Baseline establishment request
- Manual benchmark execution

**Outputs**:
- Benchmark suite
- Baseline metrics (if new)
- Performance comparison report
- Pass/fail status

**Success Criteria**:
- No performance regressions beyond threshold
- Benchmark suite executes successfully
- Statistical validity of results

---

## 5. Evaluation HARNESS Agents

### `quality-evaluator-agent`

**Role**: Comprehensive quality evaluation and scoring

**Responsibilities**:
1. Aggregate all metrics and results
2. Run quality assessments using opencode agent
3. Calculate quality scores
4. Validate against thresholds
5. Make go/no-go decision

**Skills Used**:
- `/generate-evaluation-metrics`
- `/calculate-test-scores`
- `/validate-quality`
- `/generate-kpi-metrics`

**Workflow**:
```
1. Receive artifacts from story-orchestrator-agent:
   - Refactored code
   - Test results
   - Benchmark results
   - Coverage data
2. Invoke /generate-evaluation-metrics
   a. Aggregate code quality metrics using opencode agent
   b. Run quality assessments using opencode agent
   c. Calculate composite scores
3. Invoke /calculate-test-scores
   a. Parse all test results
   b. Weight by importance
   c. Generate final test score
4. Invoke /validate-quality
   a. Check all thresholds
   b. Identify blockers
   c. Make pass/fail determination
5. If PASS:
   a. Package evaluation report
   b. Return SUCCESS to story-orchestrator-agent
6. If FAIL:
   a. Invoke /request-root-cause
   b. Generate detailed failure analysis
   c. Invoke /generate-kpi-metrics
   d. Return FAILURE with analysis
7. Update evaluation history
```

**Triggers**:
- Story-orchestrator-agent request
- Manual evaluation request
- Re-evaluation after fixes

**Outputs**:
- Comprehensive evaluation report
- Quality scores and metrics
- Pass/fail determination
- Root cause analysis (if failed)
- KPI metrics

**Success Criteria**:
- All quality thresholds met
- No blocking issues
- Test scores above minimum
- Performance acceptable

**Quality Dimensions**:
- **Correctness**: Test pass rates, spec compliance
- **Performance**: Benchmark results, no regressions
- **Coverage**: Code coverage, test coverage
- **Quality**: Code quality metrics, complexity
- **Security**: Vulnerability scans, security checks

---

## 6. CI HARNESS Agents

### `ci-integration-agent`

**Role**: Manage CI platform integration and pipeline execution

**Responsibilities**:
1. Prepare merge requests
2. Push to CI platform
3. Monitor pipeline execution
4. Handle results
5. Update tracking systems

**Skills Used**:
- `/prepare-merge-request`
- `/push-merge-request`
- `/monitor-pipeline`
- `/handle-pipeline-result`
- `/generate-kpi-metrics`

**Workflow**:
```
1. Receive approved artifacts from story-orchestrator-agent
2. Invoke /prepare-merge-request
   a. Generate MR description
   b. Attach all artifacts
   c. Create checklist
   d. Prepare metadata
3. Invoke /push-merge-request
   a. Authenticate with CI platform
   b. Create MR
   c. Upload artifacts
   d. Trigger CI pipeline
4. Invoke /monitor-pipeline
   a. Poll pipeline status
   b. Collect job results
   c. Stream logs if needed
5. Wait for pipeline completion
6. Invoke /handle-pipeline-result
   a. If SUCCESS:
      - Merge MR (if auto-merge enabled)
      - Update Kanban to Done
      - Archive artifacts
   b. If FAILURE:
      - Close MR
      - Invoke /generate-kpi-metrics
      - Invoke /request-root-cause
      - Update Kanban to Backlog
      - Notify stakeholders
7. Update tracking and history
```

**Triggers**:
- Story-orchestrator-agent request
- Manual MR creation
- Retry after pipeline fixes

**Outputs**:
- Merge request URL
- Pipeline results
- KPI metrics (if failed)
- Updated Kanban board
- Tracking data

**Success Criteria**:
- MR created successfully
- Pipeline executes without errors
- All CI checks pass
- Human review approved (if required)

**CI Checks**:
- Build success
- All tests pass
- Code quality gates
- Security scans
- Performance benchmarks

---

## 7. Specialized Utility Agents

### `failure-analyzer-agent`

**Role**: Deep root cause analysis for failures

**Responsibilities**:
1. Collect failure artifacts
2. Analyze logs and errors
3. Trace to root cause
4. Generate remediation plan

**Skills Used**:
- `/request-root-cause`
- `/update-documentation`

**Workflow**:
```
1. Receive failure data from any harness agent
2. Invoke /request-root-cause with comprehensive context
3. Analyze multiple failure dimensions:
   a. Test failures → code issues
   b. Pipeline failures → infrastructure issues
   c. Quality failures → architectural issues
4. Generate failure hypothesis
5. Suggest remediation steps
6. Update tasks.md with fix plan
7. Optionally request human intervention
8. Return analysis to requesting agent
```

**Triggers**:
- Failure in any harness
- Repeated failures
- Complex failures needing deep analysis

**Outputs**:
- Root cause analysis report
- Remediation suggestions
- Updated tasks.md
- Human escalation (if needed)

---

### `documentation-manager-agent`

**Role**: Maintain rule.md and tasks.md

**Responsibilities**:
1. Track documentation updates
2. Apply changes from human and agent feedback
3. Maintain change history
4. Validate documentation format

**Skills Used**:
- `/update-documentation`

**Workflow**:
```
1. Listen for documentation update events:
   a. Human requests
   b. Agent learnings
   c. Failed migrations needing new rules
2. Invoke /update-documentation
3. Validate changes
4. Maintain changelog
5. Notify relevant agents of changes
6. Trigger re-analysis if rules changed significantly
```

**Triggers**:
- Human update request
- Agent recommendation
- Post-failure updates
- Periodic review

**Outputs**:
- Updated `rule.md`
- Updated `tasks.md`
- Change log entries
- Notification to agents

---

### `kpi-tracker-agent`

**Role**: Track and report KPI metrics across all harnesses

**Responsibilities**:
1. Collect metrics from all agents
2. Calculate aggregate KPIs
3. Track trends over time
4. Generate reports and dashboards

**Skills Used**:
- `/generate-kpi-metrics`

**Workflow**:
```
1. Collect metrics from all harness agents:
   a. Success/failure rates
   b. Cycle times
   c. Quality scores
   d. Human intervention frequency
2. Invoke /generate-kpi-metrics
3. Calculate aggregate KPIs:
   a. Migration velocity
   b. Quality trends
   c. Automation rate
   d. Time to resolution
4. Generate dashboards
5. Identify trends and anomalies
6. Alert on threshold violations
7. Provide insights to project-tracker-agent
```

**Triggers**:
- Periodic schedule (daily, weekly)
- Manual report request
- Threshold violation detection

**Outputs**:
- KPI dashboard
- Trend analysis
- Alerts and anomalies
- Historical data

---

## Agent Communication & Coordination

### Message Passing
Agents communicate through structured message passing:
```json
{
  "from_agent": "story-orchestrator-agent",
  "to_agent": "test-generator-agent",
  "message_type": "request",
  "payload": {
    "story_id": "US-123",
    "code_scope": "/src/main/java/com/example",
    "specifications": "path/to/specs.json"
  },
  "correlation_id": "uuid-1234",
  "timestamp": "2026-05-04T10:00:00Z"
}
```

### State Management
Each agent maintains:
- **Current state**: idle, working, waiting, failed
- **Work queue**: Pending tasks
- **History**: Completed tasks and outcomes
- **Context**: Current story/migration context

### Error Handling
Agents implement:
1. **Retry logic**: Exponential backoff for transient failures
2. **Circuit breakers**: Stop after N consecutive failures
3. **Escalation**: Human intervention when stuck
4. **Rollback**: Undo changes on critical failures

### Observability
All agents log:
- State transitions
- Skill invocations
- Decisions made
- Errors and warnings
- Performance metrics

---

## Agent Lifecycle

### Initialization
1. Load configuration
2. Connect to required services (CI platform, Kanban API)
3. Validate skill availability
4. Enter idle state

### Execution
1. Receive trigger
2. Transition to working state
3. Execute workflow
4. Invoke skills as needed
5. Coordinate with other agents
6. Handle errors
7. Return results
8. Transition to idle or next task

### Termination
1. Complete current task
2. Persist state
3. Clean up resources
4. Log final metrics

---

## Agent Configuration

Each agent requires configuration for:
- **Skills**: Which skills are available
- **Thresholds**: Quality gates, timeouts, retry limits
- **Integrations**: API endpoints, credentials
- **Behavior**: Retry strategies, escalation rules
- **Logging**: Log levels, destinations

Example agent config:
```yaml
agent: test-generator-agent
skills:
  - /generate-characterization-tests
  - /generate-functional-tests
  - /validate-coverage
thresholds:
  min_coverage: 80
  max_retries: 3
  timeout_seconds: 600
integrations:
  opencode_api: "http://localhost:8080"
  openspec_api: "http://localhost:8081"
behavior:
  retry_strategy: exponential_backoff
  escalate_after_failures: 3
logging:
  level: INFO
  destination: /var/log/agents/test-generator.log
```

---

## Agent Orchestration Pattern

The overall orchestration follows this pattern:

```
project-tracker-agent (MAIN LOOP)
  └─> story-orchestrator-agent (PER STORY)
        ├─> test-generator-agent
        ├─> code-refactor-agent
        ├─> benchmark-builder-agent
        ├─> quality-evaluator-agent
        └─> ci-integration-agent
              └─> kpi-tracker-agent (on completion)
```

Supporting agents:
- `failure-analyzer-agent` (on-demand)
- `documentation-manager-agent` (on-demand)
- `kpi-tracker-agent` (periodic + on-demand)

---

## Human-in-the-Loop

Agents request human intervention when:
1. **Quality evaluation fails repeatedly** (>N retries)
2. **Root cause cannot be determined automatically**
3. **Ambiguous specifications or rules**
4. **Security or compliance concerns**
5. **Architectural decisions needed**

Human can:
- Review and approve/reject agent work
- Update `rule.md` and `tasks.md`
- Request root cause analysis
- Override agent decisions
- Adjust thresholds and configurations
- Manually retry or skip tasks
