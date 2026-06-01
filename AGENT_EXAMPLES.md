# Migrator Agent - Example Prompts

This document provides ready-to-use prompts for spawning migrator agents for various migration scenarios.

## Important: Keep Prompts Simple

**Key Principle**: You don't need to specify all migration details upfront. The **mig-prompt-builder** skill (Phase 2) is designed to gather comprehensive requirements from simple inputs.

✅ **Good**: "Migrate this Spring Boot app to Quarkus"  
❌ **Unnecessary**: Providing all dependencies, versions, approaches upfront

The examples below show **both simple and detailed** approaches. For most cases, **simple is better** - let mig-prompt-builder do its job of elaborating requirements.

## Basic Template

### Simple Template (Recommended)

Use this when you trust mig-prompt-builder to gather details:

```javascript
Agent({
  description: "Brief description for tracking",
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
  /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: Migrate this application from [source] to [target].
  
  Working Directory: [Full path to project]
  
  Follow the migiq skill workflow at /Users/sshaaf/git/konveyor/migIQ/migiq/SKILL.md:
  1. Run mig-graphify for codebase analysis
  2. Use mig-prompt-builder to gather comprehensive requirements
     (It will ask clarifying questions as needed)
  3. Run mig-plan to create migration plan
  4. Execute the migration via mig-execute
  5. Generate final migration report
  
  Provide progress updates every 15-20 minutes or at major phase boundaries.
  
  Work autonomously but request user input during requirements gathering and 
  for critical architectural decisions.`
})
```

### Detailed Template (Optional)

Use this when you already know all migration details and want to skip interactive requirements gathering:

```javascript
Agent({
  description: "Brief description for tracking",
  run_in_background: true,  // Optional: for truly async work
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
  /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: [Describe the migration]
  
  Working Directory: [Full path to project]
  
  Requirements (use these during mig-prompt-builder):
  - Source: [Current technology stack]
  - Target: [Target technology stack]
  - Deployment: Red Hat OpenShift
  - Approach: [Phased/Big Bang/Strangler Fig]
  [Any other specific requirements]
  
  Follow the migiq skill workflow:
  1. Run mig-graphify for codebase analysis
  2. Use mig-prompt-builder (provide the requirements above when asked)
  3. Run mig-plan to create comprehensive migration plan
  4. Execute the migration via mig-execute
  5. Generate final migration report
  
  Provide progress updates every 15-20 minutes or at major phase boundaries.
  
  Work autonomously - use the requirements above instead of asking the user.`
})
```

---

## Example 1: Spring Boot to Quarkus (Simple Prompt)

**Scenario**: Migrate a Spring Boot REST API to Quarkus - user provides minimal details, mig-prompt-builder handles the rest.

```javascript
Agent({
  description: "Migrate Spring Boot to Quarkus",
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
  /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: Migrate this Spring Boot application to Quarkus.
  
  Working Directory: /Users/sshaaf/projects/my-spring-app
  
  NOTE: The user request is intentionally simple. Use mig-prompt-builder (Phase 2) 
  to gather all necessary details about:
  - Current Spring Boot version and dependencies (discovered via mig-graphify)
  - Target Quarkus version
  - Migration approach (phased vs big bang)
  - Timeline and constraints
  - Any special concerns
  
  Follow the migiq skill workflow:
  1. Analyze with mig-graphify
  2. Use mig-prompt-builder to gather comprehensive requirements
     (This will ask the user clarifying questions if needed)
  3. Create migration plan with mig-plan
  4. Execute migration with mig-execute
  5. Generate comprehensive final report
  
  Provide updates every 15 minutes or at phase transitions.
  
  Work autonomously but engage the user during mig-prompt-builder phase for 
  clarifications if the codebase analysis isn't sufficient.`
})
```

---

## Example 2: Node.js Modernization (Simple Prompt)

**Scenario**: Modernize an old Node.js application - let mig-prompt-builder ask what "modernize" means.

```javascript
Agent({
  description: "Modernize Node.js app",
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
  /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: Modernize this old Node.js Express application.
  
  Working Directory: /Users/sshaaf/projects/legacy-express-app
  
  NOTE: "Modernize" is intentionally vague. During Phase 2 (mig-prompt-builder):
  - Analyze what's outdated (via mig-graphify findings)
  - Ask user about target Node.js version
  - Ask about specific modernization goals (patterns, dependencies, deployment)
  - Clarify scope (big modernization vs incremental)
  
  Follow the migiq skill workflow:
  1. Analyze with mig-graphify (identify callback-heavy code, old patterns)
  2. Use mig-prompt-builder to define "modernize" specifically for this app
  3. Create modernization plan with mig-plan
  4. Execute with mig-execute
  5. Generate final report
  
  Update me every 20 minutes or when you complete major phases.
  
  Work autonomously but engage user during requirements gathering to understand 
  their modernization goals.`
})
```

---

## Example 2b: Node.js Modernization (Detailed, if you already know the goals)

```javascript
Agent({
  description: "Modernize Node.js Express app",
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md.
  
  Task: Modernize this Node.js Express app with specific goals.
  
  Working Directory: /Users/sshaaf/projects/legacy-express-app
  
  Modernization Requirements (for mig-prompt-builder):
  - Upgrade to Node.js 20 LTS
  - Convert callbacks to async/await
  - Update all dependencies
  - Add structured logging
  - Add health check endpoints
  - Containerize for OpenShift
  
  Follow migiq workflow. Use the requirements above during Phase 2.
  Update me every 20 minutes.`
})
```

---

## Example 3: Java EE to Spring Boot

**Scenario**: Migrate a large legacy Java EE monolith with EJBs to Spring Boot.

```javascript
Agent({
  description: "Migrate Java EE to Spring Boot",
  run_in_background: true,  // Long-running migration
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
  /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: Migrate this Java EE 7 monolith to Spring Boot microservices.
  
  Working Directory: /Users/sshaaf/projects/legacy-javaee-monolith
  
  Requirements:
  - Source: Java EE 7, EJBs (stateless & stateful), JPA, JAX-RS, deployed on WebLogic
  - Target: Spring Boot 3.2, Spring Data JPA, Spring Web, Spring Security
  - Deployment: Red Hat OpenShift 4.14
  - Approach: Phased migration with strangler fig pattern
  - Timeline: This is Phase 1 - migrate one bounded context (User Management)
  
  Key Challenges:
  - 80K LOC total, but focusing on User Management module (~12K LOC)
  - 15 stateless EJBs, 3 stateful EJBs in this module
  - WebLogic-specific JNDI lookups need replacement
  - Container-managed transactions → Spring @Transactional
  - Oracle database (staying the same for now)
  
  Migration Strategy:
  - Start with User Management bounded context only
  - Leave other modules in Java EE temporarily
  - Run both systems in parallel initially
  - Need adapter layer for communication between new Spring and old EE modules
  
  Follow the migiq skill workflow:
  1. Analyze with mig-graphify (focus on User Management module dependencies)
  2. Gather requirements with mig-prompt-builder
  3. Create phased plan with mig-plan (just User Management for now)
  4. Execute migration with mig-execute
  5. Generate comprehensive report
  
  This is a long migration (estimated 2-3 hours). Update me:
  - Every 30 minutes with progress percentage
  - When you complete each phase
  - When you encounter blockers or need decisions
  
  On completion, report:
  - What EJBs were successfully converted to Spring beans
  - Any EJBs that need manual intervention
  - Test coverage for migrated code
  - Performance comparison (if possible)
  - Adapter layer design for communicating with remaining Java EE modules
  - Plan for migrating next bounded context
  
  IMPORTANT: Ask me before:
  - Converting stateful EJBs (multiple approaches possible)
  - Making changes to database schema
  - Modifying APIs consumed by other modules
  - Removing any functionality (even if it appears unused)`
})
```

---

## Example 4: Monolith to Microservices

**Scenario**: Decompose a Rails monolith into Node.js microservices.

```javascript
Agent({
  description: "Decompose Rails monolith to microservices",
  run_in_background: true,
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
  /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: Decompose this Rails monolith into Node.js microservices.
  
  Working Directory: /Users/sshaaf/projects/rails-monolith
  
  Requirements:
  - Source: Ruby on Rails 6.x monolith
  - Target: Node.js 20 microservices with Express or Fastify
  - Deployment: Red Hat OpenShift 4.14 with service mesh
  - Approach: Strangler fig - extract one service at a time
  - Initial Service: Authentication Service
  
  Context:
  - The Rails app is 120K LOC with 8 bounded contexts
  - For this migration, extract ONLY the Authentication Service
  - Other services will be migrated in subsequent phases
  - Need to maintain API compatibility with Rails app during transition
  
  Authentication Service Scope:
  - User registration
  - Login/logout
  - JWT token generation
  - Password reset
  - OAuth2 integration (Google, GitHub)
  
  Technical Requirements:
  - Use Node.js with TypeScript
  - JWT-based authentication (same as Rails currently uses)
  - PostgreSQL database (can extract auth-specific tables)
  - API must match existing Rails endpoints exactly
  - Need integration tests proving compatibility
  
  Follow the migiq skill workflow:
  1. Analyze with mig-graphify (map authentication-related code)
  2. Gather requirements with mig-prompt-builder
  3. Create extraction plan with mig-plan
  4. Extract and implement with mig-execute
  5. Generate migration report
  
  Update me every 30 minutes and when you hit major milestones.
  
  On completion, report:
  - New Node.js authentication service structure
  - API compatibility testing results
  - Database migration strategy (schema extraction)
  - Service mesh configuration for routing
  - Rollout plan (canary deployment, percentage routing)
  - Next service recommendation for extraction
  
  Ask me before:
  - Making any changes to authentication tokens (JWT structure)
  - Modifying database schemas
  - Breaking API compatibility (even temporarily)
  - Choosing between Express vs Fastify framework`
})
```

---

## Example 5: Parallel Multi-App Migration

**Scenario**: Migrate 5 microservices from Node.js 12 to Node.js 20 in parallel.

```javascript
// Spawn 5 agents in parallel - one per microservice
const microservices = [
  'user-service',
  'product-service', 
  'order-service',
  'notification-service',
  'analytics-service'
];

