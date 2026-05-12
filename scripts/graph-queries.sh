#!/bin/bash
# Common graph queries for agents
#
# Usage:
#   source scripts/graph-queries.sh
#   graph_find_services
#   graph_find_tests
#   graph_find_dependencies "ClassName"
#   graph_query "Find all classes with @Stateless annotation"
#
# Functions are exported for use in subshells and agents.

# Find all service classes in the codebase
graph_find_services() {
    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        return 1
    fi

    graphify query "Find all service classes" 2>/dev/null | jq -r '.nodes[]?.file // empty' 2>/dev/null
}

# Find all test classes
graph_find_tests() {
    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        return 1
    fi

    graphify query "Find all test classes" 2>/dev/null | jq -r '.nodes[]?.file // empty' 2>/dev/null
}

# Find dependencies of a specific class
# Usage: graph_find_dependencies "ClassName"
graph_find_dependencies() {
    local class=$1

    if [ -z "$class" ]; then
        echo "Error: Class name required" >&2
        echo "Usage: graph_find_dependencies \"ClassName\"" >&2
        return 1
    fi

    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        return 1
    fi

    graphify path "$class" "*" 2>/dev/null | grep -E "^\s*--" 2>/dev/null
}

# Generic natural language query function
# Usage: graph_query "Find all classes with @Stateless annotation"
graph_query() {
    local query=$1

    if [ -z "$query" ]; then
        echo "Error: Query required" >&2
        echo "Usage: graph_query \"Find all classes with @Stateless annotation\"" >&2
        return 1
    fi

    if [ ! -f graphify-out/graph.json ]; then
        echo "Error: graphify-out/graph.json not found" >&2
        return 1
    fi

    graphify query "$query" 2>/dev/null
}

# Export functions for use in subshells and agents
export -f graph_find_services
export -f graph_find_tests
export -f graph_find_dependencies
export -f graph_query

# If script is executed (not sourced), show usage
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Graph Query Helpers"
    echo "==================="
    echo ""
    echo "This script should be sourced, not executed:"
    echo "  source scripts/graph-queries.sh"
    echo ""
    echo "Available functions:"
    echo "  graph_find_services          - Find all service classes"
    echo "  graph_find_tests             - Find all test classes"
    echo "  graph_find_dependencies      - Find dependencies of a class"
    echo "  graph_query                  - Generic natural language query"
    echo ""
    echo "Example usage:"
    echo "  source scripts/graph-queries.sh"
    echo "  graph_find_services"
    echo "  graph_find_dependencies \"OrderService\""
    echo "  graph_query \"Find all classes with @Stateless annotation\""
    echo "  graph_query \"Find files importing javax.*\""
fi
