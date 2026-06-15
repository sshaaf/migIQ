---
name: migiq
description: Complete end-to-end application migration orchestrator. Use this skill whenever the user wants to migrate, modernize, or port their entire application from one technology stack to another. This skill automatically orchestrates the full migration workflow from analysis to execution. Trigger when users say "migrate this app", "migrate to [technology]", "modernize this application", "port to [framework]", or simply "migrate". This is the primary entry point for any complete migration - it runs mig-graphify for analysis, mig-prompt-builder for requirements, mig-plan for planning, mig-execute for implementation, and generates a comprehensive final report.
---

# MigIQ: Complete Migration Orchestrator

This skill provides end-to-end orchestration for application migration projects. It automatically chains together all migration skills in the correct sequence, handles errors gracefully, and produces a comprehensive migration report.

## What This Skill Does

When invoked, this skill orchestrates the complete migration workflow:

1. **Analysis** (mig-graphify) - Analyzes the codebase and builds a knowledge graph
2. **Requirements** (mig-prompt-builder) - Gathers migration requirements and generates a standardized prompt
3. **Planning** (mig-plan) - Creates a comprehensive migration plan with tasks and user stories
4. **Execution** (mig-execute) - Implements the migration plan with automated task execution
5. **Reporting** - Generates a final migration report summarizing the entire journey

All steps run automatically in sequence. The orchestrator only pauses if a step fails, presenting options for recovery.

## When to Use This Skill

Use this skill when the user wants to:
- Migrate an entire application from one stack to another
- Modernize a legacy application
- Port an application to a new framework or platform
- Execute a complete technology migration

**Example triggers:**
- "Migrate this app to Quarkus"
- "Modernize this Java EE application"
- "Port this application to Spring Boot"
- "Migrate to microservices on OpenShift"
- "Help me migrate from Rails to Node.js"

**When NOT to use this skill:**
- User only wants analysis (use mig-graphify directly)
- User only wants to create a plan (use mig-plan directly)
- User only wants to execute an existing plan (use mig-execute directly)

## Execution Modes: Interactive vs. Autonomous

This skill supports two execution modes:

### Interactive Mode (Default)
Run the migration directly in the current conversation:
- You invoke the skill with `/migiq`
- The orchestrator runs all 5 phases in sequence
- Pauses for user input when needed (clarifications, approvals)
- User is actively involved in the process

**Best for:**
- Migrations you want to participate in actively
- When you need to approve decisions
- Shorter migrations (< 1 hour)
- Learning and exploration

### Autonomous Mode (Via Agent)
Delegate the migration to a background migrator agent:
- Spawn a migrator agent (see AGENT.md in project root)
- The agent works independently with minimal user interaction
- Provides periodic progress updates
- User can check in asynchronously

**Best for:**
- Long-running migrations (> 1 hour)
- Multiple migrations in parallel
- Background work while you focus on other tasks
- Overnight or multi-hour migrations

### When to Use Agent Delegation

**Delegate to agent if:**
- Migration is estimated to take > 60 minutes
- User says "work on this in the background" or "let me know when done"
- User wants to run multiple migrations in parallel
- Migration is part of a batch operation

**Run directly if:**
- User is actively engaged in the conversation
- Migration is < 60 minutes
- User wants to approve each phase
- This is the user's primary focus right now

### How to Delegate to Agent

When you determine autonomous execution is appropriate:

```
I recommend running this migration autonomously via an agent since it's 
estimated to take 90-120 minutes. The agent will work independently and 
update you on progress.

Would you like me to:
1. Spawn a migrator agent to handle this in the background
2. Run it interactively in this conversation (we can pause/resume)
```

If user chooses agent delegation, spawn it:

