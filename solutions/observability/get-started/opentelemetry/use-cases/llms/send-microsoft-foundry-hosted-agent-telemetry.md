---
navigation_title: Microsoft Foundry
description: Send OpenTelemetry traces, logs, and metrics from Microsoft Foundry hosted agents to Elastic Observability through the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: ga
  deployment:
    ech: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Send Microsoft Foundry hosted agent telemetry to Elastic

[Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry) hosted agents can send OpenTelemetry traces, logs, and metrics straight to Elastic. You set the OTLP exporter settings on your hosted agent and point them at the Elastic Cloud Managed OTLP Endpoint. You don't need to change your agent code, add an OpenTelemetry SDK, or run an OpenTelemetry Collector.

The telemetry is stored in Elastic in OTLP format.

## Before you begin

Make sure you have the following:

* A Microsoft Foundry project with a hosted agent that you deploy with the Azure Developer CLI (`azd`). To set one up, refer to [Quickstart: Deploy your first hosted agent](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/quickstart-hosted-agent) in the Microsoft documentation.
* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).

## Add Elastic as an export destination

For more about how hosted agents export telemetry, refer to [Export hosted agent telemetry by using OpenTelemetry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-telemetry?tabs=otlp-export) in the Microsoft documentation.

:::::{stepper}

::::{step} Store the API key in a Foundry connection
Create the connection before you deploy the agent, so the agent can read the key when it starts. In the Foundry portal, open **Manage** → **Project details** → **Connections**, then select **Add connection** and choose **Custom keys**. Name the connection `otel-secrets`, add a field named `otlp_headers`, and set its value to `Authorization=ApiKey <your-api-key>` (the word `ApiKey`, a space, then the encoded key). For more about connections, refer to [Add a new connection to your project](https://learn.microsoft.com/en-us/azure/foundry/how-to/connections-add) in the Microsoft documentation.
::::

::::{step} Add the exporter settings
Add these three environment variables to your hosted agent. They tell it where to send telemetry and how to authenticate. In `azure.yaml`, add them to the `env` map of the service whose `host` is `azure.ai.agent`:

```yaml
services:
  <your-agent-service>:
    env:
      OTEL_EXPORTER_OTLP_ENDPOINT: https://<your-motlp-endpoint>
      OTEL_EXPORTER_OTLP_PROTOCOL: http/protobuf
      OTEL_EXPORTER_OTLP_HEADERS: $${{connections.otel-secrets.credentials.otlp_headers}}
```

For more about these settings, refer to [Configure environment variables for a hosted agent](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-env-variables) in the Microsoft documentation.
::::

::::{step} Deploy the agent again
Foundry stores environment variables with each agent version, so the settings only apply to a new version. Run `azd deploy` to create one. For more about deploying, refer to [Deploy a hosted agent](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent) in the Microsoft documentation.
::::

:::::

:::{important}
Hosted agent telemetry can include prompts, tool calls, and model responses. Before you export, check that your organization's policies allow this data to be kept in Elastic.
:::

## Check that telemetry arrives

Send a request to your hosted agent and allow a few seconds for the telemetry to arrive. Then, in {{kib}} **Discover**, run the following {{esql}} queries. Each one filters on `service.name`, which Foundry sets to the name of your agent.

* Traces:

    ```esql
    FROM traces-generic.otel-default
    | WHERE service.name == "<your-agent-name>"
    ```

* Logs:

    ```esql
    FROM logs-generic.otel-default
    | WHERE service.name == "<your-agent-name>"
    ```

* Metrics:

    ```esql
    TS metrics-generic.otel-default
    | WHERE service.name == "<your-agent-name>"
    ```

## Example: Token usage by model

In {{kib}} **Discover**, run this {{esql}} query to sum input and output tokens by model. The `attributes.gen_ai.operation.name == "chat"` filter restricts the query to the spans of model calls:

```esql
FROM traces-generic.otel-default
| WHERE service.name == "<your-agent-name>" AND attributes.gen_ai.operation.name == "chat"
| STATS
    input_tokens = SUM(attributes.gen_ai.usage.input_tokens),
    output_tokens = SUM(attributes.gen_ai.usage.output_tokens)
  BY attributes.gen_ai.request.model
```

## Related pages

* [Export hosted agent telemetry by using OpenTelemetry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-telemetry?tabs=otlp-export) (Microsoft documentation)
* [{{motlp}} reference](/reference/managed-inputs/managed-otlp-endpoint.md)
* [LLM and agentic AI observability](/solutions/observability/applications/llm-observability.md)
* To also collect Azure platform metrics and logs, use the [Microsoft Foundry](integration-docs://reference/azure_ai_foundry.md) integration.
