---
navigation_title: Anatomy of a workflow
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for every top-level field in a workflow YAML definition, what it does, and the execution lifecycle that results.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Anatomy of a workflow [workflows-anatomy]

A workflow definition has eleven top-level fields. Most of them are optional. This page is the reference for all of them.

## The complete workflow shape [workflows-anatomy-shape]

The `inputs` field can sit at the top of the workflow or inside a `manual` trigger, depending on your version. Use the tabs to see each form.

::::{applies-switch}

:::{applies-item} stack: preview 9.3, ga 9.4
```yaml
name: slo-breach-response            # identity
description: Investigate and mitigate SLO breaches.
enabled: true                        # activation
tags:                                # for filtering and organization
  - observability
  - slo

version: "1"                         # schema version

triggers:                            # when it runs
  - type: manual

inputs:                              # runtime parameters (optional)
  - name: service_name
    type: string
    required: true

consts:                              # reusable constants (optional)
  severity_threshold: 70

outputs:                             # declared output schema (optional)
  - name: result
    type: string

settings:                            # global behavior (optional)
  timeout: "5m"
  concurrency:
    strategy: drop

steps:                               # what it does
  - name: investigate
    type: elasticsearch.esql.query
    with:
      query: "..."
```
:::

:::{applies-item} { stack: ga 9.5+, serverless: ga }
```yaml
name: slo-breach-response            # identity
description: Investigate and mitigate SLO breaches.
enabled: true                        # activation
tags:                                # for filtering and organization
  - observability
  - slo

version: "1"                         # schema version

triggers:                            # when it runs
  - type: manual
    inputs:                          # runtime parameters (optional)
      - name: service_name
        type: string
        required: true

consts:                              # reusable constants (optional)
  severity_threshold: 70

outputs:                             # declared output schema (optional)
  - name: result
    type: string

settings:                            # global behavior (optional)
  timeout: "5m"
  concurrency:
    strategy: drop

steps:                               # what it does
  - name: investigate
    type: elasticsearch.esql.query
    with:
      query: "..."
```
:::

::::

## Field reference [workflows-anatomy-fields]

