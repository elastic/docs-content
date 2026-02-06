---
applies_to:
  deployment:
    self: all
    ess: all
    ece: all
    eck: all
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-hosted
---

# GenAI search - High Availability [gen-ai-architecture]

**Architecture**

A high availability architecture that is performance-optimized for low-latency information retrieval using lexical, temporal, geospatial, and/or vector/semantic search, or a hybrid combination of each.

**When to use**
- Lexical, vector/semantic, temporal, geospatial, hybrid, and multi-modal search (text, audio, image, video).
- Generative AI applications such as assistants, agents, and agentic workflows using Retrieval Augmented Generation (RAG) and/or Model Context Protocol (MCP).
- Integrating with foundation models (Azure OpenAI, Anthropic, Amazon Bedrock, etc.) and re-ranking techniques for optimal relevance.
- Applications requiring low-latency time series analytics and natural language processing.
- Integration with common development frameworks for Large Language Models, including LlamaIndex, LangChain, and LangSmith.