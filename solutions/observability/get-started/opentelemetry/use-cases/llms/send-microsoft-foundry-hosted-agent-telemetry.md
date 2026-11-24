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

* A Microsoft Foundry project with a deployed hosted agent.
* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).

## Add Elastic as an export destination

Full step-by-step setup is in Microsoft's guide: [Export hosted agent telemetry by using OpenTelemetry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-telemetry?tabs=otlp-export).

:::::{stepper}

::::{step} Store the API key in a Foundry connection
In the Foundry portal, open **Manage** → **Project details** → **Connections**, then select **Add connection** and choose **Custom keys**. Add a field named `otlp_headers` and set its value to `Authorization=ApiKey <your-api-key>` (the word `ApiKey`, a space, then the encoded key). Create the connection before you deploy the agent version.
::::

::::{step} Add the exporter settings to agent.yaml
Set the endpoint to your {{motlp}} URL, the protocol to `http/protobuf`, and the headers to the connection field:

```yaml
environment_variables:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: https://<your-motlp-endpoint>
  - name: OTEL_EXPORTER_OTLP_PROTOCOL
    value: http/protobuf
  - name: OTEL_EXPORTER_OTLP_HEADERS
    value: ${{connections.otel-secrets.credentials.otlp_headers}}
```
::::

::::{step} Create a new agent version
Foundry sets environment variables per agent version. Deploy a new version of the agent to apply them.
::::

:::::

:::{important}
Hosted agent telemetry can include prompts, tool calls, and model responses. Before you export, check that your organization's policies allow this data to be kept in Elastic.
:::

## Check that traces arrive

Send a request to your hosted agent and allow a few seconds for the telemetry to arrive. Foundry sets `service.name` to the name of your agent. In {{kib}} **Discover**, run the following {{esql}} query to find the traces:

```esql
FROM traces-*
| WHERE service.name == "<your-agent-name>"
```

The hosted agent also sends logs and metrics, which land in the `logs-generic.otel-default` and `metrics-generic.otel-default` data streams. To find them, run the following queries in **Discover**:

```esql
FROM logs-generic.otel-default
| WHERE service.name == "<your-agent-name>"
```

```esql
TS metrics-generic.otel-default
| WHERE service.name == "<your-agent-name>"
```

## Send telemetry to Application Insights and Elastic

Foundry can send the telemetry of your hosted agents to Application Insights. This is called project monitoring. When it's on, an Application Insights resource is [connected to your Foundry project](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-setup), and every hosted agent sends its telemetry there automatically. If you also add the exporter settings from this page, the agent sends its telemetry to Application Insights and to Elastic in parallel. Each backend can map, store, and display the telemetry differently, so the data in Elastic might not match Application Insights field for field.

## Example: Token usage by model

In {{kib}} **Discover**, run this {{esql}} query to sum input and output tokens by model. The `attributes.gen_ai.operation.name == "chat"` filter restricts the query to the spans of model calls:

```esql
FROM traces-*
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
