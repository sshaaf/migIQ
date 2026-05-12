#!/bin/bash
# Benchmark agent with graphify
#
# This script measures agent performance WITH graphify integration.
# It ensures the graph is fresh, runs the agent, and measures tool usage.
#
# Usage:
#   ./scripts/benchmark-with-graph.sh <agent-name> <story-id>
#
# Example:
#   ./scripts/benchmark-with-graph.sh test-generator-agent US-TEST
#
# Output:
#   - benchmark-with-graph.log - Full agent output
#   - Summary statistics printed to console

set -e

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <agent-name> <story-id>"
    echo ""
    echo "Example:"
    echo "  $0 test-generator-agent US-TEST"
    exit 1
fi

AGENT_NAME=$1
STORY_ID=$2
LOG_FILE="benchmark-with-graph.log"

echo "=========================================="
echo "Graphify Benchmark (With Graph)"
echo "=========================================="
echo "Agent: $AGENT_NAME"
echo "Story: $STORY_ID"
echo ""

# Step 1: Update graph
echo "Step 1/3: Ensuring graph is fresh..."
if [ -f scripts/update-graph.sh ]; then
    ./scripts/update-graph.sh
    echo "✓ Graph updated"
else
    echo "Warning: scripts/update-graph.sh not found"
    echo "Running graphify extract . instead..."
    graphify extract .
fi
echo ""

# Step 2: Run agent with time measurement
echo "Step 2/3: Running agent (this may take several minutes)..."
echo "Output will be saved to: $LOG_FILE"
echo ""

{ time claude-code agent run "$AGENT_NAME" --story "$STORY_ID" 2>&1 ; } > "$LOG_FILE" 2>&1

echo "✓ Agent execution complete"
echo ""

# Step 3: Count tool usage
echo "Step 3/3: Analyzing tool usage..."
echo ""

# Count Grep calls
GREP_CALLS=$(grep -c '"tool": "Grep"' "$LOG_FILE" 2>/dev/null || echo "0")

# Count Read calls
READ_CALLS=$(grep -c '"tool": "Read"' "$LOG_FILE" 2>/dev/null || echo "0")

# Count graphify queries
GRAPHIFY_QUERIES=$(grep -c 'graphify query\|graphify path' "$LOG_FILE" 2>/dev/null || echo "0")

# Extract execution time
EXEC_TIME=$(grep -E '^real\s+[0-9]+m[0-9.]+s' "$LOG_FILE" 2>/dev/null | head -1)

# Display summary
echo "=========================================="
echo "GRAPHIFY SUMMARY (With Graph)"
echo "=========================================="
echo "Grep calls:        $GREP_CALLS"
echo "Read calls:        $READ_CALLS"
echo "Graphify queries:  $GRAPHIFY_QUERIES"
echo "Execution time:    $EXEC_TIME"
echo ""
echo "Log file: $LOG_FILE"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  Compare results: python3 scripts/compare-benchmarks.py"
