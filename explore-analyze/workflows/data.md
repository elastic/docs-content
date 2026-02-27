---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how data flows through workflows, use dynamic templating, and handle errors gracefully.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Data and error handling [workflows-data]

A key feature of workflows is the ability to pass data between steps and handle failures gracefully. This page explains the mechanisms for controlling data flow and building resilient, fault-tolerant automations.

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
    type: kibana.createCaseDefaultSpace
    with:
      title: "Investigate user u-123"
      description: "A case has been opened for user {{steps.find_user_by_id.output.hits.hits[0]._source.user.fullName}}."
      tags: ["user-investigation"]
      connector:
        id: "none"
        name: "none"
        type: ".none"
```

In this example:

1. The `find_user_by_id` step searches an index for a document.
2. The `create_case_for_user` step uses the output of the first step to enrich a new [{{elastic-sec}} case](../../solutions/security/investigate/cases.md).
3. The `description` field accesses `steps.find_user_by_id.output.hits.hits[0]._source.user.fullName` to dynamically include the user's full name in the case description.

## Error handling [workflows-error-handling]

By default, if any step in a workflow fails, the entire workflow execution stops immediately. You can override this behavior using the `on-failure` block, which supports retry logic, fallback steps, and continuation options.

### Configuration levels [workflows-on-failure-levels]

You can configure `on-failure` at two levels:

**Step-level** — applies to a specific step:

```yaml
steps:
  - name: api-call
    type: http
    on-failure:
      retry:
        max-attempts: 3
        delay: "5s"
```

**Workflow-level** (configured under `settings`) - applies to all steps as the default error handling behavior:

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

:::{note}
Step-level `on-failure` configuration always overrides workflow-level settings.
:::

### Retry [workflows-on-failure-retry]

Retries the failed step a configurable number of times, with an optional delay between attempts.

```yaml
on-failure:
  retry:
    max-attempts: 3  # Required, minimum 1 (for example, "1", "2", "5")
    delay: "5s"      # Optional, duration format (for example, "5s", "1m", "2h")
```

The workflow fails when all retries are exhausted.

### Fallback [workflows-on-failure-fallback]

Executes alternative steps after the primary step fails and all retries are exhausted. In the following example, when the `delete_critical_document` step fails, the workflow executes two additional steps: one sends a Slack notification to devops-alerts using `{{workflow.name}}`, while the other logs the error details from the failed step using `{{steps.delete_critical_document.error}}`.

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
        message: "Document deletion failed, error: {{steps.delete_critical_document.error}}"
```

Within fallback steps, access error information from the failed primary step using `steps.<failed_step_name>.error`.

### Continue [workflows-on-failure-continue]

Continues workflow execution even if a step fails. The failure is recorded, but does not interrupt the workflow.

```yaml
on-failure:
  continue: true
```

### Combining options [workflows-on-failure-combining]

You can combine multiple failure-handling options. They are processed in this order: retry → fallback → continue.

In the following example:
1. The step retries up to 2 times with a 1-second delay.
2. If all retries fail, the fallback steps execute.
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

- Flow-control steps (`if`, `foreach`) cannot have workflow-level `on-failure` configurations.
- Fallback steps execute only after all retries have been exhausted.
- When combined, failure-handling options are processed in this order: retry → fallback → continue.

## Dynamic values with templating [workflows-dynamic-values]

Workflows support dynamic values through template variables and template expressions.

- **Template variables**: The data you reference, such as step outputs (`steps.<name>.output`), constants (`consts.<name>`), inputs (`inputs.<name>`), and context variables (`execution.id`, `event`).
- **Template expressions**: The syntax used to insert variables. Use `{{ }}` for string output or `${{ }}` to preserve data types like arrays and objects.

### Template variables [workflows-template-variables]

Template variables are the data sources you can reference inside template expressions. The following template variables are available:

| Variable type | Syntax | Description |
|---------------|--------|-------------|
| Step outputs | `steps.<step_name>.output` | Data produced by each step during execution. Access results from previous steps to chain operations together. Refer to [Reference outputs](./data/templating.md#workflows-ref-step-outputs) for more details. |
| Constants | `consts.<constant_name>` | Reusable values defined once at the workflow level using the `consts` block. Refer to [Reference constants](./data/templating.md#workflows-ref-constants) for more details. |
| Inputs | `inputs.<input_name>` | Parameters defined in the `inputs` block that can be provided when the workflow is triggered. Refer to [Reference inputs](./data/templating.md#workflows-ref-inputs) for more details. |
| Context variables | `execution.id`, `event`, `foreach.item` | Data automatically provided by the workflow engine at runtime, including execution metadata, trigger data, and loop state. Refer to [Context variables reference](./data/templating.md#workflows-context-variables) for more details. |

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

For syntax details and examples, refer to [Templating engine](./data/templating.md).

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