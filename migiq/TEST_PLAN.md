# MigIQ Skill Test Plan

## Overview

This document outlines the testing strategy for the migiq orchestration skill, including test cases, validation procedures, and success criteria.

## Test Structure

```
migiq/
├── SKILL.md              # The skill definition
├── evals/
│   └── evals.json        # Test case definitions
└── TEST_PLAN.md          # This file
```

## Test Cases

### Test Case 1: Spring Boot to Quarkus (Primary)
**ID**: 1  
**Name**: spring-boot-to-quarkus  
**Complexity**: Medium  
**Expected Duration**: 30-45 minutes  

**Prompt**:
```
Migrate this Spring Boot application to Quarkus. The app is a simple REST API with 
database access using Spring Data JPA. I need it running on OpenShift with all the 
containerization and deployment configs ready.
```

**Test Codebase**: Available at `mig-graphify-workspace/iteration-1/eval-1-spring-to-quarkus/`

**Expected Workflow**:
1. **Phase 1 (Analysis)**: Graphify analyzes Spring Boot code, identifies controllers, repositories, entities
2. **Phase 2 (Requirements)**: Captures target (Quarkus), platform (OpenShift), phased approach
3. **Phase 3 (Planning)**: Creates migration plan to convert Spring annotations to Quarkus, update dependencies
4. **Phase 4 (Execution)**: Implements code changes, generates tests, creates container images, produces OpenShift manifests
5. **Phase 5 (Reporting)**: Synthesizes complete migration report

**Success Criteria**:
- ✅ All 5 phases complete without critical errors
- ✅ Graph analysis identifies Spring components correctly
- ✅ Migration prompt specifies Quarkus and OpenShift
- ✅ Plan includes specific Spring → Quarkus conversion tasks
- ✅ Execution produces modified code files
- ✅ Containerization artifacts (Dockerfile) created
- ✅ OpenShift manifests (YAML) generated
- ✅ Final report synthesizes all phase results

---

### Test Case 2: Node.js Express Modernization (Secondary)
**ID**: 2  
**Name**: nodejs-express-modernization  
**Complexity**: Medium  
**Expected Duration**: 25-40 minutes  

**Prompt**:
```
I need to modernize this old Node.js Express app and deploy it to OpenShift. 
Not sure what the best approach is, but we want to use current best practices 
and get it containerized.
```

**Test Codebase**: Would need to be created or sourced

**Expected Workflow**:
1. **Phase 1**: Analyze Node.js/Express codebase structure
2. **Phase 2**: Interactive requirements gathering (user should specify Node.js version, patterns to adopt)
3. **Phase 3**: Plan modernization (update dependencies, adopt async/await, add error handling, etc.)
4. **Phase 4**: Execute modernization tasks
5. **Phase 5**: Final report

**Success Criteria**:
- ✅ Handles vague requirements gracefully (prompts for clarification)
- ✅ Migration prompt captures "modernization" intent vs. "platform switch"
- ✅ Plan addresses both code quality and deployment needs
- ✅ All phases complete successfully

---

### Test Case 3: Java EE to Spring Boot (Tertiary)
**ID**: 3  
**Name**: java-ee-to-spring-boot  
**Complexity**: High  
**Expected Duration**: 45-60 minutes  

**Prompt**:
```
Migrate this Java EE application to Spring Boot. It's a legacy monolith with 
EJBs and needs to run on OpenShift eventually.
```

**Test Codebase**: Would need to be created or sourced

**Expected Workflow**:
1. **Phase 1**: Analyze Java EE app, identify EJBs, entity beans, deployment descriptors
2. **Phase 2**: Capture Spring Boot version, decomposition strategy
3. **Phase 3**: Create complex plan for EJB → Spring component conversion
4. **Phase 4**: Execute migration (complex due to EJB specifics)
5. **Phase 5**: Report

**Success Criteria**:
- ✅ Graph analysis correctly identifies EJBs
- ✅ Plan addresses EJB transaction management → Spring @Transactional
- ✅ Plan addresses stateful EJBs appropriately
- ✅ All phases complete (may have some execution failures on complex EJB conversions)

---

## How to Run Tests

### Prerequisites

1. Ensure all mig-* skills are installed and functional:
   ```bash
   ls -l /Users/sshaaf/git/konveyor/migIQ/mig-*/SKILL.md
   ```

