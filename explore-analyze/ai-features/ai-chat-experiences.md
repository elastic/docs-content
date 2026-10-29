---
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# AI chat experiences


{{kib}} AI chat helps you answer questions about your data, suggest next steps, and explain how to use Elastic's software.

- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) is the default AI chat experience across {{kib}}. It includes built-in agents and [tools](/explore-analyze/ai-features/agent-builder/tools.md) for common tasks, and you can create custom agents, tools, and [skills](/explore-analyze/ai-features/agent-builder/skills.md) for your own use cases.
- {applies_to}`stack: ga =9.3` Agent Builder is the default for {{es}} solution users. {{product.observability}} and {{product.security}} solution users can switch to Agent Builder to opt in.
- {applies_to}`stack: deprecated` {applies_to}`serverless: deprecated`
[AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-assistant.md) was Elastic's original AI chat. Users should [](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).

To get started, refer to [Get started with {{agent-builder}}](/explore-analyze/ai-features/agent-builder/get-started.md). For connectors and tested models, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md) and [Recommended models](/explore-analyze/ai-features/agent-builder/models.md#recommended-models). To install Elastic documentation for better answers, refer to [Give {{agent-builder}} access to Elastic documentation](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#give-agent-builder-access-to-elastic-documentation).


