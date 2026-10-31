---
description: "AlertZero Workers triage alerts, hunt for threats, tune detection rules, and investigate attacks in Elastic Security, then bring proposed actions to a person to approve."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} [alertzero-overview]

{{alertzero}} brings AI-powered {{az-workers}} to {{elastic-sec}}. They triage alerts, hunt for threats, tune detection rules, and investigate attacks in the background. Changes such as closing alerts, isolating a host, or changing a detection rule come to you as {{az-proposed-actions}} that you approve or decline on the {{alertzero}} home page. Each {{az-worker}}'s [{{az-autonomy}} level](#alertzero-overview-autonomy) decides which of them wait for you.

## How {{alertzero}} works [alertzero-how-it-works]

Each {{az-watch}} groups the {{az-workers}} that share one area of expertise, such as triage or detection engineering. Work moves from {{az-workers}} to you like this:

1. Each {{az-worker}} runs in the background, either on a schedule or when another {{az-worker}} hands it work. When it finds a potential threat, it opens an {{az-investigation}}.
2. Each {{az-investigation}} collects the {{az-worker}}'s evidence and conclusion, and any {{az-proposed-actions}}.
3. You approve or decline each {{az-proposed-action}} on the [{{alertzero}} home page](use-alertzero.md). You can also assign, close, or [escalate](escalate-investigation.md) the {{az-investigation}} it belongs to.

Each {{az-worker}} runs as its own service account. When you approve {{az-proposed-actions}}, they run as you, with your privileges.

## {{az-watches}} and {{az-workers}} [alertzero-overview-watches]

{{alertzero}} includes four {{az-watches}}. For the details of each {{az-worker}}, refer to [](watches-and-workers.md).

| {{az-watch}} | {{az-workers}} | What it does |
| --- | --- | --- |
| [{{az-triage-watch}}](watches-and-workers.md#alertzero-triage-watch) | {{az-alert-triage}}, {{az-attack-discovery}} | Reviews incoming alerts. {{az-alert-triage}} classifies alerts as true or false positives and proposes closing the false positives. {{az-attack-discovery}} finds candidate attacks and opens one {{az-investigation}} per attack. |
| [{{az-hunt-watch}}](watches-and-workers.md#alertzero-hunt-watch) | {{az-continuous-threat-hunt}} | Searches your data for activity that matches {{az-threat-reports}}, without waiting for an alert. It runs every 4 hours. |
| [{{az-detection-watch}}](watches-and-workers.md#alertzero-detection-watch) | {{az-rule-tuning}}, {{az-rule-coverage}} | Improves your detection rules. {{az-rule-tuning}} diagnoses rules that are too noisy or that miss activity, and proposes tuning changes. {{az-rule-coverage}} proposes new or existing rules to close detection gaps that the {{az-hunt-watch}} finds. |
| [{{az-forensics-watch}}](watches-and-workers.md#alertzero-forensics-watch) | {{az-endpoint-analysis}} | Investigates attacks on hosts. {{az-endpoint-analysis}} reconstructs the attack timeline on the affected hosts and proposes response actions, such as isolating a host. It runs only on attacks that {{az-attack-discovery}} hands off. |

## {{az-autonomy-cap}} [alertzero-overview-autonomy]

Each {{az-worker}}'s {{az-autonomy}} level sets how far it goes before it waits for a person. There are three levels: {{az-manual}}, {{az-assisted}}, and {{az-supervised}}. Each {{az-worker}} offers at most two of them and starts at {{az-manual}}, where every {{az-proposed-action}} waits for your approval.

Changes to detection rules always wait for approval because {{az-rule-tuning}} and {{az-rule-coverage}} don't offer {{az-supervised}}. To find out which levels each {{az-worker}} offers and what it does at each one, refer to [Set a {{az-worker}}'s {{az-autonomy}}](configure-worker-settings.md#alertzero-worker-autonomy).

## Get started [alertzero-get-started]

{{alertzero}} is off by default. You turn it on separately in each [space](/deploy-manage/manage-spaces.md), then select which {{az-workers}} to run. To get started, check the [requirements](requirements.md), then follow the steps in [](set-up-alertzero.md).

## Related pages [alertzero-overview-related]

- [](use-alertzero.md): Review the home page and approve or decline {{az-proposed-actions}}.
- [](watches-and-workers.md): Learn what each {{az-watch}} and {{az-worker}} does.
- [](glossary.md): Look up any {{alertzero}} term.
