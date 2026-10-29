---
applies_to:
  stack: preview 9.3+
  serverless: preview
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# AI chat experiences

AI chat can help with a wide range of tasks throughout {{kib}}, such as helping to answer questions about your data, suggesting next steps, and explaining how to use Elastic's software.

There are two AI chat experiences which you can choose from:

- {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview` **AI Agent**: Powered by [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md), this chat experience lets you create custom agents for specific tasks, with specialized tools, and provides a unified chat experience across all of {{kib}}. Agent Builder is the default chat experience starting in 9.4.
- [AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-assistant.md): Elastic's original AI chat. {applies_to}`stack: deprecated 9.4+` {applies_to}`serverless: deprecated` The AI Assistant for {{observability}} and {{es}} is deprecated. {applies_to}`stack: deprecated 9.6+` {applies_to}`serverless: deprecated` AI Assistant for Security is deprecated. Both assistants still work, but they won't get new features. The AI Assistant for {{observability}} and {{es}} operates independently from the AI Assistant for Security.

If {{kib}} cannot use Elastic's public knowledge base artifact host—for example in air-gapped or restricted networks—refer to [Host a knowledge base artifact repo for AI Assistant](ai-chat-experiences/ai-assistant-host-doc-artifacts.md).

Refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md) for connectors and tested models. For {{agent-builder}}, refer to [Recommended models](/explore-analyze/ai-features/agent-builder/models.md#recommended-models).

To switch from AI Assistant to Agent Builder and find feature equivalents, refer to [](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).