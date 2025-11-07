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

AI is built into many parts of the {{stack}}. This page describes Elastaic's AI-powered features, organized by solution, and provides links to more detailed information about each of them.

To learn about enabling and disabling these features in your deployment, refer to [](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). 

## Requirements 

To use Elastic's AI-powered features, you need:

- An appropriate license and feature tier. These vary by solution and feature. Refer to each feature's documentation to learn more.
- At least one working LLM connector. To learn about setting up large language model (LLM) connectors used by AI-powered features, refer to [](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).


## AI-powered features in {{es}}

### Agent builder

```{applies_to}
[Agent Builder](/solutions/search/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, execute queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.
serverless:
  elasticsearch: preview
  observability: unavailable
  security: unavailable
```

[Agent Builder](/solutions/search/elastic-agent-builder.md) enables you to create AI agents that can interact with your Elasticsearch data, execute queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### AI Assistant
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

[AI-powered search](/solutions/search/ai-search/ai-search.md) helps you find data based on intent and contextual meaning using vector search technology, which uses machine learning models to capture meaning in content.  

Depending on your team's technical expertise and requirements, you can choose from two broad paths:  

- For a minimal configuration, managed workflow use [semantic_text](https://www.elastic.co/docs/solutions/search/semantic-search/semantic-search-semantic-text) 
- For more control over the implementation details, implement dense or sparse [vector search](https://www.elastic.co/docs/solutions/search/vector) 

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

### AI Assistant
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

[Streams](/solutions/observability/streams/streams.md) provides a single, centralized UI within Kibana that streamlines common tasks like extracting fields, setting data retention, and routing data, so you don't need to use multiple applications or manually configure underlying Elasticsearch components. Streams incorporates AI in the following ways:

#### Generate significant events with AI
```{applies_to}
serverless: ga
stack: preview 9.1, ga 9.2
```
[Significant Events](/solutions/observability/streams/management/significant-events.md) periodically runs a query on your stream to find important events. These can include error messages, exceptions, and other relevant log messages. You can use AI to suggest queries based on previously identified significant events in your Stream.

#### Generate Grok patterns
```{applies_to}
serverless: ga
stack: preview 9.1, ga 9.2
```
You can [generate Grok patterns](/solutions/observability/streams/management/extract/grok.md#streams-grok-patterns) using AI instead of writing them by hand. 

#### Generate stream descriptions and feature identification
```{applies_to}
serverless: ga
stack: preview 9.1, ga 9.2
```
On the Streams [advanced settings](/solutions/observability/streams/management/advanced.md) page, you can use AI to generate your [stream description](/solutions/observability/streams/management/advanced.md#streams-advanced-description) and [feature identification](/solutions/observability/streams/management/advanced.md#streams-advanced-features).

## AI-powered features in {{elastic-sec}}

### AI Assistant for Security
```{applies_to}
stack: all
serverless:
  security: all
```

[Elastic AI Assistant for Security](/solutions/security/ai/ai-assistant.md) helps you interact with your {{elastic-sec}} data and assists with tasks such as alert investigation, incident response, and query generation. It provides a chat interface where you can ask questions about the {{stack}} and your data, and provides contextual insights throughout {{kib}} that explain errors and messages and suggest remediation steps.

### Attack Discovery
```{applies_to}
stack: ga
serverless:
  security: ga
```

[Attack Discovery](/solutions/security/ai/attack-discovery.md) leverages large language models (LLMs) to analyze alerts in your environment and identify threats. Each "discovery" represents a potential attack and describes relationships among multiple alerts to tell you which users and hosts are involved, how alerts correspond to the MITRE ATT&CK matrix, and which threat actor might be responsible. This can help make the most of each security analyst’s time, fight alert fatigue, and reduce your mean time to respond.

### Automatic Migration

[Automatic Migration](/solutions/security/get-started/automatic-migration.md) helps you quickly migrate Splunk assets to {{elastic-sec}}. The following asset types are supported:

* {applies_to}`stack: preview 9.0, ga 9.1` {applies_to}`serverless: ga` Splunk rules
* {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Splunk dashboards

### Automatic Import
```{applies_to}
stack: ga
serverless:
  security: ga
```

[Automatic Import](/solutions/security/get-started/automatic-import.md) helps you quickly parse, ingest, and create ECS mappings for data from sources that don’t yet have prebuilt Elastic integrations. This can accelerate your migration to {{elastic-sec}}, and help you quickly add new data sources to an existing SIEM solution in {{elastic-sec}}. 

### Automatic Troubleshooting
```{applies_to}
stack: ga 9.2, preview 9.0
serverless:
  security: ga
```
[Automatic troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md) helps you identify and resolve issues that could prevent {{elastic-defend}} from working as intended. It provides actionable insights into the following common problem areas:

* {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga` **Policy responses**: Detect warnings or failures in {{elastic-defend}}’s integration policies.
* **Third-party antivirus (AV) software**: Identify installed third-party antivirus (AV) products that may conflict with {{elastic-defend}}.

This helps you resolve configuration errors, address incompatibilities, and ensure that your hosts remain protected.