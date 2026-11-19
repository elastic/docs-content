---
navigation_title: OpenRouter Broadcast
description: Send OpenTelemetry traces from OpenRouter Broadcast — one trace per chat completion request — to Elastic Observability through the Elastic Cloud Managed OTLP Endpoint.
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

# Send OpenRouter Broadcast traces to Elastic

[OpenRouter](https://openrouter.ai) is a gateway that routes LLM requests across many model providers. OpenRouter Broadcast can send OpenTelemetry traces of every chat completion straight to Elastic. After an account admin adds Elastic as a destination in the OpenRouter console, one trace per request starts arriving in your Elastic project. You don't need to change your code or run an OpenTelemetry Collector.

Each Broadcast trace contains two spans:

* An **`LLM Generation`** parent span with the model, provider and usage attributes of the request.
* A child **`provider attempt N: <Provider>`** span for the attempt against the upstream provider, with the attempt's own latency and response id.

The spans follow the OpenTelemetry GenAI semantic conventions and are stored in Elastic in OTLP format.

::::{note}
Broadcast sends **traces only**. For usage, cost and performance metrics by model and API key, install the companion [OpenRouter integration](integration-docs://reference/openrouter.md). The two sources are complementary and can be used together.
::::

## Before you begin

Make sure you have the following:

* An **admin** role on the OpenRouter account whose API keys you want to broadcast. If someone else administers the account, give them the endpoint and API key from the next item.
* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).

## Add Elastic as a Broadcast destination

Full step-by-step setup is in OpenRouter's own guide: [Broadcast — Elastic](https://openrouter.ai/docs/guides/features/broadcast/elastic). At a high level:

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

## Where the traces appear in Elastic

Traces land as OTLP spans under `service.name: openrouter` in the Applications section. You can view them in:

* **Discover** — filter on `service.name: openrouter` against the `traces-generic.otel-*` data view. All attributes (model, provider, tokens, finish reason, response id) are available.
* **Applications → Service inventory → `openrouter` → Transactions** — opens the request waterfall plus the **GenAI** tab, which renders the full conversation (system, user, assistant with any Reasoning tokens) alongside Operation, Request model, Response model, Provider, Input/Output/Cache tokens, Response ID and Finish reasons.
* **Applications → Traces** — the list of root transactions.

Each request produces two spans: a parent **`LLM Generation`** span and a child **`provider attempt N: <Provider>`** span.

## Group multi-turn conversations

By default each chat completion produces its own trace. To view a multi-turn conversation as a single waterfall, open a span in your own application code and pass the OTel context to OpenRouter in the request body. OpenRouter then nests its spans inside yours:

```python
with tracer.start_as_current_span("chat_turn") as turn:
    turn.set_attribute("peer.service", "openrouter")
    turn.set_attribute("gen_ai.system", "openrouter")
    ctx = turn.get_span_context()
    body["trace"] = {
        "trace_id":       f"{ctx.trace_id:032x}",
        "parent_span_id": f"{ctx.span_id:016x}",
    }
```

In Kibana you get one waterfall for the whole conversation: your application at the root, `LLM Generation` under each turn, `provider attempt` under each generation — two services in the same trace, connected in the Service map.

::::{tip}
To group multi-turn traffic without instrumenting the app, pass `session_id` (or the `x-session-id` header) on each request. Turns stay as separate traces but filter together in Discover.
::::

## Known limits

* **Prompt lengths in ES|QL.** Long prompts can return `null` in ES|QL because of the `ignore_above: 1024` mapping on the `gen_ai.prompt` field. The full value is in the span `_source`.
* **Cost.** Paid requests populate three OTel standard fields on the `LLM Generation` span: `gen_ai.usage.input_cost`, `gen_ai.usage.output_cost`, and `gen_ai.usage.total_cost` (all in USD). OpenRouter also writes richer vendor fields under `span.metadata.openrouter_cost_allocation.*` and `trace.metadata.openrouter_cost_allocation.*`, including `cost_status` (expect `unreconciled` on newly-received spans; it settles after billing) and `is_byok`. Free models don't emit cost fields.
