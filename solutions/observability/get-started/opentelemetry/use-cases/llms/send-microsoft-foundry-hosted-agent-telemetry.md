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

The runtime of a Microsoft Foundry hosted agent already emits OpenTelemetry traces, logs, and metrics. To send them to Elastic, you set the OTLP exporter variables on the agent version and point them at the Elastic Cloud Managed OTLP Endpoint. You don't need to change your agent code, add an OpenTelemetry SDK, or run an OpenTelemetry Collector.

This page covers Microsoft Foundry hosted agents only. The spans follow the OpenTelemetry GenAI semantic conventions and are stored in Elastic in OTLP format.

## Before you begin

Make sure you have the following:

* A Microsoft Foundry project with a deployed hosted agent.
* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).

## Configure the hosted agent to export to Elastic

Microsoft's own guide for this setup is [Export hosted agent telemetry by using OpenTelemetry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-telemetry?tabs=otlp-export). The setup has three steps:

:::::{stepper}

::::{step} Store the API key in a Foundry connection
Keep the Elastic API key out of `agent.yaml` by storing it in a Foundry project connection:

1. In the Foundry portal, open **Manage** → **Project details** → **Connections**, then select **Add connection**.
2. Select **Custom keys**.
3. Name the connection, for example `otel-secrets`. Add a key named `otlp_headers` with the value `Authorization=ApiKey <your-api-key>`. Enter it on one line, with one space after `ApiKey` and nothing after the key.

Create the connection before you deploy the agent version. If the connection doesn't exist, the header resolves to an empty value and Elastic rejects the data.
::::

::::{step} Add the exporter settings to agent.yaml
In the hosted agent's `agent.yaml`, set the OTLP endpoint, the protocol, and the header from the connection:

```yaml
environment_variables:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: https://<your-motlp-endpoint>
  - name: OTEL_EXPORTER_OTLP_PROTOCOL
    value: http/protobuf
  - name: OTEL_EXPORTER_OTLP_HEADERS
    value: ${{connections.otel-secrets.credentials.otlp_headers}}
```

Use the base {{motlp}} URL as the endpoint. The exporter adds the signal paths, such as `/v1/traces`. For the placeholder syntax, refer to [Reference project connections in environment variables](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent#reference-project-connections-in-environment-variables) in the Microsoft documentation.
::::

::::{step} Create a new agent version
Foundry sets environment variables per agent version and doesn't let you change them afterward. To change the endpoint or the header later, create a new version of the agent.
::::

:::::

:::{important}
Hosted agent telemetry can include prompts, tool calls, and model responses. Once exported, any user who can read the traces data streams in your Elastic project can view them. Before you export, check that your organization's policies allow this data to be kept in Elastic.
:::

## Check that traces arrive

1. Send a request to your hosted agent. Foundry sends telemetry in batches, so allow a few seconds.
2. In {{kib}}, find the spans. Foundry sets `service.name` to the name of your agent, and you can't override it with `OTEL_SERVICE_NAME`. For example, in **Discover**, run the following {{esql}} query:

    ```esql
    FROM traces-*
    | WHERE service.name == "<your-agent-name>"
    ```

The traces include `invoke_agent` spans for agent runs and `chat <model-name>` spans for model calls. The runtime's outgoing HTTP calls also appear as `GET` and `POST` spans. For the spans that Foundry defines, refer to [Agent tracing overview](https://learn.microsoft.com/en-us/azure/foundry/observability/concepts/trace-agent-concept) in the Microsoft documentation.

To see the prompt, the reply, and the token counts of a model call, open a `chat <model-name>` span in **Discover** and select the **GenAI** tab.

## Check logs and metrics

The hosted agent also sends logs and metrics:

* **Logs** arrive in the `logs-*` data streams and include the trace ID.
* **Metrics** arrive in the `metrics-*` data streams. They include `gen_ai.client.operation.duration`, `gen_ai.client.token.usage`, `http.client.duration`, and Azure Monitor performance counters such as memory and processor use.

## Send telemetry to Application Insights and Elastic

When project monitoring is enabled, Foundry also gives the hosted agent an Application Insights connection string. You can't set or override that variable in `agent.yaml`. With both configured, the agent sends its telemetry to Application Insights and to Elastic in parallel.

The two backends receive the same hosted agent telemetry, but each one can map, store, and display it differently. Don't expect field-for-field equivalence between them.

If you keep Application Insights enabled, the agent identity needs the **Monitoring Metrics Publisher** role on the Application Insights resource. Without it, the Application Insights exporter fails and `Forbidden` errors fill your logs. These errors don't affect the data that reaches Elastic. For the steps, refer to [Configure Microsoft Entra authentication for Foundry Agent trace ingestion](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-ingestion-entra-authentication) in the Microsoft documentation.

To send telemetry only to Elastic, disable monitoring at the project level in Foundry. For details, refer to [Disable tracing](https://learn.microsoft.com/en-us/azure/foundry/observability/concepts/trace-data#disable-tracing) in the Microsoft documentation.

## Related pages

* [Export hosted agent telemetry by using OpenTelemetry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-hosted-agent-telemetry?tabs=otlp-export) (Microsoft documentation)
* [{{motlp}} reference](/reference/managed-inputs/managed-otlp-endpoint.md)
* [LLM and agentic AI observability](/solutions/observability/applications/llm-observability.md)
* To collect platform metrics and logs from Microsoft Foundry, use the [Azure AI Foundry](integration-docs://reference/azure_ai_foundry.md) integration.
