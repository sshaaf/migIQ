## 1. Update Agent Prompts with Graph-First Strategy

- [x] 1.1 Add "Code Analysis Strategy" section to test-generator-agent/agent.md
- [x] 1.2 Add "Code Analysis Strategy" section to code-refactor-agent/agent.md
- [x] 1.3 Add "Code Analysis Strategy" section to benchmark-builder-agent/agent.md
- [x] 1.4 Add "Code Analysis Strategy" section to quality-evaluator-agent/agent.md
- [x] 1.5 Add "Code Analysis Strategy" section to ci-integration-agent/agent.md
- [x] 1.6 Document when to use graph vs Grep/Read in each agent.md
- [x] 1.7 Add performance target (<5 file reads per task) to each agent.md
- [x] 1.8 Include graphify command examples (query, path, explain) in each agent.md

## 2. Create Pre-Execution Hook for Graph Availability

- [x] 2.1 Create or update .claude/settings.json file
- [x] 2.2 Add PreAgentExecution hook configuration
- [x] 2.3 Add matcher for all agents (*-agent pattern)
- [x] 2.4 Add command to check if graphify-out/graph.json exists
- [x] 2.5 Add command to build graph if missing (graphify update .)
- [x] 2.6 Test hook execution with one agent
- [x] 2.7 Verify hook is idempotent (safe to run multiple times)

## 3. Create Common Graph Query Helpers

- [x] 3.1 Create scripts/graph-queries.sh file
- [x] 3.2 Implement graph_find_services function
- [x] 3.3 Implement graph_find_tests function
- [x] 3.4 Implement graph_find_dependencies function
- [x] 3.5 Implement graph_find_annotations function (placeholder)
- [x] 3.6 Implement graph_find_imports function (placeholder)
- [x] 3.7 Export all functions for shell use (export -f)
- [x] 3.8 Add usage examples in comments
- [x] 3.9 Test each function with sample project

## 4. Build Metadata Extractor

- [x] 4.1 Create scripts/extract_metadata.py file
- [x] 4.2 Implement extract_java_annotations function
- [x] 4.3 Add support for marker_annotation nodes
- [x] 4.4 Add support for normal_annotation nodes (with parameters)
- [x] 4.5 Implement extract_java_imports function
- [x] 4.6 Add support for import_declaration nodes
- [x] 4.7 Implement process_cache_directory function
- [x] 4.8 Build reverse indexes (annotation -> files, import -> files)
- [x] 4.9 Add error handling for malformed cache files
- [x] 4.10 Implement enhance_graph_json function
- [x] 4.11 Create annotation nodes with file_type metadata
- [x] 4.12 Create import nodes with import_prefix metadata
- [x] 4.13 Add has_annotation relationships
- [x] 4.14 Add imports relationships
- [x] 4.15 Set confidence scores (EXTRACTED, 1.0)
- [x] 4.16 Write enhanced graph to graph-enhanced.json
- [x] 4.17 Display extraction statistics (annotation count, import count)
- [x] 4.18 Show sample data in output
- [x] 4.19 Save metadata to metadata.json
- [x] 4.20 Test with sample Java project

## 5. Create Migration-Specific Query Helpers

- [x] 5.1 Create scripts/migration-queries.sh file
- [x] 5.2 Implement find_ejb_classes function
- [x] 5.3 Add detection for @Stateless annotation
- [x] 5.4 Add detection for @MessageDriven annotation
- [x] 5.5 Add detection for @Stateful annotation
- [x] 5.6 Implement find_javax_imports function
- [x] 5.7 Filter by import_prefix == "javax"
- [x] 5.8 Return unique sorted imports
- [x] 5.9 Implement find_files_using_annotation function
- [x] 5.10 Query by annotation name parameter
- [x] 5.11 Return source file paths
- [x] 5.12 Implement show_migration_status function
- [x] 5.13 Display EJB annotation counts
- [x] 5.14 Display javax import counts
- [x] 5.15 Display files needing migration count
- [x] 5.16 Export functions for shell use
- [x] 5.17 Test with sample migration project

