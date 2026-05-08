---
navigation_title: Context variables
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Every context variable you can reference in a Liquid expression inside a workflow, with an example for each.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Context variables [workflows-context-variables-reference]

Context variables are the data you can reference inside [Liquid expressions](/explore-analyze/workflows/templating.md) in a workflow. Every execution gets the same core set. Some variables are only populated in certain contexts (for example, `foreach.item` exists only inside a `foreach` loop).

This page is the canonical reference. For the mental model and the `{{ }}` vs. `${{ }}` distinction, refer to [Templating engine](/explore-analyze/workflows/templating.md).

## Core variables [workflows-ctx-core]

### `inputs.<name>` [workflows-ctx-inputs]

Values provided at workflow invocation time. Declared in the workflow's top-level `inputs` block.

```yaml
inputs:
  - name: service_name
    type: string
    required: true

steps:
  - name: search
    type: elasticsearch.esql.query
    with:
      query: "FROM logs-* | WHERE service.name == \"{{ inputs.service_name }}\""
```

### `consts.<name>` [workflows-ctx-consts]

Constants declared at the top of the workflow. Evaluated once at workflow load. They can't reference other context (no `inputs`, no `steps`).

```yaml
consts:
  threshold: 70
  slack_channel: "#soc-oncall"

steps:
  - name: notify
    type: slack.postMessage
    with:
      channel: "{{ consts.slack_channel }}"
      text: "Threshold {{ consts.threshold }} exceeded."
```

### `steps.<name>.output` [workflows-ctx-step-output]

The output produced by a previous step. Shape depends on the step type. Refer to each step's reference for what it returns.

```yaml
steps:
  - name: search
    type: elasticsearch.search
    with: { index: "logs-*", size: 1 }

  - name: summarize
    type: console
    with:
      message: "First hit: {{ steps.search.output.hits.hits[0]._id }}"
```

### `steps.<name>.error` [workflows-ctx-step-error]

