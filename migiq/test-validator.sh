#!/bin/bash
# migiq-test-validator.sh
# Validates that a migiq orchestration test completed successfully

echo "=== MigIQ Test Validation ==="
echo ""

ERRORS=0
WARNINGS=0

# Phase 1 outputs
echo "Phase 1: Codebase Analysis"
if [ -f "graphify-out/graph.json" ]; then
    echo "  ✅ graph.json exists"
else
    echo "  ❌ graph.json missing"
    ((ERRORS++))
fi

if [ -f "graphify-out/GRAPH_REPORT.md" ]; then
    echo "  ✅ GRAPH_REPORT.md exists"
else
    echo "  ❌ GRAPH_REPORT.md missing"
    ((ERRORS++))
fi
echo ""

# Phase 2 outputs
echo "Phase 2: Requirements Gathering"
if [ -f "mig-prompt-workspace/migration-prompt.md" ]; then
    echo "  ✅ migration-prompt.md exists"
    if grep -q "Quarkus\|Spring Boot\|Node.js" "mig-prompt-workspace/migration-prompt.md"; then
        echo "  ✅ Target technology mentioned"
    else
        echo "  ⚠️  No clear target technology"
        ((WARNINGS++))
    fi
    if grep -q "OpenShift" "mig-prompt-workspace/migration-prompt.md"; then
        echo "  ✅ Platform mentions OpenShift"
    else
        echo "  ⚠️  Platform doesn't mention OpenShift"
        ((WARNINGS++))
    fi
else
    echo "  ❌ migration-prompt.md missing"
    ((ERRORS++))
fi
echo ""

# Phase 3 outputs
echo "Phase 3: Migration Planning"
for file in tasks.md UserStory.md; do
    if [ -f "mig-plan-workspace/$file" ]; then
        echo "  ✅ $file exists"
    else
        echo "  ❌ $file missing"
        ((ERRORS++))
    fi
done
echo "  ℹ️  Note: spec.md and design.md are replaced by migration-prompt.md for token optimization"
echo ""

# Phase 4 outputs
echo "Phase 4: Migration Execution"
if [ -f "mig-execute-workspace/EXECUTION_REPORT.md" ]; then
    echo "  ✅ EXECUTION_REPORT.md exists"
else
    echo "  ❌ EXECUTION_REPORT.md missing"
    ((ERRORS++))
fi

if [ -f "mig-execute-workspace/execution-log.md" ]; then
    echo "  ✅ execution-log.md exists"
else
    echo "  ❌ execution-log.md missing"
    ((ERRORS++))
fi
echo ""

# Phase 5 outputs
echo "Phase 5: Final Reporting"
if [ -f "migiq-workspace/MIGRATION_REPORT.md" ]; then
    echo "  ✅ MIGRATION_REPORT.md exists"
    # Check that it mentions all phases
    if grep -q "Phase 1" "migiq-workspace/MIGRATION_REPORT.md" && \
       grep -q "Phase 2" "migiq-workspace/MIGRATION_REPORT.md" && \
       grep -q "Phase 3" "migiq-workspace/MIGRATION_REPORT.md" && \
       grep -q "Phase 4" "migiq-workspace/MIGRATION_REPORT.md" && \
       grep -q "Phase 5" "migiq-workspace/MIGRATION_REPORT.md"; then
        echo "  ✅ Report documents all 5 phases"
    else
        echo "  ⚠️  Report may be missing some phases"
        ((WARNINGS++))
    fi
else
    echo "  ❌ MIGRATION_REPORT.md missing"
    ((ERRORS++))
fi

if [ -f "migiq-workspace/orchestration-log.md" ]; then
    echo "  ✅ orchestration-log.md exists"
else
    echo "  ⚠️  orchestration-log.md missing"
    ((WARNINGS++))
fi
echo ""

# Integration artifacts
echo "Integration Artifacts"
if find mig-execute-workspace/outputs -name "Dockerfile" -o -name "Containerfile" 2>/dev/null | grep -q .; then
    echo "  ✅ Containerization artifacts found"
else
    echo "  ⚠️  No Dockerfile/Containerfile found"
    ((WARNINGS++))
fi

if find mig-execute-workspace/outputs -name "*.yaml" -o -name "*.yml" 2>/dev/null | grep -q .; then
    echo "  ✅ OpenShift manifests found"
else
    echo "  ⚠️  No YAML manifests found"
    ((WARNINGS++))
fi
echo ""

# Summary
echo "=== Validation Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ TEST PASSED"
    exit 0
elif [ $ERRORS -lt 3 ]; then
    echo "⚠️  TEST PARTIAL - Some outputs missing"
    exit 1
else
    echo "❌ TEST FAILED - Critical outputs missing"
    exit 2
fi
