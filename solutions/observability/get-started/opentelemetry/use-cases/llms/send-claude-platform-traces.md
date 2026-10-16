---
navigation_title: Claude Platform
description: Send OpenTelemetry traces from the Claude Platform, including Messages API requests and Claude Managed Agents sessions, to Elastic Observability through the Elastic Cloud Managed OTLP Endpoint.
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

# Send Claude Platform traces to Elastic

Anthropic can send OpenTelemetry traces of your Claude API usage straight to Elastic. After a Claude Console admin adds Elastic as a destination, traces for Messages API requests and Claude Managed Agents sessions start arriving in your Elastic project. You don't need to change your code or run an OpenTelemetry Collector.

Claude Platform spans come from two sources. Send both to the same Elastic project to see them in one trace:

* **API spans**: Anthropic emits a span for each Messages API request, Managed Agents turn, model request, and tool that the API runs. Anthropic sends these spans to the destination that you add in the Claude Console.
* **SDK spans** (optional): The Claude SDK in your application creates a span for every API call it makes and for every tool its tool runner executes. Your application sends these spans to Elastic through an OpenTelemetry exporter that you configure.

The spans follow the OpenTelemetry GenAI semantic conventions and are stored in Elastic in OTLP format.

## Before you begin

Make sure you have the following:

