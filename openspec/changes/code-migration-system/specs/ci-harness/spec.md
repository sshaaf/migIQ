## ADDED Requirements

### Requirement: Prepare merge request with artifacts
The system SHALL prepare merge request with description, artifacts, and metadata from template.

#### Scenario: Generate MR description
- **WHEN** system invokes `/prepare-merge-request` with branch and template
- **THEN** system generates MR description from template with artifacts and checklist

#### Scenario: Bundle artifacts
- **WHEN** preparing merge request
- **THEN** system collects all migration artifacts (tests, code, metrics) into bundle

### Requirement: Push merge request to CI platform
The system SHALL create merge request on CI platform (GitLab or GitHub) and trigger pipeline.

#### Scenario: Authenticate and create MR
- **WHEN** system invokes `/push-merge-request` with valid credentials
- **THEN** system authenticates, creates MR, uploads artifacts, and triggers CI pipeline

#### Scenario: Auto-assign reviewers
- **WHEN** auto-assign configured
- **THEN** system assigns reviewers, adds labels, and sets milestones automatically

### Requirement: Monitor CI pipeline execution
The system SHALL monitor pipeline status by polling CI platform and collecting job results.

#### Scenario: Track pipeline progress
- **WHEN** system invokes `/monitor-pipeline` with pipeline ID
- **THEN** system polls status at configured interval and reports status changes

#### Scenario: Stream logs on failure
- **WHEN** job fails
- **THEN** system collects job logs for failure analysis

### Requirement: Handle pipeline results
The ci-integration-agent SHALL handle pipeline success or failure with appropriate actions.

#### Scenario: Pipeline success
- **WHEN** pipeline completes successfully
- **THEN** agent closes/merges MR (if auto-merge enabled) and updates Kanban to Done

#### Scenario: Pipeline failure
- **WHEN** pipeline fails
- **THEN** agent closes MR, generates KPI metrics using opencode agent, requests root cause, and returns story to backlog

### Requirement: Update tracking systems
The system SHALL synchronize status between CI platform, Kanban board, and tasks.md.

#### Scenario: Sync Kanban status
- **WHEN** pipeline result processed
- **THEN** system updates Kanban ticket status to match pipeline outcome

#### Scenario: Update tasks.md
- **WHEN** story completes or fails
- **THEN** system updates tasks.md with status and any failure notes
