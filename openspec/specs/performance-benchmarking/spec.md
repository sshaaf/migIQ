## ADDED Requirements

### Requirement: Benchmark agent without graphify

The system SHALL provide script to measure agent performance without graphify integration.

#### Scenario: Disable graph temporarily
- **WHEN** running baseline benchmark
- **THEN** system moves `graphify-out` directory to backup location

#### Scenario: Run agent with instrumentation
- **WHEN** executing benchmark
- **THEN** system captures all agent output to log file

#### Scenario: Measure execution time
- **WHEN** benchmark runs
- **THEN** system records total execution time using `time` command

#### Scenario: Count tool usage
- **WHEN** benchmark completes
- **THEN** system counts Grep calls, Read calls, and files read from log

#### Scenario: Restore graph
- **WHEN** baseline benchmark finishes
- **THEN** system restores original `graphify-out` directory

### Requirement: Benchmark agent with graphify

The system SHALL provide script to measure agent performance with graphify integration.

#### Scenario: Ensure graph is fresh
- **WHEN** running graphify benchmark
- **THEN** system executes graph update workflow first

#### Scenario: Run agent with instrumentation
- **WHEN** executing benchmark
- **THEN** system captures all agent output to log file

#### Scenario: Measure execution time
- **WHEN** benchmark runs
- **THEN** system records total execution time

#### Scenario: Count graphify queries
- **WHEN** benchmark completes
- **THEN** system counts graphify query, path, and explain commands

#### Scenario: Count tool usage
- **WHEN** benchmark completes
- **THEN** system counts remaining Grep and Read calls

### Requirement: Compare benchmark results

The system SHALL provide script to generate performance comparison report.

#### Scenario: Parse log files
- **WHEN** comparison script runs
- **THEN** system extracts metrics from both baseline and graphify logs

#### Scenario: Calculate improvements
- **WHEN** metrics are extracted
- **THEN** system calculates percentage improvements for all metrics

#### Scenario: Generate markdown report
- **WHEN** calculations complete
- **THEN** system outputs formatted markdown table with results

#### Scenario: Display summary statistics
- **WHEN** report is generated
- **THEN** system shows overall speedup, I/O reduction, and new capabilities

### Requirement: Validate performance targets

The system SHALL validate that graphify integration achieves performance goals.

#### Scenario: Verify execution time improvement
- **WHEN** benchmarks complete
- **THEN** execution time with graphify is at least 50% faster than baseline

#### Scenario: Verify file read reduction
- **WHEN** benchmarks complete
- **THEN** file reads with graphify are reduced by at least 90%

#### Scenario: Verify graph query usage
- **WHEN** agent runs with graphify
- **THEN** agent executes multiple graph queries (>10)

### Requirement: Extract timing metrics from logs

The system SHALL extract execution timing from command output.

#### Scenario: Parse time command output
- **WHEN** processing benchmark log
- **THEN** system parses `real Xm Ys` format from time output

#### Scenario: Convert to seconds
- **WHEN** time is extracted
- **THEN** system converts minutes and seconds to total seconds

### Requirement: Support multiple agent types

The benchmark system SHALL support measuring performance of different agents.

#### Scenario: Benchmark test-generator-agent
- **WHEN** running benchmarks
- **THEN** system can measure test-generator-agent performance

#### Scenario: Benchmark other agents
- **WHEN** validating graphify integration
- **THEN** system can run same benchmarks on different agent types

### Requirement: Produce machine-readable output

The system SHALL output benchmark results in parseable format.

#### Scenario: JSON output option
- **WHEN** generating comparison report
- **THEN** system supports JSON output format for automation

#### Scenario: Include all metrics
- **WHEN** outputting JSON
- **THEN** result includes execution time, grep calls, read calls, and graphify queries
