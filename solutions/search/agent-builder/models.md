---
navigation_title: "Models"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Using different models in {{agent-builder}}

{{agent-builder}} uses large language models (LLMs) to power agent reasoning and decision-making. By default, agents use the Elastic Managed LLM, but you can configure other models through Kibana connectors.

## Default model configuration

By default, {{agent-builder}} uses the Elastic Managed LLM connector running on the [Elastic Inference Service](/explore-analyze/elastic-inference/eis.md) {applies_to}`serverless: preview` {applies_to}`ess: preview 9.2`. 

This managed service requires zero setup and no additional API key management.

Learn more about the [Elastic Managed LLM connector](kibana://reference/connectors-kibana/elastic-managed-llm.md) and [pricing](https://www.elastic.co/pricing).

## Change the default model

By default, {{agent-builder}} uses the Elastic Managed LLM. To use a different model, select a configured connector and set it as the default.

### Use a pre-configured connector

1. Search for **GenAI Settings** in the global search field
2. Select your preferred connector from the **Default AI Connector** dropdown
3. Save your changes

### Create a new connector in the UI

1. Find connectors under **Alerts and Insights / Connectors** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md)
2. Select **Create Connector** and select your model provider
3. Configure the connector with your API credentials and preferred model
4. Search for **GenAI Settings** in the global search field
5. Select your new connector from the **Default AI Connector** dropdown under **Custom connectors**
6. Save your changes

For detailed instructions on creating connectors, refer to [Connectors](https://www.elastic.co/docs/deploy-manage/manage-connectors).

Learn more about [preconfigured connectors](https://www.elastic.co/docs/reference/kibana/connectors-kibana/pre-configured-connectors).

#### Connect a local LLM

You can connect a locally hosted LLM to Elastic using the OpenAI connector. This requires your local LLM to be compatible with the OpenAI API format.

Refer to the [OpenAI connector documentation](kibana://reference/connectors-kibana/openai-action-type.md) for detailed setup instructions.

## Connectors API

For programmatic access to connector management, refer to the [Connectors API documentation]({{kib-serverless-apis}}group/endpoint-connectors).

## Recommended models

{{agent-builder}} requires models with strong reasoning and tool-calling capabilities. State-of-the-art models perform significantly better than smaller or older models.

The following models are known to work well with {{agent-builder}}:

- **OpenAI**: GPT-4.1, GPT-4o
- **Anthropic**: Claude Sonnet 4.5, Claude Sonnet 4, Claude Sonnet 3.7
- **Google**: Gemini 2.5 Pro

### Why model quality matters

Agent Builder relies on advanced LLM capabilities including:

- **Function calling**: Models must accurately select appropriate tools and construct valid parameters from natural language requests
- **Multi-step reasoning**: Agents need to plan, execute, and adapt based on tool results across multiple iterations
- **Structured output**: Models must produce properly formatted responses that the agent framework can parse

Smaller or less capable models may produce errors like:

```console-response
Error: Invalid function call syntax
```

```console-response
Error executing agent: No tool calls found in the response.
```

While any chat-completion-compatible connector can technically be configured, we strongly recommend using state-of-the-art models for reliable agent performance.

:::{note}
GPT-4o-mini and similar smaller models are not recommended for {{agent-builder}} as they lack the necessary capabilities for reliable agent workflows.
:::

## Related resources

- [Limitations and known issues](limitations-known-issues.md): Current limitations around model selection
- [Get started](get-started.md): Initial setup and configuration
- [Connectors](/deploy-manage/manage-connectors.md): Detailed connector configuration guide
