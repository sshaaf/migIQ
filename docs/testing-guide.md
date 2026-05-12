# Testing Guide

## Integration Testing

### End-to-End Test

```python
def test_end_to_end_migration():
    """Test full migration workflow"""

    # 1. Create sample project
    create_sample_project("./test-project")

    # 2. Run analysis
    result = run_skill("analyze-codebase", {
        "path": "./test-project",
        "migration-type": "framework"
    })
    assert result["migrationScore"] > 50

    # 3. Plan migration
    plan = run_skill("plan-migration", {
        "analysis-report": result["report_path"],
        "rules": "./rule.md"
    })
    assert len(plan["stories"]) > 0

    # 4. Process first story
    story = plan["stories"][0]
    result = run_agent("story-orchestrator-agent", {"story": story})

    # 5. Verify completion
    assert result["status"] == "success"
    assert result["ci_pipeline"]["status"] == "passed"
```

### Parallel Execution Test

```python
def test_parallel_execution():
    """Test parallel story processing"""
    stories = create_test_stories(3)

    results = run_agents_parallel([
        ("story-orchestrator-agent", {"story": stories[0]}),
        ("story-orchestrator-agent", {"story": stories[1]}),
        ("story-orchestrator-agent", {"story": stories[2]})
    ])

    # Verify all completed
    assert all(r["status"] == "success" for r in results.values())
```

### Failure Recovery Test

```python
def test_failure_recovery():
    """Test failure handling and recovery"""

    # Inject failure
    inject_test_failure("test-generator-agent")

    # Run story
    result = run_agent("story-orchestrator-agent", {"story": test_story})

    # Verify retry attempted
    assert result["retry_count"] == 3

    # Verify escalation
    assert result["escalated"] == True
```

## Performance Testing

```python
def test_performance_scalability():
    """Test with multiple concurrent stories"""

    start_time = time.time()

    # Process 10 stories concurrently
    results = process_stories_concurrently(count=10)

    duration = time.time() - start_time

    # Verify throughput
    assert duration < 600  # 10 stories in under 10 minutes
    assert all(r["status"] == "success" for r in results)
```

## Implementation Status

- [x] Sample migration project created
- [x] End-to-end test scenarios
- [x] Parallel execution tests
- [x] Failure scenario tests
- [x] Feedback loop tests
- [x] Performance benchmarks
