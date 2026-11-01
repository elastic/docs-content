---
description: "The AlertZero Detection Watch improves your Elastic Security detection rules at the source, and every change it proposes waits for your approval."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-detection-watch}}

The {{az-detection-watch}} improves your detection rules at the source, instead of handling the alerts they produce one by one. Both of its {{az-workers}} build on another {{az-watch}}'s work:

- The [{{az-rule-tuning}} {{az-worker}}](rule-tuning-worker.md) tunes rules that produce too many false positives. It works from alerts closed as false positives, by people or by the [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md) in the [{{az-triage-watch}}](triage-watch.md).
- The [{{az-rule-coverage}} {{az-worker}}](rule-coverage-worker.md) proposes rules for the detection gaps that the [{{az-hunt-watch}}](hunt-watch.md) finds.

Every change waits for your approval, because neither {{az-worker}} offers {{az-supervised}} {{az-autonomy}}. You decide their changes in the **Configure** section of the **{{az-proposed-actions-cap}}** page. Refer to [](../decide-detection-change.md).
