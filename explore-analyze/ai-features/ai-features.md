---
navigation_title: AI-powered features
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# AI-powered features

AI is a core part of the {{stack}}. It augments certain features and helps you analyze your data more effectively. This page lists the AI-powered capabilities and features available to you in each solution, and provides links to more detailed information about each of them.

To learn about enabling and disabling these features in your deployment, refer to [](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

For pricing information, refer to [pricing](https://www.elastic.co/pricing).

## Requirements

- To use Elastic's AI-powered features, you need an appropriate license and feature tier. These vary by solution and feature. Refer to each feature's documentation to learn more.
- Most features require at least one working LLM connector. To learn about setting up large language model (LLM) connectors used by AI-powered features, refer to [](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md). Elastic Managed LLM is available by default if your license supports it. 

## AI-powered features on the Elastic platform

### Elastic {{infer-cap}}
```{applies_to}
stack:
serverless:
```

[Elastic {{infer-cap}}](/explore-analyze/elastic-inference.md) enables you to use {{ml}} or AI models to make predictions or enact operations — such as text embedding, or reranking - on your data.

To learn more, refer to:

- [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md): a managed service that runs {{infer}} outside your cluster resources.
- [The {{infer}} API](/explore-analyze/elastic-inference/inference-api.md): a general-purpose API that enables you to run {{infer}} using EIS, your own models, or third-party services.

### Natural language processing
```{applies_to}
stack:
serverless:
```
Natural Language Processing (NLP) enables you to analyze natural language data and make predictions.

Elastic offers a range of [built-in NLP models](/explore-analyze/machine-learning/nlp/ml-nlp-built-in-models.md) such as the Elastic-trained [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md). You can also [deploy custom models](/explore-analyze/machine-learning/nlp/ml-nlp-overview.md).

## AI-powered features in {{es}}

### Agent builder

```{applies_to}
serverless:
  elasticsearch: preview
  observability: unavailable
  security: unavailable
```

[Agent Builder](/solutions/search/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, run queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### AI assistant for {{es}}
```{applies_to}
stack:
serverless:
```

[](/solutions/observability/observability-ai-assistant.md) helps you understand, analyze, and interact with your Elastic data throughout {{kib}}. It provides a chat interface where you can ask questions about the {{stack}} and your data, and provides contextual insights throughout {{kib}} that explain errors and messages and suggest remediation steps.

### AI-powered search
```{applies_to}
stack:
serverless:
```

[AI-powered search](/solutions/search/ai-search/ai-search.md) helps you find data based on intent and contextual meaning using vector search technology, which uses {{ml}} models to capture meaning in content.

Depending on your team's technical expertise and requirements, you can choose from two broad paths:

- For a minimal configuration, managed workflow use [semantic_text](https://www.elastic.co/docs/solutions/search/semantic-search/semantic-search-semantic-text) which is the recommended way to perform semantic search.
- For more control over the implementation details, implement dense or sparse [vector search](https://www.elastic.co/docs/solutions/search/vector).

### Hybrid search
```{applies_to}
stack:
serverless:
```

[Hybrid search](/solutions/search/hybrid-search.md) combines traditional full-text search with AI-powered search for more powerful search experiences that serve a wider range of user needs.

### Playground
```{applies_to}
stack: preview 9.0, beta 9.1
serverless: beta
```

[Playground](/solutions/search/rag/playground.md) enables you to use large language models (LLMs) to understand, explore, and analyze your {{es}} data using retrieval augmented generation (RAG), via a chat interface. Playground is also very useful for testing and debugging your {{es}} queries, using the [retrievers](/solutions/search/retrievers-overview.md) syntax with the `_search` endpoint.

### Model context protocol
```{applies_to}
stack:
serverless:
```

The [Model Context Protocol (MCP)](/solutions/search/mcp.md) lets you connect AI agents and assistants to your {{es}} data to enable natural language interactions with your indices.

## AI-powered features in {{observability}}

### AI assistant for {{observability}}
```{applies_to}
stack:
serverless:
```

[](/solutions/observability/observability-ai-assistant.md) helps you understand, analyze, and interact with your Elastic data throughout {{kib}}. It provides a chat interface where you can ask questions about the {{stack}} and your data, and provides [contextual insights](/solutions/observability/observability-ai-assistant.md#obs-ai-prompts) throughout {{kib}} that explain errors and messages and suggest remediation steps.

### Streams
```{applies_to}
serverless: ga
stack: preview 9.1, ga 9.2
```

[Streams](/solutions/observability/streams/streams.md) is an AI-assisted centralized UI within {{kib}} that streamlines common tasks like extracting fields, setting data retention, and routing data. Streams incorporates AI in the following features:

* [Significant Events](/solutions/observability/streams/management/significant-events.md): Use AI to suggest queries based on your data that find important events in your stream.
* [Grok processing](/solutions/observability/streams/management/extract/grok.md#streams-grok-patterns): Use AI to generate grok patterns that extract meaningful fields from your data.
* [Partitioning](/solutions/observability/streams/management/partitioning.md): {applies_to}`stack: preview 9.2` Use AI to suggest logical groupings and child streams based on your data when using wired streams.
* [advanced settings](/solutions/observability/streams/management/advanced.md): Use AI to generate a [stream description](/solutions/observability/streams/management/advanced.md#streams-advanced-description) and a [feature identification](/solutions/observability/streams/management/advanced.md#streams-advanced-features) that other AI features, like significant events, use when generating suggestions.

## AI-powered features in {{elastic-sec}}

{{elastic-sec}}'s AI-powered features all require an [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md). When you use one of these features, you can select any LLM connector that's configured in your environment. The connector you select for one feature does not affect which connector any other feature uses. For specific configuration instructions, refer to each feature's documentation.

### AI Assistant for Security
```{applies_to}
stack: all
serverless:
  security: all
```

[Elastic AI Assistant for Security](/solutions/security/ai/ai-assistant.md) helps you with tasks such as alert investigation, incident response, and query generation throughout {{elastic-sec}}. It provides a chat interface where you can ask questions about the {{stack}} and your data, and provides contextual insights that explain errors and messages and suggest remediation steps.

:::{note}
This feature requires an [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
:::

### Attack Discovery
```{applies_to}
stack: ga
serverless:
  security: ga
```

[Attack Discovery](/solutions/security/ai/attack-discovery.md) uses AI to triage your alerts and identify potential threats. Each "discovery" represents a potential attack and describes relationships among alerts to identify related users and hosts, map alerts to the MITRE ATT&CK matrix, and help identify threat actors. 

:::{note}
This feature requires an [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
:::

### Automatic Migration

[Automatic Migration](/solutions/security/get-started/automatic-migration.md) uses AI to help you migrate Splunk assets to {{elastic-sec}} by translating them into the necessary format and adding them to your {{elastic-sec}} environment. It supports the following asset types:

* {applies_to}`stack: preview 9.0, ga 9.1` {applies_to}`serverless: ga` Splunk rules
* {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Splunk dashboards

:::{note}
This feature requires an [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
:::

### Automatic Import
```{applies_to}
stack: ga
serverless:
  security: ga
```

[Automatic Import](/solutions/security/get-started/automatic-import.md) helps you ingest data from sources that do not have prebuilt Elastic integrations. It uses AI to parse a sample of the data you want to ingest, and creates a new integration specifically for that type of data.

:::{note}
This feature requires an [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
:::

### Automatic Troubleshooting
```{applies_to}
stack: ga 9.2, preview 9.0
serverless:
  security: ga
```
[Automatic troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md) uses AI to help you identify and resolve issues that could prevent {{elastic-defend}} from working as intended. It provides actionable insights into the following common problem areas:

* {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga` **Policy responses**: Detect warnings or failures in {{elastic-defend}}’s integration policies.
* **Third-party antivirus (AV) software**: Identify installed third-party antivirus (AV) products that might conflict with {{elastic-defend}}.

:::{note}
This feature requires an [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
:::