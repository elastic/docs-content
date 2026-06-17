---
navigation_title: Workflow settings
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for workflow-wide settings. Timeout, timezone, concurrency, max step size, and global on-failure.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Workflow settings [workflows-settings]

The top-level `settings` block configures workflow-wide behavior. Every field is optional. Use only what you need.

## Fields [workflows-settings-fields]

| Field | Type | Purpose |
|---|---|---|
| `timeout` | duration | Maximum execution duration for the entire workflow. Format as `5s`, `10m`, `2h`. |
| `timezone` | IANA string | Timezone name (for example `America/New_York`). Used by scheduled triggers and date formatting. |
| `concurrency` | object | Controls what happens when a new execution starts while one is already running. Refer to [Concurrency control](#workflows-settings-concurrency). |
| `max-step-size` | byte size | Cap on per-step output size (for example `10mb`). |
| `on-failure` | object | Global failure handling applied to every step. Same shape as per-step `on-failure`. Refer to [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md). |

Fields not set take the engine defaults.

## Which setting do I need? [workflows-settings-which]

| If you want to… | Set |
|---|---|
| Stop long-running workflows from running forever | `timeout` |
| Control which timezone a scheduled trigger interprets | `timezone` |
| Prevent overlapping runs from colliding on shared state | `concurrency` |
| Keep a single step from producing 100 MB of output that bogs down the UI | `max-step-size` |
| Apply a default retry policy to every step | `on-failure` |

## `timeout` [workflows-settings-timeout]

Caps the wall-clock duration of the entire execution. If the workflow hasn't reached a terminal state by the deadline, the execution is cancelled.

```yaml
settings:
  timeout: "30m"
```

A few things to know:

- The timeout clock starts at the first step and includes [`wait`](/explore-analyze/workflows/steps/wait.md) steps and [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md) pauses.
- If a step is still running when the timeout fires, it receives a cancel signal. Steps that honor cancellation promptly (most HTTP and {{es}} steps) will stop; others may finish briefly after.
- For human-in-the-loop workflows that need to wait indefinitely, either leave `timeout` unset or set it generously (for example `7d`).

## `timezone` [workflows-settings-timezone]

Sets the default IANA timezone for the workflow. Affects:

- **Scheduled triggers.** If a scheduled trigger's `rrule` doesn't specify a `tzid`, `settings.timezone` is used.
- **Date formatting in Liquid.** The `date` filter interprets relative times (`now`, `now-1h`) against this timezone.

```yaml
settings:
  timezone: "America/Los_Angeles"
```

If both `settings.timezone` and `rrule.tzid` are set, `rrule.tzid` wins for that trigger.

## `max-step-size` [workflows-settings-max-step-size]

Puts a ceiling on the size of any one step's output. Defaults apply at the deployment level; set this to override globally for this workflow.

```yaml
settings:
  max-step-size: "25mb"
```

Steps that produce outputs exceeding this limit fail with a clear error. Useful to catch runaway {{es}} queries before they push the whole execution past the deployment limit.

## Concurrency control [workflows-settings-concurrency]

Use `settings.concurrency` to prevent overlapping executions from colliding. This is important for:

- Noisy detection rules that might fire many alerts in a burst.
- Workflows that mutate shared state (create or update a case, write a counter).
- Scheduled workflows whose runtime can exceed the schedule interval.

### Fields [workflows-settings-concurrency-fields]

| Field | Type | Purpose |
|---|---|---|
| `key` | Liquid string | Expression that resolves to a group identifier. Executions with the same key belong to the same concurrency group. |
| `strategy` | string | `cancel-in-progress` (cancel the currently running execution when a new one arrives) or `drop` (the new execution is skipped). |
| `max` | number | Maximum concurrent executions per group. |

### Serialize per host [workflows-settings-concurrency-per-host]

The most common use case is "per host, only one execution at a time": group by host, drop new executions when one is already running.

```yaml
settings:
  concurrency:
    key: "{{ event.alerts[0].host.name }}"
    strategy: drop
    max: 1
```

When two alerts fire on the same host within seconds, the first workflow runs; the second goes straight to the `skipped` terminal state.

:::{warning}
Concurrency keys that use `event.*` are alert-specific. `event.alerts[0].host.name` is only populated when an [alert trigger](/explore-analyze/workflows/triggers/alert-triggers.md) fires. If the same workflow is ever invoked by a manual or scheduled trigger, the key evaluates to the empty string and all executions share one group. For workflows that mix trigger types, prefer a key derived from an input (`{{ inputs.host_name }}`) or a static key (`"my-workflow"`).
:::

### Cancel in-progress runs for scheduled health checks [workflows-settings-concurrency-cancel]

A health-check workflow runs every 5 minutes but occasionally takes longer. You want the newest status, not a backlog:

```yaml
settings:
  concurrency:
    key: "health-check"
    strategy: cancel-in-progress
    max: 1
```

When the new execution arrives, the old one is cancelled and the new one starts.

### Choosing `drop` versus `cancel-in-progress` [workflows-settings-concurrency-choose]

| Use | When |
|---|---|
| `drop` | The ongoing execution is doing valid work you don't want to interrupt. The new trigger would have done the same thing anyway. |
| `cancel-in-progress` | The new trigger carries fresher information than the ongoing one. You'd rather have the new one complete than the old one. |

## Complete settings example [workflows-settings-full-example]

```yaml
settings:
  timeout: "10m"
  timezone: "America/Los_Angeles"
  max-step-size: "10mb"
  concurrency:
    key: "{{ event.alerts[0].host.name }}"
    strategy: drop
    max: 1
  on-failure:
    retry:
      max-attempts: 2
      delay: "10s"
```

## Related [workflows-settings-related]

- [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md): How `settings` fits among the other top-level fields.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): Per-step and workflow-level `on-failure`.
- [Scheduled triggers](/explore-analyze/workflows/triggers/scheduled-triggers.md): How `timezone` interacts with scheduled triggers.