| Field | Type | Required | Purpose |
|---|---|---|---|
| [`name`](#workflows-anatomy-name) | string | Yes | Unique name for the workflow. Appears in the UI and identifies the workflow programmatically. |
| [`description`](#workflows-anatomy-description) | string | No | Short description shown in the workflow list. |
| [`enabled`](#workflows-anatomy-enabled) | boolean | No | Whether the workflow is active. Defaults to `true`. Set to `false` to park a workflow without deleting it. |
| [`tags`](#workflows-anatomy-tags) | `string[]` | No | Classification tags. Used for filtering in the list UI and for organizational conventions. |
| [`version`](#workflows-anatomy-version) | string | No | Schema version. Defaults to `"1"`. The engine uses this for forward compatibility; leave it unset unless instructed otherwise. |
| [`triggers`](#workflows-anatomy-triggers) | `Trigger[]` | Yes | One or more triggers that start the workflow. Refer to [Triggers](/explore-analyze/workflows/triggers.md). |
| [`inputs`](#workflows-anatomy-inputs) | object or `Input[]` | No | Runtime parameters the workflow accepts. Values provided at invocation time become `{{ inputs.<name> }}` inside the workflow. On 9.5+, defined under the `manual` trigger. |
| [`consts`](#workflows-anatomy-consts) | object | No | Constant values reusable as `{{ consts.<name> }}`. Use for thresholds, index names, or other values you want to name. |
| [`outputs`](#workflows-anatomy-outputs) | object or `Output[]` | No | Declared output schema. Required for workflows invoked through [composition](/explore-analyze/workflows/steps/composition.md) — the parent needs to know the child's output shape. |
| [`settings`](#workflows-anatomy-settings) | object | No | Global behavior: timeout, timezone, concurrency, global error handling, output-size cap. Refer to [Workflow settings](/explore-analyze/workflows/authoring-techniques/settings.md). |
| [`steps`](#workflows-anatomy-steps) | `Step[]` | Yes | Ordered list of steps to execute. Refer to [Steps](/explore-analyze/workflows/steps.md). |

## `name` — workflow identity [workflows-anatomy-name]

`name` is what you'll type when you talk about this workflow. Pick something that reads well in a list. A common convention is `<domain>--<verb>-<noun>`:

```yaml
name: security--triage-malware-alert
name: observability--respond-to-slo-breach
name: platform--rotate-service-account-keys
```

The name must be unique within the {{kib}} space. The engine also uses it as the workflow's identifier in API calls.

## `description` — short subtitle [workflows-anatomy-description]

`description` is the short subtitle shown directly below the name in the workflow list UI. Keep it to one sentence that explains what the workflow does, not how it does it.

```yaml
description: Investigate and mitigate SLO breaches in production services.
```

## `enabled` — the kill switch [workflows-anatomy-enabled]

`enabled: false` parks the workflow without deleting it. Scheduled triggers stop firing, alert-attached workflows stop responding, and manual runs return a clear "workflow is disabled" error. Flip it back to `true` when you're ready.

Disabling is safer than deleting when you're experimenting or reworking a workflow because alerting rules that reference the workflow don't break.

## `tags` — for filtering and organization [workflows-anatomy-tags]

`tags` are the filter keys in the workflow list. Teams often tag by product area, by criticality, or by audience:

```yaml
tags:
  - security
  - prod
  - soc
```

Tags are free-form strings. Pick a convention that matches how your team navigates the workflow list. Common patterns include product-area tags (`security`, `observability`, `search`), criticality tags (`prod`, `demo`), and audience tags (`soc`, `oncall`).

## `version` — schema version [workflows-anatomy-version]

`version` declares the workflow schema version. It defaults to `"1"` and you can leave it unset. The engine uses this field for forward compatibility: if the workflow schema ever evolves in an incompatible way, older workflows can be migrated based on this field.

```yaml
version: "1"
```

Note the value is the string `"1"`, not the number `1`. Unquoted `1` is parsed as a number and the schema rejects it.

## `triggers` — when it runs [workflows-anatomy-triggers]

Every workflow needs at least one trigger. You can list several:

```yaml
triggers:
  - type: manual
  - type: scheduled
    with:
      every: "1h"
```

That workflow can be run on demand and also runs hourly automatically. Refer to [Triggers](/explore-analyze/workflows/triggers.md) for the available trigger types.

## `inputs` — runtime parameters [workflows-anatomy-inputs]

`inputs` declare values the workflow expects at invocation time. They're what the user types in the **Run** modal, or what an API caller provides in the request body.

The location of `inputs` in the YAML depends on your version. On stack 9.4 and earlier, `inputs` sits at the top level of the workflow. From stack 9.5+ and on serverless, new workflows place `inputs` inside the `manual` trigger; existing top-level workflows continue to run.

::::{applies-switch}

:::{applies-item} stack: preview 9.3, ga 9.4
```yaml
inputs:
  - name: alert_id
    type: string
    required: true
  - name: severity
    type: choice
    options: [low, medium, high, critical]
    default: medium
  - name: dry_run
    type: boolean
    default: false
```
:::

:::{applies-item} { stack: ga 9.5+, serverless: ga }
```yaml
triggers:
  - type: manual
    inputs:
      - name: alert_id
        type: string
        required: true
      - name: severity
        type: choice
        options: [low, medium, high, critical]
        default: medium
      - name: dry_run
        type: boolean
        default: false
```
:::

::::

Inside the workflow, reference them as `{{ inputs.alert_id }}` (the reference form is the same in either placement).

Supported input types are `string`, `number`, `boolean`, `choice` (with an `options` array), and `array` (with optional `minItems` and `maxItems`). `required` defaults to `false`; provide a `default` to give optional inputs a fallback value. The legacy array-of-fields form documented here is being migrated to a JSON Schema form; both are accepted today.

:::{note}
The trigger defines *when* a workflow runs. Inputs define *what values* it accepts at runtime. A manual-triggered workflow typically has explicit inputs the user fills in. An alert-triggered workflow usually has no inputs, because the alert payload arrives as `event` automatically. You can still add inputs if you need values the alert payload doesn't carry.
:::

## `consts` — named constants [workflows-anatomy-consts]

`consts` are fixed values you want to name once and reference many times.

```yaml
consts:
  watch_index: "security.watch.findings"
  threshold: 0.85
  slack_channel: "#soc-oncall"

steps:
  - name: post
    type: slack.postMessage
    with:
      channel: "{{ consts.slack_channel }}"
      text: "Threshold {{ consts.threshold }} exceeded."
```

Constants are evaluated once at workflow load. They don't have access to `inputs`, `steps`, or `event`. Use a [`data.set` step](/explore-analyze/workflows/steps/data.md#data-set) if you need a dynamic value.

## `outputs` — declared result shape [workflows-anatomy-outputs]

`outputs` describe what the workflow produces when it finishes. The canonical use case is [workflow composition](/explore-analyze/workflows/steps/composition.md) — a parent workflow that invokes this one needs to know what shape to expect back.

```yaml
outputs:
  - name: verdict
    type: string
  - name: severity
    type: number
  - name: evidence
    type: object
```

A workflow that doesn't declare outputs can still complete successfully. `outputs` is only required when the workflow is called as a child workflow through composition.

## `settings` — global behavior [workflows-anatomy-settings]

`settings` is the grab bag for workflow-wide behavior: timeout, timezone, concurrency, and global error handling.

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

Every field in `settings` is optional. The full reference with per-field semantics lives on the [Workflow settings page](/explore-analyze/workflows/authoring-techniques/settings.md).

## `steps` — the body of the workflow [workflows-anatomy-steps]

`steps` is an ordered list. Each step has a required `name` (unique within the workflow), a required `type` (the step type identifier), and a type-specific `with` block.

```yaml
steps:
  - name: fetch
    type: elasticsearch.search
    with:
      index: logs-*
      size: 100
  - name: summarize
    type: ai.summarize
    connector-id: my-openai
    with:
      input: "{{ steps.fetch.output.hits.hits | map: '_source.message' | join: '\\n' }}"
```

Every step also accepts a standard set of common fields for control flow and error handling. Refer to the [Steps overview](/explore-analyze/workflows/steps.md) for those.

## The execution lifecycle of a workflow [workflows-anatomy-lifecycle]

When you invoke a workflow — manually, on schedule, or through a trigger — the engine puts it through this lifecycle:

| State | Meaning |
|---|---|
| `pending` | The execution is queued and waiting to start. |
| `running` | At least one step is executing. |
| `waiting` | The workflow has paused on a [`wait`](/explore-analyze/workflows/steps/wait.md) step. Returns to `running` when the timer fires. |
| `waiting_for_input` | The workflow has paused on a [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md) step. Returns to `running` when the input arrives. |
| `waiting_for_child` | The workflow has paused waiting for a child workflow invoked through [`workflow.execute`](/explore-analyze/workflows/steps/composition.md) to complete. |
| `completed` | Terminal. The workflow finished successfully. |
| `failed` | Terminal. A step failed and `on-failure` did not recover. |
| `cancelled` | Terminal. The operator cancelled the run, or the concurrency strategy stopped it. |
| `timed_out` | Terminal. The workflow exceeded its `settings.timeout`. |
| `skipped` | Terminal. The concurrency `drop` strategy skipped this run because another execution was already in flight. |

Five states are terminal: `completed`, `failed`, `cancelled`, `timed_out`, and `skipped`. Every terminal execution reports its usage to the consumption metering system. Refer to the [Workflow settings page](/explore-analyze/workflows/authoring-techniques/settings.md) for how concurrency and execution metering interact.

## Related [workflows-anatomy-related]

- [Workflow settings](/explore-analyze/workflows/authoring-techniques/settings.md): The full `settings` reference.
- [Choose the right step](/explore-analyze/workflows/authoring-techniques/choose-the-right-step.md): Decision aid for picking step types.
- [Steps overview](/explore-analyze/workflows/steps.md): The step catalog.
- [Triggers overview](/explore-analyze/workflows/triggers.md): The trigger catalog.
- [Cheat sheet](/explore-analyze/workflows/reference/cheat-sheet.md): One-page bookmark reference.
