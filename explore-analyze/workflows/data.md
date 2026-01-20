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

This workflow demonstrates a common pattern: searching for data in one step and using the results in a later step.

```yaml
name: Create Case for a Specific User
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

By default, if any step in a workflow fails, the entire workflow execution stops immediately. You can override this behavior and define custom error handling logic using the `on-failure` block.

### The `on-failure` block [workflows-on-failure]

The `on-failure` block is a special property you can add to any step. It contains a `fallback` array of steps that execute only if the primary step fails.

```yaml
steps:
  - name: risky_operation
    type: elasticsearch.search
    with:
      index: "non-existent-index"
      query:
        match_all: {}
    on-failure:
      fallback:
        - name: log_error
          type: console
          with:
            message: "Operation failed, using fallback"
        - name: default_response
          type: http
          with:
            method: GET
            url: "https://api.example.com/default"
```

Within the `on-failure.fallback` steps, you can access error information from the failed step using:

```text
steps.<failed_step_name>.error
```

### Example: Handle {{es}} failures [workflows-handle-es-failures]

This workflow attempts to delete a document. If the `elasticsearch.delete` action fails, the `on-failure` block executes alternative steps:

```yaml
- name: delete_critical_document
  type: elasticsearch.delete
  with:
    index: "my-critical-index"
    id: "doc-abc-123"
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

### Example: Continue after failure [workflows-continue-after-failure]

Sometimes a failure is not critical and you want the workflow to continue. Set `continue: true` in the `on-failure` block to allow the workflow to proceed after handling the error:

```yaml
- name: create_ticket
  type: jira
  connector-id: "my-jira-project"
  with:
    projectKey: "PROJ"
    summary: "New issue from workflow"
  on-failure:
    continue: true
    fallback:
      - name: notify_jira_failure
        type: slack
        connector-id: "devops-alerts"
        with:
          message: "Warning: Failed to create {{jira}} ticket. Continuing workflow."
```

## Dynamic values with templating [workflows-dynamic-values]

To inject dynamic values into your workflow steps, use the templating engine. The templating engine uses the [Liquid templating language](https://liquidjs.com/) and allows you to:

- **Reference step outputs**: Access data from previous steps using `steps.<step_name>.output`
- **Use constants**: Reference workflow-level constants with `consts.<constant_name>`
- **Apply filters**: Transform values with filters like `upcase`, `downcase`, and `date`
- **Add conditional logic**: Use `if`/`else` statements for dynamic content
- **Loop through data**: Iterate over arrays with `for` loops

For complete syntax details and examples, refer to [Templating engine](./data/templating.md).

## Quick reference [workflows-data-quick-reference]

By combining data flow, templating, and robust error handling, you can build complex, reliable automations that react to dynamic conditions and recover from unexpected failures.

| Action | Syntax | Description |
|---------|--------|-------------|
| Step output | `steps.<step_name>.output` | Access the result of a previous step |
| Step error | `steps.<step_name>.error` | Access error details from a failed step |
| Fallback steps | `on-failure.fallback` | Define recovery actions when a step fails |
| Continue on failure | `on-failure.continue: true` | Allow the workflow to proceed after a failure |