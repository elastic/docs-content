---
navigation_title: External systems and apps
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about action steps for interacting with external systems such as Slack or Jira.
---

# External systems and apps steps

External systems actions allow your workflows to communicate with third-party services and custom endpoints. You can interact with external systems in the following ways:

* [Connector-based actions](#connector-based-actions): Use pre-configured connectors to integrate with services such as Slack and {{jira}}
* [HTTP actions](#http-actions): Make direct HTTP requests to any API endpoint

## Connector-based actions

Connector-based actions use {{kib}}'s centralized {{connectors-ui}} framework. Before using them, you must first [configure a connector](/deploy-manage/manage-connectors.md).

The step `type` is a keyword for the service (for example, `slack` or `jira`). You must also provide a `connector-id` at the same level as `type`.

To view the available connectors, click **Actions menu** and select **External Systems & Apps**. 

### Identify a connector

The `connector-id` field accepts one of the following:

* The unique name you gave the connector (for example, `"my-slack-connector"`). This is the recommended method for readability.
* The connector's raw ID (for example, `"d6b62e80-ff9b-11ee-8678-0f2b2c0c3c68"`).

### Example: Send a Slack notification

This example uses a pre-configured Slack connector named `"security-alerts-channel"`.

```yaml
steps:
  - name: notify_security_channel
    type: slack
    connector-id: "security-alerts-channel"
    with:
      message: "High-priority alert: {{ event.name }}. Please investigate immediately."
```

### Example: Create a {{jira}} issue

This example uses a {{jira}} connector named `"engineering-project"`.

```yaml
steps:
  - name: create_jira_ticket
    type: jira
    connector-id: "engineering-project"
    with:
      projectKey: "ENG"
      issueType: "Task"
      summary: "Automated Task: Review '{{ event.name }}'"
      description: "Workflow '{{ workflow.name }}' requires manual review for a potential issue."
```

## HTTP actions

The native `http` action is a built-in HTTP client that does not require a pre-configured connector. Use it for one-off requests to public or internal APIs.

Use the following parameters in the `with` block to configure the request:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | The full URL of the endpoint to call |
| `method` | No (defaults to `GET`) | The HTTP method (`GET`, `POST`, `PUT`, or `DELETE`) |
| `headers` | No | An object with key-value pairs for HTTP headers |
| `body` | No | The request body (typically a JSON object) |

::::{admonition} Known limitation
The native `http` action does not have access to a centralized secret store for managing authentication credentials. If your endpoint requires authentication, you must include the credentials directly in the `headers` block.

:::{dropdown} Click to show syntax example
```yaml
steps:
  - name: call_secure_api
    type: http
    with:
      url: "https://api.thirdparty.com/v1/data"
      method: "GET"
      headers:
        Authorization: "Bearer my-secret-api-token"
```
:::
::::

### Example: Call a custom webhook

This example makes a POST request to a custom automation endpoint, passing data from the workflow context.

```yaml
steps:
  - name: trigger_custom_automation
    type: http
    with:
      url: "https://hooks.example.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
      method: "POST"
      headers:
        Content-Type: "application/json"
      body:
        event_id: "{{ event.id }}"
        message: "Workflow action triggered by '{{ workflow.name }}'"
```

