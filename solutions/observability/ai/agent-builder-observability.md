---
applies_to:
  stack: preview 9.3+
  serverless:
    observability: preview 9.3+
products:
  - id: observability
  - id: cloud-serverless
description: Learn how Elastic Agent Builder works with Elastic Observability
---

# Agent Builder for {{observability}}

[Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) is Elastic's AI platform which includes a natural language chat interface, built-in agents and Elastic tools, and allows creating custom agents and tools for your use case. You can manage and interact with your agents using the {{kib}} UI or work programmatically.

Agent Builder integrates tightly with {{observability}}, shipping with built-in agents and tools designed for observability use cases, and you can create your own custom agents and tools to fit your specific needs. Combine your agents with [Elastic Workflows](/explore-analyze/workflows.md) to automatically isolate hosts, create cases, send notification messages to external platforms, and more.

:::{note}
:applies_to: {stack: preview 9.3+, serverless: preview}
To use Agent Builder in {{observability}}, you need to [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).
:::

## Observability agent

Agent Builder features a built-in [Observability agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#observability-agent) designed to assist with infrastructure monitoring and application performance troubleshooting.

By default it includes the [platform core tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#platform-core-tools) and [Observability tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#observability-tools). You can [clone the agent](/explore-analyze/ai-features/agent-builder/custom-agents.md#create-a-new-agent) to create a version with access to additional built-in or custom tools. To learn more about the available tools, refer to [](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md).

## Use Agent Builder and Workflows together

[Workflows](/explore-analyze/workflows.md) is an automation engine built into the Elastic platform. You can define workflows declaratively in YAML to create deterministic, event-driven automation, without building custom integrations or switching context from your Elastic environment. Combined with Agent Builder, Workflows enable you to:

- Reduce alert fatigue by automating responses to reduce manual triage
- Automate routine tasks
- Eliminate the need for external automation tools

Workflows are tightly integrated with Agent Builder functionalities:

- **Agents can trigger workflows** to take reliable, repeatable actions. For more information, refer to [](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md).

- **Workflows can call agents** when a step benefits from reasoning, language understanding, or other LLM capabilities. For more information, refer to [](/explore-analyze/workflows/steps.md).

## Examples: Agent Builder and Elastic Workflows

For specific examples of workflows, including complete annotated code samples, refer to the [elastic/workflows/observability](https://github.com/elastic/workflows/tree/main/workflows/observability) GitHub repo.


## Related resources

- [](/explore-analyze/ai-features/ai-chat-experiences.md)
- [](/explore-analyze/ai-features/elastic-agent-builder.md)
- [](/explore-analyze/workflows.md)