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

While Agent Builder works with any [configured model](/explore-analyze/ai-features/agent-builder/models.md), model performance varies. Refer to [recommended models](/explore-analyze/ai-features/agent-builder/models.md#recommended-models) to select a model that performs well for your intended use cases.

## {{observability}} capabilities

### Built-in skills
```{applies_to}
stack: preview 9.4+
serverless: preview
```

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

### Investigate an alert or the service map [observability-agent-investigation-requirements]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

{{agent-builder}} can start an investigation from the {{observability}} view where you spotted a problem. Use **Add to chat** in the header of an alert detail page, or **Investigate map** on the full **Service map** page. Each action opens a new conversation that already includes the context of what you were viewing, so the agent can begin investigating without you describing the problem first.

Both actions require:

- An Enterprise license on the {{stack}}, or the [Observability Complete feature tier](/solutions/observability/observability-serverless-feature-tiers.md#obs-subscription-features) on {{obs-serverless}}.
- The [Agent Builder chat experience](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).
- An available model through a supported inference endpoint or Generative AI connector, including preconfigured models. Refer to [Model configuration](/explore-analyze/ai-features/agent-builder/models.md).
- [Permission to use Agent Builder](/explore-analyze/ai-features/agent-builder/permissions.md) and read the data you want to investigate.

If an action is missing, check these requirements with your administrator.

#### Alert context [observability-agent-alert-context]

When you click **Add to chat** on an {{observability}} alert detail page, the new conversation includes an `observability.alert` attachment. The attachment identifies the selected alert so the agent can retrieve its full details, including the rule, status, reason, and related entities, using your permissions.

The conversation automatically starts with `Investigate this alert`. Follow the steps to [start an AI investigation from an alert](/solutions/observability/incident-management/view-alerts.md#observability-alert-ai-investigation).

#### Service map context [observability-agent-service-map-context]

When you click **Investigate map** on the full **Service map** page, the new conversation includes a **Service map context** attachment (`observability.service-map-context`). It captures these settings from the view:

- Time range
- Selected environment
- KQL query
- Selected service group
- Highlighted services

The attachment contains the view settings, not a snapshot of the map data. The agent retrieves data for the investigation and prioritizes highlighted services.

The service group is included as context but does not restrict the investigation's data queries to that group. The environment and KQL query filter service health information, but the topology can include connections from other environments.

For the entry point and the investigation's findings, refer to [Investigate the service map with AI](/solutions/observability/apm/service-map.md#service-map-ai-investigation).

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