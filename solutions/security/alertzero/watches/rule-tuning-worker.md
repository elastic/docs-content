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

The {{az-rule-tuning}} {{az-worker}} finds rules that produce too many false positives and proposes one change per rule to reduce them. It's part of the [{{az-detection-watch}}](detection-watch.md).

It checks how many false positives each enabled rule produced in its analysis window. For each rule that meets both false positive thresholds, it opens an {{az-investigation}}, diagnoses the cause, and proposes one change to the rule's exceptions, query, risk score, threshold, or schedule. Most changes come with a backtest that compares the alerts the rule produced with the alerts it would have produced after the change. It works from alerts closed as false positives, by people or by the [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md).

By default, it runs every 2 hours. It offers {{az-manual}} and {{az-assisted}} {{az-autonomy}}, and at either level, every change waits for your approval. Refer to [what it does at each level](../configure-worker-settings.md#alertzero-worker-autonomy).

% After elastic/docs-content#9114 merges, link "what it needs" below to ../set-up-alertzero.md#alertzero-requirements-specific-workers.

## Settings [alertzero-rule-tuning-settings]

Besides the [settings every {{az-worker}} has](../configure-worker-settings.md#alertzero-shared-worker-settings), {{az-rule-tuning}} has these settings:

**Analysis window (days)**
:   How many days of alerts it checks.

    Default: 7. Range: 1–30.

**False positive count**
:   How many false positives a rule needs in the analysis window.

    Default: 10. Range: 2–100.

**False positive rate**
:   What share of a rule's alerts must be false positives.

    Default: 50%. Range: 0–100%.

## Limits [alertzero-rule-tuning-limits]

* Each run reviews up to 10 rules and uses each rule's newest 100 false positives.
* It doesn't backtest changes to saved query or {{ml}} rules, or exceptions on {{esql}} rules.

## Work with this {{az-worker}} [alertzero-rule-tuning-tasks]

- **Before you turn it on:** Check [what it needs](../set-up-alertzero.md).
- **Decide its work:** Its {{az-proposed-actions}} appear in the **Configure** section of the **{{az-proposed-actions-cap}}** page. Refer to [](../decide-detection-change.md).
- **Change its settings:** Refer to [](../configure-worker-settings.md).
