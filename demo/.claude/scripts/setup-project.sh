#!/bin/bash
# Setup script for Code Migration System
# Initializes project configuration files and validates structure

set -e

PROJECT_ROOT="${1:-.}"
cd "$PROJECT_ROOT"

echo "🚀 Setting up Code Migration System..."
echo

# Function to check if file exists
file_exists() {
    [ -f "$1" ]
}

# Function to check if directory exists
dir_exists() {
    [ -d "$1" ]
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Verify directory structure
echo
echo "📁 Verifying directory structure..."

REQUIRED_DIRS=(
    ".claude/agents"
    ".claude/skills"
    "templates"
    "specs"
    "rules"
    "benchmarks"
    "docs/adr"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if dir_exists "$dir"; then
        echo "  ✓ $dir"
    else
        echo "  ❌ $dir not found"
        echo "Creating $dir..."
        mkdir -p "$dir"
    fi
done

# Initialize configuration files
echo
echo "⚙️  Initializing configuration files..."

# Copy templates if they don't exist
if ! file_exists "rule.md"; then
    if file_exists "templates/rule.md"; then
        echo "  Copying rule.md from template..."
        cp templates/rule.md rule.md
        echo "  ✓ rule.md created"
    else
        echo "  ⚠️  templates/rule.md not found"
    fi
else
    echo "  ✓ rule.md already exists"
fi

if ! file_exists "tasks.md"; then
    if file_exists "templates/tasks.md"; then
        echo "  Copying tasks.md from template..."
        cp templates/tasks.md tasks.md
        echo "  ✓ tasks.md created"
    else
        echo "  ⚠️  templates/tasks.md not found"
    fi
else
    echo "  ✓ tasks.md already exists"
fi

if ! file_exists "CLAUDE.md"; then
    if file_exists "templates/CLAUDE.md"; then
        echo "  Copying CLAUDE.md from template..."
        cp templates/CLAUDE.md CLAUDE.md
        echo "  ✓ CLAUDE.md created"
    else
        echo "  ⚠️  templates/CLAUDE.md not found"
    fi
else
    echo "  ✓ CLAUDE.md already exists"
fi

# Set up environment file
echo
echo "🔐 Setting up environment configuration..."

if ! file_exists ".env"; then
    if file_exists ".env.example"; then
        echo "  Copying .env from .env.example..."
        cp .env.example .env
        echo "  ✓ .env created"
        echo
        echo "  ⚠️  IMPORTANT: Edit .env and configure your API credentials!"
        echo "     Required: CI_PLATFORM_TOKEN, KANBAN_API_TOKEN, OPENCODE_AGENT_API_KEY"
    else
        echo "  ⚠️  .env.example not found"
    fi
else
    echo "  ✓ .env already exists"
fi

# Create .gitignore if it doesn't exist
if ! file_exists ".gitignore"; then
    echo
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Environment and secrets
.env
.env.local

# Logs and state
logs/
.claude/state/

# Build artifacts
target/
build/
dist/
*.jar
*.war
*.ear

# Test coverage
coverage/
.coverage
htmlcov/

# Benchmark results
benchmarks/results/

# IDE
.idea/
.vscode/
*.iml

# Dependencies
node_modules/
.venv/
venv/

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
*.swp
*~
EOF
    echo "  ✓ .gitignore created"
fi

# Validate configuration
echo
echo "✅ Running configuration validation..."
echo

if [ -f ".claude/scripts/validate-config.py" ]; then
    python3 .claude/scripts/validate-config.py --project-root .
    VALIDATION_EXIT=$?
else
    echo "⚠️  Validation script not found, skipping validation"
    VALIDATION_EXIT=0
fi

# Summary
echo
echo "=" "================================================================"
echo "📊 Setup Summary"
echo "================================================================="
echo
echo "Next steps:"
echo
echo "1. ✏️  Edit configuration files for your project:"
echo "   - rule.md (migration rules and patterns)"
echo "   - tasks.md (user stories and tasks)"
echo "   - CLAUDE.md (project-specific instructions)"
echo
echo "2. 🔐 Configure environment variables in .env:"
echo "   - CI platform credentials (GitLab or GitHub)"
echo "   - Kanban board credentials (Jira, Linear, or GitHub Projects)"
echo "   - OpenCode Agent API endpoint and key"
echo
echo "3. 🧪 Verify setup:"
echo "   source .env"
echo "   python3 .claude/scripts/validate-config.py"
echo
echo "4. 🚀 Start implementing:"
echo "   - Create skills in .claude/skills/"
echo "   - Create agents in .claude/agents/"
echo "   - Define migration rules in rule.md"
echo "   - Add user stories to tasks.md"
echo
echo "================================================================="

exit $VALIDATION_EXIT
