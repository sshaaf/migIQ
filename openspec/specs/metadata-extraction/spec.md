## REMOVED Requirements

### Requirement: Extract Java annotations from AST cache

**Reason**: Graphify performs annotation extraction automatically via tree-sitter AST parsing. Custom extraction script duplicates this functionality and creates maintenance burden.

**Migration**: Use graphify's built-in extraction. Annotations are included in `graphify-out/graph.json` automatically. Query with: `graphify query "Find classes with @AnnotationName"`

### Requirement: Extract Java imports from AST cache

**Reason**: Graphify performs import extraction automatically via tree-sitter AST parsing. Custom extraction script is redundant.

**Migration**: Use graphify's built-in extraction. Imports are included in `graphify-out/graph.json` automatically. Query with: `graphify query "Find files importing package.name.*"`

### Requirement: Enhance knowledge graph with metadata

**Reason**: Graphify's graph.json already contains all metadata (annotations, imports, dependencies). No need for custom graph-enhanced.json file.

**Migration**: Use `graphify-out/graph.json` directly instead of `graph-enhanced.json`. Graphify's output includes annotation and import relationships by default.

### Requirement: Save enhanced graph

**Reason**: Custom metadata extraction and graph enhancement workflow is unnecessary. Graphify produces complete graph in single step.

**Migration**: Delete `scripts/extract_metadata.py` and `scripts/update-graph.sh`. Use `/graphify .` or `graphify extract .` directly to build complete graph with all metadata.

### Requirement: Report extraction statistics

**Reason**: Graphify generates `GRAPH_REPORT.md` with comprehensive statistics including annotations, imports, and relationships.

**Migration**: Read `graphify-out/GRAPH_REPORT.md` for graph statistics instead of custom extraction output. Graphify's report includes god nodes, unexpected connections, and confidence scores.

### Requirement: Handle extraction errors gracefully

**Reason**: Graphify has robust error handling built-in. Custom extraction error handling is redundant.

**Migration**: Rely on graphify's error handling. If extraction fails, graphify will report errors clearly. No need for custom error handling wrapper.
