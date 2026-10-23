---
navigation_title: OpenRouter
description: Send OpenRouter Broadcast traces to Elastic Observability through the Elastic Cloud Managed OTLP Endpoint.
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

[OpenRouter Broadcast](https://openrouter.ai/docs/guides/features/broadcast/elastic) sends a trace for each API request to the [{{motlp}}](opentelemetry://reference/motlp.md). After you add **Elastic Observability** as a destination, traces start arriving in your Elastic project. You don't change your application code or install a Fleet integration. Broadcast sends traces only, not logs or metrics.

The spans follow the OpenTelemetry GenAI semantic conventions and are stored in Elastic in OTLP format. `service.name` is `openrouter`.

## Before you begin

Make sure you have the following:

* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments. OpenRouter sends OTLP/HTTP JSON, which {{apm-server}} doesn't accept.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).
* An OpenRouter API key, and the organization admin role if the OpenRouter account is an organization. Organization admins are the users who can edit Broadcast settings.

## Add Elastic as a destination

Add **Elastic Observability** in OpenRouter. The destination tells OpenRouter where to send traces and how to authenticate. Live chat completions come from this destination. A **Webhook** test span is named `Test Generation` and is not a chat completion.

:::::{stepper}

::::{step} Open Broadcast settings
In OpenRouter, go to **Settings** → **Observability** and turn on **Enable Broadcast**.
::::

::::{step} Add Elastic Observability
Add the **Elastic Observability** destination and enter:

* **Endpoint**: your {{motlp}} URL. OpenRouter appends `/v1/traces`. A URL that already ends in `/v1` or `/v1/traces` also works.
* **API Key**: the encoded Elastic API key. OpenRouter sends it as `Authorization: ApiKey <key>`.

Optional **Headers** are extra HTTP headers as JSON. They can't override `Authorization` or `Content-Type`.
::::

::::{step} Test and save
Select **Test Connection**, then save the destination. The configuration saves only if the test passes. A `401` response means Elastic rejected the API key. Use the encoded key, and confirm it has the `event:write` privilege for the `apm` application.
::::

:::::

## Check that traces arrive

Send a chat completion through OpenRouter:

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "openai/gpt-4o",
    "messages": [
      {"role": "user", "content": "Summarize this incident in one sentence."}
    ]
  }'
```

Copy the `id` from the response (`gen-<id>`). Set the {{kib}} time range so it includes the request. Spans are stored in the `traces-generic.otel-default` data stream.

In **Discover**, run:

```esql
FROM traces-*
| WHERE service.name == "openrouter"
```

To find that generation, run:

```esql
FROM traces-*
| WHERE service.name == "openrouter"
    AND attributes.gen_ai.response.id == "gen-<id>"
```

You can also open the trace from **Applications**:

* [**Service inventory**](/solutions/observability/apm/services.md) → the `openrouter` service → **Transactions**
* [**Traces**](/solutions/observability/apm/traces-ui.md)

**Traces** searches fields on the root transaction. To filter on `session.id` or `gen_ai.*`, use **Discover**.

The generation span carries the model, token counts, and the messages:

| Attribute | Contents |
| --- | --- |
| `gen_ai.operation.name` | Operation, such as `chat` |
| `gen_ai.request.model` | Model you requested |
| `gen_ai.response.model` | Model that served the request |
| `gen_ai.provider.name` | Provider that served the request |
| `gen_ai.usage.input_tokens` | Input tokens |
| `gen_ai.usage.output_tokens` | Output tokens |
| `gen_ai.input.messages` | Request messages |
| `gen_ai.output.messages` | Model response |
| `gen_ai.response.id` | OpenRouter generation ID |

If **Privacy Mode** is on for this destination, `gen_ai.input.messages` and `gen_ai.output.messages` are omitted. Token counts, timing, the model, and cost are still sent.

## Group turns on one trace

`user` is stored as `user.id`. `session_id` is stored as `session.id`. Filter on `session.id` in **Discover** to list every turn in a session. Those turns share a trace when each request sends the same `trace.trace_id`. Use 32 hexadecimal characters.

```json
{
  "model": "openai/gpt-4o",
  "messages": [{"role": "user", "content": "What failed?"}],
  "user": "user_12345",
  "session_id": "session_abc",
  "trace": {
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "trace_name": "Incident summary",
    "generation_name": "Summarize"
  }
}
```

Send that same `trace_id` on later turns, and include the previous messages in `messages`. `trace.trace_name` names the root span. `trace.generation_name` names the generation span. Any other key in `trace` is stored as `trace.metadata.*`.

To nest the OpenRouter generation under a span your application already sent to Elastic, set `trace.trace_id` to the application's trace ID and `trace.parent_span_id` to that span's ID. A span ID is 16 hexadecimal characters.

```json
{
  "model": "openai/gpt-4o",
  "messages": [{"role": "user", "content": "What failed?"}],
  "trace": {
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "parent_span_id": "00f067aa0ba902b7"
  }
}
```

## Related pages

* [Broadcast to Elastic Observability](https://openrouter.ai/docs/guides/features/broadcast/elastic) (OpenRouter documentation)
* [{{motlp}} reference](opentelemetry://reference/motlp.md)
* [LLM and agentic AI observability](/solutions/observability/applications/llm-observability.md)
