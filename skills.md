# Skills Definition - Code Migration System

## Overview

Skills are reusable, focused commands that execute specific actions within each harness phase. They are invoked by agents or directly by users.

---

## 1. Project Tracking HARNESS Skills

### `/analyze-codebase`
**Description**: Analyze codebase to identify migration needs

**Parameters**:
- `path` - Target codebase path
- `migration-type` - Type of migration (e.g., framework, language, platform)
- `scope` - Analysis scope (full, incremental, specific-modules)

**Actions**:
1. Scan codebase structure
2. Identify dependencies and frameworks
3. Detect anti-patterns and technical debt
4. Generate migration complexity assessment
5. Output analysis report

**Outputs**:
- `analysis-report.json` - Structured analysis data
- `complexity-score.json` - Migration complexity metrics

---

### `/plan-migration`
**Description**: Create migration plan from analysis

**Parameters**:
- `analysis-report` - Path to analysis report
- `rule-file` - Path to rule.md
- `priority` - Prioritization strategy (risk, complexity, business-value)

**Actions**:
1. Parse analysis report
2. Apply migration rules from rule.md
3. Generate user stories
4. Prioritize stories based on strategy
5. Create task breakdown

**Outputs**:
- `migration-plan.json` - Complete migration plan
- `user-stories.json` - Backlog of user stories
- Updated `tasks.md`

---

### `/generate-backlog`
**Description**: Generate and update Kanban backlog

**Parameters**:
- `user-stories` - Path to user stories JSON
- `kanban-api` - Kanban board API endpoint

**Actions**:
1. Parse user stories
2. Create Kanban tickets
3. Set priorities and labels
4. Link dependencies
5. Assign to appropriate columns

**Outputs**:
- Updated Kanban board
- `backlog-mapping.json` - Story to ticket mapping

---

## 2. Test HARNESS Skills

### `/generate-characterization-tests`
**Description**: Create tests that capture current behavior

**Parameters**:
- `source-path` - Path to source code
- `test-framework` - Target test framework (JUnit, pytest, etc.)
- `coverage-target` - Minimum coverage percentage

**Actions**:
1. Analyze source code structure
2. Identify public APIs and methods
3. Capture current behavior through execution
4. Generate test cases that lock in behavior
5. Validate test coverage

**Outputs**:
- Generated test files
- `coverage-report.json`
- `characterization-tests.json` - Test metadata

**Tools**: opencode agent

---

### `/generate-functional-tests`
**Description**: Create tests for expected migrated behavior

**Parameters**:
- `spec-path` - Path to specifications
- `test-framework` - Target test framework
- `behavior-rules` - Path to expected behavior rules

**Actions**:
1. Parse specifications
2. Identify expected behaviors post-migration
3. Generate functional test cases
4. Include edge cases and error scenarios
5. Validate against specifications

**Outputs**:
- Generated functional test files
- `functional-tests.json` - Test metadata
- `spec-coverage.json`

**Tools**: opencode agent

---

### `/validate-coverage`
**Description**: Validate test coverage meets requirements

**Parameters**:
- `test-results` - Path to test execution results
- `min-coverage` - Minimum coverage threshold
- `coverage-type` - line, branch, mutation

**Actions**:
1. Analyze test execution results
2. Calculate coverage metrics
3. Identify coverage gaps
4. Generate gap report
5. Pass/fail determination

**Outputs**:
- `coverage-validation.json`
- `coverage-gaps.json`
- Pass/fail status

---

## 3. Code HARNESS Skills

### `/apply-refactor-rules`
**Description**: Apply refactoring rules using opencode agent

**Parameters**:
- `source-path` - Path to source code
- `rules-path` - Path to refactoring rules YAML
- `dry-run` - Preview changes without applying

**Actions**:
1. Load refactoring rules
2. Parse source code using opencode agent
3. Apply refactoring transformations using opencode agent
4. Validate syntax and semantics using opencode agent
5. Generate diff report

**Outputs**:
- Refactored source files
- `refactor-diff.json`
- `refactor-log.json`

**Tools**: opencode agent

---

### `/generate-spec-driven-code`
**Description**: Generate code based on specifications

