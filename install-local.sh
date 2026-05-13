#!/bin/bash
# Local installer for mig-agent-mesh
# Installs migration agents, skills, and scripts to a target project's .claude directory
#
# This installer copies the complete mig-agent-mesh package including:
# - 10 specialized agents for migration workflow orchestration
# - 24 skills for code analysis, refactoring, and testing
# - Helper scripts for Graphify integration and benchmarking
#
# Usage: ./install-local.sh <target-project-directory>

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
TARGET_AGENTS_DIR="$TARGET_CLAUDE_DIR/agents"
TARGET_SCRIPTS_DIR="$TARGET_CLAUDE_DIR/scripts"
TARGET_SKILLS_DIR="$TARGET_CLAUDE_DIR/skills"

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
echo "Creating .claude directory structure..."

echo "Copying agents"
mkdir -p "$TARGET_AGENTS_DIR"
cp -r "$SCRIPT_DIR/agents"/* "$TARGET_AGENTS_DIR"

echo "Copying scripts"
mkdir -p "$TARGET_SCRIPTS_DIR"
cp -r "$SCRIPT_DIR/scripts"/* "$TARGET_SCRIPTS_DIR"
echo "Copying skills"
mkdir -p "$TARGET_SKILLS_DIR"
cp -r "$SCRIPT_DIR/skills"/* "$TARGET_SKILLS_DIR"


# Copy .env example files
echo ""
echo "Copying configuration templates..."
if [ -f "$SCRIPT_DIR/.env.example" ]; then
  cp "$SCRIPT_DIR/.env.example" "$TARGET_DIR/.env.example"
  cp "$SCRIPT_DIR/.env.example" "$TARGET_CLAUDE_DIR/"
  echo "  ✓ .env.example (tracker configuration)"
fi
if [ -f "$SCRIPT_DIR/.env.test" ]; then
  cp "$SCRIPT_DIR/.env.test" "$TARGET_DIR/.env.test.example"
  echo "  ✓ .env.test.example (test configuration)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚙️  REQUIRED: Configuration & Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Install Graphify CLI tool (REQUIRED for migration to work):"
echo "   # Option A: Using uv (recommended)"
echo "   uv tool install graphifyy"
echo ""
echo "   # Option B: Using pip"
echo "   pip install graphifyy"
echo ""
echo "   # Verify installation:"
echo "   graphify --version"
echo ""
echo "   Note: The /mig-graphify skill will check if the CLI is installed"
echo "   and provide installation instructions if needed."
echo ""
echo "2. (Optional) Create .env in your project for configuration:"
echo "   The migration automatically loads config from your project's .env file."
echo ""
echo "   # Copy example to your project directory"
echo "   cp .env.example /path/to/your-project/.env"
echo ""
echo "   # Edit with your settings"
echo "   vim /path/to/your-project/.env"
echo ""
echo "   Example configuration:"
echo "     TRACKER_TYPE=github"
echo "     TRACKER_GITHUB_TOKEN=ghp_xxxxx"
echo "     TRACKER_GITHUB_ORGANIZATION=my-org"
echo ""
echo "   Then run: /migration --project-path /path/to/your-project --migration-type framework"
echo ""
echo "   ⚠️  IMPORTANT: Never commit .env to git (contains secrets)"
echo ""
echo "4. Test the installation:"
echo "   cd $TARGET_DIR"
echo "   /migration --help"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Quick Start"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run a migration:"
echo "  /migration --project-path ./your-app --migration-type framework"
echo ""
echo "The migration workflow will:"
echo "  1. Build knowledge graph with Graphify (~30s)"
echo "  2. Analyze codebase for dependencies and patterns"
echo "  3. Generate migration plan with prioritized tasks"
echo "  4. Execute migration with 50-70% faster performance"
echo ""
echo "For more details, see:"
echo "  $TARGET_CLAUDE_DIR/MIG_AGENT_MESH_README.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
