#!/bin/bash
# Migration-specific graph queries
#
# Usage:
#   source scripts/migration-queries.sh
#   find_ejb_classes
#   find_javax_imports
#   show_migration_status
#
# Requires:
#   - graphify-out/graph.json (run /graphify . or graphify extract .)

# Find classes with EJB annotations (@Stateless, @MessageDriven, @Stateful)
find_ejb_classes() {
    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        echo "Run: /graphify . or graphify extract ." >&2
        return 1
    fi

    # Query for all three EJB annotation types
    {
        graphify query "Find classes with @Stateless annotation" 2>/dev/null
        graphify query "Find classes with @MessageDriven annotation" 2>/dev/null
        graphify query "Find classes with @Stateful annotation" 2>/dev/null
    } | sort -u
}

# Find all files importing javax.* packages
find_javax_imports() {
    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        echo "Run: /graphify . or graphify extract ." >&2
        return 1
    fi

    graphify query "Find files importing javax.*" 2>/dev/null | sort -u
}

# Find files using a specific annotation
# Usage: find_files_using_annotation "Stateless"
find_files_using_annotation() {
    local annotation=$1

    if [ -z "$annotation" ]; then
        echo "Error: Annotation name required" >&2
        echo "Usage: find_files_using_annotation \"Stateless\"" >&2
        return 1
    fi

    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        echo "Run: /graphify . or graphify extract ." >&2
        return 1
    fi

    graphify query "Find classes with @$annotation annotation" 2>/dev/null
}

# Show migration status summary
show_migration_status() {
    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        echo "Run: /graphify . or graphify extract ." >&2
        return 1
    fi

    echo "=== Migration Analysis ==="
    echo ""

    # EJB Annotations
    local ejb_classes=$(find_ejb_classes 2>/dev/null)
    local ejb_count=$(echo "$ejb_classes" | grep -c . 2>/dev/null || echo "0")
    echo "EJB Classes: $ejb_count"
    if [ "$ejb_count" -gt 0 ]; then
        echo "  Found:"
        echo "$ejb_classes" | sed 's/^/    /'
    fi
    echo ""

    # javax.* imports
    local javax_files=$(find_javax_imports 2>/dev/null)
    local javax_count=$(echo "$javax_files" | grep -c . 2>/dev/null || echo "0")
    echo "Files with javax.* imports: $javax_count"
    if [ "$javax_count" -gt 0 ]; then
        echo "  Sample files (first 5):"
        echo "$javax_files" | head -5 | sed 's/^/    /'
    fi
    echo ""

    # Total files needing migration
    echo "Summary:"
    echo "  Files with javax imports: $javax_count"
    echo "  Files with EJB annotations: $ejb_count"
    echo "  (Note: Some files may have both)"
}

# Export functions for shell use
export -f find_ejb_classes
export -f find_javax_imports
export -f find_files_using_annotation
export -f show_migration_status

# If script is executed (not sourced), show usage
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Migration Query Helpers"
    echo "======================="
    echo ""
    echo "This script should be sourced, not executed:"
    echo "  source scripts/migration-queries.sh"
    echo ""
    echo "Available functions:"
    echo "  find_ejb_classes             - Find classes with EJB annotations"
    echo "  find_javax_imports           - Find javax.* imports"
    echo "  find_files_using_annotation  - Find files using specific annotation"
    echo "  show_migration_status        - Display migration status summary"
    echo ""
    echo "Example usage:"
    echo "  source scripts/migration-queries.sh"
    echo "  find_ejb_classes"
    echo "  find_javax_imports"
    echo "  show_migration_status"
fi
