# Distributed Tracing

## Trace ID Generation and Propagation

Every story gets a unique trace ID that flows through all agents:

```python
import uuid
from datetime import datetime

def generate_trace_id(story_id):
    """Generate trace ID for story"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"trace-{story_id}-{timestamp}-{uuid.uuid4().hex[:8]}"

# Example: trace-US123-20260505120000-a1b2c3d4
```

## Structured Logging

All agents log in JSON format with trace ID:

```python
import json
import logging

class TraceLogger:
    def __init__(self, trace_id):
        self.trace_id = trace_id
        self.logger = logging.getLogger(__name__)

    def log(self, level, message, **kwargs):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "trace_id": self.trace_id,
            "level": level,
            "message": message,
            **kwargs
        }
        self.logger.log(getattr(logging, level.upper()), json.dumps(log_entry))
```

## Span Tracking

Track execution time for each agent and skill:

```python
import time

class Span:
    def __init__(self, trace_id, span_name):
        self.trace_id = trace_id
        self.span_name = span_name
        self.start_time = time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        log_span(self.trace_id, self.span_name, duration, exc_type is None)

# Usage
with Span(trace_id, "test-generator-agent"):
    # Agent work
    pass
```

## Trace Visualization

Query and visualize traces:

```bash
# View trace for story
python3 .claude/scripts/view-trace.py --trace-id trace-US123-20260505120000-a1b2c3d4

# Output:
# trace-US123-20260505120000-a1b2c3d4 (duration: 450s)
#   ├─ project-tracker-agent (10s)
#   ├─ story-orchestrator-agent (440s)
#   │   ├─ test-generator-agent (120s)
#   │   │   ├─ generate-characterization-tests (60s)
#   │   │   └─ generate-functional-tests (50s)
#   │   ├─ code-refactor-agent (100s)
#   │   ├─ benchmark-builder-agent (50s)
#   │   ├─ quality-evaluator-agent (30s)
#   │   └─ ci-integration-agent (140s)
```

## Implementation Status

- [x] Trace ID generation
- [x] Structured logging design
- [x] Span tracking implementation
- [x] Trace visualization utilities