```
Agent({
  description: "Migrate [source] to [target]",
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md.
  
  Task: Migrate this application from [source] to [target].
  
  Working Directory: [project-path]
  
  Requirements:
  - Source: [current technology]
  - Target: [target technology]
  - Deployment: Red Hat OpenShift
  - Approach: [phased/big bang based on user input or analysis]
  
  Follow the migiq skill workflow (5 phases):
  1. Run mig-graphify for codebase analysis
  2. Use mig-prompt-builder for requirements (use the requirements above)
  3. Run mig-plan to create migration plan
  4. Execute via mig-execute
  5. Generate final migration report
  
  Provide progress updates every 15-20 minutes or at phase boundaries.
  
  On completion, present the final migration report and highlight:
  - What succeeded
  - What needs attention
  - Next steps
  
  Work autonomously but ask for user input on critical architectural decisions.`
})
```

Then inform the user:

```
✅ Migrator agent spawned successfully!

The agent will:
- Analyze your [source] codebase
- Create a comprehensive migration plan to [target]
- Execute the migration
- Generate a final report

I'll notify you when it completes (estimated [time]). You can continue 
working on other things - the agent will update you on major milestones.
```

## Prerequisites

**Required:**
- A codebase to migrate (current working directory should be the project root)

**Optional:**
- Existing graphify-out/ directory (if not present, will be created)
- Existing migration plan (if present, will ask user if they want to use it or create new)

## Workflow

### Phase 0: Initialize and Validate

**Step 1: Verify environment**

Check the current working directory and verify it's a valid project:

```bash
# Verify we're in a project directory
pwd
ls -la

# Check for existing migration artifacts
[ -d graphify-out ] && echo "graphify-out exists" || echo "graphify-out missing"
[ -d mig-plan-workspace ] && echo "mig-plan-workspace exists" || echo "mig-plan-workspace missing"
[ -d mig-execute-workspace ] && echo "mig-execute-workspace exists" || echo "mig-execute-workspace missing"
```

**Step 2: Create orchestration workspace**

```bash
mkdir -p migiq-workspace
cd migiq-workspace

# Initialize orchestration log
cat > orchestration-log.md << 'EOF'
# MigIQ Orchestration Log

**Started**: $(date)
**Project**: $(basename $(pwd))

---

## Orchestration Timeline

EOF
```

**Step 3: Determine migration target**

If the user's request includes the target technology (e.g., "migrate to Quarkus"), extract it.
If not, you'll need to ask during the mig-prompt-builder phase.

**Log initialization:**

```markdown
### Phase 0: Initialization - STARTED
**Timestamp**: [timestamp]
**Working Directory**: [directory]
**Target Technology**: [if known, otherwise "TBD"]

---
```

### Phase 0.5: Migration Skill Detection

**Goal**: Check if a pre-built migration skill is available for this migration.

**Step 1: Check for installed migration skills**

```bash
[ -f .claude/skills/migration-skills.json ] && echo "Migration skills installed" || echo "No migration skills"
```

If the manifest exists, read it and extract the list of available skills.

**Step 2: Attempt early matching**

If the user's request includes source and/or target technology (e.g., "migrate to Quarkus"):
- Search the manifest's `source_tech` and `target_tech` fields for a match
- Normalize for comparison: lowercase, treat hyphens/spaces as equivalent, strip version suffixes for broad match

**Step 3: Log the result**

If a skill was matched:
```markdown
### Phase 0.5: Migration Skill Detection - MATCHED
**Skill**: [skill name]
**Source**: [source_tech] → **Target**: [target_tech]
**Phases**: [phase list]
**Build Command**: [build_tool]

This migration will use authoritative mapping tables from the migration skill.
```

If no match was found:
```markdown
### Phase 0.5: Migration Skill Detection - NO MATCH
No pre-built migration skill found for this migration path.
Migration will proceed using general LLM knowledge.
Tip: Install migration skills with `npx migiq add <git-url-or-path>`
```

**Note**: This detection is informational. Each downstream skill (mig-prompt-builder, mig-plan, mig-execute) independently checks for the migration skill reference and uses it if available. No explicit passing is needed.

---

### Phase 1: Codebase Analysis (mig-graphify)

**Goal**: Build a comprehensive knowledge graph of the current codebase.

**Step 1: Check for existing graphify output**

```bash
if [ -d ../graphify-out ]; then
    echo "Found existing graphify-out/"
    echo "Last modified: $(stat -f %Sm ../graphify-out)"
