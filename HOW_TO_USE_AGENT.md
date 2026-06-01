# How to Use the Migrator Agent

There are several ways to invoke the migrator agent in Claude Code. This guide explains each approach.

---

## Method 1: Ask Claude to Spawn the Agent (Recommended)

**What you do**: Just ask Claude in natural language to run a migration as an agent.

**Example prompts**:

```
"Can you spawn a migrator agent to migrate this Spring Boot app to Quarkus? 
I want it to work in the background."
```

```
"I need to migrate this to Quarkus. Can you run that as an autonomous agent 
following AGENT.md? I'll check back later."
```

```
"Migrate this Spring Boot app to Quarkus using the migrator agent. 
Let it run in the background."
```

**What happens**:
1. Claude reads your request
2. Claude recognizes you want autonomous/background work
3. Claude spawns an agent using the Agent tool (you don't see this)
4. The agent starts working following AGENT.md instructions
5. You get updates when the agent completes

**When to use this**: 
- ✅ Most flexible - just describe what you want
- ✅ You don't need to know the agent syntax
- ✅ Claude figures out the right prompt

---

## Method 2: Use the /migiq Skill with Delegation Request

**What you do**: Use the `/migiq` skill and ask for agent delegation.

**Example**:

```
/migiq

"Migrate this Spring Boot app to Quarkus. This will take a while, 
so please delegate to a migrator agent to work autonomously."
```

**What happens**:
1. The `/migiq` skill sees you want autonomous execution
2. It asks: "Should I run this directly or spawn an agent?"
3. You confirm agent delegation
4. The skill spawns an agent with the migration details
5. Agent works autonomously

**When to use this**:
- ✅ You want the skill to help set up the agent correctly
- ✅ You want to review the plan first, then delegate execution
- ✅ You trust the skill's judgment on autonomous vs interactive

---

## Method 3: Provide Agent Prompt Details (Advanced)

**What you do**: Give Claude specific instructions using the patterns from AGENT_EXAMPLES.md.

**Example**:

```
Please spawn a migrator agent with these details:

Task: Migrate this Spring Boot application to Quarkus
Working Directory: /Users/sshaaf/projects/my-spring-app

Follow the instructions in AGENT.md at:
/Users/sshaaf/git/konveyor/migIQ/AGENT.md

Use the migiq skill workflow. Update me at major milestones.
```

**What happens**:
1. Claude uses your detailed prompt to spawn the agent
2. Agent follows your specific instructions
3. You get exactly what you asked for

**When to use this**:
- ✅ You want precise control over the agent's instructions
- ✅ You've reviewed AGENT_EXAMPLES.md and know what you want
- ✅ You're doing something non-standard

---

## Method 4: Reference an Example from AGENT_EXAMPLES.md

**What you do**: Point to a specific example and customize it.

**Example**:

```
Use Example 1 from AGENT_EXAMPLES.md to spawn a migrator agent for my app.

Customizations:
- Working Directory: /Users/sshaaf/projects/my-app
- Target: Quarkus (instead of whatever the example uses)
```

**What happens**:
1. Claude reads AGENT_EXAMPLES.md
2. Finds Example 1
3. Customizes it with your changes
4. Spawns the agent

**When to use this**:
- ✅ You found an example that's close to what you need
- ✅ You want to reuse proven patterns
- ✅ You just need to change a few details

---

## Comparison of Methods

| Method | Complexity | Control | Best For |
|--------|-----------|---------|----------|
| **Method 1: Ask Claude** | Simple | Low | Most users, simple migrations |
| **Method 2: /migiq delegation** | Simple | Medium | Guided setup, plan review first |
| **Method 3: Provide prompt** | Advanced | High | Precise control, complex scenarios |
| **Method 4: Use example** | Medium | Medium | Reusing patterns, standard migrations |

---

## What You CANNOT Do

❌ **You cannot directly call `Agent({...})`**  
That's a tool only Claude has access to. You must ask Claude to spawn the agent.

❌ **You cannot run AGENT.md like a script**  
AGENT.md is instructions for the agent, not executable code. Claude reads it and follows it.

❌ **You cannot spawn agents without Claude**  
The agent spawning mechanism is built into Claude Code, not a separate CLI tool.

---

## Common Patterns

### Pattern 1: Quick Background Migration

```
"Migrate this Spring Boot app to Quarkus. 
Run it as an agent in the background - I'll check back in an hour."
```

Claude will:
1. Understand you want autonomous execution
2. Spawn an agent following AGENT.md
3. Agent runs migration workflow
4. You get notified when done

---

### Pattern 2: Overnight Migration

```
"I'm going to sleep. Can you spawn an agent to migrate this Java EE app 
to Spring Boot overnight? I'll review results in the morning."
```

Claude will:
1. Spawn agent with `run_in_background: true`
2. Agent works for several hours if needed
3. Saves comprehensive report
4. You review when you wake up

---

### Pattern 3: Parallel Multi-App Migration

```
"I have 5 microservices in /Users/sshaaf/projects/microservices/.
Can you spawn 5 migrator agents in parallel to upgrade them all 
from Node 12 to Node 20?"
```

Claude will:
1. Identify the 5 services
2. Spawn 5 agents (one per service)
3. All work in parallel
4. Report results as each completes

---

### Pattern 4: Plan Review Then Delegate

```
/migiq
"Migrate this to Quarkus"

[Review the plan Claude creates]

"The plan looks good. Can you spawn an agent to execute phases 4-5 
autonomously while I work on something else?"
```

Claude will:
1. Run phases 1-3 interactively (analysis, requirements, planning)
2. You review the plan
3. Spawn agent to execute phases 4-5 (execution, reporting)
4. You come back when done

---

## How to Monitor an Agent

Once an agent is spawned, you can:

### Check Status
```
"What's the status of the migrator agent?"
```

### View Progress
```
"Show me what the migration agent has done so far"
```

### Check Logs
Claude will tell you where logs are saved. Usually:
```bash
cat /Users/sshaaf/git/konveyor/migIQ/agent-test-run/migiq-workspace/orchestration-log.md
```

### Wait for Completion
You'll automatically get a notification when the agent completes:
```
✅ Migrator agent completed!

Results:
- 45/47 tasks successful
- Migration report: migiq-workspace/MIGRATION_REPORT.md
- 2 tasks need manual review

Would you like me to review the failed tasks?
```

---

## Troubleshooting

### "I asked for an agent but Claude ran it directly"

**Possible causes**:
- Your request wasn't clear about autonomous execution
- Migration seemed short enough for direct execution
- Claude chose interactive mode as safer

**Solution**: Be explicit:
```
"Run this as a background agent, not interactively"
```

---

### "The agent isn't responding"

**Possible causes**:
- Agent is waiting for permission prompts
- Agent encountered a blocker

**Solution**: Check for permission prompts in Claude Code. You may need to approve actions.

---

### "I don't know if agent is still running"

**Solution**: Ask Claude:
```
"Is my migrator agent still running?"
```

Or check the process:
```
/tasks
```

---

## Best Practices

### ✅ DO:
- Be clear about wanting autonomous/background execution
- Provide the working directory path
- Trust the agent to gather requirements via mig-prompt-builder
- Check back periodically for long migrations

### ❌ DON'T:
- Specify every detail upfront (let mig-prompt-builder ask)
- Expect instant results (agents take time)
- Try to manually run AGENT.md as a script
- Spawn too many agents at once (5-10 max)

---

## Examples from Real Usage

### Example 1: First-time User (Simple)

**User**: "I want to migrate my app but don't know much about migrations. Can you help?"

**Claude**: "Absolutely! I can spawn a migrator agent to handle this. What technology are you migrating from and to?"

**User**: "Spring Boot to Quarkus"

**Claude**: "Got it. I'll spawn an agent to migrate your Spring Boot app to Quarkus. It will analyze your code, create a plan, and execute the migration. This will take about 30-60 minutes. I'll notify you when it's done."

[Agent spawns and works autonomously]

---

### Example 2: Experienced Developer (Precise)

**User**: "Spawn a migrator agent following AGENT.md. Migrate /Users/sshaaf/projects/my-app from Spring Boot to Quarkus. Use phased approach. Target OpenShift deployment."

**Claude**: "Spawning migrator agent with your specifications..."

[Agent spawns with precise instructions]

---

### Example 3: Architect with Multiple Apps

**User**: "I need to upgrade 10 microservices from Java 11 to Java 17. Can you spawn agents to do them in parallel?"

**Claude**: "Yes, I'll spawn 10 migrator agents - one per service. They'll work in parallel. Estimated total time: 45 minutes (parallel) vs 7.5 hours (sequential). Proceed?"

**User**: "Yes"

[Claude spawns 10 agents]

---

## Quick Reference

| What You Want | What You Say |
|---------------|--------------|
| Simple background migration | "Migrate this to X using an agent" |
| Overnight work | "Spawn an agent to migrate overnight" |
| Parallel migrations | "Spawn agents for these 5 apps in parallel" |
| Plan then delegate | Use `/migiq`, review plan, ask for agent execution |
| Precise control | Provide detailed prompt from AGENT_EXAMPLES.md |

---

## Additional Resources

- **AGENT.md** - Agent instructions and persona
- **AGENT_EXAMPLES.md** - 6 example prompts you can reference
- **migiq/SKILL.md** - Orchestration workflow details
- **README.md** - Project overview

---

## Summary

**The simplest way**: Just ask Claude to spawn an agent in natural language.

```
"Migrate this Spring Boot app to Quarkus using an agent. 
Work in the background - I'll check back later."
```

That's it! Claude handles the rest.