microservices.forEach(serviceName => {
  Agent({
    description: `Upgrade ${serviceName} to Node.js 20`,
    run_in_background: true,
    prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
    /Users/sshaaf/git/konveyor/migIQ/AGENT.md
    
    Task: Upgrade ${serviceName} from Node.js 12 to Node.js 20.
    
    Working Directory: /Users/sshaaf/projects/microservices/${serviceName}
    
    Requirements:
    - Source: Node.js 12.x
    - Target: Node.js 20 LTS
    - Deployment: Red Hat OpenShift 4.14
    - Approach: In-place upgrade with testing
    
    Upgrade Checklist:
    - Update package.json to specify "engines": {"node": ">=20.0.0"}
    - Update all dependencies to latest compatible versions
    - Test for Node.js 20 breaking changes
    - Update Dockerfile to use node:20-alpine base
    - Run existing test suite
    - Generate new tests if coverage gaps found
    - Update CI/CD pipeline for Node.js 20
    
    Follow the migiq skill workflow (condensed for simple upgrade):
    1. Quick analysis with mig-graphify
    2. Requirements via mig-prompt-builder (use above requirements)
    3. Upgrade plan with mig-plan
    4. Execute upgrade with mig-execute
    5. Generate report
    
    This is a simple upgrade, estimated 20-30 minutes.
    Update me when you complete or encounter issues.
    
    On completion, report:
    - Dependencies updated (list any major version bumps)
    - Test results (all passing?)
    - Any Node.js 12 → 20 breaking changes encountered
    - Container image size comparison
    - Ready for deployment? (yes/no with rationale)
    
    Proceed autonomously - this is a straightforward upgrade.`
  });
});

console.log(`Spawned ${microservices.length} migrator agents for parallel upgrades.`);
console.log('Each agent will update you independently. Check back in ~30 minutes.');
```

---

## Example 6: Overnight Large Migration

**Scenario**: Migrate a massive legacy codebase overnight while you sleep.

```javascript
Agent({
  description: "Large legacy migration - overnight",
  run_in_background: true,
  prompt: `You are a migrator agent. Follow the instructions in AGENT.md located at:
  /Users/sshaaf/git/konveyor/migIQ/AGENT.md
  
  Task: Migrate this large legacy .NET Framework application to .NET 8.
  
  Working Directory: /Users/sshaaf/projects/legacy-dotnet-app
  
  Requirements:
  - Source: .NET Framework 4.8, Windows-specific, IIS deployment
  - Target: .NET 8, cross-platform, containerized
  - Deployment: Red Hat OpenShift 4.14
  - Approach: Big bang migration (app is self-contained, no gradual migration possible)
  
  Context:
  - This is a 200K LOC application
  - Estimated 4-6 hour migration
  - I'm starting this before going to sleep - work overnight
  - I'll review results in the morning (~8 hours from now)
  
  Requirements:
  - Convert .NET Framework → .NET 8
  - Replace Windows-specific APIs with cross-platform equivalents
  - Migrate IIS → Kestrel
  - Containerize with proper .NET 8 multi-stage Dockerfile
  - Generate OpenShift deployment manifests
  
  Follow the migiq skill workflow:
  1. Analyze with mig-graphify (identify Windows-specific code)
  2. Gather requirements with mig-prompt-builder
  3. Create comprehensive plan with mig-plan
  4. Execute migration with mig-execute (this will take hours)
  5. Generate detailed final report
  
  Update Strategy (for overnight work):
  - Log major milestones to execution log
  - Don't spam notifications - I'm asleep
  - Save comprehensive report for morning review
  - If you hit critical blockers that prevent progress, document them clearly
  
  On completion (when I wake up), I expect to see:
  - Final migration report at migiq-workspace/MIGRATION_REPORT.md
  - Clear summary: what % of tasks completed successfully
  - List of Windows-specific APIs that were successfully migrated
  - List of any APIs that need manual intervention
  - Test results
  - Container build status
  - OpenShift deployment readiness
  
  Decision-Making Guidance:
  - Work autonomously on technical conversions
  - If multiple approaches exist, choose the most .NET-idiomatic one
  - Document your reasoning in the execution log
  - If you encounter a true blocker (not just a failed task), stop and report clearly
  
  I'll review your work in the morning. Good luck!`
})

console.log('🌙 Overnight migration started.');
console.log('The agent will work for 4-6 hours.');
console.log('Check migiq-workspace/MIGRATION_REPORT.md in the morning.');
```

---

## Tips for Writing Agent Prompts

### 1. Keep It Simple (Let mig-prompt-builder Elaborate)

**Preferred Approach** - Simple task description:
```javascript
Task: Migrate this Spring Boot app to Quarkus.
Working Directory: /Users/sshaaf/projects/my-app

// mig-prompt-builder will:
// - Discover Spring Boot version via graphify
// - Ask about target Quarkus version
// - Ask about migration approach
// - Clarify deployment requirements
```

**Alternative** - Detailed requirements (only if you already know everything):
```javascript
Task: Migrate with these specific requirements...
Requirements:
- Source: Spring Boot 3.2.1
- Target: Quarkus 3.6
- Approach: Phased migration
// Agent uses these during mig-prompt-builder phase
```

### 2. Always Provide Working Directory
The only required field - full absolute path:
```javascript
Working Directory: /Users/sshaaf/projects/my-app
```

### 3. Set Update Expectations
Tell the agent how often to update you:
```javascript
// For active monitoring:
Update me every 15 minutes or at phase transitions.

// For background work:
Update me only at major milestones or blockers.

// For overnight work:
Log to file, don't notify me. I'll review in the morning.
```

### 4. Define What Needs User Input
Be explicit about when the agent should ask vs. decide:
```javascript
Ask me before:
- Making breaking API changes
- Modifying database schemas
- Removing functionality

Decide autonomously on:
- Dependency version updates
- Code style and formatting
- Test implementation details
```

### 5. Specify Success Criteria
Tell the agent what "done" looks like:
```javascript
On completion, report:
- Migration success rate (% tasks completed)
- Test coverage and results
- Deployment readiness
- Next steps
```

---

## Advanced: Agent Coordination

For complex multi-agent scenarios, coordinate agents:

```javascript
// Spawn orchestrator agent
Agent({
  description: "Migration orchestrator",
  prompt: `You are a migration orchestrator agent.
  
  Task: Coordinate the migration of 10 microservices from Java 11 to Java 17.
  
  Strategy:
  1. Analyze all 10 services to determine dependencies
  2. Create migration order (dependencies first)
  3. Spawn child migrator agents for each service in the correct order
  4. Monitor progress of all child agents
  5. Report consolidated results
  
  Working Directory: /Users/sshaaf/projects/microservices/
  
  Services to migrate:
  - config-server (no dependencies - start here)
  - discovery-server (depends on config-server)
  - api-gateway (depends on discovery-server)
  - user-service (depends on discovery-server)
  - product-service (depends on discovery-server)
  - order-service (depends on user-service, product-service)
  - payment-service (depends on order-service)
  - notification-service (depends on order-service)
  - analytics-service (depends on all services)
  - admin-dashboard (depends on all services)
  
  For each service, spawn a migrator agent following AGENT.md.
  Track their progress and report consolidated results.`
})
```

---

## Monitoring Agent Progress

After spawning an agent, you can check its status:

```bash
# If running in background
/tasks  # List all background tasks

# Check specific agent output
tail -f /tmp/claude-*/tasks/<agent-id>.output
```

The agent will also notify you at completion with a summary.