Error details if the step failed and its `on-failure: continue` caught the error. `null` if the step succeeded. Refer to [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md#workflows-on-failure-continue) for the `continue` strategy.

```yaml
- name: flaky_call
  type: http
  on-failure:
    continue: true
  with: { url: "https://flaky.example" }

- name: handle
  type: if
  condition: "steps.flaky_call.error : null"
  steps: [ ... ]     # success path
  else:  [ ... ]     # failure path (steps.flaky_call.error has detail)
```

## Trigger-provided variables [workflows-ctx-trigger]

### `event.*` [workflows-ctx-event]

The trigger payload. Shape depends on the trigger type:

| Trigger | `event.*` structure |
|---|---|
| `manual` | `{}` (empty — use `inputs.*` instead) |
| `scheduled` | `{}` (empty) |
| `alert` | `event.alerts` (array of alert documents), `event.rule` (rule metadata), `event.spaceId`, `event.params.*` (params from the rule's action configuration) |
| `workflows.failed` | `event.spaceId`, `event.timestamp`, `event.workflow.{id, name, spaceId, isErrorHandler}`, `event.execution.{id, startedAt, failedAt}`, `event.error.{message, stepId, stepName, stepExecutionId}` |

For the full `workflows.failed` payload, refer to [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md).

Alert trigger example:

```yaml
- name: log
  type: console
  with:
    message: |
      Got {{ event.alerts | size }} alerts from rule "{{ event.rule.name }}".
      First host: {{ event.alerts[0].host.name }}
```

### `execution.*` [workflows-ctx-execution]

Metadata about the current workflow execution.

| Field | Contains |
|---|---|
| `execution.id` | Execution ID. |
| `execution.startedAt` | ISO timestamp of start. |
| `execution.isTestRun` | `true` if run from the editor's **Test** button. |
| `execution.executedBy` | UID of the user or system that invoked the workflow. |
| `execution.triggeredBy` | Which trigger initiated this execution (`manual`, `scheduled`, `alert`, `workflows.failed`). |
| `execution.url` | Deep link to the execution view in {{kib}}. |
| `execution.compositionDepth` | 0 for a top-level invocation. Increments by 1 for each [`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute) level. |
| `execution.parentWorkflowId` | ID of the parent workflow, if this is a composed child execution. |

```yaml
- name: link
  type: console
  with:
    message: "View this execution: {{ execution.url }}"
```

### `workflow.*` [workflows-ctx-workflow]

Metadata about the workflow itself, not the execution.

| Field | Contains |
|---|---|
| `workflow.id` | Workflow ID. |
| `workflow.name` | Workflow name. |
| `workflow.enabled` | `true` or `false`. |
| `workflow.spaceId` | The {{kib}} space ID. |

```yaml
- name: audit
  type: elasticsearch.index
  with:
    index: "workflow-audit"
    document:
      workflow_id:   "{{ workflow.id }}"
      workflow_name: "{{ workflow.name }}"
      space_id:      "{{ workflow.spaceId }}"
      execution_id:  "{{ execution.id }}"
```

## Loop-local variables [workflows-ctx-loops]

### `foreach.*` [workflows-ctx-foreach]

Available inside a [`foreach`](/explore-analyze/workflows/steps/foreach.md) loop body.

| Field | Contains |
|---|---|
| `foreach.item` | Current iteration's element. |
| `foreach.index` | Zero-based iteration index. |
| `foreach.total` | Total items in the array. |
| `foreach.items` | The full array being iterated. |

```yaml
- name: process
  foreach: "${{ event.alerts }}"
  steps:
    - name: log
      type: console
      with:
        message: "[{{ foreach.index }}/{{ foreach.total }}] {{ foreach.item._id }}"
```

### `while.iteration` [workflows-ctx-while]

Available inside a [`while`](/explore-analyze/workflows/steps/while.md) loop body. Zero-based iteration counter.

```yaml
- name: poll
  type: while
  condition: "steps.check.output.status : 'pending'"
  max-iterations: 30
  steps:
    - name: log
      type: console
      with: { message: "Attempt {{ while.iteration }}" }
    - name: check
      type: elasticsearch.search
      with: { index: "jobs", size: 1 }
    - name: wait
      type: wait
      with: { duration: "2s" }
```

## User-defined variables [workflows-ctx-variables]

### `variables.<name>` [workflows-ctx-data-set]

Variables set by one or more [`data.set`](/explore-analyze/workflows/steps/data.md#data-set) steps. Global within the workflow execution. Later `data.set` steps can overwrite earlier values.

```yaml
- name: init
  type: data.set
  with:
    service: "checkout"
    region: "us-east"

- name: query
  type: elasticsearch.esql.query
  with:
    query: "FROM logs-{{ variables.region }}-* | WHERE service.name == \"{{ variables.service }}\""
```

## Standard helpers [workflows-ctx-helpers]

### `now` [workflows-ctx-now]

Current timestamp as an ISO 8601 string. Evaluated per reference, so repeated uses in the same expression will match.

```yaml
- name: index_row
  type: elasticsearch.index
  with:
    index: "events"
    document:
      at: "{{ now }}"
      formatted: "{{ now | date: '%Y-%m-%d %H:%M' }}"
```

### `kibanaUrl` [workflows-ctx-kibanaurl]

Base URL of the {{kib}} instance. Useful for building deep links in notifications.

```yaml
- name: notify
  type: slack.postMessage
  with:
    channel: "#soc"
    text: |
      Case created: <{{ kibanaUrl }}/app/security/cases/{{ steps.create_case.output.id }}|Open in {{kib}}>
```

## Related [workflows-ctx-related]

- [Templating engine](/explore-analyze/workflows/templating.md): How Liquid expressions evaluate these variables.
- [Liquid filters](/explore-analyze/workflows/reference/liquid-filters.md): Transformations you can apply to any variable.
- [Cheat sheet](/explore-analyze/workflows/reference/cheat-sheet.md): The condensed version of this table.
- [Steps overview](/explore-analyze/workflows/steps.md): Each step's reference documents what its `output` contains.

% Ben Ironside Goldstein, 2026-04-16: PM source claimed `event.step.*` for workflows.failed payload.
% PR A verified against Kibana source: the correct shape is `event.error.{message, stepId, stepName, stepExecutionId}`.
% Following PR A here. Flagged in PR summary for SME confirmation.
