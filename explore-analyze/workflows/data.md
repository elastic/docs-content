---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how data flows through workflows, use dynamic templating, and handle errors gracefully.
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

### Example: Chain steps with data [workflows-chain-steps-example]

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
2. The `create_case_for_user` step uses the output of the first step to enrich a new case.
3. The `description` field accesses `steps.find_user_by_id.output.hits.hits[0]._source.user.fullName` to dynamically include the user's full name.

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

**Workflow-level** — applies to all steps as a default (under `settings`):

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

The workflow fails if all retries are exhausted.

### Fallback [workflows-on-failure-fallback]

Executes alternative steps after the primary step fails and all retries (if configured) are exhausted.

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

Within fallback steps, access error information from the failed step using `steps.<failed_step_name>.error`.

### Continue [workflows-on-failure-continue]

Continues workflow execution even if a step fails. The failure is recorded, but does not interrupt the workflow.

```yaml
on-failure:
  continue: true
```

### Combining options [workflows-on-failure-combining]

You can combine multiple failure-handling options. They are processed in this order: retry → fallback → continue.

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

In this example:
1. The step retries up to 2 times with a 1-second delay.
2. If all retries fail, the fallback steps execute.
3. The workflow continues regardless of the outcome.

### Restrictions [workflows-on-failure-restrictions]

- Flow-control steps (`if`, `foreach`) cannot have workflow-level `on-failure` configurations.
- Fallback steps execute only after all retries have been exhausted.

## Dynamic values with templating [workflows-dynamic-values]

To inject dynamic values into your workflow steps, use the templating engine. The templating engine uses the [Liquid templating language](https://liquidjs.com/) and allows you to:

- **Reference step outputs**: Access data from previous steps using `steps.<step_name>.output`.
- **Use constants**: Reference workflow-level constants with `consts.<constant_name>`.
- **Apply filters**: Transform values with filters like `upcase`, `downcase`, and `date`.
- **Add conditional logic**: Use `if`/`else` statements for dynamic content.
- **Loop through data**: Iterate over arrays with `for` loops.

For complete syntax details and examples, refer to [Templating engine](./data/templating.md).

## Quick reference [workflows-data-quick-reference]

By combining data flow, templating, and robust error handling, you can build complex, reliable automations that react to dynamic conditions and recover from unexpected failures.

| Action | Syntax | Description |
|---------|--------|-------------|
| Step output | `steps.<step_name>.output` | Access the result of a previous step. |
| Step error | `steps.<step_name>.error` | Access error details from a failed step. |
| Retry on failure | `on-failure.retry` | Retry a failed step with optional delay. |
| Fallback steps | `on-failure.fallback` | Define recovery actions when a step fails. |
| Continue on failure | `on-failure.continue: true` | Allow the workflow to proceed after a failure. |