else
    echo "No existing graphify output found"
fi
```

If graphify-out exists and is recent (< 1 day old), ask user:
```
I found existing codebase analysis from [timestamp]. 
Would you like to:
1. Use existing analysis (faster)
2. Re-analyze codebase (recommended if code changed)
```

If user chooses to re-analyze or if graphify-out doesn't exist, proceed with analysis.

**Step 2: Invoke mig-graphify**

Announce to user:
```
🔍 Phase 1/4: Analyzing codebase structure...
Running mig-graphify to build knowledge graph.
```

Run the graphify skill:
```bash
cd ..  # Return to project root
graphify update .
```

Wait for completion. Graphify runs offline with no API calls.

**Step 3: Validate graphify output**

```bash
# Verify outputs were created
[ -f graphify-out/graph.json ] && echo "✅ graph.json created" || echo "❌ graph.json missing"
[ -f graphify-out/GRAPH_REPORT.md ] && echo "✅ GRAPH_REPORT.md created" || echo "❌ GRAPH_REPORT.md missing"

# Get basic stats
echo "Graph Statistics:"
cat graphify-out/GRAPH_REPORT.md | grep -E "Total (Nodes|Edges|Communities)"
```

**Step 4: Log completion**

Update orchestration-log.md:
```markdown
### Phase 1: Codebase Analysis - COMPLETED
**Duration**: [time]
**Outputs**:
- graphify-out/graph.json
- graphify-out/GRAPH_REPORT.md
- graphify-out/graph.html

**Statistics**:
- Nodes: [count]
- Edges: [count]
- Communities: [count]

---
```

Announce to user:
```
✅ Phase 1 complete: Analyzed [X] files, [Y] dependencies, [Z] communities
```

**On Failure:**
If graphify fails, stop orchestration and report:
```
❌ Phase 1 failed: Codebase analysis error

**Error**: [error message]

**Options**:
1. Retry with different settings
2. Continue with limited analysis (not recommended)
3. Abort orchestration

What would you like to do?
```

### Phase 2: Requirements Gathering (mig-prompt-builder)

**Goal**: Gather migration requirements and generate a standardized migration prompt.

**Step 1: Announce phase**

```
📝 Phase 2/4: Gathering migration requirements...
Running mig-prompt-builder to create comprehensive migration prompt.
```

**Step 2: Invoke mig-prompt-builder**

The mig-prompt-builder skill will:
- Read the graphify-out/ analysis
- Ask the user about target technology (if not already known)
- Gather migration approach, timeline, team context, risk tolerance
- Generate a standardized migration prompt

This phase is interactive - let mig-prompt-builder handle the conversation with the user.

**Step 3: Validate prompt output**

```bash
# Check that prompt was created
[ -f mig-prompt-workspace/migration-prompt.md ] && echo "✅ Migration prompt created" || echo "❌ Prompt missing"

# Show preview to user
echo "Migration Prompt Preview:"
head -n 20 mig-prompt-workspace/migration-prompt.md
```

**Step 4: Log completion**

Update orchestration-log.md:
```markdown
### Phase 2: Requirements Gathering - COMPLETED
**Duration**: [time]
**Output**: mig-prompt-workspace/migration-prompt.md

**Migration Details**:
- Source: [technology]
- Target: [technology]
- Approach: [phased/big bang/hybrid]
- Team Size: [if known]

---
```

Announce to user:
```
✅ Phase 2 complete: Migration prompt ready
   Source: [source tech]
   Target: [target tech]
   Approach: [migration approach]
```

**On Failure:**
If prompt building fails (user cancels, insufficient info), stop and report:
```
❌ Phase 2 failed: Could not generate migration prompt

**Reason**: [reason]

**Options**:
1. Retry with different inputs
2. Manually create migration prompt
3. Abort orchestration

