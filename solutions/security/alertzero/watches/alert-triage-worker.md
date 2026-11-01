---
description: "Find what the AlertZero Alert Triage Worker does in Elastic Security, and the settings that control which alerts it triages and closes."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-alert-triage}} {{az-worker}}

The {{az-alert-triage}} {{az-worker}} is part of the [{{az-triage-watch}}](triage-watch.md). It classifies detection alerts as true or false positives and proposes closing the false positives, so your analysts see only the alerts that need them. This page explains when to use the {{az-alert-triage}} {{az-worker}}, what data it needs, how it triages alerts, where to decide its {{az-proposed-actions}}, and which settings control the alerts it triages.

## When to use the {{az-alert-triage}} {{az-worker}} [alertzero-alert-triage-when-to-use]

The {{az-alert-triage}} {{az-worker}} is the right fit when:

* Your analysts spend much of their time closing alerts that turn out to be false positives.
* You want the [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md) to build candidate attacks from fewer, more meaningful alerts.
* You want the [{{az-rule-tuning}} {{az-worker}}](rule-tuning-worker.md) to have a steady supply of false positive closures to find noisy rules from.

The {{az-alert-triage}} {{az-worker}} isn't the best fit when:

* A few rules cause most of your false positives. Fixing those rules stops the alerts at the source. Use the [{{az-rule-tuning}} {{az-worker}}](rule-tuning-worker.md) instead, or alongside it.
* You want a person to approve every alert closure. You can still use the {{az-alert-triage}} {{az-worker}}, but keep it at **{{az-manual}}** so you approve each one.

## Data requirements [alertzero-alert-triage-data]

The {{az-alert-triage}} {{az-worker}} needs detection alerts in the space with a status of open or acknowledged. It includes building block alerts unless you turn on **Exclude building-block alerts**.

## How it works [alertzero-alert-triage-how-it-works]

On each run, the {{az-alert-triage}} {{az-worker}}:

1. Analyzes open and acknowledged alerts in batches.
2. Tags each alert as a true positive, false positive, or inconclusive, and adds a note explaining why.
3. Groups alerts with the same pattern into one {{az-investigation}} and one {{az-proposed-action}}.
4. Proposes closing the alerts it's confident are false positives.

When the {{az-alert-triage}} {{az-worker}} closes an alert as a false positive, the alert drops out of your analysts' open alerts, and the [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md) skips it, because that {{az-worker}} analyzes only open and acknowledged alerts. The [{{az-rule-tuning}} {{az-worker}}](rule-tuning-worker.md) counts these closures when it looks for rules to tune.

You review the {{az-alert-triage}} {{az-worker}}'s {{az-proposed-actions}} in the **Investigate** section of the **{{az-proposed-actions-cap}}** page. To learn how to review a proposed closure and then approve or decline it, refer to [](../decide-proposed-action.md).

### Example [alertzero-alert-triage-example]

A vulnerability scanner on your network triggers a port scan rule 40 times overnight. The {{az-alert-triage}} {{az-worker}} analyzes the alerts, tags each one as a false positive with a note explaining that the activity comes from the scanner, and groups them into one {{az-investigation}} with one {{az-proposed-action}} to close them. At **{{az-manual}}**, you approve that one closure instead of closing 40 alerts by hand. After the {{az-alert-triage}} {{az-worker}} closes them, the {{az-attack-discovery}} {{az-worker}} skips them, and the {{az-rule-tuning}} {{az-worker}} counts them toward the port scan rule's false positives.

% After elastic/docs-content#9114 merges, consider linking to ../set-up-alertzero.md#alertzero-requirements-specific-workers from the intro.

## Settings [alertzero-alert-triage-settings]

**Trigger**
:   How often the {{az-alert-triage}} {{az-worker}} runs.

    Default: Every 15 minutes

**{{az-autonomy-cap}}**
:   How much the {{az-alert-triage}} {{az-worker}} does without you. You can set it to **{{az-manual}}** or **{{az-supervised}}**. Refer to [what it does at each level](../configure-worker-settings.md#alertzero-worker-autonomy).

    Default: {{az-manual}}

**Models**
:   Opens **Feature settings**, where you select the models that {{alertzero}} uses in the space. The {{az-alert-triage}} {{az-worker}} has no model setting of its own, so it uses the models you select there.

% Link the model recommendations page once it exists: For help choosing models, refer to [](../model-recommendations.md).

**Minimum confidence score**
:   How confident it must be that an alert is a false positive before it proposes closing the alert. If its confidence is lower, it tags the alert inconclusive.

    Default: 85%, and you can set it to any whole number from 0 to 100.

**Minimum severity**
:   The lowest alert severity it triages. You can select **Low**, **Medium**, **High**, or **Critical**.

    Default: Low, which triages every alert.

**Exclude building-block alerts**
:   Skips alerts from building block rules.

    Default: Off

**Excluded rule tags**
:   Skips alerts from rules with any of these tags. Tags must match exactly, including case.

    Default: None, you can add up to 50 tags.

