---
name: mig-plan
description: Creates comprehensive migration plans for application modernization projects. Use this skill whenever the user mentions migrating, modernizing, or upgrading an application from one platform/framework/language to another (e.g., Java EE to Spring Boot, monolith to microservices, on-prem to cloud). Also trigger when users ask for migration roadmaps, migration strategies, or how to plan a migration. This skill orchestrates the full planning workflow including specification, design, task breakdown, and user story generation.
---

# Migration Planning Skill

This skill creates comprehensive, actionable migration plans for application modernization projects. It produces structured documentation that guides teams through complex migrations.

## What This Skill Does

When invoked, this skill:

1. **Analyzes the codebase** using mig-graphify to build a knowledge graph
2. **Generates spec.md** - detailed specification of current state and migration scenario
3. **Creates design.md** - overall design and architecture for the target state
4. **Produces tasks.md** - granular task breakdown with subtasks
5. **Generates UserStory.md** - user stories linking tasks to business value

All outputs are saved to `mig-plan-workspace/`.

## When to Use This Skill

Use this skill when the user:
- Wants to migrate from technology A to technology B
- Asks "how do I plan this migration?"
- Needs a migration roadmap or strategy
- Mentions modernization, platform upgrade, or technology transition
- Has a complex migration ahead and needs structure

## Workflow

### Phase 1: Knowledge Gathering

First, ensure you have the knowledge graph:

1. Check if `graphify-out/` exists in the project
2. If not, invoke the `graphify` skill to analyze the codebase
3. Read the knowledge graph output to understand:
   - Code structure and dependencies
   - Architectural patterns
   - Technology stack
   - Integration points

### Phase 2: Understand Migration Context

Ask the user for migration specifics:
- **Source**: What are we migrating FROM? (platform, framework, version)
- **Target**: What are we migrating TO? (platform, framework, version)
- **Constraints**: Timeline, budget, risk tolerance
- **Scope**: Full migration or phased approach?

### Phase 3: Generate Specification (spec.md)

Create `mig-plan-workspace/spec.md` with detailed analysis:

```markdown
# Migration Specification

## Overview
[One paragraph summary of the migration]

## Current State Analysis

### Technology Stack
- [Current technologies with versions]
- [Dependencies and libraries]
- [Infrastructure and deployment]

### Architecture
[Describe current architecture with observations from graphify output]

### Key Components
[List major components, modules, services discovered in the knowledge graph]

### Integration Points
[External systems, APIs, databases, message queues]

### Code Examples
[Include 2-3 representative code snippets from the current codebase that illustrate patterns to be migrated]

## Target State

### Technology Stack
- [Target technologies with versions]
- [New dependencies and libraries]
- [Target infrastructure]

### Architecture Changes
[What architectural changes are needed?]

## Migration Scenario

### Migration Type
[Replatform, refactor, rearchitect, etc.]

### Migration Strategy
[Big bang, strangler fig, phased, etc.]

### Risk Assessment
[Key risks and mitigation strategies]

### Success Criteria
[How do we know the migration succeeded?]

## Observations and Challenges

### Technical Challenges
- [Challenge 1 with context from code analysis]
- [Challenge 2]

### Dependencies
- [Critical dependencies to address]

### Data Migration
- [Data migration requirements if applicable]
```

**Why detailed analysis matters**: The spec becomes the source of truth. Include specific code examples from the graphify analysis so developers understand exactly what patterns they're changing.

### Phase 4: Generate Design (design.md)

Create `mig-plan-workspace/design.md`:

```markdown
# Migration Design

## Architecture Overview

### Target Architecture
[Describe the target architecture with diagrams if possible]

### Components
[List new/modified components and their responsibilities]

### Technology Choices

#### Framework/Platform
- **Choice**: [Selected technology]
- **Rationale**: [Why this choice?]
- **Alternatives Considered**: [What else was considered?]

[Repeat for each major technology decision]

### Design Patterns
[Patterns to be used in the target state]

## Migration Approach

### Phasing Strategy
[If phased, describe the phases]

### Component Migration Order
1. [Component 1] - Why first?
2. [Component 2]
...

### Parallel Run Strategy
[How will old and new systems coexist during migration?]

## Integration Design

### External Systems
[How will integrations change?]

### Data Strategy
[Data migration, synchronization approach]

### API Compatibility
[Backward compatibility strategy if needed]

## Testing Strategy

### Test Approach
[Unit, integration, E2E testing plans]

### Validation Criteria
[How to validate each migration phase]

## Deployment Strategy

### Containerization
[Container strategy - see mig-containerization integration]

### Orchestration
[Kubernetes, OpenShift, etc.]

### CI/CD Pipeline
[Pipeline changes needed]

## Rollback Plan
[How to rollback if things go wrong]

## Monitoring and Observability
[Logging, metrics, tracing in target state]
```

