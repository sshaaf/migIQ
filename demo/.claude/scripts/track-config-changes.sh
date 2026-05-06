#!/bin/bash
# Track configuration file changes in git
# Provides helpers for committing configuration updates

set -e

CONFIG_FILES=("rule.md" "tasks.md" "CLAUDE.md")
CHANGE_TYPE="${1:-update}"
DESCRIPTION="${2:-Configuration update}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
Usage: $0 [CHANGE_TYPE] [DESCRIPTION]

Track and commit configuration file changes to git.

Arguments:
    CHANGE_TYPE    Type of change: update, rule-add, task-add, threshold-update (default: update)
    DESCRIPTION    Brief description of the change (default: "Configuration update")

Examples:
    $0 rule-add "Add Spring Boot 3.x migration rule"
    $0 task-add "Add database migration user story"
    $0 threshold-update "Increase code coverage threshold to 85%"
    $0 update "General configuration refinement"

Configuration Files Tracked:
    - rule.md      Migration rules and patterns
    - tasks.md     Task backlog and user stories
    - CLAUDE.md    Project instructions for Claude Code

EOF
    exit 1
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

# Check which config files have changes
echo -e "${GREEN}🔍 Checking for configuration changes...${NC}"
echo

CHANGED_FILES=()
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        if git diff --quiet "$file" 2>/dev/null; then
            echo -e "  ${YELLOW}○${NC} $file - no changes"
        else
            echo -e "  ${GREEN}●${NC} $file - modified"
            CHANGED_FILES+=("$file")
        fi
    else
        echo -e "  ${YELLOW}○${NC} $file - not found"
    fi
done

if [ ${#CHANGED_FILES[@]} -eq 0 ]; then
    echo
    echo -e "${YELLOW}No configuration changes to commit${NC}"
    exit 0
fi

# Show diff summary
echo
echo -e "${GREEN}📝 Changes summary:${NC}"
echo

for file in "${CHANGED_FILES[@]}"; do
    echo "=== $file ==="
    git diff --stat "$file" || true
    echo
done

# Ask for confirmation
echo -e "${YELLOW}Commit these changes?${NC} [y/N]"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Aborted${NC}"
    exit 0
fi

# Construct commit message based on change type
case "$CHANGE_TYPE" in
    rule-add)
        COMMIT_MSG="Add migration rule: $DESCRIPTION"
        ;;
    rule-update)
        COMMIT_MSG="Update migration rule: $DESCRIPTION"
        ;;
    task-add)
        COMMIT_MSG="Add task: $DESCRIPTION"
        ;;
    task-update)
        COMMIT_MSG="Update task: $DESCRIPTION"
        ;;
    threshold-update)
        COMMIT_MSG="Update quality threshold: $DESCRIPTION"
        ;;
    update)
        COMMIT_MSG="Update configuration: $DESCRIPTION"
        ;;
    *)
        COMMIT_MSG="$CHANGE_TYPE: $DESCRIPTION"
        ;;
esac

# Stage and commit files
echo
echo -e "${GREEN}📦 Committing changes...${NC}"

for file in "${CHANGED_FILES[@]}"; do
    git add "$file"
    echo -e "  ✓ Staged $file"
done

# Create commit with structured message
git commit -m "$COMMIT_MSG

Files updated: ${CHANGED_FILES[*]}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

echo
echo -e "${GREEN}✅ Configuration changes committed${NC}"
echo
echo "Commit message:"
echo "  $COMMIT_MSG"
echo
echo "To push to remote:"
echo "  git push"
