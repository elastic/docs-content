---
description: "AlertZero Workers triage alerts, hunt for threats, tune detection rules, and investigate attacks in Elastic Security, then bring proposed actions to a person to approve."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} [alertzero-overview]

{{alertzero}} is the agentic layer of {{elastic-sec}}. Its {{az-workers}}, AI agents that each specialize in one kind of security work, triage alerts, hunt for threats, tune detection rules, and investigate attacks in the background. When a step needs a person, such as closing alerts, isolating a host, or changing a detection rule, a {{az-worker}} brings it to you as a {{az-proposed-action}} that you approve or decline on the [{{alertzero}} home page](use-alertzero.md).

Each {{az-proposed-action}} comes with an {{az-investigation}} that holds the {{az-worker}}'s evidence and conclusion, so you can check its reasoning before you decide. You control which {{az-workers}} run and [how much {{az-autonomy}} each one has](#alertzero-overview-autonomy).

## What {{az-workers}} take on [alertzero-overview-watches]

{{alertzero}} has four {{az-watches}}, one for each area of security operations. Each {{az-watch}} brings together the {{az-workers}} for that area. In the {{az-triage-watch}}, for example, {{az-alert-triage}} classifies individual alerts, while {{az-attack-discovery}} connects related alerts into attacks.

| {{az-watch}} | What it does | {{az-workers}} |
| --- | --- | --- |
| [{{az-triage-watch}}](configure-worker-settings.md) | Classifies new alerts, proposes closing false positives, and groups related alerts into attacks. | {{az-alert-triage}}, {{az-attack-discovery}} |
| [{{az-hunt-watch}}](configure-worker-settings.md) | Hunts your data for activity described in {{az-threat-reports}}, before any alert fires. | {{az-continuous-threat-hunt}} |
| [{{az-detection-watch}}](configure-worker-settings.md) | Tunes noisy rules and proposes new rules for the gaps that the {{az-hunt-watch}} finds. | {{az-rule-tuning}}, {{az-rule-coverage}} |
| [{{az-forensics-watch}}](configure-worker-settings.md) | Investigates attacks that the {{az-triage-watch}} hands off and proposes response actions, such as isolating a host. | {{az-endpoint-analysis}} |

<!--
Uncomment after elastic/docs-content#9118 merges. That PR adds a page for each Watch.
Then use these links for the Watch names in the table, in place of the configure-worker-settings.md links:

[{{az-triage-watch}}](watches/triage-watch.md)
[{{az-hunt-watch}}](watches/hunt-watch.md)
[{{az-detection-watch}}](watches/detection-watch.md)
[{{az-forensics-watch}}](watches/forensics-watch.md)
-->

To learn how {{az-watches}} hand work to each other, refer to [](configure-worker-settings.md).

% After elastic/docs-content#9118 merges, link the reference on how Watches hand work to each other to configure-worker-settings.md#alertzero-worker-on-off, the "How Workers depend on each other" section.

## How much {{az-workers}} can act on their own [alertzero-overview-autonomy]

Every {{az-worker}} starts at {{az-manual}} {{az-autonomy}}, so each {{az-proposed-action}} waits for your approval. You can raise the level for some {{az-workers}}. A {{az-worker}} approves its own {{az-proposed-actions}} only at {{az-supervised}}, and changes to detection rules always wait for you.

To change a {{az-worker}}'s level, or to check what it does at each level, refer to [](configure-worker-settings.md#alertzero-worker-autonomy).

## What you're billed for [alertzero-costs]
```{applies_to}
serverless:
  security: preview
deployment:
  ech: preview
```

{{az-workers}} can add to your bill in three ways:

- **Workflow executions:** {{az-workers}} in every {{az-watch}} run as workflows, so their runs count as [workflow executions](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-billing).
- **{{agent-builder}} executions:** When a {{az-worker}} in any {{az-watch}} asks an AI agent to analyze its findings, each agent response counts as an [{{agent-builder}} execution](/explore-analyze/ai-features/agent-builder/monitor-usage.md).
- **AI model tokens:** If the space uses an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md), Elastic bills its model calls by token. Third-party model providers bill you directly.

For rates and free monthly allowances, refer to [{{elastic-sec}} {{serverless-short}} billing dimensions](/deploy-manage/cloud-organization/billing/security-billing-dimensions.md) for {{serverless-short}} and [{{ech}} billing dimensions](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md) for {{ech}}.

## Get started [alertzero-get-started]

{{alertzero}} is off by default, and you turn it on separately in each [space](/deploy-manage/manage-spaces.md).

- [](set-up-alertzero.md): Turn on {{alertzero}} and start its {{az-workers}}.
- [](alertzero-privileges.md): Give your team access to view and decide {{az-proposed-actions}}.
- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
