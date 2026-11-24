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

Microsoft Foundry hosted agents can send OpenTelemetry traces, logs, and metrics straight to Elastic. You set the OTLP exporter settings on the hosted agent version and point them at the Elastic Cloud Managed OTLP Endpoint. You don't need to change your agent code, add an OpenTelemetry SDK, or run an OpenTelemetry Collector.

The telemetry is stored in Elastic in OTLP format.

## Before you begin

Make sure you have the following:

* A Microsoft Foundry project with a deployed hosted agent.
* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).

## Add Elastic as an export destination

Full step-by-step setup is in Microsoft's guide: [Export hosted agent telemetry by using OpenTelemetry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-telemetry?tabs=otlp-export). The three steps:

:::::{stepper}

::::{step} Store the API key in a Foundry connection
In your Foundry project, add a **Custom keys** connection with a field named `otlp_headers`. Set its value to `Authorization=ApiKey <your-api-key>` (the word `ApiKey`, a space, then the encoded key). Create the connection before you deploy the agent version.
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

The hosted agent also sends logs and metrics, which land in the `logs-*` and `metrics-*` data streams of your project.

## Send telemetry to Application Insights and Elastic

When project monitoring is enabled, Foundry also sends the hosted agent's telemetry to Application Insights. With both configured, the agent sends to both in parallel. To send telemetry only to Elastic, disable monitoring at the project level in Foundry. Refer to Microsoft's guide for details.

## Related pages

* [Export hosted agent telemetry by using OpenTelemetry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-telemetry?tabs=otlp-export) (Microsoft documentation)
* [{{motlp}} reference](/reference/managed-inputs/managed-otlp-endpoint.md)
* [LLM and agentic AI observability](/solutions/observability/applications/llm-observability.md)
* To collect platform metrics and logs from Microsoft Foundry, use the [Azure AI Foundry](integration-docs://reference/azure_ai_foundry.md) integration.
