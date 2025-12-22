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

AI is a core part of the Elastic platform. It augments features and helps you analyze your data more effectively. This page lists the AI-powered capabilities and features available to you in each solution, and provides links to more detailed information about each of them.

To learn about enabling and disabling these features in your deployment, refer to [](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

For pricing information, refer to [pricing](https://www.elastic.co/pricing).

## Requirements

- To use Elastic's AI-powered features, you need an appropriate subscription level or serverless feature tier. These vary by solution and feature. Refer to each feature's documentation to learn more.
- Most features require at least one working LLM connector. To learn about setting up large language model (LLM) connectors used by AI-powered features, refer to [](/explore-analyze/ai-features/llm-guides/llm-connectors.md). Elastic Managed LLM is available by default if your license supports it.

## AI-powered features on the Elastic platform

The following AI-powered features are available across the Elastic platform. These are core {{es}} capabilities that you can use regardless of your chosen solution or project type.

### Elastic {{infer-cap}}

[Elastic {{infer-cap}}](/explore-analyze/elastic-inference.md) enables you to use {{ml}} models to perform operations such as text embedding or reranking on your data.

To learn more, refer to:

- [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md):
A managed service that runs {{infer}} without the need of deploying a model, or managing infrastructure and resources.
- [Elastic Managed LLM connector](kibana://reference/connectors-kibana/elastic-managed-llm.md):
This connector enables you to use built-in LLMs vetted for GenAI product features across the platform.
- [The {{infer}} API](/explore-analyze/elastic-inference/inference-api.md):
This general-purpose API enables you to perform {{infer}} operations using EIS, your own models, or third-party services.

### Natural language processing models

Natural Language Processing (NLP) enables you to analyze natural language data and make predictions.  Elastic offers a range of [built-in NLP models](/explore-analyze/machine-learning/nlp/ml-nlp-built-in-models.md) such as the Elastic-trained [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) or [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md). You can also [deploy custom NLP models](/explore-analyze/machine-learning/nlp/ml-nlp-overview.md).

### AI-powered search

[AI-powered search](/solutions/search/ai-search/ai-search.md) helps you find data based on intent and contextual meaning using vector search technology, which uses {{ml}} models to capture meaning in content.

#### Semantic and hybrid search

Depending on your team's technical expertise and requirements, you can choose from two broad paths for implementing semantic search:

- For a minimal configuration, managed workflow use [semantic_text](https://www.elastic.co/docs/solutions/search/semantic-search/semantic-search-semantic-text).
- For more control over the implementation details, implement dense or sparse [vector search](https://www.elastic.co/docs/solutions/search/vector) manually.

[Hybrid search](/solutions/search/hybrid-search.md) combines traditional full-text search with AI-powered search for more powerful search experiences that serve a wider range of user needs.

### Semantic re-ranking

[Semantic re-ranking](/solutions/search/ranking/semantic-reranking.md) involves using ML models to reorder search results based on semantic similarity to queries, using models hosted in {{es}} or using third-party inference endpoints.

### Learning to Rank (LTR)

[Learning To Rank](/solutions/search/ranking/learning-to-rank-ltr.md) is an advanced feature that involves using trained ML models to build custom ranking functions for search. Best suited for use cases with substantial training data and requirements for highly customized relevance tuning.

## AI-powered features in the {{es}} solution/project type

The [{{es}}](/solutions/search.md) solution view (or project type in {{serverless-short}}) includes certain AI-powered features beyond the core {{es}} capabilities available on the Elastic platform.

### Agent Builder

[Agent Builder](/solutions/search/elastic-agent-builder.md) enables you to create AI agents that can interact with your {{es}} data, run queries, and provide intelligent responses. It provides a complete framework for building conversational AI experiences on top of your search infrastructure.

### AI assistant for {{es}}

[](/solutions/observability/observability-ai-assistant.md) helps you understand, analyze, and interact with your Elastic data throughout {{kib}}. It provides a chat interface where you can ask questions about the {{stack}} and your data, and provides contextual insights throughout {{kib}} that explain errors and messages and suggest remediation steps.

### Playground

[Playground](/solutions/elasticsearch-solution-project/playground.md) enables you to use large language models (LLMs) to understand, explore, and analyze your {{es}} data using retrieval augmented generation (RAG), via a chat interface. Playground is also very useful for testing and debugging your {{es}} queries, using the [retrievers](/solutions/search/retrievers-overview.md) syntax with the `_search` endpoint.

### Model context protocol

The [Model Context Protocol (MCP)](/solutions/elasticsearch-solution-project/mcp.md) lets you connect AI agents and assistants to your {{es}} data to enable natural language interactions with your indices.

## AI-powered features in {{observability}}

{{observability}}'s AI-powered features all require an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md). When you use one of these features, you can select any LLM connector that's configured in your environment. The connector you select for one feature does not affect which connector any other feature uses. For specific configuration instructions, refer to each feature's documentation.

### AI assistant for {{observability}}

[](/solutions/observability/observability-ai-assistant.md) helps you understand, analyze, and interact with your Elastic data throughout {{kib}}. It provides a chat interface where you can ask questions about the {{stack}} and your data, and provides [contextual insights](/solutions/observability/observability-ai-assistant.md#obs-ai-prompts) throughout {{kib}} that explain errors and messages and suggest remediation steps.

### Streams

[Streams](/solutions/observability/streams/streams.md) is an AI-assisted centralized UI within {{kib}} that streamlines common tasks like extracting fields, setting data retention, and routing data. Streams leverages AI in the following features:

* [Significant Events](/solutions/observability/streams/management/significant-events.md): Use AI to suggest queries based on your data that find important events in your stream.
* [Grok processing](/solutions/observability/streams/management/extract/grok.md#streams-grok-patterns): Use AI to generate grok patterns that extract meaningful fields from your data.
* [Partitioning](/solutions/observability/streams/management/partitioning.md): Use AI to suggest logical groupings and child streams based on your data when using wired streams.
* [Advanced settings](/solutions/observability/streams/management/advanced.md): Use AI to generate a [stream description](/solutions/observability/streams/management/advanced.md#streams-advanced-description) and a [feature identification](/solutions/observability/streams/management/advanced.md#streams-advanced-features) that other AI features, like significant events, use when generating suggestions.

## AI-powered features in {{elastic-sec}}

{{elastic-sec}}'s AI-powered features all require an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md). When you use one of these features, you can select any LLM connector that's configured in your environment. The connector you select for one feature does not affect which connector any other feature uses. For specific configuration instructions, refer to each feature's documentation.

### AI Assistant for Security

[Elastic AI Assistant for Security](/solutions/security/ai/ai-assistant.md) helps you with tasks such as alert investigation, incident response, and query generation throughout {{elastic-sec}}. It provides a chat interface where you can ask questions about the {{stack}} and your data, and provides contextual insights that explain errors and messages and suggest remediation steps.

This feature requires an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).


### Attack Discovery

[Attack Discovery](/solutions/security/ai/attack-discovery.md) uses AI to triage your alerts and identify potential threats. Each "discovery" represents a potential attack and describes relationships among alerts to identify related users and hosts, map alerts to the MITRE ATT&CK matrix, and help identify threat actors.

This feature requires an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).


### Automatic Migration

[Automatic Migration](/solutions/security/get-started/automatic-migration.md) uses AI to help you migrate Splunk assets to {{elastic-sec}} by translating them into the necessary format and adding them to your {{elastic-sec}} environment. It supports the following asset types:

* Splunk rules
* Splunk dashboards

This feature requires an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).


### Automatic Import

[Automatic Import](/solutions/security/get-started/automatic-import.md) helps you ingest data from sources that do not have prebuilt Elastic integrations. It uses AI to parse a sample of the data you want to ingest, and creates a new integration specifically for that type of data.

This feature requires an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).


### Automatic Troubleshooting

[Automatic troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md) uses AI to help you identify and resolve issues that could prevent {{elastic-defend}} from working as intended. It provides actionable insights into the following common problem areas:

* **Policy responses**: Detect warnings or failures in {{elastic-defend}}’s integration policies.
* **Third-party antivirus (AV) software**: Identify installed third-party antivirus (AV) products that might conflict with {{elastic-defend}}.

This feature requires an [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