What would you like to do?
```

### Phase 3: Migration Planning (mig-plan)

**Goal**: Create a comprehensive, actionable migration plan.

**Step 1: Check for existing plan**

```bash
if [ -d ../mig-plan-workspace ]; then
    echo "Found existing migration plan"
    echo "Last modified: $(stat -f %Sm ../mig-plan-workspace)"
else
    echo "No existing plan found"
fi
```

If an existing plan is found, ask user:
```
I found an existing migration plan from [timestamp].
Would you like to:
1. Use existing plan
2. Create new plan (will overwrite existing)
```

**Step 2: Announce phase**

```
🗺️ Phase 3/4: Creating migration plan...
Running mig-plan to generate spec, design, tasks, and user stories.
```

**Step 3: Invoke mig-plan**

Pass the migration prompt from Phase 2 to mig-plan:

```bash
# Read the migration prompt
MIGRATION_PROMPT=$(cat mig-prompt-workspace/migration-prompt.md)

# Invoke mig-plan skill with the prompt
# This will generate:
# - mig-plan-workspace/tasks.md
# - mig-plan-workspace/UserStory.md
# Note: spec and design are in migration-prompt.md from Phase 2
```

The mig-plan skill will:
- Use the graphify analysis from Phase 1
- Use the migration prompt from Phase 2
- Generate comprehensive planning documents
- Invoke integration skills (mig-test-gen, mig-containerize, mig-deploy) as needed

This phase may take several minutes for complex migrations.

**Step 4: Validate plan outputs**

```bash
# Verify all plan documents were created
echo "Plan Validation:"
[ -f mig-plan-workspace/tasks.md ] && echo "✅ tasks.md" || echo "❌ tasks.md missing"
[ -f mig-plan-workspace/UserStory.md ] && echo "✅ UserStory.md" || echo "❌ UserStory.md missing"
echo "Note: Specification and design are in mig-prompt-workspace/migration-prompt.md"

# Count user stories and tasks
echo "Plan Statistics:"
echo "User Stories: $(grep -c "^## User Story" mig-plan-workspace/UserStory.md)"
echo "Task Groups: $(grep -c "^## " mig-plan-workspace/tasks.md)"
echo "Subtasks: $(grep -c "^- \[ \]" mig-plan-workspace/tasks.md)"
```

**Step 5: Present plan summary to user**

```
✅ Phase 3 complete: Migration plan created

**Plan Summary**:
- User Stories: [count]
- Task Groups: [count]  
- Subtasks: [count]
- Estimated Duration: [from plan]

**Key Documents**:
- Migration Prompt (spec + design): mig-prompt-workspace/migration-prompt.md
- Tasks: mig-plan-workspace/tasks.md
- User Stories: mig-plan-workspace/UserStory.md

Would you like to:
1. Review the plan before execution (I can pause here)
2. Proceed automatically to execution
```

If user wants to review, wait for their confirmation before proceeding to Phase 4.

**Step 6: Log completion**

Update orchestration-log.md:
```markdown
### Phase 3: Migration Planning - COMPLETED
**Duration**: [time]

**Outputs**:
- mig-plan-workspace/tasks.md
- mig-plan-workspace/UserStory.md
(Note: spec/design in mig-prompt-workspace/migration-prompt.md)

**Statistics**:
- User Stories: [count]
- Task Groups: [count]
- Subtasks: [count]

---
```

**On Failure:**
If planning fails, stop and report:
```
❌ Phase 3 failed: Migration planning error

**Error**: [error message]
**Context**: [what was being planned]

**Options**:
1. Retry planning with modifications
2. Review partial plan (if available)
3. Abort orchestration

What would you like to do?
```

### Phase 4: Migration Execution (mig-execute)

**Goal**: Execute the migration plan and implement all tasks.

**Step 1: Announce phase**

```
🚀 Phase 4/4: Executing migration plan...
Running mig-execute to implement all tasks.

This will:
- Execute [X] user stories
- Complete [Y] tasks
- Invoke test generation, containerization, and deployment skills

