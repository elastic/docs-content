---
description: "Find what the AlertZero Rule Tuning Worker does in Elastic Security, the false positive thresholds that decide which rules it tunes, and its limits."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-rule-tuning}} {{az-worker}}

The {{az-rule-tuning}} {{az-worker}} is part of the [{{az-detection-watch}}](detection-watch.md). It finds rules that produce too many false positives and proposes one change per rule to reduce them. This page explains when to use the {{az-rule-tuning}} {{az-worker}}, what data it needs, how it chooses which rules to tune, where to decide its {{az-proposed-actions}}, and which settings and limits apply.

## When to use the {{az-rule-tuning}} {{az-worker}} [alertzero-rule-tuning-when-to-use]

The {{az-rule-tuning}} {{az-worker}} is the right fit when:

* A few rules produce most of your false positives.
* Your analysts, or the [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md), close false positives with the false positive reason, so the {{az-rule-tuning}} {{az-worker}} can count them.
* You want a rule preview of each proposed change before you apply it.

The {{az-rule-tuning}} {{az-worker}} isn't the best fit when:

* Your rules rarely produce false positives. With the default settings, a rule needs at least 10 false positives that make up at least 50% of its alerts over 7 days before the {{az-rule-tuning}} {{az-worker}} tunes it.
* Your analysts close false positives with a different reason, or without one. The {{az-rule-tuning}} {{az-worker}} counts only alerts closed as false positives.
* Your noisiest rules are saved query or {{ml}} rules. The {{az-rule-tuning}} {{az-worker}} can't preview changes to them, so you need to check those changes yourself.

## Data requirements [alertzero-rule-tuning-data]

* Enabled rules that generated alerts in the space during the analysis window.
* Alerts closed as false positives. For each rule, the {{az-rule-tuning}} {{az-worker}} uses the newest 100.

## How it works [alertzero-rule-tuning-how-it-works]

On each run, the {{az-rule-tuning}} {{az-worker}}:

1. Counts how many false positives each enabled rule produced in its analysis window.
2. For each rule that meets both false positive thresholds, opens an {{az-investigation}} and diagnoses the cause.
3. Proposes one change to the rule's exceptions, query, risk score, threshold, or schedule. Most changes come with a [rule preview](/solutions/security/detect-and-alert/validate-and-test-rules.md#validate-historical-data) that compares how many alerts the rule generated with how many it would have generated after the change.

The {{az-rule-tuning}} {{az-worker}} counts every alert closed as a false positive, whether a person or the [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md) closed it.

You review the {{az-rule-tuning}} {{az-worker}}'s proposed changes in the **Configure** section of the **{{az-proposed-actions-cap}}** page. To learn how to review a proposed change and approve it, refer to [](../decide-detection-change.md).

### Example [alertzero-rule-tuning-example]

A rule that detects new service creation generated 30 alerts last week, and analysts closed 24 of them as false positives because a software deployment tool creates services. That's 24 false positives at an 80% rate, above both default thresholds. The {{az-rule-tuning}} {{az-worker}} diagnoses the cause and proposes an exception for the deployment tool's process. The rule preview shows that the rule would have generated 6 alerts instead of 30.

% After elastic/docs-content#9114 merges, consider linking to ../set-up-alertzero.md#alertzero-requirements-specific-workers from the intro.

## Settings [alertzero-rule-tuning-settings]

**Trigger**
:   How often the {{az-rule-tuning}} {{az-worker}} runs.

    Default: Every 2 hours

**{{az-autonomy-cap}}**
:   How much the {{az-rule-tuning}} {{az-worker}} does without you. You can set it to **{{az-manual}}** or **{{az-assisted}}**, and at either level, you approve each change before it reaches the rule. Refer to [what it does at each level](../configure-worker-settings.md#alertzero-worker-autonomy).

    Default: {{az-manual}}

**Models**
:   Opens **Feature settings**, where you select the models that {{alertzero}} uses in the space. The {{az-rule-tuning}} {{az-worker}} has no model setting of its own, so it uses the models you select there.

% Link the model recommendations page once it exists: For help choosing models, refer to [](../model-recommendations.md).

**Analysis window (days)**
:   How many days of alerts it checks.

    Default: 7 days, and you can set it from 1 to 30 days.

**False positive count**
:   How many false positives a rule needs in the analysis window.

    Default: 10, and you can set it from 2 to 100.

**False positive rate**
:   What share of a rule's alerts must be false positives.

    Default: 50%, and you can set it from 0 to 100.

## Limits [alertzero-rule-tuning-limits]

* Each time the {{az-rule-tuning}} {{az-worker}} runs, it reviews up to 10 rules and uses each rule's newest 100 false positives.
* The {{az-rule-tuning}} {{az-worker}}  doesn't preview changes to saved query or {{ml}} rules, or exceptions on {{esql}} rules.
