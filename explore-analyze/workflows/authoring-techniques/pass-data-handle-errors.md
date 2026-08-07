---
navigation_title: Pass data and handle errors
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Pass data between workflow steps with templating, reference inputs and constants, and handle step failures with retries, fallbacks, continue, and a cross-workflow error handler.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Pass data and handle errors [workflows-data]

A key feature of workflows is the ability to pass data between steps and handle failures gracefully. This page explains the mechanisms for controlling data flow and building resilient, fault-tolerant automations.

For definitions of the terms used on this page, refer to the [Glossary](/explore-analyze/workflows/reference/glossary.md).

## Data flow [workflows-data-flow]

Every step in a workflow produces an output. By default, this output is added to a global `steps` object in the workflow's context, making it available to all subsequent steps.

### Access step outputs [workflows-access-outputs]

Use the following syntax to access the output of a specific step:

```text
steps.<step_name>.output
```

You can also access error information from a step:

```text
steps.<step_name>.error
```

### Example: Chain steps to move output data [workflows-chain-steps-example]

This example demonstrates a common pattern: searching for data in one step and using the results in a later step. In this case, the workflow searches for a specific user's full name, then uses it to create a new security case.

```yaml
name: Create case for a specific user
steps:
  - name: find_user_by_id
    type: elasticsearch.search
    with:
      index: "my-user-index"
      query:
        term:
          user.id: "u-123"

  - name: create_case_for_user
    type: cases.createCase
    with:
      title: "Investigate user u-123"
      description: "A case has been opened for user {{ steps.find_user_by_id.output.hits.hits[0]._source.user.fullName }}."
      owner: "securitySolution"
      tags: ["user-investigation"]
```

In this example:

1. The `find_user_by_id` step searches an index for a document.
2. The `create_case_for_user` step uses the output of the first step to enrich a new [{{elastic-sec}} case](/solutions/security/investigate/security-cases.md).
3. The `description` field accesses `steps.find_user_by_id.output.hits.hits[0]._source.user.fullName` to dynamically include the user's full name in the case description.

## Error handling [workflows-error-handling]

By default, if any step fails the entire workflow execution stops immediately (the `abort` behavior). Override this with the `on-failure` block, which supports retry logic, fallback steps, and continuation. For failures that cross workflow boundaries, the [`workflows.failed` trigger](/explore-analyze/workflows/triggers/event-driven-triggers.md) lets a separate handler workflow react after another workflow has failed.

### Three layers of error handling [workflows-error-layers]

| Layer | What it controls | Use for |
|---|---|---|
| **Per-step** `on-failure` | What happens when one step fails. | Retry transient failures, continue past non-critical steps, or provide a fallback. |
| **Workflow-level** `settings.on-failure` | Default `on-failure` applied to every step. Refer to [Workflow settings](/explore-analyze/workflows/authoring-techniques/settings.md). | A consistent global retry policy. |
| **Cross-workflow** [`workflows.failed` trigger](/explore-analyze/workflows/triggers/event-driven-triggers.md) | A separate handler workflow that runs after another workflow has failed. | Paging on-call, opening cases, central error reporting. |

### Configuration levels [workflows-on-failure-levels]

You can configure `on-failure` at two levels:

**Step-level** — Applies to a specific step:

```yaml
steps:
  - name: api-call
    type: http
    on-failure:
      retry:
        max-attempts: 3
        delay: "5s"
```

**Workflow-level** (configured under `settings`) — Applies to all steps as the default error handling behavior:

```yaml
settings:
  on-failure:
    retry:
      max-attempts: 2
      delay: "1s"
steps:
  - name: api-call
    type: http
```

Precedence: per-step `on-failure` > workflow-level `settings.on-failure` > engine default (`abort`).

:::{note}
Step-level `on-failure` configuration always overrides workflow-level settings.
:::

### Retry [workflows-on-failure-retry]

