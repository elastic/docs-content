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

:::{applies-item} { stack: ga 9.4+, serverless: ga }

## Elastic AI Agent and Security skills [elastic-ai-agent-security-skills]

{{elastic-sec}} uses the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) with modular [Security skills](skills-model.md). You enable the skills that match your role (for example, threat hunting, alert triage, or incident response), then chat with the same default agent instead of switching between separate built-in agents.

Read these pages next:

* [Elastic AI Agent, skills, and tools in {{elastic-sec}}](skills-model.md)
* [Security skills use cases](skills-use-cases.md)
* [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md) for the full platform reference

The standalone [Threat Hunting Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) is deprecated. Hunting use cases now use the Elastic AI Agent with the Threat Hunting skill. For details, refer to the built-in agents reference.

:::

:::{applies-item} { stack: preview =9.2, ga 9.3 }

## Threat Hunting agent [threat-hunting-agent-security]

Agent Builder features a built-in [Threat Hunting agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) designed to accelerate security investigations by synthesizing data from sources such as Alerts, Attack Discovery, and Entity Risk Scores. 

By default it includes the [platform core tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#platform-core-tools) and [security tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#security-tools). You can [clone the agent](/explore-analyze/ai-features/agent-builder/custom-agents.md#create-a-new-agent) to create a version with access to additional built-in or custom tools. To learn more about the available tools, refer to [Custom tools](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md).

:::

::::

## Create and refine detection rules in Agent Builder [create-and-refine-detection-rules-in-agent-builder]

```{applies_to}
stack: ga 9.4
serverless:
  security: ga
```

You can pass a detection rule into the Agent Builder chat so you can ask questions about it, get suggestions for improving rule fields, or request an appropriate investigation guide, without copying and pasting rule content between the UI and the chat. Open Agent Builder with a rule in context from any of these places:

- **AI rule creation**: On the [Detection rules (SIEM)](/solutions/security/detect-and-alert/manage-detection-rules.md) page, choose **Create a rule > AI rule creation**. The flyout opens with an empty rule attachment and a prefilled prompt for an {{esql}} detection rule with the main rule fields. You can edit the prompt before sending the message.
- **Rule details**: Open a rule from the list, then use **Add to chat** on the rule details page.
- **Rule form (create or edit)**: While [creating](/solutions/security/detect-and-alert/using-the-rule-ui.md) or [editing](/solutions/security/detect-and-alert/manage-detection-rules.md#edit-single-rule) a rule, use **Add to chat** to send the current rule draft.
- **Alerts flyout**: Open an alert, expand the rule summary in the flyout, then use **Add to chat**.
- **Alerts table rule flyout**: From the alerts table, open the rule flyout for an alert and use **Add to chat**.

This flow opens Agent Builder with a security session context and the default agent used in {{elastic-sec}} (the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent)).

Security skills such as `threat-hunting` and `alert-analysis` activate as needed based on your prompts. When the assistant responds, the rule appears in the chat as a rich attachment that shows the rule type, description, query with syntax highlighting, index patterns, tags, severity and risk score, and schedule. It draws on the attached rule to help with detection intent, query logic, MITRE ATT&CK coverage, timing and scheduling, and rule metadata quality.

:::{note}
Agent Builder only has access to the fields included in the rule attachment. It does not retrieve [exception lists](/solutions/security/detect-and-alert/add-manage-exceptions.md). Rules reference exceptions by ID only.
:::

If your role has the [privileges required to manage detection rules](/solutions/security/detect-and-alert/detections-privileges.md), use **Apply to creation** or **Update rule** on that attachment to open the create or edit rule form with the fields filled in. 

If your role does not have access to managing rules, the actions aren't shown. On the **Create rule** or **Edit rule** page, when the Agent Builder flyout is open at the same time, the rule fields in the form and the rule attachment in the chat update together when you edit either side.

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

:::{note}
:applies_to: { stack: ga 9.4+, serverless: ga }
These flows use the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) with the relevant [Security skills](skills-model.md) enabled.
:::

:::{note}
:applies_to: { stack: preview =9.2, ga 9.3 }
Substitute the standalone [Threat Hunting agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) where the examples mention the agent.
:::

### Example 1: Run Attack Discovery using a workflow

You can create a workflow that:

 - Runs periodically, and initiates Attack Discovery when it runs
 - Sends any discovered attacks to an AI agent to analyze and create a report
 - Sends that report to a third-party incident management platform and sends alerts to your team

### Example 2: Triage an alert with a workflow

You can create a workflow that:

- Triggers automatically when a rule generates an alert
- Provides the alert data to an AI agent with a pre-defined prompt such as `analyze this alert, check whether it's connected to existing attacks, and identify all implicated entities`
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

With Agent Builder, you can automate this process to speed it up and require less user input. For example, in response to the prompt `"Analyze alert abc123. What's the entity risk score for the affected host? Are there any related attack discoveries in the last 24 hours?"` an AI agent would take the following actions:

- Fetch alert details (using `alerts_tool`)
- Retrieve entity risk scores (using `entity_risk_score_tool`)
- Search Attack Discovery for related attacks (using `attack_discovery_search_tool`)
- Return an actionable alert summary based on rich context

## Related resources

- [](/explore-analyze/ai-features/ai-chat-experiences.md)
- [](/explore-analyze/ai-features/elastic-agent-builder.md)
- [](/explore-analyze/workflows.md)
