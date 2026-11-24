---
navigation_title: OpenRouter Broadcast
description: Send OpenTelemetry traces from OpenRouter Broadcast, one trace per chat completion request, to Elastic Observability through the Elastic Cloud Managed OTLP Endpoint.
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

# Send OpenRouter traces to Elastic

[OpenRouter](https://openrouter.ai) is a gateway that routes LLM requests across many model providers. OpenRouter [Broadcast](https://openrouter.ai/docs/guides/features/broadcast) can send OpenTelemetry traces of every chat completion straight to Elastic. After an account admin adds Elastic as a destination in the OpenRouter console, one trace per request starts arriving in your Elastic project. You don't need to change your code or run an OpenTelemetry Collector.

Each request produces a parent span for the LLM generation plus one child span per upstream provider attempt. The spans follow the OpenTelemetry GenAI semantic conventions and are stored in Elastic in OTLP format.

## Before you begin

Make sure you have the following:

* An **admin** role on the OpenRouter account whose API keys you want to broadcast. If someone else administers the account, give them the endpoint and API key from the next item.
* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).

## Add Elastic as a Broadcast destination

Full step-by-step setup is in OpenRouter's own guide: [Broadcast — Elastic](https://openrouter.ai/docs/guides/features/broadcast/elastic). The three steps:

:::::{stepper}

::::{step} Open the Observability settings
In the OpenRouter console, open **Settings → Observability**. Select **Add destination** and choose **Elastic Observability**.
::::

::::{step} Enter your Elastic endpoint and API key
Set the OTLP endpoint to your {{motlp}} URL. Set the header `Authorization` to `ApiKey <your-api-key>` (the word `ApiKey`, a space, then the encoded key).
::::

::::{step} Test the connection
Select **Test Connection** and confirm the synthetic `Test Generation` span lands in Elastic Discover under `service.name: openrouter`. Then save the destination.
::::

:::::

::::{tip}
OpenRouter's Broadcast has a **Privacy Mode** that strips prompt and completion content from the trace, keeping only metadata (model, tokens, latency, response id). Enable it from the same destination if you don't want message content to leave OpenRouter.
::::

## Check that traces arrive

To verify Elastic is receiving spans without sending a real chat completion, use OpenRouter's **Test Connection** button at **Settings → Observability → your Elastic destination**. It fires a synthetic `Test Generation` span.

In {{kib}} **Discover**, run this {{esql}} query to find the test span (and any real Broadcast span) by `service.name`:

```esql
FROM traces-*
| WHERE service.name == "openrouter"
```

The destination's delivery status in the OpenRouter console shows a healthy indicator once spans are being accepted. This can take about a minute after setup.

## Where the traces appear in Elastic

Traces land as OTLP spans under `service.name: openrouter`. Each span carries the request metadata (model, provider, tokens, cost, finish reason, response id) and the full conversation. You can reach them from:

* **Discover**: Query with {{esql}}, then expand a row.
* **Applications → Service inventory → `openrouter` → Transactions**: Opens the request waterfall; pick a transaction to view its details.
* **Applications → Traces**: The list of root transactions.

## Example: Token usage by model

In {{kib}} **Discover**, run this {{esql}} query to sum input and output tokens by model. The `name == "LLM Generation"` filter restricts the query to the parent request spans, so child `provider attempt` spans aren't counted twice:

```esql
FROM traces-*
| WHERE service.name == "openrouter" AND name == "LLM Generation"
| STATS
    input_tokens = SUM(attributes.gen_ai.usage.input_tokens),
    output_tokens = SUM(attributes.gen_ai.usage.output_tokens)
  BY attributes.gen_ai.request.model
```

## Related pages

* [OpenRouter Broadcast documentation](https://openrouter.ai/docs/guides/features/broadcast) (OpenRouter documentation)
* [{{motlp}} reference](/reference/managed-inputs/managed-otlp-endpoint.md)
* [LLM and agentic AI observability](/solutions/observability/applications/llm-observability.md)