Retries the failed step a configurable number of times. The full shape accepts backoff strategy, maximum delay, jitter, and a KQL condition so you only retry on specific errors.

```yaml
on-failure:
  retry:
    max-attempts: 5           # Total attempts, including the first. Required, minimum 1.
    delay: "1s"               # Base delay between attempts. Duration format, for example "5s", "1m".
    strategy: exponential     # "fixed" (default) or "exponential".
    multiplier: 2             # Only used with strategy: exponential.
    max-delay: "30s"          # Ceiling on the delay between retries.
    jitter: true              # Add randomness to avoid thundering-herd retry storms.
    condition: "steps.self.error.status : 429"   # Optional KQL predicate over steps.self.error.
```

`condition` is a KQL expression evaluated against `steps.self.error`. Use it to retry only on specific failure modes: for example, retry on HTTP 429s and 5xxs but not on 4xx client errors.

The workflow fails when all retries are exhausted, unless paired with `fallback` or `continue`.

### Fallback [workflows-on-failure-fallback]

Runs alternative steps after the primary step fails and all retries are exhausted. In the following example, when the `delete_critical_document` step fails, the workflow runs two additional steps: one sends a Slack notification to devops-alerts using `{{workflow.name}}`, while the other logs the error details from the failed step using `{{steps.delete_critical_document.error.message}}`. The `error` object also exposes other fields, such as `error.status` for HTTP-style failures; reference a specific field rather than the whole object, which renders as `[object Object]`.

```yaml
on-failure:
  fallback:
    - name: notify_on_failure
      type: slack
      connector-id: "devops-alerts"
      with:
        message: "Failed to delete document in workflow '{{workflow.name}}'"
    - name: log_failure
      type: console
      with:
        message: "Document deletion failed, error: {{steps.delete_critical_document.error.message}}"
```

Within fallback steps, access the failed primary step's error object at `steps.<failed_step_name>.error` and reference its fields (`message`, `status`, and others) rather than the object itself.

### Continue [workflows-on-failure-continue]

Continues workflow execution even if a step fails. The failure is recorded at `steps.<name>.error`, but the workflow moves on to the next step. Use this for non-critical steps whose failure shouldn't take down the whole workflow.

```yaml
on-failure:
  continue: true
```

### Abort [workflows-on-failure-abort]

Stops the workflow. This is the default when no `on-failure` is configured, so you rarely need to write it explicitly. Use `abort` when a downstream step depends on this step's output and continuing makes no sense.

### Combining options [workflows-on-failure-combining]

You can combine multiple failure-handling options. They are processed in this order: retry → fallback → continue.

In the following example:
1. The step retries up to 2 times with a 1-second delay.
2. If all retries fail, the fallback steps run.
3. The workflow continues regardless of the outcome.

```yaml
- name: create_ticket
  type: jira
  connector-id: "my-jira-project"
  with:
    projectKey: "PROJ"
    summary: "New issue from workflow"
  on-failure:
    retry:
      max-attempts: 2
      delay: "1s"
    fallback:
      - name: notify_jira_failure
        type: slack
        connector-id: "devops-alerts"
        with:
          message: "Warning: Failed to create ticket. Continuing workflow."
    continue: true
```

### Restrictions [workflows-on-failure-restrictions]

- The `if` step cannot have an `on-failure` configuration. (`foreach` and `while` loops do support loop-level `on-failure`; see their step references.)
- Fallback steps run only after all retries have been exhausted.
- When combined, failure-handling options are processed in this order: retry → fallback → continue.
- For `foreach` and `while` loops, use `iteration-on-failure` when you want to handle one failed iteration without failing the whole loop.

### Handle failures across workflows [workflows-cross-workflow-handler]

For production-critical workflows, the final layer is a separate handler workflow that fires when another workflow fails. The [`workflows.failed` trigger](/explore-analyze/workflows/triggers/event-driven-triggers.md) fires after a workflow execution reaches the `failed` terminal state, so you can build handlers that page on-call, open a case, or post to a dedicated index for workflow-failure observability. Refer to [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md) for the trigger reference and examples.