**Parameters**:
- `spec-path` - Path to code specifications
- `template-path` - Optional code templates
- `target-framework` - Target framework/language

**Actions**:
1. Parse code specifications
2. Load code templates if provided
3. Generate implementation code
4. Validate against specifications
5. Format and organize code

**Outputs**:
- Generated source files
- `generation-report.json`
- `spec-validation.json`

**Tools**: opencode agent

---

### `/validate-refactoring`
**Description**: Validate refactored code meets specifications

**Parameters**:
- `refactored-path` - Path to refactored code
- `spec-path` - Path to specifications
- `test-suite` - Path to test suite

**Actions**:
1. Run test suite against refactored code
2. Validate against specifications
3. Check for regressions
4. Verify behavior preservation
5. Generate validation report

**Outputs**:
- `validation-report.json`
- Test results
- Pass/fail status

**Tools**: opencode agent

---

## 4. Benchmark HARNESS Skills

### `/build-benchmark-suite`
**Description**: Compile benchmark test suite

**Parameters**:
- `test-path` - Path to test files
- `benchmark-framework` - Benchmark framework (JMH, pytest-benchmark, etc.)
- `baseline-data` - Path to baseline metrics

**Actions**:
1. Collect all passing tests
2. Configure benchmark framework
3. Build benchmark suite
4. Set baseline comparisons
5. Package suite for execution

**Outputs**:
- Benchmark test suite
- `benchmark-config.json`
- `suite-manifest.json`

---

### `/establish-baseline`
**Description**: Establish performance baseline

**Parameters**:
- `benchmark-suite` - Path to benchmark suite
- `runs` - Number of benchmark runs
- `warmup` - Warmup iterations

**Actions**:
1. Execute benchmark suite
2. Collect performance metrics
3. Calculate statistical baselines
4. Identify performance characteristics
5. Store baseline data

**Outputs**:
- `baseline-metrics.json`
- `performance-profile.json`

---

### `/run-benchmarks`
**Description**: Execute benchmark tests and compare

**Parameters**:
- `benchmark-suite` - Path to benchmark suite
- `baseline` - Path to baseline metrics
- `threshold` - Acceptable performance delta

**Actions**:
1. Execute benchmark suite
2. Collect current metrics
3. Compare against baseline
4. Calculate performance deltas
5. Pass/fail determination

**Outputs**:
- `benchmark-results.json`
- `performance-delta.json`
- Pass/fail status

---

## 5. Evaluation HARNESS Skills

### `/generate-evaluation-metrics`
**Description**: Generate comprehensive evaluation metrics

**Parameters**:
- `code-path` - Path to code
- `test-results` - Path to test results
- `benchmark-results` - Path to benchmark results
- `quality-rules` - Path to quality rules

**Actions**:
1. Collect all artifacts
2. Calculate quality metrics using opencode agent
3. Run quality assessments using opencode agent
4. Aggregate scores
5. Generate evaluation report

**Outputs**:
- `evaluation-metrics.json`
- `quality-score.json`
- `deepeval-report.json`

**Tools**: opencode agent

---

### `/calculate-test-scores`
**Description**: Calculate comprehensive test scores

**Parameters**:
- `test-results` - Path to test results
- `coverage-data` - Path to coverage data
- `scoring-rules` - Path to scoring rules

**Actions**:
1. Parse test results
2. Calculate pass/fail rates
3. Weight by test importance
4. Factor in coverage metrics
5. Generate final score

**Outputs**:
- `test-scores.json`
- `score-breakdown.json`

---

### `/validate-quality`
**Description**: Validate code quality meets thresholds

**Parameters**:
- `evaluation-metrics` - Path to metrics
- `quality-thresholds` - Path to threshold config
- `blocking-rules` - Rules that fail the validation

**Actions**:
1. Load evaluation metrics
2. Apply quality thresholds
3. Check blocking rules
4. Generate pass/fail determination
5. Create validation report

**Outputs**:
- `quality-validation.json`
- Pass/fail status
- `blockers.json` (if failed)

---

## 6. CI HARNESS Skills

### `/prepare-merge-request`
**Description**: Prepare merge request with all artifacts

**Parameters**:
- `branch-name` - Feature branch name
- `target-branch` - Target merge branch
- `artifacts-path` - Path to migration artifacts
- `template` - MR template path

