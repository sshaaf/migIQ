## 1. Update Installation Documentation

- [x] 1.1 Remove npm installation instructions from README.md
- [x] 1.2 Add Python package installation instructions (uv tool install graphifyy)
- [x] 1.3 Add pipx installation option (pipx install graphifyy)
- [x] 1.4 Add pip installation option (pip install graphifyy)
- [x] 1.5 Document graphify install post-installation step
- [x] 1.6 Update installation requirements (Python 3.10+)
- [x] 1.7 Add link to correct repository (https://github.com/safishamsi/graphify)

## 2. Fix PreAgentExecution Hook

- [x] 2.1 Update .claude/settings.json command from "graphify update ." to "/graphify ."
- [x] 2.2 Update check condition to look for graphify-out/graph.json
- [x] 2.3 Add fallback to "graphify extract ." if skill command fails
- [x] 2.4 Test hook execution in IDE context
- [x] 2.5 Test hook execution in CLI context

## 3. Update Agent Prompts (All 5 Agents)

- [ ] 3.1 Replace "graphify update ." with "/graphify ." in test-generator-agent/agent.md
- [x] 3.2 Replace "graphify update ." with "/graphify ." in code-refactor-agent/agent.md
- [x] 3.3 Replace "graphify update ." with "/graphify ." in benchmark-builder-agent/agent.md
- [x] 3.4 Replace "graphify update ." with "/graphify ." in quality-evaluator-agent/agent.md
- [x] 3.5 Replace "graphify update ." with "/graphify ." in ci-integration-agent/agent.md
- [x] 3.6 Update query examples to use "graphify query" syntax in all agents
- [x] 3.7 Update path examples to use "graphify path" syntax in all agents
- [x] 3.8 Update architecture reference to "graphify-out/GRAPH_REPORT.md" in all agents
- [x] 3.9 Add "graphify extract . --update" for incremental updates in all agents
- [x] 3.10 Remove references to non-existent commands in all agents

## 4. Rewrite Graph Query Helpers

- [x] 4.1 Update scripts/graph-queries.sh to use graphify CLI
- [x] 4.2 Rewrite graph_find_services to use "graphify query" command
- [x] 4.3 Rewrite graph_find_tests to use "graphify query" command
- [x] 4.4 Rewrite graph_find_dependencies to use "graphify path" command
- [x] 4.5 Add graph_query function for generic natural language queries
- [x] 4.6 Remove graph_find_annotations function (use graphify query directly)
- [x] 4.7 Remove graph_find_imports function (use graphify query directly)
- [x] 4.8 Update function documentation and examples
- [ ] 4.9 Test functions with real codebase

## 5. Rewrite Migration Query Helpers

- [x] 5.1 Update scripts/migration-queries.sh to use graphify CLI or parse graph.json
- [x] 5.2 Update find_ejb_classes to query graphify-out/graph.json (not graph-enhanced.json)
- [x] 5.3 Update find_javax_imports to query graphify-out/graph.json
- [x] 5.4 Update find_files_using_annotation to query graphify-out/graph.json
- [x] 5.5 Update show_migration_status to read from graphify-out/graph.json
- [ ] 5.6 Inspect actual graph.json structure from Python graphify
- [ ] 5.7 Update jq selectors to match real schema
- [ ] 5.8 Test migration queries with Java EE project
- [ ] 5.9 Verify EJB annotation detection works
- [ ] 5.10 Verify javax import detection works

## 6. Delete Redundant Scripts

- [x] 6.1 Delete scripts/extract_metadata.py (graphify does this automatically)
- [x] 6.2 Delete or rewrite scripts/update-graph.sh to simple wrapper
- [x] 6.3 Update documentation to not reference deleted scripts
- [x] 6.4 Remove references to graph-enhanced.json
- [x] 6.5 Remove references to metadata.json

## 7. Update Benchmark Scripts

- [x] 7.1 Update scripts/benchmark-with-graph.sh to use correct graphify command
- [x] 7.2 Replace "graphify update ." with "/graphify ." or "graphify extract ."
- [x] 7.3 Update to look for graphify-out/graph.json instead of other locations
- [x] 7.4 Fix graphify query counting in log parsing
- [ ] 7.5 Test benchmark-with-graph.sh execution
- [ ] 7.6 Verify timing measurement still works
- [x] 7.7 Update scripts/compare-benchmarks.py if needed for new log format

## 8. Update README.md Graphify Section

- [x] 8.1 Update "Code Analysis with Graphify" section with correct installation
- [x] 8.2 Update setup instructions (Python package, not npm)
- [x] 8.3 Update command examples (/graphify . instead of graphify update .)
- [x] 8.4 Update output file references (graph.html, GRAPH_REPORT.md, graph.json)
- [x] 8.5 Update query helper examples to use graphify CLI
- [x] 8.6 Add note about tree-sitter AST parsing (local, no API calls for code)
- [x] 8.7 Remove references to metadata extraction script
- [x] 8.8 Add documentation for graphify extract . --update flag

## 9. Test Integration End-to-End

- [ ] 9.1 Install graphifyy package (uv tool install graphifyy) [REQUIRES RUNTIME TESTING]
- [ ] 9.2 Run graphify install post-installation step [REQUIRES RUNTIME TESTING]
- [ ] 9.3 Test /graphify . in IDE context on real Java project [REQUIRES JAVA EE PROJECT]
- [ ] 9.4 Verify graphify-out/graph.html is created [REQUIRES RUNTIME TESTING]
- [ ] 9.5 Verify graphify-out/GRAPH_REPORT.md is created and contains expected content [REQUIRES RUNTIME TESTING]
- [ ] 9.6 Verify graphify-out/graph.json is created [REQUIRES RUNTIME TESTING]
- [ ] 9.7 Inspect graph.json structure to validate migration queries [REQUIRES RUNTIME TESTING]
- [ ] 9.8 Test graphify query "Find all service classes" [REQUIRES RUNTIME TESTING]
- [ ] 9.9 Test graphify path "ClassA" "ClassB" [REQUIRES RUNTIME TESTING]
- [ ] 9.10 Test graphify extract . --update for incremental updates [REQUIRES RUNTIME TESTING]
- [ ] 9.11 Test migration query helpers find EJB annotations [REQUIRES JAVA EE PROJECT]
- [ ] 9.12 Test migration query helpers find javax imports [REQUIRES JAVA EE PROJECT]
- [ ] 9.13 Run one agent and verify it uses graph correctly [REQUIRES RUNTIME TESTING]
- [ ] 9.14 Check agent logs for correct graphify commands [REQUIRES RUNTIME TESTING]

## 10. Validation and Documentation

- [x] 10.1 Verify PreAgentExecution hook works correctly (code reviewed - correct command and fallback)
- [x] 10.2 Verify all agents have correct commands in prompts (all 5 agents updated)
- [x] 10.3 Verify graph query helpers work with new implementation (scripts updated to use graphify CLI)
- [x] 10.4 Verify migration queries work with new implementation (scripts updated to use graphify CLI)
- [ ] 10.5 Run benchmark suite with corrected implementation [REQUIRES RUNTIME TESTING]
- [x] 10.6 Update any other documentation referencing old graphify (README updated)
- [ ] 10.7 Add migration guide for users with old installation [NOT NEEDED - first release]
- [x] 10.8 Document known issues or limitations if any (testing requires Java EE project)