### Choose the right error-handling layer [workflows-error-layer-decision]

| Problem | Use |
|---|---|
| "This API is flaky and should retry automatically." | Per-step `on-failure: retry`. |
| "Every step in this workflow should get 2 retries by default." | Workflow-level `settings.on-failure: retry`. |
| "This step is nice-to-have, so don't fail the workflow if it dies." | Per-step `on-failure: continue`. |
| "Try the primary API, and if it fails, use the backup API." | Per-step `on-failure: fallback`. |
| "When a production workflow fails, page on-call and open a case." | A separate [`workflows.failed` handler workflow](/explore-analyze/workflows/triggers/event-driven-triggers.md). |
| "This workflow is critical and I want monitoring on its failure rate." | `workflows.failed` handler that writes to an index, plus your existing observability stack. |

## Dynamic values with templating [workflows-dynamic-values]

Workflows support dynamic values through template variables and template expressions.

- **Template variables**: The data you reference, such as step outputs (`steps.<name>.output`), constants (`consts.<name>`), inputs (`inputs.<name>`), and context variables (`execution.id`, `event`).
- **Template expressions**: The syntax used to insert variables. Use `{{ }}` for string output or `${{ }}` to preserve data types like arrays and objects.

### Template variables [workflows-template-variables]

Template variables are the data sources you can reference inside template expressions. The most common ones:

- `inputs.<name>` — values provided when the workflow was invoked.
- `consts.<name>` — constants declared at the top of the workflow.
- `steps.<name>.output` — output of a previous step.
- `steps.<name>.error` — error from a failed step (when paired with `on-failure: continue`).
- `event.*` — the trigger payload.
- `execution.*` — metadata about the current execution.
- `foreach.item`, `foreach.index`, `foreach.total` — loop context inside a `foreach` step.

For the full canonical reference with every variable and an example per entry, refer to [Context variables](/explore-analyze/workflows/reference/context-variables.md).

#### Choose between constants and inputs [workflows-constants-or-inputs]

Constants and inputs are both template variables that let you define reusable values in your workflow, but they serve different purposes:

- **Constants** — Use for values that are fixed for the workflow definition and don't change between runs, such as index names, API endpoints, and threshold values.
- **Inputs** — Use for values that might vary each time the workflow runs, such as user-provided parameters, environment toggles, or any value that changes per execution.

### Template expressions [workflows-template-expressions]

Use template expressions to insert template variables into your workflow. The templating engine supports two syntax options:

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ }}` | Insert values as strings | `"Hello, {{user.name}}"` |
| `${{ }}` | Preserve data types (arrays, objects, numbers) | `${{steps.search.output.hits}}` |

For syntax details and examples, refer to [Templating engine](/explore-analyze/workflows/templating.md).

## Quick reference [workflows-data-quick-reference]

By combining data flow, templating, and robust error handling, you can build complex, reliable automations that react to dynamic conditions and recover from unexpected failures.

| Action | Syntax | Description |
|---------|--------|-------------|
| Step output | `steps.<step_name>.output` | Access the result of a previous step. |
| Step error | `steps.<step_name>.error` | Access error details from a failed step. |
| Constants | `consts.<constant_name>` | Access workflow-level constants. |
| Inputs | `inputs.<input_name>` | Access parameters passed at trigger time. |
| Execution metadata | `execution.id`, `execution.startedAt` | Access information about the current run. |
| Trigger data | `event` | Access data from the trigger that started the workflow. |
| Retry on failure | `on-failure.retry` | Retry a failed step with optional delay. |
| Fallback steps | `on-failure.fallback` | Define recovery actions when a step fails. |
| Continue on failure | `on-failure.continue: true` | Allow the workflow to proceed after a failure. |