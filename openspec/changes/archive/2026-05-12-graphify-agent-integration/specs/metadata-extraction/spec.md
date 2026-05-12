## ADDED Requirements

### Requirement: Extract Java annotations from AST cache

The system SHALL extract Java annotation metadata from graphify AST cache files.

#### Scenario: Extract marker annotations
- **WHEN** metadata extractor processes AST cache
- **THEN** system identifies all `marker_annotation` nodes and extracts annotation names

#### Scenario: Extract parameterized annotations
- **WHEN** metadata extractor encounters normal annotations
- **THEN** system identifies `annotation` nodes and extracts annotation names

#### Scenario: Build annotation index
- **WHEN** all cache files are processed
- **THEN** system creates reverse index mapping annotations to source files

### Requirement: Extract Java imports from AST cache

The system SHALL extract Java import statements from graphify AST cache files.

#### Scenario: Extract import declarations
- **WHEN** metadata extractor processes AST cache
- **THEN** system identifies all `import_declaration` nodes

#### Scenario: Build import index
- **WHEN** all imports are extracted
- **THEN** system creates reverse index mapping imports to source files

#### Scenario: Extract import prefixes
- **WHEN** processing imports
- **THEN** system extracts first segment as import prefix (javax, jakarta, etc.)

### Requirement: Enhance knowledge graph with metadata

The system SHALL add annotation and import nodes to the existing knowledge graph.

#### Scenario: Create annotation nodes
- **WHEN** enhancing graph
- **THEN** system adds nodes with `file_type: "annotation"` for each unique annotation

#### Scenario: Link annotations to files
- **WHEN** annotation nodes are created
- **THEN** system creates `has_annotation` relationships from source file nodes to annotation nodes

#### Scenario: Create import nodes
- **WHEN** enhancing graph
- **THEN** system adds nodes with `file_type: "import"` for each unique import

#### Scenario: Link imports to files
- **WHEN** import nodes are created
- **THEN** system creates `imports` relationships from source file nodes to import nodes

### Requirement: Save enhanced graph

The system SHALL save enhanced graph with confidence scoring for metadata relationships.

#### Scenario: Write enhanced graph file
- **WHEN** metadata extraction completes
- **THEN** system writes `graphify-out/graph-enhanced.json`

#### Scenario: Mark metadata confidence
- **WHEN** creating metadata relationships
- **THEN** system sets `confidence: "EXTRACTED"` and `confidence_score: 1.0`

### Requirement: Report extraction statistics

The system SHALL report metadata extraction statistics to user.

#### Scenario: Display annotation count
- **WHEN** extraction completes
- **THEN** system displays count of unique annotations found

#### Scenario: Display import count
- **WHEN** extraction completes
- **THEN** system displays count of unique imports found

#### Scenario: Display sample data
- **WHEN** reporting statistics
- **THEN** system shows sample annotations and imports with file counts

### Requirement: Handle extraction errors gracefully

The system SHALL continue processing remaining files when individual file extraction fails.

#### Scenario: Cache file read error
- **WHEN** cache file cannot be read
- **THEN** system logs error and continues with remaining files

#### Scenario: AST parse error
- **WHEN** AST structure is unexpected
- **THEN** system skips file and continues processing
