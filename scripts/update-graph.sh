#!/bin/bash
# Simple wrapper for graphify extraction
#
# This script runs graphify extract to build the knowledge graph.
# Graphify automatically extracts annotations and imports via tree-sitter AST parsing.
#
# Usage:
#   ./scripts/update-graph.sh           # Full extraction
#   ./scripts/update-graph.sh --update  # Incremental update
#
# Requirements:
#   - graphify CLI installed (uv tool install graphifyy)

set -e  # Exit on error

echo "Updating knowledge graph..."
echo ""

# Check if graphify is installed
if ! command -v graphify &> /dev/null; then
    echo "Error: graphify command not found" >&2
    echo "Install with: uv tool install graphifyy && graphify install" >&2
    echo "Or: pipx install graphifyy && graphify install" >&2
    exit 1
fi

# Run graphify extract
if [ "$1" == "--update" ]; then
    echo "Running incremental update..."
    graphify extract . --update
else
    echo "Running full extraction..."
    graphify extract .
fi

if [ $? -ne 0 ]; then
    echo "Error: graphify extract failed" >&2
    exit 1
fi

echo ""
echo "=========================================="
echo "Graph updated successfully!"
echo "=========================================="
echo ""
echo "Output files:"
echo "  - graphify-out/graph.json (complete graph with annotations and imports)"
echo "  - graphify-out/graph.html (interactive visualization)"
echo "  - graphify-out/GRAPH_REPORT.md (architecture summary)"
echo ""
echo "Next steps:"
echo "  - Query graph: graphify query \"Find services\""
echo "  - View report: cat graphify-out/GRAPH_REPORT.md"
echo "  - Migration analysis: source scripts/migration-queries.sh && show_migration_status"
