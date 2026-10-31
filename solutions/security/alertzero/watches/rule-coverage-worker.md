---
description: "Find what the AlertZero Rule Coverage Worker does, what it needs, its settings, and where its work appears in Elastic Security."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-rule-coverage}} {{az-worker}}

The {{az-rule-coverage}} {{az-worker}} belongs to the [{{az-detection-watch}}](detection-watch.md). It proposes rules to close the detection gaps that the [{{az-hunt-watch}}](hunt-watch.md) finds.

It opens one {{az-investigation}} for each gap and checks whether a rule already covers it. Depending on what it finds, it proposes turning on an existing rule, installing a prebuilt rule, or creating a new {{esql}} rule with a backtest of how often the rule would have matched. If a rule already covers the gap, it asks you to confirm that instead.

## Requirements [alertzero-rule-coverage-requirements]

The {{az-rule-coverage}} {{az-worker}} needs the [{{az-continuous-threat-hunt}} {{az-worker}}](continuous-threat-hunt-worker.md), which is the only source of the gaps it works on, and [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) turned on in the space (the `contextEngine:enabled` advanced setting). Refer to [{{az-worker}} dependencies](../requirements.md).

## Settings [alertzero-rule-coverage-settings]

Find these settings on the {{az-detection-watch}} page. To change them, refer to [](../configure-worker-settings.md).

**{{az-autonomy-cap}}**
:   How much it does without waiting for you. At either level, every rule waits for your approval. Default: {{az-manual}}.

    * **{{az-manual}}**: You approve each gap before it drafts a rule.
    * **{{az-assisted}}**: It drafts a rule for every gap without asking.

**Trigger**
:   How often it runs, in minutes, hours, or days.

    Default: every hour.

**Models**
:   A link to **Feature Settings**, where you select the models that {{alertzero}} uses in the space.

**Lookback (days)**
:   How far back it looks for gaps.

    Default: 14. Range: 8–90.

**Max gaps per run**
:   The most gaps it works on in one run.

    Default: 5. Range: 1–50.

## Where its work appears [alertzero-rule-coverage-work]

Its {{az-proposed-actions}} appear in the **Configure** section of the **{{az-proposed-actions-cap}}** page, in an {{az-investigation}} named **Detection coverage: _gap_**. Refer to [](../decide-detection-change.md).

## Limits [alertzero-rule-coverage-limits]

* Up to 100 gaps can be under review in a space at once.