* The **admin** role in your [Claude Console](https://platform.claude.com) organization, the one where your Claude API keys are created. This isn't the same as an organization you use at claude.ai. Users with the developer role can see destinations but can't add them. If someone else administers your Claude organization, give them the endpoint and API key from the next item.
* An {{obs-serverless}} project or an {{ech}} deployment. On {{ech}}, the {{motlp}} requires version 9.0 or later. The {{motlp}} isn't available for self-managed, {{ece}}, or {{eck}} deployments.
* Your {{motlp}} endpoint and an API key with the `event:write` privilege for the `apm` application. To get both, follow the **Find your endpoint** and **Create an API key** steps in [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md#send-data-to-elastic).

## Add Elastic as a destination to send API spans

Add Elastic as a telemetry destination in the Claude Console. The destination tells Anthropic where to send API spans and how to authenticate.

:::::{stepper}

::::{step} Open the OpenTelemetry settings
In the Claude Console, open the [OpenTelemetry settings](https://platform.claude.com/settings/telemetry-destinations) page of your organization. If a workspace is selected in the workspace filter, clear it. Then select **Add destination**.
::::

::::{step} Select Elastic
For **Provider**, select **Elastic**. Optionally, enter a **Name** for the destination, such as `Elastic production`.

Enter your {{motlp}} endpoint, then set the header `Authorization` to ApiKey and add the encoded key.
::::

::::{step} Choose a content mode
For **Content mode**, select one of the following:

* **Metadata only**: Spans carry IDs, timing, status, and token usage. Prompts and responses aren't included.
* **Full content**: Spans also carry system instructions, prompts, model responses, and tool input and output.

:::{important}
**Full content** puts prompts and responses in your Elastic project, where any user who can read the traces data streams can view them. Before you select it, check that your organization's policies allow this data to be kept in Elastic.
:::
::::

::::{step} Choose the workspaces
For **Workspaces**, choose which Claude workspaces send spans to Elastic: **All**, **Selected**, or **All except**.
::::

::::{step} Save and test the destination
Select **Add destination**. Then open the destination's **More actions** menu and select **Test**. The Claude Console reports whether the test span was delivered.
::::

:::::

## Check that traces arrive

1. Generate some activity in a workspace that the destination covers. For example, send a message in the Claude Console playground, send a Messages API request, or run a Managed Agents session.
2. In the Claude Console, on the OpenTelemetry settings page, check that the **Delivery** column for your destination shows **Healthy**. This can take about a minute.
3. In {{kib}}, find the spans. All API spans have `service.name` set to `claude-platform`. For example, in **Discover**, run the following {{esql}} query:

    ```esql
    FROM traces-*
    | WHERE service.name == "claude-platform"
    ```

    To find the test span from the previous section, run:

    ```esql
    FROM traces-*
    | WHERE service.name == "claude-platform" AND span.name == "anthropic.test"
    ```

The main spans that the Claude Platform sends are:

| Span | What it represents |
|---|---|
| `anthropic.messages.create` | A Messages API request. With **Full content**, it holds the system prompt, input messages, and response. |
| `anthropic.model_request` | One model request within a Messages API request or a Managed Agents turn, with the model and token usage. |
| `anthropic.session.turn` | One Managed Agents turn. With **Full content**, it holds the turn's input and output. |
| `anthropic.tool_use`, `anthropic.mcp_tool_use` | A tool that the API runs, such as a server tool or an MCP connector tool. |

To group the spans of one Managed Agents session across traces, filter on `anthropic.session.id`. For every span and attribute, refer to the [OpenTelemetry span reference](https://platform.claude.com/docs/en/api/opentelemetry/spans) in the Anthropic documentation.

## Send Claude SDK spans to Elastic from your application [send-sdk-spans]

To see the work your application does around each Claude API request in the same trace, send the Claude SDK spans to Elastic too. The following Python example configures the exporter with the standard OpenTelemetry environment variables, the same way you configure any OpenTelemetry SDK for the {{motlp}}.

1. Install the Claude SDK and the OpenTelemetry SDK with the OTLP HTTP exporter:

    ```bash
    pip install anthropic opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
    ```

2. Set the environment variables for the exporter and the Claude SDK:

    ```bash
    export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>"
    export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <encoded-api-key>"
    ```

    The exporter adds `/v1/traces` to the endpoint. The header value needs the space after `ApiKey`.

3. In your application, register a tracer provider before you create the Claude client:

    ```python
    from anthropic import Anthropic
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    # The exporter reads the endpoint and headers from the OTEL_* variables.
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "<your-service-name>"}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)

    # Use "metadata_only" to leave prompts and responses out of the SDK spans.
    client = Anthropic(
        open_telemetry={
            "tracer_provider": provider,
            "traces": {"content_mode": "content"},
        }
    )
    ```

When you call the SDK inside one of your own spans, the SDK sends the trace context to the API, and the API spans nest under your application's spans in one trace. For other languages and SDK options, refer to [Use OpenTelemetry with the Claude SDK](https://platform.claude.com/docs/en/manage-claude/opentelemetry/sdk) in the Anthropic documentation.

## Avoid counting tokens twice [count-tokens]

Some Claude Platform spans report the same token usage, so summing usage across all spans counts tokens more than once. To count each token once, follow these rules from Anthropic:

* **Messages API requests**: Sum the `anthropic.model_request` spans, plus any `anthropic.compaction` spans. Don't also sum the `anthropic.messages.create` span, which reports the same tokens.
* **Managed Agents sessions**: Sum the `anthropic.model_request` and `anthropic.session.outcome_evaluation` spans.
* **SDK spans**: If you also send SDK spans, each Messages API request has two `anthropic.messages.create` spans that report the same usage. Count only the API span, which has span kind `SERVER`, and skip the SDK span, which has span kind `CLIENT`.

Input token counts already include tokens read from and written to the prompt cache, so don't add the cache attributes to them. Anthropic can deliver the same span more than once, so count each span once by its trace ID and span ID. For details, refer to [Counting tokens](https://platform.claude.com/docs/en/manage-claude/opentelemetry#count-tokens) in the Anthropic documentation.

For example, the following {{esql}} query sums token usage by model:

```esql
FROM traces-*
| WHERE service.name == "claude-platform"
    AND name IN ("anthropic.model_request", "anthropic.compaction", "anthropic.session.outcome_evaluation")
| STATS
    input_tokens = SUM(attributes.gen_ai.usage.input_tokens),
    output_tokens = SUM(attributes.gen_ai.usage.output_tokens)
  BY attributes.gen_ai.request.model
```

## Related pages

* [OpenTelemetry for the Claude API](https://platform.claude.com/docs/en/manage-claude/opentelemetry) (Anthropic documentation)
* [{{motlp}} reference](opentelemetry://reference/motlp.md)
* [LLM and agentic AI observability](/solutions/observability/applications/llm-observability.md)
* To collect other Anthropic data, use the [Anthropic](integration-docs://reference/anthropic.md) integration for compliance audit logs, the [Anthropic Metrics](integration-docs://reference/anthropic_metrics.md) integration for usage, cost, and rate limits, or the [Claude Code](integration-docs://reference/claude_code.md) integration for Claude Code telemetry.
