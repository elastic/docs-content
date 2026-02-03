---
applies_to:
  stack: preview 9.3+
  serverless:
    security: preview 9.3+
products:
  - id: security
  - id: cloud-serverless
---

# Agent Builder

[Agent Builder](/explore-analyze/ai-features/agent-builder/get-started.md) is Elastic's agent creation platform that integrates into {{kib}} and allows you to design custom agents with specialized tool access. For {{elastic-sec}} specifically, it can provide automation capabilities for a wide range of tasks to help your team achieve more. 

You can create custom agents equipped with additional tools, and create Elastic Workflows that can automatically isolate hosts, create cases, send notification messages to external platforms, and more. 

:::{note}
:applies_to: {stack: preview 9.3+, serverless: preview}
Agent builder is in technical preview. To use it in Elastic Security, you need to [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md). 
:::

## The Threat Hunting agent

Agent Builder features a pre-built [Threat Hunting agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) designed to accelerate security investigations by synthesizing data from Alerts, Attack Discovery, Entity Risk Scores, and Elastic Security Labs. By default it includes the [platform core tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#platform-core-tools) and [security tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#security-tools). 

You can customize it by giving it access to additional built-in tools, or to your own [custom tools](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md). 


## Example: Alert triage 
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