### Phase 5: Generate Tasks (tasks.md)

Create `mig-plan-workspace/tasks.md` with detailed task breakdown.

**Task Structure**: Group related work into numbered task groups. Each task has subtasks with checkboxes.

**Critical Integration Points**: Every task group MUST include these subtasks:

A. **Test Generation**: Hook into mig-test-gen
B. **Containerization & Deployment**: Hook into mig-containerization and mig-deploy  
C. **Documentation**: Document the changes

```markdown
# Migration Tasks

## Task Group 1: [Task Group Name]

- [ ] 1.1 [Subtask description]
- [ ] 1.2 [Subtask description]
- [ ] 1.3 [Subtask description]
- [ ] 1.4 **Test Generation**: Use mig-test-gen to create test cases for [specific aspect]
  - Command: `/skill mig-test-gen` for [component/feature]
  - Expected: Unit tests for [X], integration tests for [Y]
- [ ] 1.5 **Containerization**: Use mig-containerization to containerize [component]
  - Command: `/skill mig-containerize` for [component]
  - Config needs: Environment variables for [X], secrets for [Y], ConfigMaps for [Z]
- [ ] 1.6 **Deployment**: Use mig-deploy to create deployment manifests
  - Command: `/skill mig-deploy` for [component]
  - Dependencies: [service A], [database B]
  - Network: Expose port [X], connect to [Y]
- [ ] 1.7 **Documentation**: Document [aspect]
  - Update README with [migration notes]
  - Add runbook for [operations]

## Task Group 2: [Next Task Group]
...
```

**How to create tasks**: 

1. Break the migration into logical phases based on the design
2. Each phase becomes a task group
3. Within each group, create subtasks that are:
   - **Actionable**: Clear what needs to be done
   - **Testable**: Can verify completion
   - **Sized appropriately**: 2-8 hours of work each
4. Always include the integration subtasks (test gen, containerization, deploy, docs)

**Example task breakdown for "Migrate Authentication Service"**:

```markdown
## 1. Migrate Authentication Service

- [ ] 1.1 Create new Spring Security configuration class
- [ ] 1.2 Migrate JWT token generation logic
- [ ] 1.3 Implement OAuth2 integration
- [ ] 1.4 Migrate user credential storage to target database
- [ ] 1.5 **Test Generation**: Use mig-test-gen for auth service
  - Command: `/skill mig-test-gen` targeting authentication module
  - Expected: Security tests, token validation tests, OAuth flow tests
- [ ] 1.6 **Containerization**: Use mig-containerization for auth service
  - Command: `/skill mig-containerize` for auth-service
  - Config needs: JWT_SECRET (secret), OAUTH_CLIENT_ID (secret), DB_CONNECTION (ConfigMap)
- [ ] 1.7 **Deployment**: Use mig-deploy for auth service
  - Command: `/skill mig-deploy` for auth-service
  - Dependencies: PostgreSQL database, Redis session store
  - Network: Expose 8080, connect to postgres:5432 and redis:6379
- [ ] 1.8 **Documentation**: Document authentication changes
  - Update API docs with new auth endpoints
  - Create migration guide for user credentials
  - Add troubleshooting guide for common auth issues
```

### Phase 6: Generate User Stories (UserStory.md)

Create `mig-plan-workspace/UserStory.md` that groups tasks into user stories.

**User Story Principles**:
- **Simple**: 1-2 sentences
- **User-focused**: Role + action + benefit
- **Clear language**: No jargon

```markdown
# User Stories

## User Story 1: [Title]

**As a:** [role/persona]  
**I want:** [action]  
**So that:** [benefit/outcome]

---

### Tasks
- [Link to task group: ## 1. Task Group Name from tasks.md]
- [Link to task group: ## 2. Another Task Group]

### Acceptance Criteria
- [ ] [Specific, testable criterion with expected result]
- [ ] [Another criterion]
- [ ] [Another criterion]

---

### Details
- **Priority:** [High / Medium / Low - based on migration dependencies]
- **Estimate:** [Story points or t-shirt size based on task complexity]

---

### Preconditions
- [What must be true before starting this story]
- [Dependencies from design.md]

---

### Steps to Reproduce / Implementation Notes
1. [High-level step referencing task groups]
2. [Another step]
3. [Validation step]

---

### Dependencies
- [Other user stories that must complete first]
- [External dependencies]

---

### Test Cases
- Test 1: [scenario] - expected result [reference to mig-test-gen output]
- Test 2: [scenario] - expected result

---

### Notes / Comments
- [Migration-specific context]
- [Risk mitigation notes]

---

[Repeat for each user story]
```

