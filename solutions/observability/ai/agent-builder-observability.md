---
applies_to:
  stack: preview 9.3+
  serverless:
    observability: preview
products:
  - id: observability
  - id: cloud-serverless
description: Learn how Elastic Agent Builder works with Elastic Observability
---

# Agent Builder for {{observability}}

[Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) is Elastic's AI platform which includes a natural language chat interface, built-in agents and Elastic tools, and allows creating custom agents and tools for your use case. You can manage and interact with your agents using the {{kib}} UI or work programmatically.

Agent Builder integrates tightly with {{observability}}, shipping with built-in agents and tools designed for observability use cases, and you can create your own custom agents and tools to fit your specific needs. Combine your agents with [Elastic Workflows](/explore-analyze/workflows.md) to automatically isolate hosts, create cases, send notification messages to external platforms, and more.

:::{note}
- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` {{agent-builder}} is the default chat experience in {{observability}}.
- {applies_to}`stack: preview =9.3` In {{stack}} version 9.3, you need to [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md) to use Agent Builder in {{observability}}.
:::

## Recommended models

While Agent Builder works with any [configured LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md), model performance varies. Refer to [recommended models](/explore-analyze/ai-features/agent-builder/models.md#recommended-models) to select a model that performs well for your intended use cases.

## {{observability}} capabilities

::::{applies-switch}

:::{applies-item} { stack: preview 9.4+, serverless: preview }

The Elastic AI Agent includes built-in [{{observability}} skills](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#observability-skills) designed to assist with infrastructure monitoring, application performance troubleshooting, and root cause analysis.

By default it includes the [`observability.investigation`](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-observability-investigation-skill) skill. You can [create a custom skill](/explore-analyze/ai-features/agent-builder/custom-skills.md) to extend the agent's capabilities for your specific use case. To learn more about the available skills, refer to [](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md).

### Time range awareness

```{applies_to}
stack: ga 9.4+
serverless: ga
```

When you chat with the agent from an {{observability}} UI, it uses the current page's time picker as the default time range when invoking tools, unless you specify a different range in your prompt. Outside of a UI context, tools fall back to their built-in defaults.

### Synthetics monitor context

```{applies_to}
stack: ga 9.4+
serverless: ga
```

When you chat with the agent from a Synthetics monitor detail page, it automatically has access to the monitor's configuration via the `observability.monitor` attachment. This context is available on all monitor detail tabs (Overview, History, Errors, and Alerts), and includes:

- Monitor name, type, and schedule
- Configured locations (public and private)
- Tags

:::

:::{applies-item} stack: preview =9.3, removed =9.4

Agent Builder features a built-in [{{observability}} agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#observability-agent) designed to assist with infrastructure monitoring and application performance troubleshooting.

By default it includes some of the [platform core tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#platform-core-tools) and [{{observability}} tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#observability-tools). You can [clone the agent](/explore-analyze/ai-features/agent-builder/custom-agents.md#create-a-new-agent) to create a version with access to additional built-in or custom tools. To learn more about the available tools, refer to [](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md).

:::

::::

## Use Agent Builder and Workflows together

[Workflows](/explore-analyze/workflows.md) is an automation engine built into the Elastic platform. You can define workflows declaratively in YAML to create deterministic, event-driven automation, without building custom integrations or switching context from your Elastic environment. Combined with Agent Builder, Workflows enable you to:

- Reduce alert fatigue by automating responses to reduce manual triage
- Automate routine tasks
- Eliminate the need for external automation tools

Workflows are tightly integrated with Agent Builder functionalities:

- **Agents can trigger workflows** to take reliable, repeatable actions. For more information, refer to [](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md).

- **Workflows can call agents** when a step benefits from reasoning, language understanding, or other LLM capabilities. For more information, refer to [](/explore-analyze/workflows/steps.md).

## Examples: Agent Builder and Elastic Workflows

For an end-to-end documented example, refer to [Automate root cause analysis for an {{observability}} alert](/explore-analyze/workflows/use-cases/observability/root-cause-analysis.md), which invokes an Agent Builder agent on each alert, opens a case populated with the analysis, and supports configurable next-step branches.

For additional examples, including complete annotated code samples, refer to the [elastic/workflows/observability](https://github.com/elastic/workflows/tree/main/workflows/observability) GitHub repo.


## Related resources

- [](/explore-analyze/ai-features/ai-chat-experiences.md)
- [](/explore-analyze/ai-features/elastic-agent-builder.md)
- [](/explore-analyze/workflows.md)