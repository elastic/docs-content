---
navigation_title: Kibana
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about Kibana action steps for automating tasks such as creating cases and managing alerts in workflows.
---

# {{kib}} action steps

{{kib}} actions are built-in steps that allow your workflows to interact with {{kib}} APIs. You can automate tasks such as creating cases, updating alerts, or interacting with other {{kib}} features.

All {{kib}} actions are automatically authenticated using the permissions of the user or API key executing the workflow.

There are two ways to use {{kib}} actions:

* [Named actions](#named-actions): Simplified, high-level interface for common {{kib}} operations
* [Generic request actions](#generic-request-actions): Full control over the HTTP request for advanced use cases

## Named actions

Named actions provide a simplified, high-level interface for common {{kib}} operations. Each action type corresponds to a specific {{kib}} function. The following example demonstrates a common use case.

### Example: Create a case

The `kibana.createCaseDefaultSpace` action opens a new security case. The parameters in the `with` block are specific to this action.

```yaml
steps:
  - name: create_a_case
    type: kibana.createCaseDefaultSpace
    with:
      title: "Suspicious Login Detected"
      description: "Automated case created by workflow. Host '{{ event.host.name }}' exhibited unusual activity."
      tags: ["workflow", "automated-response"]
      severity: "critical"
      connector:
        id: "none"
        name: "none"
        type: ".none"
```

## Generic request actions

The generic `kibana.request` type gives you full control over the HTTP request. Use it for:

* Accessing {{kib}} APIs that do not have a named action
* Advanced use cases that require specific headers or query parameters not exposed by a named action

::::{note}
We recommend using named actions whenever possible. They are more readable and provide a stable interface for common operations.
::::

Use the following parameters in the `with` block to configure the request:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `method` | No (defaults to `GET`) | The HTTP method (`GET`, `POST`, `PUT`, `DELETE`) |
| `path` | Yes | The API endpoint path, starting with `/api/` or `/internal/` |
| `body` | No | The JSON request body |
| `query` | No | An object representing URL query string parameters |
| `headers` | No | Custom HTTP headers to include in the request. `kbn-xsrf` and `Content-Type` are added automatically |

::::{note}
You do not need to pass an `Authorization` header. The workflow engine automatically attaches the correct authentication headers based on the execution context. Do not manage or pass API keys or secrets in the `headers` block.
::::

### Example: Unisolate an endpoint

This example uses the generic request to call the Security endpoint management API to unisolate a host ([Release an isolated endpoint]({{kib-apis}}operation/operation-endpointunisolateaction)).

```yaml
steps:
  - name: unisolate_endpoint_with_case
    type: kibana.request
    with:
      method: POST
      path: /api/endpoint/action/unisolate
      body:
        endpoints: 
          - "{{ endpoint_id_value }}"
        comment: "Unisolating endpoint as part of automated cleanup."
```