2. Verify graphify CLI is available:
   ```bash
   which graphify
   graphify --version
   ```

3. Have permissions configured for:
   - Running graphify commands
   - Reading/writing files in test workspace
   - Spawning sub-agents (for mig-execute)

### Running Test Case 1 (Recommended First Test)

1. **Set up test environment**:
   ```bash
   cd /Users/sshaaf/git/konveyor/migIQ
   mkdir -p migiq-test-run
   cd migiq-test-run
   
   # Copy Spring Boot test app
   cp -r ../mig-graphify-workspace/iteration-1/eval-1-spring-to-quarkus/src .
   cp ../mig-graphify-workspace/iteration-1/eval-1-spring-to-quarkus/pom.xml .
   
   # Verify clean state
   ls -la
   # Should see: src/, pom.xml
   ```

2. **Invoke migiq skill**:
   ```
   In Claude Code, type:
   /migiq
   
   Then provide the prompt:
   "Migrate this Spring Boot application to Quarkus. The app is a simple REST API 
   with database access using Spring Data JPA. I need it running on OpenShift with 
   all the containerization and deployment configs ready."
   ```

3. **Monitor progress**:
   The skill will run all 5 phases automatically, pausing only if errors occur.
   
   Expected checkpoints:
   - ✅ "Phase 1/4: Analyzing codebase..." → graphify runs
   - ✅ "Phase 2/4: Gathering requirements..." → may ask clarifying questions
   - ✅ "Phase 3/4: Creating migration plan..." → generates plan files
   - ✅ "Phase 4/4: Executing migration..." → implements changes
   - ✅ "Generating final migration report..." → creates comprehensive report

4. **Validate outputs**:
   ```bash
   # Check all expected outputs exist
   ls -la graphify-out/
   # Should see: graph.json, GRAPH_REPORT.md, graph.html
   
   ls -la mig-prompt-workspace/
   # Should see: migration-prompt.md
   
   ls -la mig-plan-workspace/
   # Should see: spec.md, design.md, tasks.md, UserStory.md
   
   ls -la mig-execute-workspace/
   # Should see: EXECUTION_REPORT.md, execution-log.md, outputs/
   
   ls -la migiq-workspace/
   # Should see: MIGRATION_REPORT.md, orchestration-log.md
   ```

5. **Manual validation checklist**:
   
   **Phase 1 - Codebase Analysis**:
   - [ ] `graphify-out/graph.json` exists and is valid JSON
   - [ ] `GRAPH_REPORT.md` mentions Spring Boot components (controllers, repositories)
   - [ ] Graph statistics (nodes, edges, communities) are reasonable
   
   **Phase 2 - Requirements**:
   - [ ] `migration-prompt.md` specifies source as "Spring Boot"
   - [ ] Target is "Quarkus" with version
   - [ ] Deployment platform is "Red Hat OpenShift"
   - [ ] Migration approach is specified (phased/big bang)
   - [ ] Deliverables include containerization, deployment, testing, plan
   
   **Phase 3 - Planning**:
   - [ ] `spec.md` describes current Spring Boot app accurately
   - [ ] `design.md` outlines Quarkus target architecture
   - [ ] `tasks.md` includes specific Spring → Quarkus conversion tasks
   - [ ] `UserStory.md` groups work into stories with acceptance criteria
   - [ ] Task breakdown includes integration hooks (test-gen, containerize, deploy)
   
   **Phase 4 - Execution**:
   - [ ] `EXECUTION_REPORT.md` shows task completion statistics
   - [ ] Some tasks completed (may have failures on complex conversions)
   - [ ] `execution-log.md` has detailed timeline entries
   - [ ] `outputs/` directory contains generated artifacts
   - [ ] Code files were modified (check git diff or file timestamps)
   
   **Phase 5 - Reporting**:
   - [ ] `MIGRATION_REPORT.md` exists and is comprehensive
   - [ ] Executive summary is clear and accurate
   - [ ] All 5 phases are documented
   - [ ] Technical details section describes changes
   - [ ] Statistics are present and reasonable
   - [ ] Next steps are actionable
   
   **Integration Artifacts**:
   - [ ] Dockerfile or Containerfile created
   - [ ] OpenShift YAML manifests created (Deployment, Service, etc.)
   - [ ] Test files generated or referenced
   
   **Orchestration**:
   - [ ] `orchestration-log.md` tracks all phase transitions
   - [ ] Timestamps are present for each phase
   - [ ] No critical errors in orchestration log