**Creating User Stories**: 

1. Group related task groups into stories
2. Each story should be completable in 1-2 sprints
3. Order stories by dependency (what must happen first)
4. Link back to specific task groups in tasks.md

**Example User Story**:

```markdown
## User Story 1: Secure Authentication Migration

**As a:** Platform Engineer  
**I want:** To migrate the authentication service from Java EE to Spring Security with OAuth2  
**So that:** Users can securely authenticate using modern OAuth2 standards and we can deprecate the legacy auth system

---

### Tasks
- ## 1. Migrate Authentication Service (from tasks.md)
- ## 2. Migrate User Database Schema (from tasks.md)

### Acceptance Criteria
- [ ] Users can authenticate using OAuth2 flow with no downtime
- [ ] All existing user credentials are successfully migrated with password hashes intact
- [ ] Legacy authentication endpoints return 410 Gone with migration instructions
- [ ] Security tests pass with 100% coverage on auth flows

---

### Details
- **Priority:** High
- **Estimate:** 8 story points

---

### Preconditions
- PostgreSQL database is deployed and accessible
- OAuth2 provider is configured
- SSL certificates are in place

---

### Steps to Reproduce / Implementation Notes
1. Deploy new Spring Security auth service alongside legacy system
2. Migrate user credentials using batch script with validation
3. Enable OAuth2 endpoints and validate token flow
4. Switch traffic to new service with canary deployment
5. Monitor for 48 hours before deprecating legacy endpoints

---

### Dependencies
- Database migration user story must complete first
- Certificate management user story

---

### Test Cases
- Test 1: OAuth2 login flow - user redirected to provider, receives valid JWT token
- Test 2: Migrated credentials - existing user can login with same password
- Test 3: Token validation - API endpoints accept new JWT format
- Test 4: Load test - auth service handles 1000 req/sec

---

### Notes / Comments
- Plan for 48-hour parallel run before cutting over
- Keep legacy auth service running for 30 days post-migration for rollback
- Monitor failed login attempts for credential migration issues
```

## Executing the Workflow

When this skill runs, follow these steps in order:

1. **Invoke mig-graphify** if graphify-out/ doesn't exist
2. **Read knowledge graph** from graphify-out/
3. **Gather migration context** from user (source, target, constraints)
4. **Generate spec.md** using knowledge graph + user context
5. **Generate design.md** based on spec and best practices
6. **Generate tasks.md** breaking down the design into actionable work
7. **For each task with integration hooks**, actually invoke the relevant skill:
   - Call `/skill mig-test-gen` with context from the task
   - Call `/skill mig-containerize` with component details
   - Call `/skill mig-deploy` with deployment requirements
   - Capture outputs and embed references in the task
8. **Generate UserStory.md** grouping tasks into stories
9. **Present summary** to user with links to all documents

## Output Structure

```
mig-plan-workspace/
├── spec.md           # Detailed specification
├── design.md         # Overall design
├── tasks.md          # Task breakdown with subtasks
└── UserStory.md      # User stories linking tasks
```

## Important Notes

**Auto-execution of integration skills**: Unlike traditional planning tools, this skill actively invokes mig-test-gen, mig-containerize, and mig-deploy during plan generation. This produces concrete, actionable outputs rather than placeholders.

**Incremental refinement**: After generating the initial plan, offer to refine specific sections based on user feedback. The plan is a living document.

**Realistic estimates**: When creating tasks and user stories, base estimates on actual code complexity from the knowledge graph, not generic assumptions.

**Link everything**: Maintain traceability from user stories → tasks → design → spec → knowledge graph. Each decision should trace back to code reality.

## Example Invocation

User: "I need to migrate our Java EE monolith to Spring Boot microservices"

Skill flow:
1. Check for graphify-out/ (invoke graphify if missing)
2. Ask clarifying questions about target Spring Boot version, microservice boundaries, deployment platform
3. Generate spec.md analyzing the current monolith structure
4. Generate design.md proposing microservice decomposition
5. Generate tasks.md with detailed migration tasks
6. For each task, invoke integration skills to generate tests, containers, and deployment configs
7. Generate UserStory.md grouping work into deliverable stories
8. Present complete plan to user

## Tips for Success

- **Use the knowledge graph**: Don't guess about code structure, read it from graphify output
- **Be specific**: Include actual class names, file paths, and code patterns from the codebase
- **Consider dependencies**: Order tasks and stories based on technical dependencies
- **Plan for testing**: Every migration task needs corresponding tests
- **Plan for deployment**: Every component needs containerization and deployment configuration
- **Document everything**: Migration knowledge is valuable for future maintenance
