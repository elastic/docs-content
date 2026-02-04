---
applies_to:
  stack: preview 9.3+
  serverless:
    security: preview 9.3+
products:
  - id: security
  - id: cloud-serverless
description: Learn how Elastic Agent Builder works with Elastic Security
---

# Agent Builder for Elastic Security

[Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) is Elastic's AI platform which includes a natural language chat interface, built-in agents and Elastic tools, and allows creating custom agents and tools for your use case. You can manage and interact with your agents using the {{kib}} UI or work programmatically. 

Agent Builder integrates tightly with {{elastic-sec}}, shipping with built-in agents and tools designed for security use cases, and you can create your own custom agents and tools to fit your specific needs. Combine your agents with [Elastic Workflows](/explore-analyze/workflows.md) to automatically isolate hosts, create cases, send notification messages to external platforms, and more. 

:::{note}
:applies_to: {stack: preview 9.3+, serverless: preview}
To use Agent Builder in Elastic Security, you need to [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md). 
:::

## Threat Hunting agent

Agent Builder features a built-in [Threat Hunting agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) designed to accelerate security investigations by synthesizing data from sources such as Alerts, Attack Discovery, and Entity Risk Scores. By default it includes the [platform core tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#platform-core-tools) and [security tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#security-tools). 

You can [clone the agent](/explore-analyze/ai-features/agent-builder/custom-agents.md#create-a-new-agent) to grant access to additional built-in or custom tools. To learn more about the available tools, refer to [](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md).

## Use Agent Builder and Workflows together

[Workflows](/explore-analyze/workflows.md) is an automation engine built into the Elastic platform. You can define workflows declaratively in YAML to create deterministic, event-driven automation, without building custom integrations or switching context from your Elastic environment. Combined with Agent Builder, Workflows enable you to:

- Reduce alert fatigue by automating responses to reduce manual triage
- Automate routine tasks
- Eliminate the need for external automation tools

Workflows are tightly integrated with Agent Builder functionalities:

- **Agents can trigger workflows** to take reliable, repeatable actions. For more information, refer to [](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md).

- **Workflows can call agents** when a step benefits from reasoning, language understanding, or other LLM capabilities. For more information, refer to [](/explore-analyze/workflows/steps.md).




## Examples: Agent Builder and Elastic Workflows

This section provides conceptual examples of what you can achieve with Agent Builder workflows. For specific examples of workflows, including complete annotated code samples, refer to the [elastic/workflows/security](https://github.com/elastic/workflows/tree/main/workflows/security) GitHub repo.

### Example 1: Run Attack Discovery using a workflow
You can create a workflow that:

 - Runs periodically, and initiates Attack Discovery when it runs
 - Sends any discovered attacks to the Threat Hunting agent to analyze and create a report 
 - Sends that report to a third-party incident management platform and sends alerts to your team

### Example 2: Triage an alert with a workflow
You can create a workflow that:

- Triggers automatically when a rule generates an alert
- Provides the alert data to the Threat Hunting agent with a pre-defined prompt such as `analyze this alert, check whether it's connected to existing attacks, and identify all implicated entities`
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

With Agent Builder, you can automate this process to speed it up and require less user input. For example, in response to the prompt `"Analyze alert abc123. What's the entity risk score for the affected host? Are there any related attack discoveries in the last 24 hours?"` Agent Builder (using the Threat Hunting agent and its assigned tools) would take the following actions:

- Fetch alert details (using `alerts_tool`)
- Retrieve entity risk scores (using `entity_risk_score_tool`)
- Search Attack Discovery for related attacks (using `attack_discovery_search_tool`)
- Return an actionable alert summary based on rich context


## Related resources

- [](/explore-analyze/ai-features/ai-chat-experiences.md)
- [](/explore-analyze/ai-features/elastic-agent-builder.md)
- [](/explore-analyze/workflows.md)