6. **Grade the test**:
   
   Based on the checklist above, determine:
   
   - **PASS**: All 5 phases complete, all expected outputs present, migration report is comprehensive
   - **PARTIAL**: Some phases complete, some outputs missing, but workflow is functional
   - **FAIL**: Critical errors prevent completion, major outputs missing, workflow breaks

---

## Validation Script

You can use this script to automatically check for expected outputs:

```bash
#!/bin/bash
# migiq-test-validator.sh

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
    if grep -q "Quarkus" "mig-prompt-workspace/migration-prompt.md"; then
        echo "  ✅ Target mentions Quarkus"
    else
        echo "  ⚠️  Target doesn't mention Quarkus"
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
for file in spec.md design.md tasks.md UserStory.md; do
    if [ -f "mig-plan-workspace/$file" ]; then
        echo "  ✅ $file exists"
    else
        echo "  ❌ $file missing"
        ((ERRORS++))
    fi
done
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
if ls mig-execute-workspace/outputs/containers/* 2>/dev/null | grep -q "Dockerfile\|Containerfile"; then
    echo "  ✅ Containerization artifacts found"
else
    echo "  ⚠️  No Dockerfile/Containerfile found"
    ((WARNINGS++))
fi

if ls mig-execute-workspace/outputs/deployments/* 2>/dev/null | grep -q "\.yaml\|\.yml"; then
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
```

Save this as `migiq/test-validator.sh` and run after completing a test:

```bash
cd migiq-test-run
bash ../migiq/test-validator.sh
```

---

## Test Metrics

For each test run, capture:

1. **Duration Metrics**:
   - Total time (start to finish)
   - Time per phase
   - Slowest operations

2. **Completion Metrics**:
   - Phases completed / total phases
   - Tasks completed / total tasks (from execution report)
   - Acceptance criteria met / total criteria

3. **Quality Metrics**:
   - Errors encountered
   - Warnings logged
   - Manual validation checklist score

4. **Artifact Metrics**:
   - Files created
   - Lines of code changed
   - Test coverage (if measurable)

---

## Known Limitations and Edge Cases

### Permission Prompts
- **Issue**: The orchestration may pause for permission prompts (especially for graphify, file writes, sub-agents)
- **Impact**: Interrupts automatic flow
- **Mitigation**: Pre-configure permissions or run interactively

### Long Execution Times
- **Issue**: Full end-to-end tests take 30-60 minutes
- **Impact**: Slow feedback loop
- **Mitigation**: Test individual phases first, then full orchestration

### Sub-agent Failures
- **Issue**: mig-execute spawns sub-agents that may timeout or fail
- **Impact**: Partial execution, some tasks incomplete
- **Mitigation**: This is expected behavior; the skill should handle failures gracefully and report them

### Complex Migrations
- **Issue**: Some migrations (Java EE → Spring Boot) are inherently complex
- **Impact**: Execution phase may have high failure rate on specific tasks
- **Mitigation**: Success = graceful failure handling + good reporting, not 100% task success

---

## Next Steps After Testing

1. **If all tests pass**:
   - Document the skill as production-ready
   - Create examples and demos
   - Add to official skill catalog

2. **If tests reveal issues**:
   - Iterate on the skill definition
   - Fix workflow bugs
   - Re-test

3. **Ongoing**:
   - Collect real-world usage data
   - Refine based on user feedback
   - Add more test cases for edge cases

---

## Quick Start Summary

**To quickly validate the migiq skill works**:

```bash
# 1. Set up test
cd /Users/sshaaf/git/konveyor/migIQ
mkdir -p migiq-test-run && cd migiq-test-run
cp -r ../mig-graphify-workspace/iteration-1/eval-1-spring-to-quarkus/{src,pom.xml} .

# 2. Run migiq skill in Claude Code
# Type: /migiq
# Prompt: "Migrate this Spring Boot app to Quarkus for OpenShift"

# 3. Validate outputs
bash ../migiq/test-validator.sh

# 4. Review final report
cat migiq-workspace/MIGRATION_REPORT.md
```

Expected result: All 5 phases complete, comprehensive migration report generated, test passes.
