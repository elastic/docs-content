---
applies_to:
  stack: preview 9.3+
  serverless:
    security: preview 9.3+
products:
  - id: security
  - id: cloud-serverless
---

# Agent Builder for Elastic Security

[Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) is Elastic's AI platform which includes a natural language chat interface, built-in agents and Elastic tools, and allows creating custom agents and tools for your use case. You can manage and interact with your agents using the {{kib}} UI or work programmatically. 

For {{elastic-sec}} specifically, it can provide automation capabilities for a wide range of tasks to help your team achieve more. 

You can create custom agents equipped with additional tools, and create Elastic Workflows that can automatically isolate hosts, create cases, send notification messages to external platforms, and more. 

:::{note}
:applies_to: {stack: preview 9.3+, serverless: preview}
Agent builder is in technical preview. To use it in Elastic Security, you need to [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md). 
:::

## The Threat Hunting agent

Agent Builder features a pre-built [Threat Hunting agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) designed to accelerate security investigations by synthesizing data from Alerts, Attack Discovery, Entity Risk Scores, and Elastic Security Labs. By default it includes the [platform core tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#platform-core-tools) and [security tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#security-tools). 

You can customize it by giving it access to additional built-in tools, or to your own [custom tools](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md). 

To learn more about the types of Agent Builder tools that you can create, refer to [](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md).

## Use Agent Builder and Workflows together

[Workflows](/explore-analyze/workflows.md) lets you augment your team's capabilities for responding to threats by setting up automated processes that use a wide range of tools, without needing an external automation platform. 

There are two main ways to use workflows alongside Agent Builder:

- **Enable an agent to run workflows:** You can allow custom agents to independently start workflows. For more information, refer to [](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md).
- **Add AI-powered steps to your workflows:** AI steps introduce reasoning and language understanding into workflows. Use AI steps to process natural language, make context-aware decisions, or operate through agents. For more information, refer to [](/explore-analyze/workflows/steps.md)

In combination, these tools can help:

- Reduce alert fatigue by automating responses to reduce manual triage
- Automate routine tasks
- Eliminate the need for external automation tools


## Examples: Agent Builder and Elastic Workflows

This section provides conceptual examples of what you can achieve with Agent Builder workflows. For specific examples of workflows, including complete annotated code samples, refer to the [elastic/workflows/security](https://github.com/elastic/workflows/tree/main/workflows/security) GitHub repo.

### Example 1: Run Attack Discovery using a workflow
You can create a workflow that:

 - Runs periodically, and initiates Attack Discovery when it runs
 - Sends any discovered attacks to the Threat Hunting agent to analyze and create a report 
 - Sends that report to a third-party incident management platform and sends alerts to your team

### Example 3: Triage an alert with a workflow
You can create a workflow that:

- Runs manually on an alert of your choosing
- Provides the alert data to the Threat Hunting agent with a pre-defined prompt such as `analyze this alert, check whether it's connected to existing attacks, and identify all implicated entities`
- Creates a report based on what it finds and sends it to a Slack channel
- Suggests next steps

### Example 3: Alert an triage using an Agent Builder prompt
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