This may take considerable time. I'll provide progress updates.
```

**Step 2: Invoke mig-execute**

The mig-execute skill will:
- Load the migration plan from Phase 3
- Execute tasks in dependency order
- Parallelize independent tasks
- Invoke integration skills (mig-test-gen, mig-containerize, mig-deploy)
- Update task checkboxes in real-time
- Handle failures gracefully
- Generate execution report

This phase is largely autonomous but may interact with the user for failure remediation.

**Step 3: Monitor execution progress**

As mig-execute runs, relay progress updates to the user:
```
Progress Update:
✅ User Story 1/5 complete
✅ User Story 2/5 complete
⏳ User Story 3/5 in progress...
```

If mig-execute pauses for user input (e.g., task failure), relay the question and wait for the user's decision.

**Step 4: Validate execution results**

Once mig-execute completes:

```bash
# Check execution outputs
echo "Execution Validation:"
[ -f mig-execute-workspace/EXECUTION_REPORT.md ] && echo "✅ Execution report" || echo "❌ Report missing"
[ -f mig-execute-workspace/execution-log.md ] && echo "✅ Execution log" || echo "❌ Log missing"

# Get execution statistics
echo "Execution Statistics:"
grep "Total User Stories" mig-execute-workspace/EXECUTION_REPORT.md
grep "Completed:" mig-execute-workspace/EXECUTION_REPORT.md
grep "Failed:" mig-execute-workspace/EXECUTION_REPORT.md
```

**Step 5: Log completion**

Update orchestration-log.md:
```markdown
### Phase 4: Migration Execution - COMPLETED
**Duration**: [time]
**Status**: [Success/Partial/Failed]

