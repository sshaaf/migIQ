#!/bin/bash
# Local installer for mig-agent-mesh
# Copies all necessary files to a target project's .claude directory for testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_DIR="$(pwd)"
TARGET_DIR="${1:-.}"

if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Target directory '$TARGET_DIR' does not exist"
  exit 1
fi

# Resolve to absolute paths
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
TARGET_CLAUDE_DIR="$TARGET_DIR/.claude"

# Safety check: Never run from source directory
if [ "$CURRENT_DIR" = "$SCRIPT_DIR" ]; then
  echo "Error: Cannot run installer from source directory"
  echo "Current directory: $CURRENT_DIR"
  echo "Source directory: $SCRIPT_DIR"
  echo ""
  echo "Please run from outside the source tree, or provide an absolute path:"
  echo "Example: $0 /tmp/test-project"
  exit 1
fi

# Safety checks: Never overwrite source directory
if [ "$TARGET_DIR" = "$SCRIPT_DIR" ]; then
  echo "Error: Target directory cannot be the same as source directory"
  echo "Usage: $0 <target-directory>"
  echo ""
  echo "Example: $0 /path/to/test/project"
  exit 1
fi

# Check if target is inside source (would create subdirectory in source)
case "$TARGET_DIR" in
  "$SCRIPT_DIR"/*)
    echo "Error: Target directory cannot be inside source directory"
    echo "Target: $TARGET_DIR"
    echo "Source: $SCRIPT_DIR"
    echo ""
    echo "This would modify the source tree. Please use an external directory."
    exit 1
    ;;
esac

# Check if source is inside target (would overwrite source when copying)
case "$SCRIPT_DIR" in
  "$TARGET_DIR"/*)
    echo "Error: Source directory is inside target directory"
    echo "Target: $TARGET_DIR"
    echo "Source: $SCRIPT_DIR"
    echo ""
    echo "This would create recursive copies. Please use an external directory."
    exit 1
    ;;
esac

echo "Installing mig-agent-mesh to: $TARGET_CLAUDE_DIR"
echo "Source: $SCRIPT_DIR"
echo ""

# Create .claude directory structure
mkdir -p "$TARGET_CLAUDE_DIR/agents"
mkdir -p "$TARGET_CLAUDE_DIR/scripts"

# Copy agents
echo "Copying agents..."
for agent in benchmark-builder-agent ci-integration-agent code-refactor-agent \
             documentation-manager-agent failure-analyzer-agent kpi-tracker-agent \
             project-tracker-agent quality-evaluator-agent story-orchestrator-agent \
             test-generator-agent; do
  if [ -d "$SCRIPT_DIR/agents/$agent" ]; then
    echo "  - $agent"
    cp -r "$SCRIPT_DIR/agents/$agent" "$TARGET_CLAUDE_DIR/agents/"
  fi
done

# Copy scripts
echo "Copying scripts..."
if [ -d "$SCRIPT_DIR/scripts" ]; then
  cp -r "$SCRIPT_DIR/scripts"/* "$TARGET_CLAUDE_DIR/scripts/" 2>/dev/null || true
fi

# Copy .env example files
echo "Copying configuration templates..."
if [ -f "$SCRIPT_DIR/.env.example" ]; then
  # Copy to target root for easy access
  cp "$SCRIPT_DIR/.env.example" "$TARGET_DIR/.env.example"
  # Also copy to .claude for reference
  cp "$SCRIPT_DIR/.env.example" "$TARGET_CLAUDE_DIR/"
fi
if [ -f "$SCRIPT_DIR/.env.test.example" ]; then
  cp "$SCRIPT_DIR/.env.test.example" "$TARGET_DIR/.env.test.example"
  cp "$SCRIPT_DIR/.env.test.example" "$TARGET_CLAUDE_DIR/"
fi

# Copy settings.json if it exists
if [ -f "$SCRIPT_DIR/.claude/settings.json" ]; then
  echo "Copying Claude settings..."
  cp "$SCRIPT_DIR/.claude/settings.json" "$TARGET_CLAUDE_DIR/"
fi

# Copy README and documentation
echo "Copying documentation..."
if [ -f "$SCRIPT_DIR/README.md" ]; then
  cp "$SCRIPT_DIR/README.md" "$TARGET_CLAUDE_DIR/MIG_AGENT_MESH_README.md"
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Files installed to: $TARGET_CLAUDE_DIR"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "IMPORTANT: Configuration Required"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Create your .env file:"
echo "   cd $TARGET_DIR"
echo "   cp .env.example .env"
echo ""
echo "2. Edit .env and configure:"
echo "   • TRACKER_TYPE - Choose: local, github"
echo "   • For GitHub tracker:"
echo "     - TRACKER_GITHUB_TOKEN (required)"
echo "     - TRACKER_GITHUB_ORGANIZATION (required)"
echo "     - TRACKER_GITHUB_PROJECT_NUMBER (optional, auto-creates if missing)"
echo "   • For local tracker:"
echo "     - TRACKER_LOCAL_TASKS_PATH (default: ./tasks.md)"
echo ""
echo "3. The .env file location:"
echo "   → $TARGET_DIR/.env (project root)"
echo "   ⚠️  Never commit .env to git (contains secrets)"
echo ""
echo "4. Test the installation:"
echo "   cd $TARGET_DIR"
echo "   claude-code"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
