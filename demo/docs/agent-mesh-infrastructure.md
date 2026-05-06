# Agent Mesh Infrastructure

## Overview

The Agent Mesh provides distributed coordination, state management, and resilience patterns for all agents.

## Message Passing Protocol

### Message Format

```json
{
  "traceId": "story-US123-20260505",
  "messageId": "msg-uuid",
  "from": "story-orchestrator-agent",
  "to": "test-generator-agent",
  "type": "invoke",
  "payload": {
    "storyId": "US-123",
    "context": {},
    "parameters": {}
  },
  "timestamp": "2026-05-05T12:00:00Z"
}
```

### Message Types

- **invoke**: Request agent to perform work
- **response**: Agent completes work
- **error**: Agent reports failure
- **status**: Progress update
- **escalate**: Request human intervention

## Agent State Management

### Local State

Each agent maintains:
- Current task
- Work queue
- Execution history
- Performance metrics

### Shared State

Coordinated via:
- `tasks.md` - Source of truth for backlog
- Kanban board - External sync
- Git - Configuration versioning
- File system - Artifacts and reports

### State Persistence

```python
class AgentState:
    def __init__(self, agent_name):
        self.state_dir = Path(f".claude/state/{agent_name}")
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, state_data):
        """Save state checkpoint"""
        checkpoint_file = self.state_dir / f"checkpoint-{int(time.time())}.json"
        checkpoint_file.write_text(json.dumps(state_data))

    def load_latest_checkpoint(self):
        """Load most recent checkpoint"""
        checkpoints = sorted(self.state_dir.glob("checkpoint-*.json"))
        if checkpoints:
            return json.loads(checkpoints[-1].read_text())
        return None
```

## Retry Mechanisms

### Exponential Backoff

```python
def retry_with_backoff(func, max_retries=3, base_delay=1000):
    """Retry with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay / 1000.0)
            logger.info(f"Retrying after {delay}ms (attempt {attempt + 1}/{max_retries})")
```

### Retry Policies

- **Transient Failures**: Network errors, timeouts → Retry
- **Validation Errors**: Bad input, config issues → No retry, escalate
- **Resource Errors**: Out of memory, disk full → No retry, alert

## Circuit Breaker Pattern

### Implementation

```python
class CircuitBreaker:
    def __init__(self, threshold=5, timeout=60000, reset_timeout=300000):
        self.threshold = threshold
        self.timeout = timeout
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func):
        """Execute function with circuit breaker"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.threshold:
            self.state = "OPEN"
```

### Usage

```python
# Per-agent circuit breaker
circuit_breaker = CircuitBreaker(threshold=5)

try:
    result = circuit_breaker.call(lambda: invoke_agent("test-generator-agent", params))
except CircuitOpenError:
    # Route to backup or escalate to human
    logger.error("Agent circuit breaker open, escalating to human")
    escalate_to_human()
```

## Graceful Degradation

### Degradation Strategies

1. **Skip Non-Critical Harnesses**: Continue without optional validations
2. **Use Cached Results**: Reuse previous successful runs
3. **Manual Intervention**: Escalate to human for manual completion
4. **Simplified Workflow**: Use basic migration without advanced features

### Implementation

```python
def execute_harness_with_degradation(harness_name, params):
    """Execute harness with graceful degradation"""
    try:
        # Try normal execution
        return execute_harness(harness_name, params)
    except ServiceUnavailableError:
        # Check if harness is optional
        if is_optional_harness(harness_name):
            logger.warning(f"Skipping optional harness: {harness_name}")
            return None
        else:
            # Try cached result
            cached = get_cached_result(harness_name, params)
            if cached:
                logger.info(f"Using cached result for {harness_name}")
                return cached
            else:
                # Escalate to human
                escalate_to_human(f"Required harness {harness_name} unavailable")
                raise
```

## Agent Communication Patterns

### Synchronous Invocation

```python
def invoke_agent_sync(agent_name, params):
    """Synchronous agent invocation"""
    message = create_message(
        to=agent_name,
        type="invoke",
        payload=params
    )

    # Send message and wait for response
    response = send_message_and_wait(message, timeout=3600)

    if response["type"] == "error":
        raise AgentError(response["payload"]["error"])

    return response["payload"]
```

### Asynchronous Invocation

```python
async def invoke_agent_async(agent_name, params):
    """Asynchronous agent invocation"""
    message = create_message(
        to=agent_name,
        type="invoke",
        payload=params
    )

    # Send message without waiting
    message_id = send_message(message)

    # Register callback
    register_callback(message_id, on_agent_response)

    return message_id
```

### Parallel Invocation

```python
def invoke_agents_parallel(agents_and_params):
    """Invoke multiple agents in parallel"""
    with ThreadPoolExecutor(max_workers=len(agents_and_params)) as executor:
        futures = []
        for agent_name, params in agents_and_params:
            future = executor.submit(invoke_agent_sync, agent_name, params)
            futures.append((agent_name, future))

        results = {}
        for agent_name, future in futures:
            try:
                results[agent_name] = future.result()
            except Exception as e:
                logger.error(f"Agent {agent_name} failed: {e}")
                results[agent_name] = {"error": str(e)}

        return results
```

## Configuration

### Agent Mesh Config

```yaml
# .claude/config/agent-mesh.yaml
agent_mesh:
  # Message passing
  message_queue:
    type: file  # file, redis, rabbitmq
    path: .claude/state/messages/

  # State management
  state_persistence:
    enabled: true
    backend: file  # file, database
    checkpoint_interval: 60  # seconds

  # Retry configuration
  retry:
    max_attempts: 3
    base_delay_ms: 1000
    max_delay_ms: 30000

  # Circuit breaker
  circuit_breaker:
    enabled: true
    failure_threshold: 5
    timeout_ms: 60000
    reset_timeout_ms: 300000

  # Timeouts
  timeouts:
    agent_invocation: 3600  # seconds
    skill_execution: 600
    http_request: 30

  # Parallelism
  concurrency:
    max_concurrent_stories: 3
    max_concurrent_harnesses: 2
    thread_pool_size: 10
```

## Monitoring

### Health Checks

```python
def health_check_agents():
    """Check health of all agents"""
    agents = [
        "project-tracker-agent",
        "story-orchestrator-agent",
        "test-generator-agent",
        # ... etc
    ]

    health = {}
    for agent in agents:
        try:
            response = invoke_agent_sync(agent, {"action": "health_check"})
            health[agent] = "healthy" if response["status"] == "ok" else "unhealthy"
        except Exception as e:
            health[agent] = f"error: {e}"

    return health
```

### Metrics Collection

```python
# Track agent invocation metrics
metrics = {
    "agent_invocations_total": Counter(),
    "agent_invocation_duration_seconds": Histogram(),
    "agent_failures_total": Counter(),
    "circuit_breaker_state": Gauge(),
}

def record_agent_invocation(agent_name, duration, success):
    """Record agent invocation metrics"""
    metrics["agent_invocations_total"].inc(labels={"agent": agent_name})
    metrics["agent_invocation_duration_seconds"].observe(duration, labels={"agent": agent_name})
    if not success:
        metrics["agent_failures_total"].inc(labels={"agent": agent_name})
```

## Implementation Status

- [x] Message passing protocol defined
- [x] State management design
- [x] Retry mechanisms with exponential backoff
- [x] Circuit breaker pattern
- [x] Graceful degradation strategies
- [x] Agent communication patterns
- [x] Configuration structure
- [x] Health checks and monitoring

## References

- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Retry Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Agent Mesh Architecture](/openspec/changes/code-migration-system/specs/agent-mesh-orchestration/spec.md)
