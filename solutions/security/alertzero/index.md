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

{{alertzero}} is the agentic layer of {{elastic-sec}}. Its {{az-workers}} are AI agents that triage alerts, hunt for threats, tune detection rules, and investigate attacks on a schedule, so your team spends less time sorting through noise and more time on the decisions that need a person.

When a step needs a person, such as closing alerts, isolating a host, or changing a detection rule, a {{az-worker}} brings it to you as a {{az-proposed-action}} on the [**{{az-proposed-actions-cap}}** page](work-in-alertzero.md). Each {{az-proposed-action}} comes with an {{az-investigation}} that holds the {{az-worker}}'s evidence and conclusion, so you can check its reasoning before you approve or decline instead of redoing the work.

## What {{az-workers}} take on [alertzero-overview-watches]

{{az-workers}} are grouped into four {{az-watches}}, one for each area of security operations. The {{az-watches}} pass work to each other, so a finding in one area can lead to action in another.

| {{az-watch}} | What it does | {{az-workers}} |
| --- | --- | --- |
| [{{az-triage-watch}}](watches-and-workers.md#alertzero-triage-watch) | Classifies new alerts, proposes closing false positives, and groups related alerts into attacks, so you review {{az-proposed-actions}} instead of individual alerts. | {{az-alert-triage}}, {{az-attack-discovery}} |
| [{{az-hunt-watch}}](watches-and-workers.md#alertzero-hunt-watch) | Hunts your data for activity described in {{az-threat-reports}} that your detection rules might have missed, so you have fewer blind spots. | {{az-continuous-threat-hunt}} |
| [{{az-detection-watch}}](watches-and-workers.md#alertzero-detection-watch) | Tunes noisy rules to cut false positives, and proposes turning on an existing rule, installing a prebuilt rule, or creating a new one to cover gaps in your detections. | {{az-rule-tuning}}, {{az-rule-coverage}} |
| [{{az-forensics-watch}}](watches-and-workers.md#alertzero-forensics-watch) | Investigates attacks and proposes response actions, such as isolating a host. | {{az-endpoint-analysis}} |

To learn how {{az-watches}} pass work to each other, refer to [](watches-and-workers.md).

## How much {{az-workers}} can act on their own [alertzero-overview-autonomy]

Every {{az-worker}} starts at {{az-manual}} {{az-autonomy}}, so each {{az-proposed-action}} waits for your approval. You can raise the level for some {{az-workers}}. A {{az-worker}} approves its own {{az-proposed-actions}} only at {{az-supervised}}, and changes to detection rules always wait for you.

To change a {{az-worker}}'s level, or to check what it does at each level, refer to [](configure-worker-settings.md).

## What you're billed for [alertzero-costs]
```{applies_to}
serverless:
  security: preview
deployment:
  ech: preview
```

{{az-workers}} can add to your bill in three ways:

- **Workflow executions:** {{az-workers}} run as workflows, so each run counts as a [workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-billing).
- **{{agent-builder}} executions:** When a {{az-worker}} asks an AI agent to analyze its findings, each agent response counts as an [{{agent-builder}} execution](/explore-analyze/ai-features/agent-builder/monitor-usage.md).
- **AI model tokens:** If the space uses an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md), Elastic bills its model calls by token. Third-party model providers bill you directly.

For rates and free monthly allowances, refer to [{{elastic-sec}} {{serverless-short}} billing dimensions](/deploy-manage/cloud-organization/billing/security-billing-dimensions.md) for {{serverless-short}} and [{{ech}} billing dimensions](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md) for {{ech}}.

## Get started [alertzero-get-started]

{{alertzero}} is off by default, and you turn it on separately in each [space](/deploy-manage/manage-spaces.md).

- [](set-up-alertzero.md): Turn on {{alertzero}} and start its {{az-workers}}.
- [](alertzero-privileges.md): Give your team access to view and decide {{az-proposed-actions}}.
- [](work-in-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