**Outputs**:
- mig-execute-workspace/EXECUTION_REPORT.md
- mig-execute-workspace/execution-log.md
- mig-execute-workspace/outputs/*

**Statistics**:
- User Stories Completed: [X] of [Y]
- Tasks Completed: [X] of [Y]
- Subtasks Completed: [X] of [Y]
- Failed Tasks: [count]

---
```

**On Failure:**
If execution fails completely (not just individual tasks), stop and report:
```
❌ Phase 4 failed: Migration execution error

**Error**: [error message]
**Progress**: [X] of [Y] user stories completed

See detailed report: mig-execute-workspace/EXECUTION_REPORT.md

**Options**:
1. Fix failed tasks and resume execution
2. Review partial results
3. Revise plan and retry

What would you like to do?
```

### Phase 5: Final Report Generation

**Goal**: Synthesize all outputs into a comprehensive migration report.

**Step 1: Announce final phase**

```
📊 Generating final migration report...
Synthesizing results from all phases.
```

**Step 2: Collect data from all phases**

Read outputs from all phases:
- graphify-out/GRAPH_REPORT.md
- mig-prompt-workspace/migration-prompt.md
- mig-plan-workspace/*.md
- mig-execute-workspace/EXECUTION_REPORT.md
- orchestration-log.md

**Step 3: Generate comprehensive migration report**

Create `migiq-workspace/MIGRATION_REPORT.md`:

```markdown
# Migration Report

**Project**: [project name]
**Migration**: [Source] → [Target]
**Date**: [date]
**Duration**: [total time from start to finish]

---

## Executive Summary

[2-3 paragraph narrative summary of the migration journey]

**Migration Objective**: [from migration prompt]

**Approach**: [phased/big bang/hybrid from migration prompt]

**Overall Status**: ✅ Success | ⚠️ Partial Success | ❌ Failed

**Key Achievements**:
- [Achievement 1 from execution results]
- [Achievement 2]
- [Achievement 3]

**Challenges Encountered**:
- [Challenge 1 if any]
- [Challenge 2 if any]

---

## Migration Journey

### Phase 1: Codebase Analysis
**Status**: ✅ Completed
**Duration**: [time]

Analyzed the existing codebase to understand structure and dependencies:
- **Files Analyzed**: [count from graphify]
- **Dependencies Mapped**: [count from graphify]
- **Communities Identified**: [count from graphify]
- **God Nodes Detected**: [count from graphify - critical dependencies]

Key insights from analysis:
- [Insight 1 from GRAPH_REPORT.md]
- [Insight 2]

### Phase 2: Requirements Gathering
**Status**: ✅ Completed
**Duration**: [time]

Gathered migration requirements and established target state:
- **Source Technology**: [from migration prompt]
- **Target Technology**: [from migration prompt]
- **Migration Strategy**: [from migration prompt]
- **Deployment Platform**: Red Hat OpenShift
- **Team Context**: [from migration prompt if available]

### Phase 3: Migration Planning
**Status**: ✅ Completed
**Duration**: [time]

Created comprehensive migration plan:
- **User Stories**: [count]
- **Task Groups**: [count]
- **Subtasks**: [count]

Planning artifacts generated:
- Technical specification documenting current and target state
- Architecture design for migrated system
- Detailed task breakdown with integration hooks
- User stories mapping work to business value

### Phase 4: Migration Execution
**Status**: [status from execution report]
**Duration**: [time]

Executed the migration plan with automated task orchestration:

**Completion Statistics**:
- User Stories: [X] of [Y] completed ([percentage]%)
- Task Groups: [X] of [Y] completed ([percentage]%)
- Subtasks: [X] of [Y] completed ([percentage]%)

**Acceptance Criteria Met**: [X] of [Y]

[If failures occurred]
**Failed Tasks**: [count]
- [Failed task 1 with brief description]
- [Failed task 2 with brief description]

---

## Technical Details

### Source Application Analysis

**Technology Stack** (before migration):
[From migration-prompt.md - Current Application Summary]

**Architecture Pattern**: [from migration-prompt.md]

**Key Components**:
[List from migration-prompt.md]

**Code Metrics**:
- Lines of Code: [from graphify if available]
- Primary Language: [from graphify]
- Frameworks: [from migration-prompt.md]

### Target Application Design

**Technology Stack** (after migration):
[From migration-prompt.md - Target Platform and Technologies]

**Architecture Pattern**: [from migration-prompt.md]

**Key Changes**:
[List architectural changes from migration-prompt.md]

### Files Changed

**Total Files Modified**: [count from execution report]

[Sample of key files changed - top 10-15]
- [file 1] - [what changed]
- [file 2] - [what changed]
- [file 3] - [what changed]
...

Full list: See mig-execute-workspace/EXECUTION_REPORT.md

### Integration Work Completed

**Testing**:
- Characterization tests: [status]
- Unit tests: [coverage if available]
- Integration tests: [status]
- End-to-end tests: [status]

**Containerization**:
- Components containerized: [count]
- Container images created: [count]
- Dockerfile best practices applied: [yes/no]

**Deployment**:
- OpenShift manifests created: [count]
- Services configured: [count]
- ConfigMaps/Secrets configured: [count]

---

## Execution Statistics

### Timeline
- **Total Duration**: [time from start to finish]
- **Phase 1 (Analysis)**: [time]
- **Phase 2 (Requirements)**: [time]
- **Phase 3 (Planning)**: [time]
- **Phase 4 (Execution)**: [time]
- **Phase 5 (Reporting)**: [time]

### Success Metrics
- **User Stories Completed**: [X]/[Y] ([percentage]%)
- **Tasks Completed**: [X]/[Y] ([percentage]%)
- **Subtasks Completed**: [X]/[Y] ([percentage]%)
- **Acceptance Criteria Met**: [X]/[Y] ([percentage]%)

[If applicable]
### Failure Analysis
- **Failed Tasks**: [count]
- **Common Failure Reasons**:
  - [Reason 1]: [count] occurrences
  - [Reason 2]: [count] occurrences

---

## Deliverables

All migration artifacts are organized in the following structure:

```
project-root/
├── graphify-out/              # Codebase analysis
│   ├── graph.json
│   ├── GRAPH_REPORT.md
│   └── graph.html
│
├── mig-prompt-workspace/      # Requirements
│   └── migration-prompt.md
│
├── mig-plan-workspace/        # Planning artifacts
│   ├── tasks.md
│   └── UserStory.md
│   # Note: spec/design in mig-prompt-workspace/migration-prompt.md
│
├── mig-execute-workspace/     # Execution results
│   ├── EXECUTION_REPORT.md
│   ├── execution-log.md
│   └── outputs/
│       ├── tests/
│       ├── containers/
│       └── deployments/
│
└── migiq-workspace/           # Orchestration artifacts
    ├── orchestration-log.md
    └── MIGRATION_REPORT.md (this file)
```

### Key Documents
1. **Migration Plan**: mig-plan-workspace/tasks.md
2. **Execution Report**: mig-execute-workspace/EXECUTION_REPORT.md
3. **Migration Prompt (spec + design)**: mig-prompt-workspace/migration-prompt.md
4. **User Stories**: mig-plan-workspace/UserStory.md
5. **Codebase Analysis**: graphify-out/GRAPH_REPORT.md
6. **Orchestration Log**: migiq-workspace/orchestration-log.md

---

## Migration Knowledge Source

[If a migration skill was used during this migration]
**Migration Skill**: [skill name]
**Source Repository**: [from manifest source field]
**Mapping Tables Applied**:
- Dependency replacements: [count of rows in dependency-map.md]
- API changes: [count of rows in api-map.md]
- Config property renames: [count of rows in config-map.md]
- Pattern transformations: [count of rows in pattern-map.md]

[If no migration skill was used]
**Migration Knowledge**: General LLM training data
**Recommendation**: For improved accuracy in future migrations, install curated migration skills:
```
npx migiq add https://github.com/savitharaghunathan/migration-skills
```
Run `npx migiq list` to see available migration skills.

---

## Recommendations

[Based on execution results, provide 3-5 specific recommendations]

### Immediate Next Steps
[If migration succeeded]
1. Review acceptance criteria validation
2. Run comprehensive integration tests in staging environment
3. Conduct performance testing against baseline metrics
4. Deploy to staging for user acceptance testing
5. Plan production cutover with rollback procedures

[If migration partially succeeded]
1. Address failed tasks (see failure analysis above)
2. Review and update plan based on learnings
3. Re-execute remaining tasks
4. Validate completed portions before proceeding

[If migration failed]
1. Review failure root causes in execution report
2. Update migration plan to address blockers
3. Consider revised approach for problematic areas
4. Re-run orchestration when ready

### Long-term Recommendations
1. [Recommendation based on code analysis]
2. [Recommendation based on execution learnings]
3. [Recommendation for operational excellence]

---

## Conclusion

[1-2 paragraph conclusion summarizing the migration outcome and impact]

**Migration Status**: [Final status]

[If successful]
The migration has been successfully completed. All deliverables have been produced and are ready for deployment. Review the detailed execution report and follow the next steps outlined above.

[If partial]
The migration was partially completed with [X]% of tasks successfully executed. Address the failed tasks documented in the execution report and re-run the orchestration to complete remaining work.

[If failed]
The migration encountered critical issues during execution. Review the failure analysis and execution logs to understand root causes. Update the migration approach and re-run when ready.

---

**Report Generated**: [timestamp]
**Generated by**: MigIQ Orchestrator
```

**Step 4: Present report to user**

Display the executive summary and key statistics:

```
🎉 Migration orchestration complete!

**Final Status**: [status]

**Journey Summary**:
✅ Phase 1: Codebase Analysis - [duration]
✅ Phase 2: Requirements - [duration]
✅ Phase 3: Planning - [duration]
[✅/⚠️/❌] Phase 4: Execution - [duration]
✅ Phase 5: Reporting - [duration]

**Total Duration**: [time]

**Results**:
- User Stories Completed: [X]/[Y]
- Tasks Completed: [X]/[Y]
- Acceptance Criteria Met: [X]/[Y]

📄 Comprehensive migration report: migiq-workspace/MIGRATION_REPORT.md

[If successful]
🎯 Migration successful! Review the report and proceed with deployment to staging.

[If partial]
⚠️ Migration partially completed. [X] tasks need attention - see report for details.

[If failed]
❌ Migration encountered critical issues. Review the failure analysis in the report.
```

**Step 5: Offer next actions**

Based on the outcome:

[If successful]
```
Next steps:
1. Review comprehensive report: migiq-workspace/MIGRATION_REPORT.md
2. Validate acceptance criteria
3. Run integration tests
4. Deploy to staging environment

Would you like me to help with any of these?
```

[If partial or failed]
```
Would you like me to:
1. Review the failures in detail
2. Help fix the failed tasks
3. Re-run execution for remaining work
4. Revise the migration plan
```

## Output Structure

```
project-root/
├── graphify-out/              # Phase 1: Analysis
│   ├── graph.json
│   ├── GRAPH_REPORT.md
│   └── graph.html
│
├── mig-prompt-workspace/      # Phase 2: Requirements
│   └── migration-prompt.md
│
├── mig-plan-workspace/        # Phase 3: Planning
│   ├── tasks.md
│   └── UserStory.md
│   # Note: spec/design in migration-prompt.md (Phase 2)
│
├── mig-execute-workspace/     # Phase 4: Execution
│   ├── EXECUTION_REPORT.md
│   ├── execution-log.md
│   └── outputs/
│       ├── tests/
│       ├── containers/
│       └── deployments/
│
└── migiq-workspace/           # Phase 5: Orchestration & Reporting
    ├── orchestration-log.md
    └── MIGRATION_REPORT.md
```

## Error Handling

This skill follows a "stop and report" error handling strategy:

**On any phase failure**:
1. Stop the orchestration immediately
2. Log the failure with full context
3. Present the error and options to the user
4. Wait for user decision before proceeding

**Recovery options** typically include:
- Retry the failed phase
- Skip the phase (if safe)
- Abort orchestration with partial results
- Modify inputs and retry

**Graceful degradation**: If execution completes with partial success, the final report still generates, highlighting what was accomplished and what remains.

## Important Notes

**Automatic orchestration**: This skill runs all phases automatically in sequence. It only pauses for user input when:
- A phase fails
- User explicitly requested to review the plan before execution
- mig-prompt-builder needs additional requirements

**Idempotent phases**: Each phase checks for existing outputs and asks the user if they want to reuse or regenerate. This allows resuming after interruptions.

**Progress visibility**: The orchestration log and frequent updates keep the user informed throughout the multi-phase workflow.

**Comprehensive reporting**: The final migration report synthesizes outputs from all phases into a single cohesive document suitable for stakeholder review.

## Tips for Success

**Set expectations**: This is a multi-phase, time-intensive workflow. Let the user know upfront that the orchestration may take considerable time (30 minutes to several hours depending on codebase size and migration complexity).

**Preserve all artifacts**: Never delete intermediate outputs. They're valuable for debugging, learning, and future iterations.

**Use existing work**: If graphify-out/ or mig-plan-workspace/ exist, ask before regenerating. Reusing recent analysis saves time.

**Communicate clearly**: At each phase transition, announce what's happening and what's coming next.

**Handle failures gracefully**: Don't panic on failure. Present clear options and let the user decide how to proceed.

**Generate great reports**: The final migration report is often shared with stakeholders. Make it comprehensive, well-formatted, and actionable.

## Example Invocation

User: "Migrate this app to Quarkus"

Skill flow:
1. **Phase 0**: Initialize migiq-workspace, validate environment
2. **Phase 1**: Run graphify to analyze Java EE codebase
3. **Phase 2**: Invoke mig-prompt-builder, gather Quarkus migration requirements
4. **Phase 3**: Invoke mig-plan to create migration plan from EE to Quarkus
5. **Phase 4**: Invoke mig-execute to implement all tasks
6. **Phase 5**: Generate comprehensive migration report
7. Present final results and next steps

Total time: 30-90 minutes depending on codebase size
