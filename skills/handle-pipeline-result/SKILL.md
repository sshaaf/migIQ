---
name: handle-pipeline-result
trigger: /handle-pipeline-result
description: Handle CI/CD pipeline results and failures. Use when the user wants to process pipeline results, analyze build failures, handle CI/CD outcomes, or respond to pipeline events.
---

Handle pipeline success/failure

## Parameters

--pipeline-id (required), --result (required)

## Returns

Action taken (merge, retry, escalate)

## Example

```bash
/handle-pipeline-result --help
```
