---
applies_to:
  stack: ga 9.4+, preview 9.3
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Learn how Elastic Agent Builder works with Elastic Security.
---

# Agent Builder for Elastic Security

[Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) is Elastic's AI platform which includes a natural language chat interface, built-in agents and Elastic tools, and allows creating custom agents and tools for your use case. You can manage and interact with your agents using the {{kib}} UI or work programmatically. 

Agent Builder integrates tightly with {{elastic-sec}}, shipping with built-in agents and tools designed for security use cases, and you can create your own custom agents and tools to fit your specific needs. Combine your agents with [Elastic Workflows](/explore-analyze/workflows.md) to automatically isolate hosts, create cases, send notification messages to external platforms, and more. 

:::{note}
To use {{agent-builder}} in {{elastic-sec}}, you need to [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).
:::

## Recommended models

While Agent Builder works with any [configured LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md), model performance varies. Refer to the [LLM performance matrix for {{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md) to select a model that performs well for your intended use cases.

::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

## Elastic AI Agent and Security skills [elastic-ai-agent-security-skills]

{{elastic-sec}} uses the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) with modular [Security skills](skills-model.md). You enable the skills that match your role (for example, threat hunting, alert triage, or incident response), then chat with the same default agent instead of switching between separate built-in agents.

Read these pages next:

* [Elastic AI Agent, skills, and tools in {{elastic-sec}}](skills-model.md)
* [Security skills use cases](skills-use-cases.md)
* [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md) for the full platform reference

The standalone [Threat Hunting Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) is deprecated; hunting workflows use the Elastic AI Agent with the Threat Hunting skill. For details, refer to the built-in agents reference.

::::

::::{applies-item} { stack: preview =9.2, ga 9.3 }

## Threat Hunting agent [threat-hunting-agent-security]

Agent Builder features a built-in [Threat Hunting agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) designed to accelerate security investigations by synthesizing data from sources such as Alerts, Attack Discovery, and Entity Risk Scores. 

By default it includes the [platform core tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#platform-core-tools) and [security tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#security-tools). You can [clone the agent](/explore-analyze/ai-features/agent-builder/custom-agents.md#create-a-new-agent) to create a version with access to additional built-in or custom tools. To learn more about the available tools, refer to [Custom tools](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md).

::::

::::

## Use Agent Builder and Workflows together

[Workflows](/explore-analyze/workflows.md) is an automation engine built into the Elastic platform. You can define workflows declaratively in YAML to create deterministic, event-driven automation, without building custom integrations or switching context from your Elastic environment. Combined with Agent Builder, Workflows enable you to:

- Reduce alert fatigue by automating responses to reduce manual triage
- Automate routine tasks
- Eliminate the need for external automation tools

Workflows are tightly integrated with Agent Builder functionalities:

- Agents can trigger workflows to take reliable, repeatable actions. For more information, refer to [Workflow tools](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md).

- Workflows can call agents when a step benefits from reasoning, language understanding, or other LLM capabilities. For more information, refer to [Workflow steps](/explore-analyze/workflows/steps.md).

## Examples: Agent Builder and Elastic Workflows

This section provides conceptual examples of what you can achieve with Agent Builder workflows. For specific examples of workflows, including complete annotated code samples, refer to the [elastic/workflows/security](https://github.com/elastic/workflows/tree/main/workflows/security) GitHub repo.

::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

:::{note}
These flows use the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) with the relevant [Security skills](skills-model.md) enabled.
:::

::::

::::{applies-item} { stack: preview =9.2, ga 9.3 }

:::{note}
Substitute the standalone [Threat Hunting agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) where the examples mention the agent.
:::

::::

::::

### Example 1: Run Attack Discovery using a workflow

You can create a workflow that:

- Runs periodically, and initiates Attack Discovery when it runs
- Sends any discovered attacks to Agent Builder to analyze and create a report
- Sends that report to a third-party incident management platform and sends alerts to your team

### Example 2: Triage an alert with a workflow

You can create a workflow that:

- Triggers automatically when a rule generates an alert
- Provides the alert data to Agent Builder with a pre-defined prompt such as `analyze this alert, check whether it's connected to existing attacks, and identify all implicated entities`
- Creates a report based on what it finds and sends it to a Slack channel
- Suggests next steps

### Example 3: Alert triage using an Agent Builder prompt

When conducted manually, alert triage in {{elastic-sec}} typically includes multiple steps which consume analyst time:

- Receive alert
- Open alert flyout and review entity details
- Pivot to Risk Score page
- Search Attack Discovery for related attacks
- Manually correlate new alert with its context
- Make a triage decision

With Agent Builder, you can automate this process to speed it up and require less user input. For example, in response to the prompt `"Analyze alert abc123. What's the entity risk score for the affected host? Are there any related attack discoveries in the last 24 hours?"` Agent Builder would take the following actions:

- Fetch alert details (using `alerts_tool`)
- Retrieve entity risk scores (using `entity_risk_score_tool`)
- Search Attack Discovery for related attacks (using `attack_discovery_search_tool`)
- Return an actionable alert summary based on rich context

## Related resources

- [](/explore-analyze/ai-features/ai-chat-experiences.md)
- [](/explore-analyze/ai-features/elastic-agent-builder.md)
- [](/explore-analyze/workflows.md)
