# Walkthrough: Migrating an App with MigIQ + Migration Skills

This guide walks you through using MigIQ with curated migration skills to migrate a Spring Boot 3.5 application to Spring Boot 4.0. The same workflow applies to any migration path that has a migration skill available.

We'll use [ConfigHub](https://github.com/savitharaghunathan/springboot-confighub-migration) as the example app — a Spring Boot 3.5.14 configuration management app that exercises 47 distinct API patterns that change in 4.0.

## Why Migration Skills?

MigIQ works out of the box using general LLM knowledge. Migration skills make it better:

- **Without skills**: MigIQ infers what needs to change from training data. Works for common patterns, but may miss edge cases or use outdated mappings.
- **With skills**: MigIQ reads authoritative mapping tables (dependency, API, config, pattern) extracted from official migration guides. Every transformation is grounded in documentation, not inference.

When we ran ConfigHub through MigIQ with the `spring-boot-3-to-4` skill loaded, it applied 42 mapping entries across 31 files and the build passed clean on the first attempt.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Java 17+ and Maven (for this example — adapt for your stack)
- Git

## Step 1: Install MigIQ

Navigate to your project directory and run:

```bash
npx @sshaaf/migiq
```

This installs 8 core skills into `.claude/skills/`:
`migiq`, `mig-graphify`, `mig-plan`, `mig-prompt-builder`, `mig-execute`, `mig-test-gen`, `mig-containerize`, `mig-deploy`

## Step 2: Install Migration Skills

```bash
npx @sshaaf/migiq add https://github.com/savitharaghunathan/migration-skills
```

You'll see all available skills installed:

```
📚 Installing 8 migration skill(s):

  ✅ httpclient-4-to-5 (httpclient-4 → httpclient-5)
  ✅ jboss-eap-7-to-8 (jboss-eap-7 → jboss-eap-8)
  ✅ jdk-21-to-25 (jdk-21 → jdk-25)
  ✅ spring-boot-2-to-3 (spring-boot-2 → spring-boot-3)
  ✅ spring-boot-3-to-4 (spring-boot-3 → spring-boot-4)
  ✅ spring-boot-to-quarkus (spring-boot-3 → quarkus-3)
  ✅ spring-framework-4-to-5 (spring-framework-4 → spring-framework-5)
  ✅ spring-framework-5-to-6 (spring-framework-5 → spring-framework-6)
```

Verify what's installed:
```bash
npx @sshaaf/migiq list
```

## Step 3: Run the Migration

Open Claude Code in your project directory. You have two options:

### Option A: Full Orchestration (Recommended)

One command runs all 5 phases automatically:

```
/migiq
Migrate this Spring Boot 3.5 app to Spring Boot 4.0
```

MigIQ will:

1. **Detect the skill** — reads `.claude/skills/migration-skills.json`, matches `spring-boot-3-to-4`
2. **Analyze the codebase** — runs graphify to build a knowledge graph (files, dependencies, communities)
3. **Build the migration prompt** — auto-populates from the skill's metadata and the graphify analysis
4. **Create the plan** — generates task groups aligned to the skill's phases (build-system → code → config → testing → additional → cleanup), with subtasks derived from the mapping tables
5. **Execute** — sub-agents apply the mapping tables, with build gates (`mvn compile`) between phases
6. **Report** — summarizes what changed and which mappings were applied

### Option B: Step-by-Step (More Control)

Run each phase individually to review output in between:

```
/mig-graphify                    # Analyze codebase → graphify-out/
/mig-prompt-builder              # Build migration prompt → mig-prompt-workspace/
/mig-plan                        # Create task plan → mig-plan-workspace/
/mig-execute                     # Execute the plan → mig-execute-workspace/
```

This lets you review and adjust the plan before execution, or re-run a single phase if needed.

## What Happens at Each Phase

### Phase 0.5: Skill Detection

MigIQ reads the manifest and fuzzy-matches your source/target technologies against installed skills. For example, "Spring Boot 3.5" matches the `spring-boot-3-to-4` skill's `source_tech: spring-boot-3`. If multiple skills match, it asks you to choose.

### Phase 1: Codebase Analysis (graphify)

Runs offline (no API calls) using tree-sitter AST extraction. Produces:
- `graphify-out/graph.json` — nodes, edges, communities
- `graphify-out/GRAPH_REPORT.md` — god nodes, surprising connections, architecture insights
- `graphify-out/graph.html` — interactive visualization

For ConfigHub: 188 files, 1,466 nodes, 1,550 edges, 173 communities.

### Phase 2: Migration Prompt

Combines the graphify analysis with the skill's metadata to produce `mig-prompt-workspace/migration-prompt.md`. This includes:
- A **Migration Skill Reference** section (skill name, path, build command, phases)
- Current application summary from graphify
- Target platform and technologies

### Phase 3: Planning

Reads the skill's `modules/` and `references/` directories to generate `mig-plan-workspace/tasks.md`. Task groups align to the skill's phases, and subtasks are derived from mapping table rows.

### Phase 4: Execution

Sub-agents receive the module instructions and mapping tables as authoritative context. Each phase has a **build gate** — the build must pass before moving to the next phase.

### Phase 5: Reporting

Produces `mig-execute-workspace/EXECUTION_REPORT.md` with per-file change logs and which mapping table entries were applied.

## What the Skill Contains

Each migration skill provides two things:

**Modules** — step-by-step instructions per phase:
```
modules/
├── build-system.md    # Dependency renames, version bumps, plugin changes
├── code.md            # API replacements, annotation renames, import changes
├── config.md          # Property renames in application.properties/yaml
├── testing.md         # Test annotation and framework changes
├── additional.md      # Edge cases, removals, structural changes
└── cleanup.md         # Verification steps
```

**References** — authoritative mapping tables:
```
references/
├── dependency-map.md  # Old dependency → new dependency
├── api-map.md         # Old API/class/annotation → new equivalent
├── config-map.md      # Old property name → new property name
└── pattern-map.md     # Structural/pattern changes
```

For the `spring-boot-3-to-4` skill, the mapping tables cover starter renames, Jackson 3 namespace changes (`com.fasterxml.jackson` → `tools.jackson`), JSpecify nullability annotations, `@MockBean` → `@MockitoBean`, config property renames, and more.

## Bring Your Own App

The workflow is the same for any app. Just make sure the right migration skill is installed:

```bash
# Check what skills you have
npx @sshaaf/migiq list

# Then in Claude Code:
/migiq
Migrate this app to [target]
```

MigIQ will match the skill automatically based on your app's technologies and your target.

## Creating New Migration Skills

If no skill exists for your migration path, generate one from an official migration guide:

```
/generate-migration-skill
Generate a migration skill from https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide
```

This produces a complete skill directory with mapping tables and phased modules. Install it:

```bash
npx @sshaaf/migiq add /path/to/your/migration-skills
```

See the [migration-skills](https://github.com/savitharaghunathan/migration-skills) repo for the generator and existing skills.

## Managing Skills

```bash
npx @sshaaf/migiq list                                              # List installed skills
npx @sshaaf/migiq add https://github.com/savitharaghunathan/migration-skills  # Install from git
npx @sshaaf/migiq add /path/to/local/migration-skills               # Install from local path
npx @sshaaf/migiq add https://github.com/.../migration-skills -g    # Install globally
npx @sshaaf/migiq remove spring-boot-3-to-4                         # Remove a specific skill
```
