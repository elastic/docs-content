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

The {{az-detection-watch}} improves your detection rules at the source, instead of handling the alerts they produce one by one. Every change it proposes waits for your approval, because neither of its {{az-workers}} offers {{az-supervised}} {{az-autonomy}}.

| {{az-worker}} | What it does |
| --- | --- |
| [{{az-rule-tuning}}](rule-tuning-worker.md) | Finds rules that produce too many false positives, and proposes one change per rule to reduce them. |
| [{{az-rule-coverage}}](rule-coverage-worker.md) | Proposes rules to close the detection gaps that the {{az-hunt-watch}} finds. |

Their work appears in the **Configure** section of the **{{az-proposed-actions-cap}}** page. To review a change, refer to [](../decide-detection-change.md).
