#!/bin/bash
# Benchmark agent without graphify
#
# This script measures agent performance WITHOUT graphify integration.
# It temporarily disables the graph, runs the agent, and measures tool usage.
#
# Usage:
#   ./scripts/benchmark-without-graph.sh <agent-name> <story-id>
#
# Example:
#   ./scripts/benchmark-without-graph.sh test-generator-agent US-TEST
#
# Output:
#   - benchmark-without-graph.log - Full agent output
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
LOG_FILE="benchmark-without-graph.log"

echo "=========================================="
echo "Baseline Benchmark (Without Graphify)"
echo "=========================================="
echo "Agent: $AGENT_NAME"
echo "Story: $STORY_ID"
echo ""

# Step 1: Backup graphify-out directory
echo "Step 1/4: Backing up graphify-out..."
if [ -d graphify-out ]; then
    mv graphify-out graphify-out.bak
    echo "✓ Backed up to graphify-out.bak"
else
    echo "  (no graphify-out directory found)"
fi
echo ""

# Step 2: Run agent with time measurement
echo "Step 2/4: Running agent (this may take several minutes)..."
echo "Output will be saved to: $LOG_FILE"
echo ""

{ time claude-code agent run "$AGENT_NAME" --story "$STORY_ID" 2>&1 ; } > "$LOG_FILE" 2>&1

echo "✓ Agent execution complete"
echo ""

# Step 3: Count tool usage
echo "Step 3/4: Analyzing tool usage..."
echo ""

# Count Grep calls
GREP_CALLS=$(grep -c '"tool": "Grep"' "$LOG_FILE" 2>/dev/null || echo "0")

# Count Read calls
READ_CALLS=$(grep -c '"tool": "Read"' "$LOG_FILE" 2>/dev/null || echo "0")

# Count files read (unique file paths)
FILES_READ=$(grep '"file_path"' "$LOG_FILE" 2>/dev/null | wc -l | tr -d ' ')

# Extract execution time
EXEC_TIME=$(grep -E '^real\s+[0-9]+m[0-9.]+s' "$LOG_FILE" 2>/dev/null | head -1)

# Step 4: Restore graphify-out
echo "Step 4/4: Restoring graphify-out..."
if [ -d graphify-out.bak ]; then
    mv graphify-out.bak graphify-out
    echo "✓ Restored graphify-out"
fi
echo ""

# Display summary
echo "=========================================="
echo "BASELINE SUMMARY (Without Graphify)"
echo "=========================================="
echo "Grep calls:     $GREP_CALLS"
echo "Read calls:     $READ_CALLS"
echo "Files read:     $FILES_READ"
echo "Execution time: $EXEC_TIME"
echo ""
echo "Log file: $LOG_FILE"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Run: ./scripts/benchmark-with-graph.sh $AGENT_NAME $STORY_ID"
echo "  2. Compare: python3 scripts/compare-benchmarks.py"