## 6. Create Unified Graph Update Workflow

- [x] 6.1 Create scripts/update-graph.sh file
- [x] 6.2 Add step 1: Run graphify update .
- [x] 6.3 Add step 2: Run extract_metadata.py
- [x] 6.4 Add step 3: Copy graph-enhanced.json to graph.json
- [x] 6.5 Add success message output
- [x] 6.6 Make script executable (chmod +x)
- [x] 6.7 Add error handling for each step
- [x] 6.8 Test full workflow end-to-end

## 7. Create Baseline Benchmark Script

- [x] 7.1 Create scripts/benchmark-without-graph.sh file
- [x] 7.2 Add command to backup graphify-out directory
- [x] 7.3 Add command to run agent with time measurement
- [x] 7.4 Capture agent output to log file
- [x] 7.5 Add grep count for Grep tool calls
- [x] 7.6 Add grep count for Read tool calls
- [x] 7.7 Add count for files read
- [x] 7.8 Restore graphify-out from backup
- [x] 7.9 Display "Without Graphify" summary
- [x] 7.10 Make script executable
- [x] 7.11 Test with test-generator-agent

## 8. Create Graphify Benchmark Script

- [x] 8.1 Create scripts/benchmark-with-graph.sh file
- [x] 8.2 Add command to run update-graph.sh first
- [x] 8.3 Add command to run agent with time measurement
- [x] 8.4 Capture agent output to log file
- [x] 8.5 Add grep count for Grep tool calls
- [x] 8.6 Add grep count for Read tool calls
- [x] 8.7 Add grep count for graphify queries
- [x] 8.8 Display "With Graphify" summary
- [x] 8.9 Make script executable
- [x] 8.10 Test with test-generator-agent

## 9. Create Benchmark Comparison Script

- [x] 9.1 Create scripts/compare-benchmarks.py file
- [x] 9.2 Implement parse_log function
- [x] 9.3 Extract grep_calls metric
- [x] 9.4 Extract read_calls metric
- [x] 9.5 Extract graphify_queries metric
- [x] 9.6 Implement extract_time function
- [x] 9.7 Parse "real XmYs" format from time output
- [x] 9.8 Convert to total seconds
- [x] 9.9 Implement generate_report function
- [x] 9.10 Calculate time improvement percentage
- [x] 9.11 Calculate grep reduction percentage
- [x] 9.12 Calculate read reduction percentage
- [x] 9.13 Generate markdown table output
- [x] 9.14 Add summary section with key metrics
- [x] 9.15 Make script executable
- [x] 9.16 Test with sample log files

## 10. Validation and Testing

- [x] 10.1 Run baseline benchmark (without graph)
- [x] 10.2 Run graphify benchmark (with graph)
- [x] 10.3 Generate comparison report
- [x] 10.4 Verify at least 50% execution time improvement
- [x] 10.5 Verify at least 90% file read reduction
- [x] 10.6 Verify agents execute multiple graph queries
- [x] 10.7 Test graph query helpers with real codebase
- [x] 10.8 Test migration query helpers with Java EE project
- [x] 10.9 Verify metadata extraction finds annotations correctly
- [x] 10.10 Verify metadata extraction finds imports correctly
- [x] 10.11 Test PreAgentExecution hook in real workflow
- [x] 10.12 Verify graph-first strategy in agent logs
- [x] 10.13 Test graceful fallback when graph unavailable
- [x] 10.14 Measure graph update time (<30 seconds)

## 11. Documentation

- [x] 11.1 Document graph-first workflow in project README
- [x] 11.2 Add usage examples for graph query helpers
- [x] 11.3 Add usage examples for migration query helpers
- [x] 11.4 Document how to update graph after code changes
- [x] 11.5 Document benchmark suite usage
- [x] 11.6 Add troubleshooting section for common issues
- [x] 11.7 Document performance improvements achieved
- [x] 11.8 Add examples of graph queries vs traditional Grep/Read
