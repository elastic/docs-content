---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about the wait step for adding delays in workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Wait

The `wait` step pauses workflow execution for a specified duration before continuing to the next step.

Use the following parameters to configure a `wait` step:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Unique step identifier |
| `type` | Yes | Step type - must be `wait` |
| `with.duration` | Yes | Duration to wait before continuing (for example, `"5s"`) |

```yaml
steps:
  - name: waitStep
    type: wait
    with:
      duration: "5s"
```

## Duration format

The supported units are:

* Weeks: `w`
* Days: `d`
* Hours: `h`
* Minutes: `m`
* Seconds: `s`
* Milliseconds: `ms`

Duration strings must follow the following format rules:

* Units must be in descending order: `1w2d3h4m5s6ms`
* Each unit can only appear once
* No spaces between number and unit
* Positive integer values only (no decimals, commas, negative values, or zero)

```yaml
duration: "1w"
duration: "2d12h"
duration: "1d"
duration: "1h30m"
duration: "1h"
duration: "5m30s"
duration: "2m"
duration: "30s"
duration: "2s500ms"
duration: "500ms"
duration: "1w3d5h20m10s"
```

## Examples

Wait for 10 seconds:

```yaml
steps:
  - name: delay
    type: wait
    with:
      duration: "10s"
```

Wait for one minute after the API call completes:

```yaml
steps:
  - name: api-call
    type: http
    on-failure:
      retry:
        max-attempts: 3
        delay: "5s"

  - name: wait-before-next
    type: wait
    with:
      duration: "1m"
```

Wait for one day:

```yaml
steps:
  - name: wait-one-day
    type: wait
    with:
      duration: "1d"
```
