---
description: "Find what the AlertZero Rule Tuning Worker does, what it needs, its settings, and where its work appears in Elastic Security."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-rule-tuning}} {{az-worker}}

The {{az-rule-tuning}} {{az-worker}} belongs to the [{{az-detection-watch}}](detection-watch.md). It finds rules that produce too many false positives and proposes one change per rule to reduce them.

It checks how many false positives each enabled rule produced in its analysis window. For each rule that meets both false positive thresholds, it opens an {{az-investigation}}, diagnoses the cause, and proposes one change to the rule's exceptions, query, risk score, threshold, or schedule. Most changes come with a backtest that compares the alerts the rule produced with the alerts it would have produced after the change.

## Requirements [alertzero-rule-tuning-requirements]

The {{az-rule-tuning}} {{az-worker}} needs alerts closed as false positives, by people or by the [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md).

## Settings [alertzero-rule-tuning-settings]

Find these settings on the {{az-detection-watch}} page. To change them, refer to [](../configure-worker-settings.md).

**{{az-autonomy-cap}}**
:   How much it does without waiting for you. At either level, every change waits for your approval. Default: {{az-manual}}.

    * **{{az-manual}}**: You approve each rule before it analyzes the rule.
    * **{{az-assisted}}**: It analyzes every rule that qualifies without asking.

**Trigger**
:   How often it runs, in minutes, hours, or days.

    Default: every 2 hours.

**Models**
:   A link to **Feature Settings**, where you select the models that {{alertzero}} uses in the space.

**Analysis window (days)**
:   How many days of alerts it checks.

    Default: 7. Range: 1–30.

**False positive count**
:   How many false positives a rule needs in the analysis window.

    Default: 10. Range: 2–100.

**False positive rate**
:   What share of a rule's alerts must be false positives.

    Default: 50%. Range: 0–100%.

## Where its work appears [alertzero-rule-tuning-work]

Its {{az-proposed-actions}} appear in the **Configure** section of the **{{az-proposed-actions-cap}}** page, in an {{az-investigation}} named **Rule tuning: _rule name_**. Refer to [](../decide-detection-change.md).

## Limits [alertzero-rule-tuning-limits]

* Each run reviews up to 10 rules and uses each rule's newest 100 false positives.
* It doesn't backtest changes to saved query or {{ml}} rules, or exceptions on {{esql}} rules.
