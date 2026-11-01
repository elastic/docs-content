---
description: "The AlertZero Detection Watch improves your Elastic Security detection rules at the source, and you approve every change before it reaches your rules."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-detection-watch}}

The {{az-detection-watch}} improves your detection rules at the source, instead of handling the alerts they produce one by one.

| {{az-worker}} | What it does | Works with |
| --- | --- | --- |
| [{{az-rule-tuning}}](rule-tuning-worker.md) | Tunes rules that produce too many false positives. | The [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md) in the [{{az-triage-watch}}](triage-watch.md), whose false positive closures this {{az-worker}} counts, along with the ones people make. |
| [{{az-rule-coverage}}](rule-coverage-worker.md) | Proposes rules to close detection gaps. | The [{{az-continuous-threat-hunt}} {{az-worker}}](continuous-threat-hunt-worker.md) in the [{{az-hunt-watch}}](hunt-watch.md), which finds the detection gaps this {{az-worker}} proposes rules for. |

You review the {{az-watch}}'s proposed changes and rules in the **Configure** section of the **{{az-proposed-actions-cap}}** page. Neither {{az-worker}} offers **{{az-supervised}}** {{az-autonomy}}, so you approve every change before it reaches your rules. To learn how to approve a rule change or a new rule, refer to [](../decide-detection-change.md).

## When to turn on the {{az-detection-watch}} [alertzero-detection-watch-when]

Turn on the {{az-detection-watch}} when noisy rules or missing detections cost your team time:

* Turn on the {{az-rule-tuning}} {{az-worker}} when a few rules produce most of your false positives. To learn whether your rules and data are a good fit, refer to [when to use {{az-rule-tuning}}](rule-tuning-worker.md#alertzero-rule-tuning-when-to-use).
* Turn on the {{az-rule-coverage}} {{az-worker}} together with the [{{az-hunt-watch}}](hunt-watch.md), because it works only on the detection gaps that Watch records. To learn whether it fits your environment, refer to [when to use {{az-rule-coverage}}](rule-coverage-worker.md#alertzero-rule-coverage-when-to-use).
