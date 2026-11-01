---
description: "Find what the AlertZero Rule Coverage Worker does in Elastic Security, the settings that control how many detection gaps it works on, and its limits."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-rule-coverage}} {{az-worker}}

The {{az-rule-coverage}} {{az-worker}} proposes rules to close the detection gaps that the [{{az-hunt-watch}}](hunt-watch.md) finds. It's part of the [{{az-detection-watch}}](detection-watch.md).

It opens one {{az-investigation}} for each gap and checks whether a rule already covers it. Depending on what it finds, it proposes turning on an existing rule, installing a prebuilt rule, or creating a new {{esql}} rule with a backtest of how often the rule would have matched. If a rule already covers the gap, it asks you to confirm that instead. It works only on gaps from the [{{az-continuous-threat-hunt}} {{az-worker}}](continuous-threat-hunt-worker.md).

By default, it runs every hour. It offers {{az-manual}} and {{az-assisted}} {{az-autonomy}}, and at either level, every rule waits for your approval. Refer to [what it does at each level](../configure-worker-settings.md#alertzero-worker-autonomy).

% After elastic/docs-content#9114 merges, link "what it needs" below to ../set-up-alertzero.md#alertzero-requirements-specific-workers.

## Settings [alertzero-rule-coverage-settings]

Besides the [settings every {{az-worker}} has](../configure-worker-settings.md#alertzero-shared-worker-settings), {{az-rule-coverage}} has these settings:

**Lookback (days)**
:   How far back it looks for gaps.

    Default: 14. Range: 8–90.

**Max gaps per run**
:   The most gaps it works on in one run.

    Default: 5. Range: 1–50.

## Limits [alertzero-rule-coverage-limits]

* Up to 100 gaps can be under review in a space at once.

## Work with this {{az-worker}} [alertzero-rule-coverage-tasks]

- **Before you turn it on:** Check [what it needs](../set-up-alertzero.md).
- **Decide its work:** Its {{az-proposed-actions}} appear in the **Configure** section of the **{{az-proposed-actions-cap}}** page. Refer to [](../decide-detection-change.md).
- **Change its settings:** Refer to [](../configure-worker-settings.md).
