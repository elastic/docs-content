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

{{alertzero}} adds AI-powered {{az-workers}} to {{elastic-sec}}. They triage alerts, hunt for threats, tune detection rules, and investigate attacks in the background. Changes they want to make, such as closing alerts, isolating a host, or editing a detection rule, come to you as {{az-proposed-actions}} to approve or decline.

You decide which {{az-workers}} run and [how much each one does without you](#alertzero-overview-autonomy).

## How {{alertzero}} works [alertzero-how-it-works]

Work moves from {{az-workers}} to you like this:

1. Each {{az-worker}} runs in the background, either on a schedule or when another {{az-worker}} hands it work. When it finds a potential threat, it opens an {{az-investigation}}.
2. The {{az-investigation}} collects the {{az-worker}}'s evidence, its conclusion, and any {{az-proposed-actions}}.
3. You approve or decline each {{az-proposed-action}} on the **{{az-proposed-actions-cap}}** page. You can also assign, close, or [escalate](escalate-investigation.md) the {{az-investigation}}. Refer to [](use-alertzero.md).

For example, the {{az-alert-triage}} {{az-worker}} classifies new alerts every 15 minutes by default. When it's confident that alerts are false positives, it proposes closing them, with one {{az-investigation}} for alerts that share a pattern. At {{az-manual}} {{az-autonomy}}, the default, nothing closes until you approve.

## What {{alertzero}} covers [alertzero-overview-watches]

Four {{az-watches}} group the {{az-workers}}, one {{az-watch}} for each area of work:

| {{az-watch}} | What it does | {{az-workers}} |
| --- | --- | --- |
| [{{az-triage-watch}}](watches-and-workers.md) | Classifies incoming alerts, proposes closing false positives, and groups related alerts into attacks. | {{az-alert-triage}}, {{az-attack-discovery}} |
| [{{az-hunt-watch}}](watches-and-workers.md) | Searches your data for activity that matches {{az-threat-reports}}, without waiting for an alert. | {{az-continuous-threat-hunt}} |
| [{{az-detection-watch}}](watches-and-workers.md) | Proposes changes to rules that produce too many false positives, and proposes rules for the detection gaps that the {{az-hunt-watch}} finds. | {{az-rule-tuning}}, {{az-rule-coverage}} |
| [{{az-forensics-watch}}](watches-and-workers.md) | Investigates the attacks that the {{az-triage-watch}} hands off, and proposes response actions, such as isolating a host. | {{az-endpoint-analysis}} |

<!--
Uncomment after elastic/docs-content#9118 merges. That PR adds a page for each Watch.
Then use these links for the Watch names in the table above, in place of the watches-and-workers.md links:

[{{az-triage-watch}}](watches/triage-watch.md)
[{{az-hunt-watch}}](watches/hunt-watch.md)
[{{az-detection-watch}}](watches/detection-watch.md)
[{{az-forensics-watch}}](watches/forensics-watch.md)
-->

For what each {{az-worker}} does, what it needs, and how {{az-watches}} pass work to each other, refer to [](watches-and-workers.md).

## How much {{az-workers}} do without you [alertzero-overview-autonomy]

Every {{az-worker}} starts at {{az-manual}} {{az-autonomy}}, where each {{az-proposed-action}} waits for your approval. You can give some {{az-workers}} more {{az-autonomy}}, but only at {{az-supervised}} do they approve their own {{az-proposed-actions}}. Changes to detection rules always wait for you. Refer to [Set a {{az-worker}}'s {{az-autonomy}}](configure-worker-settings.md#alertzero-worker-autonomy).

## What {{alertzero}} costs [alertzero-costs]
```{applies_to}
serverless:
  security: preview
deployment:
  ech: preview
```

{{az-workers}} run as [workflows](/explore-analyze/workflows.md), and Elastic bills for workflow executions. Each {{az-worker}} run counts, along with the reviews and handoffs it starts, so {{az-workers}} that run more often cost more. For pricing, refer to [{{elastic-sec}} {{serverless-short}} billing dimensions](/deploy-manage/cloud-organization/billing/security-billing-dimensions.md) for {{serverless-short}} and [Execution-based billing](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-billing) for {{ech}}.

## Get started [alertzero-get-started]

{{alertzero}} is off by default, and you set it up separately in each [space](/deploy-manage/manage-spaces.md):

1. Check the [requirements](requirements.md).
2. [Set up {{alertzero}}](set-up-alertzero.md) in the space.
3. Give your team the [privileges](alertzero-privileges.md) they need to view and decide {{az-proposed-actions}}.
4. [Review your first {{az-proposed-action}}](review-first-proposed-action.md).

## Related pages [alertzero-overview-related]

- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](watches-and-workers.md): Learn what each {{az-watch}} and {{az-worker}} does.
- [](manage-alertzero.md): Change how {{az-workers}} run, or turn {{alertzero}} off in a space.
- [](glossary.md): Look up any {{alertzero}} term.
