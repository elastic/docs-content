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
3. You approve or decline each {{az-proposed-action}} on the [**{{az-proposed-actions-cap}}** page](use-alertzero.md). You can also assign, close, or [escalate](escalate-investigation.md) the {{az-investigation}}.

{{az-workers}} run as their own service accounts, but an action you approve runs as you, with your privileges. Refer to [](alertzero-privileges.md).

## What each {{az-watch}} does [alertzero-overview-watches]

Each {{az-watch}} groups the {{az-workers}} for one area of work, such as triage or detection engineering. {{alertzero}} includes four {{az-watches}}:

| {{az-watch}} | {{az-workers}} | What it does |
| --- | --- | --- |
| [{{az-triage-watch}}](watches-and-workers.md#alertzero-triage-watch) | {{az-alert-triage}}, {{az-attack-discovery}} | Reviews incoming alerts. {{az-alert-triage}} classifies alerts as true or false positives and proposes closing the false positives. {{az-attack-discovery}} finds candidate attacks and opens one {{az-investigation}} per attack. |
| [{{az-hunt-watch}}](watches-and-workers.md#alertzero-hunt-watch) | {{az-continuous-threat-hunt}} | Searches your data every 4 hours for activity that matches {{az-threat-reports}}, without waiting for an alert. |
| [{{az-detection-watch}}](watches-and-workers.md#alertzero-detection-watch) | {{az-rule-tuning}}, {{az-rule-coverage}} | Improves your detection rules. {{az-rule-tuning}} diagnoses rules that are too noisy or that miss activity, and proposes tuning changes. {{az-rule-coverage}} proposes new or existing rules to close detection gaps that the {{az-hunt-watch}} finds. |
| [{{az-forensics-watch}}](watches-and-workers.md#alertzero-forensics-watch) | {{az-endpoint-analysis}} | Investigates attacks on hosts. {{az-endpoint-analysis}} reconstructs the attack timeline on the affected hosts and proposes response actions, such as isolating a host. It runs only on attacks that {{az-attack-discovery}} hands off. |

For the details of each {{az-worker}}, refer to [](watches-and-workers.md).

## How much {{az-workers}} do on their own [alertzero-overview-autonomy]

The {{az-autonomy}} level of each {{az-worker}} sets how far it goes before it waits for a person. The three levels are {{az-manual}}, {{az-assisted}}, and {{az-supervised}}. Each {{az-worker}} offers at most two of them and starts at {{az-manual}}, where every {{az-proposed-action}} waits for your approval. Only at {{az-supervised}} do {{az-workers}} approve their own {{az-proposed-actions}}.

{{az-rule-tuning}} and {{az-rule-coverage}} don't offer {{az-supervised}}, so changes to detection rules always wait for your approval. For the levels each {{az-worker}} offers and what it does at each one, refer to [Set a {{az-worker}}'s {{az-autonomy}}](configure-worker-settings.md#alertzero-worker-autonomy).

## Get started [alertzero-get-started]

{{alertzero}} is off by default, and you turn it on separately in each [space](/deploy-manage/manage-spaces.md). Check the [requirements](requirements.md), then follow the steps in [](set-up-alertzero.md).

## Related pages [alertzero-overview-related]

- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](watches-and-workers.md): Learn what each {{az-watch}} and {{az-worker}} does.
- [](glossary.md): Look up any {{alertzero}} term.