**Actions**:
1. Collect all migration artifacts
2. Generate MR description from template
3. Attach test results and metrics
4. Create checklist from validation steps
5. Prepare MR metadata

**Outputs**:
- `mr-description.md`
- `mr-metadata.json`
- `artifacts-bundle.zip`

---

### `/push-merge-request`
**Description**: Push MR to CI platform

**Parameters**:
- `mr-metadata` - Path to MR metadata
- `ci-platform` - gitlab or github
- `api-token` - CI platform API token
- `auto-assign` - Auto-assign reviewers

**Actions**:
1. Authenticate with CI platform
2. Create merge request
3. Upload artifacts
4. Assign reviewers if configured
5. Add labels and milestones
6. Trigger CI pipeline

**Outputs**:
- MR URL
- `mr-tracking.json`
- Pipeline trigger ID

---

### `/monitor-pipeline`
**Description**: Monitor CI pipeline execution

**Parameters**:
- `pipeline-id` - CI pipeline ID
- `ci-platform` - gitlab or github
- `poll-interval` - Polling interval in seconds

**Actions**:
1. Connect to CI platform
2. Poll pipeline status
3. Collect job results
4. Track test execution
5. Report status changes

**Outputs**:
- `pipeline-status.json`
- Real-time status updates
- `job-results.json`

---

### `/handle-pipeline-result`
**Description**: Handle pipeline success or failure

**Parameters**:
- `pipeline-result` - Path to pipeline results
- `kanban-api` - Kanban board API
- `retry-strategy` - Auto-retry strategy

**Actions**:
1. Parse pipeline results
2. On SUCCESS: Close MR, update Kanban to Done
3. On FAILURE: Close MR, generate KPI metrics, return to backlog
4. Update task tracking
5. Notify stakeholders

**Outputs**:
- Updated Kanban board
- `pipeline-outcome.json`
- `kpi-metrics.json` (if failed)

**Tools**: opencode agent (for KPI metrics)

---

## 7. Cross-Cutting Skills

### `/generate-kpi-metrics`
**Description**: Generate KPI metrics for tracking

**Parameters**:
- `pipeline-results` - Path to pipeline results
- `test-results` - Path to test results
- `evaluation-metrics` - Path to evaluation metrics
- `time-data` - Execution time data

**Actions**:
1. Aggregate all metrics
2. Calculate KPIs (success rate, cycle time, etc.)
3. Track trends over time
4. Generate visualizations
5. Store historical data

**Outputs**:
- `kpi-dashboard.json`
- `metrics-history.json`
- `trend-analysis.json`

**Tools**: opencode agent

---

### `/update-documentation`
**Description**: Update rule.md and tasks.md

**Parameters**:
- `doc-type` - rule or tasks
- `updates` - Updates to apply
- `reason` - Reason for update

**Actions**:
1. Read current documentation
2. Apply updates
3. Validate format
4. Add change log entry
5. Commit changes

**Outputs**:
- Updated `rule.md` or `tasks.md`
- `changelog.md` entry

---

### `/request-root-cause`
**Description**: Request root cause analysis for failures

**Parameters**:
- `failure-data` - Path to failure information
- `context` - Additional context
- `depth` - Analysis depth (quick, deep, comprehensive)

**Actions**:
1. Collect failure artifacts
2. Analyze logs and error messages
3. Trace failure to root cause
4. Generate hypothesis
5. Suggest remediation

**Outputs**:
- `root-cause-analysis.md`
- `remediation-suggestions.json`
- Updated `tasks.md` with fix

---

## Skill Invocation

Skills can be invoked:
1. **By agents** - During autonomous workflow execution
2. **By users** - Direct command line invocation
3. **By hooks** - Triggered by events (commit, MR, etc.)
4. **By CI pipeline** - Automated pipeline steps

## Skill Configuration

Each skill should have:
- Clear parameter schema
- Input/output contracts
- Error handling strategy
- Logging and observability
- Rollback capabilities (where applicable)

## Skill Dependencies

Skills may depend on:
- opencode agent (all code operations)
- API access (CI platform, Kanban board)
- File system access
- Git repository access
