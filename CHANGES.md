# Changes Summary

## Update: Single Tool Architecture (opencode agent)

**Date**: 2026-05-04

### Overview

The specification has been updated to use **opencode agent** as the single, unified tool for all code operations instead of multiple separate tools.

### What Changed

**Before** (Multiple Tools):
- openrewrite - Automated refactoring
- openCode - Code analysis and generation
- OpenSpec - Specification validation
- DeepEval - Evaluation framework
- OpenLIT - KPI metrics

**After** (Single Tool):
- **opencode agent** - Unified tool for all operations:
  - Code analysis and understanding
  - Automated refactoring
  - Code generation
  - Test generation (characterization and functional)
  - Specification validation
  - Quality metrics and evaluation
  - KPI tracking and reporting
  - Multi-language support

### Benefits

1. **Simplified Architecture** - Single integration point instead of 5+ tools
2. **Unified Context** - opencode agent maintains context across all operations
3. **Easier Setup** - One tool to configure and deploy
4. **Better Integration** - Seamless data flow between operations
5. **Reduced Complexity** - Fewer dependencies and configurations
6. **Consistent Interface** - Single API for all code operations

### Files Updated

All major specification files have been updated:

1. **SPECIFICATION.md** - Updated all harness phases to use opencode agent
2. **skills.md** - Updated all 19 skills to use opencode agent
3. **agents.md** - Updated all agent workflows to use opencode agent
4. **AGENT-MESH.md** - Updated architecture description
5. **README.md** - Updated prerequisites, setup, and technical stack
6. **QUICKSTART.md** - Updated getting started guide
7. **templates/rule.md** - Updated migration rules
8. **templates/tasks.md** - Updated task examples
9. **templates/CLAUDE.md** - Updated tool configuration

### Configuration Changes

**Environment Variables**:

Before:
```bash
export OPENCODE_API="http://localhost:8080"
export OPENSPEC_API="http://localhost:8081"
export DEEPEVAL_CONFIG="./deepeval.yaml"
export OPENLIT_URL="http://localhost:3000"
```

After:
```bash
export OPENCODE_AGENT_API="http://localhost:8080"
export OPENCODE_AGENT_API_KEY="your-api-key"
export OPENCODE_AGENT_CONFIG="./opencode-agent.yaml"
```

### Implementation Impact

**Skills** - All skills now interface with opencode agent:
- `/analyze-codebase` → Uses opencode agent
- `/generate-characterization-tests` → Uses opencode agent
- `/generate-functional-tests` → Uses opencode agent
- `/apply-refactor-rules` → Uses opencode agent
- `/generate-spec-driven-code` → Uses opencode agent
- `/validate-refactoring` → Uses opencode agent
- `/validate-coverage` → Uses opencode agent
- `/generate-evaluation-metrics` → Uses opencode agent
- `/validate-quality` → Uses opencode agent
- `/generate-kpi-metrics` → Uses opencode agent

**Agents** - All agents use opencode agent through skills:
- `test-generator-agent` → Uses opencode agent for all test generation
- `code-refactor-agent` → Uses opencode agent for refactoring and generation
- `quality-evaluator-agent` → Uses opencode agent for evaluation
- All other agents → Use opencode agent as needed

### Migration Path

For existing implementations:

1. **Replace tool dependencies** - Remove openrewrite, OpenSpec, DeepEval, OpenLIT
2. **Install opencode agent** - Single deployment
3. **Update configurations** - Use new environment variables
4. **Update skill implementations** - Point to opencode agent API
5. **Test end-to-end** - Verify all harnesses work with opencode agent

### Backward Compatibility

This is a **breaking change** that requires:
- New tool deployment (opencode agent)
- Configuration updates
- Skill implementation updates

The workflow, architecture, and agent patterns remain the same - only the underlying tool has changed.

### Next Steps

1. Deploy opencode agent
2. Configure opencode agent with project-specific rules
3. Update skill implementations to use opencode agent API
4. Test each harness phase independently
5. Run end-to-end migration test
6. Validate metrics and KPIs

### Questions?

See the updated documentation:
- [README.md](./README.md) - Project overview
- [QUICKSTART.md](./QUICKSTART.md) - Getting started
- [SPECIFICATION.md](./SPECIFICATION.md) - Complete specification
- [templates/CLAUDE.md](./templates/CLAUDE.md) - Configuration guide
