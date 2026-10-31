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

You decide which {{az-workers}} run and how much each one does without you. Each {{az-worker}}'s [{{az-autonomy}} level](#alertzero-overview-autonomy) sets which {{az-proposed-actions}} wait for your decision.

## How {{alertzero}} works [alertzero-how-it-works]

Work moves from {{az-workers}} to you like this:

1. Each {{az-worker}} runs in the background, either on a schedule or when another {{az-worker}} hands it work. When it finds a potential threat, it opens an {{az-investigation}}.
2. The {{az-investigation}} collects the {{az-worker}}'s evidence, its conclusion, and any {{az-proposed-actions}}.
3. You approve or decline each {{az-proposed-action}} on the **{{az-proposed-actions-cap}}** page. You can also assign, close, or [escalate](escalate-investigation.md) the {{az-investigation}}. Refer to [](use-alertzero.md).

To control who can view, decide, and set up {{alertzero}}, refer to [](alertzero-privileges.md).

## What each {{az-watch}} does [alertzero-overview-watches]

Each {{az-watch}} groups the {{az-workers}} for one area of work, such as triage or detection engineering. {{alertzero}} includes four {{az-watches}}:

| {{az-watch}} | {{az-workers}} | What it does |
| --- | --- | --- |
| [{{az-triage-watch}}](watches-and-workers.md) | {{az-alert-triage}}, {{az-attack-discovery}} | Reviews incoming alerts. {{az-alert-triage}} classifies alerts as true or false positives and proposes closing the false positives. {{az-attack-discovery}} finds candidate attacks and opens one {{az-investigation}} per attack. |
| [{{az-hunt-watch}}](watches-and-workers.md) | {{az-continuous-threat-hunt}} | Searches your data every 4 hours for activity that matches {{az-threat-reports}}, without waiting for an alert. |
| [{{az-detection-watch}}](watches-and-workers.md) | {{az-rule-tuning}}, {{az-rule-coverage}} | Improves your detection rules. {{az-rule-tuning}} diagnoses rules that are too noisy or that miss activity, and proposes tuning changes. {{az-rule-coverage}} proposes new or existing rules to close detection gaps that the {{az-hunt-watch}} finds. |
| [{{az-forensics-watch}}](watches-and-workers.md) | {{az-endpoint-analysis}} | Investigates attacks on hosts. {{az-endpoint-analysis}} reconstructs the attack timeline on the affected hosts and proposes response actions, such as isolating a host. It runs only on attacks that {{az-attack-discovery}} hands off. |

<!--
Uncomment after elastic/docs-content#9118 merges. That PR adds a page for each Watch.
Then use these links for the Watch names in the table above, in place of the watches-and-workers.md links:

[{{az-triage-watch}}](watches/triage-watch.md)
[{{az-hunt-watch}}](watches/hunt-watch.md)
[{{az-detection-watch}}](watches/detection-watch.md)
[{{az-forensics-watch}}](watches/forensics-watch.md)
-->

For the details of each {{az-worker}}, refer to [](watches-and-workers.md).

## How {{az-watches}} pass work to each other [alertzero-context-engine]

Some {{az-workers}} pick up work that a {{az-worker}} in another {{az-watch}} started. They pass that work through [{{context-engine}}](/explore-analyze/ai-features/context-engine.md), which stores information that AI features share. You don't work in {{context-engine}} directly, but it must be on in each space where these {{az-workers}} run:

- **Detection gaps:** The {{az-hunt-watch}} records each detection gap it finds. The {{az-rule-coverage}} {{az-worker}} picks up each gap and proposes a rule for it.
- **Forensics handoffs:** When the {{az-attack-discovery}} {{az-worker}} hands an attack to the {{az-forensics-watch}}, it records the handoff. The {{az-endpoint-analysis}} {{az-worker}} picks up the handoff and investigates the affected hosts.

If {{context-engine}} is off, these {{az-workers}} can't pass work to each other, and their {{az-watch}} page shows **Worker setup needs attention**. To turn it on, select **Enable {{context-engine}}**. Refer to [](requirements.md#alertzero-requirements-worker-settings).

### Indexes that {{alertzero}} adds [alertzero-context-engine-indexes]

{{alertzero}} keeps this shared work in two indexes, which you might notice in **Index Management**. {{alertzero}} creates and manages them, so you don't need to set them up.

- `ai-index-idx-security-investigations`: The detection gaps and forensics handoffs that {{az-workers}} pass to each other.
- `ai-index-idx-security-attack-fingerprints`: Lets the {{az-attack-discovery}} {{az-worker}} recognize an attack it already reported, so it adds the attack to the open {{az-investigation}} instead of opening a new one.

## What {{alertzero}} costs [alertzero-costs]
```{applies_to}
serverless:
  security: preview
deployment:
  ech: preview
```

{{az-workers}} run as [workflows](/explore-analyze/workflows.md), and Elastic bills for workflow executions. Each {{az-worker}} run counts as an execution, and so does the work it starts, such as reviews and handoffs to other {{az-workers}}. A {{az-worker}} that runs more often uses more executions, so its **Trigger** setting affects your costs.

For pricing, refer to [{{elastic-sec}} {{serverless-short}} billing dimensions](/deploy-manage/cloud-organization/billing/security-billing-dimensions.md) for {{serverless-short}} and [Execution-based billing](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-billing) for {{ech}}.

## How much {{az-workers}} do on their own [alertzero-overview-autonomy]

The {{az-autonomy}} level of each {{az-worker}} sets how far it goes before it waits for a person. The three levels are {{az-manual}}, {{az-assisted}}, and {{az-supervised}}. Each {{az-worker}} offers at most two of them and starts at {{az-manual}}, where every {{az-proposed-action}} waits for your approval. Only at {{az-supervised}} do {{az-workers}} approve their own {{az-proposed-actions}}.

{{az-rule-tuning}} and {{az-rule-coverage}} don't offer {{az-supervised}}, so changes to detection rules always wait for your approval. For the levels each {{az-worker}} offers and what it does at each one, refer to [Set a {{az-worker}}'s {{az-autonomy}}](configure-worker-settings.md#alertzero-worker-autonomy).

## Get started [alertzero-get-started]

{{alertzero}} is off by default, and you turn it on separately in each [space](/deploy-manage/manage-spaces.md). Check the [requirements](requirements.md), then follow the steps in [](set-up-alertzero.md).

## Related pages [alertzero-overview-related]

- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](watches-and-workers.md): Learn what each {{az-watch}} and {{az-worker}} does.
- [](glossary.md): Look up any {{alertzero}} term.
