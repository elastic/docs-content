---
description: "The AlertZero Triage Watch reviews incoming Elastic Security alerts so that people see only the ones that still need a person."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-triage-watch}}

The {{az-triage-watch}} reviews incoming alerts so your analysts see only the ones that need their attention.

| {{az-worker}} | What it does | Works with |
| --- | --- | --- |
| [{{az-alert-triage}}](alert-triage-worker.md) | Classifies alerts and proposes closing the false positives. | The [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md), which skips the false positives this {{az-worker}} closes, and the [{{az-rule-tuning}} {{az-worker}}](rule-tuning-worker.md), which counts them when it looks for rules to tune. |
| [{{az-attack-discovery}}](attack-discovery-worker.md) | Groups related alerts into attacks and checks each one. | The [{{az-forensics-watch}}](forensics-watch.md), which investigates the attacks this {{az-worker}} confirms or can't rule out. |

You review the {{az-watch}}'s {{az-proposed-actions}} in the **Investigate** section of the **{{az-proposed-actions-cap}}** page. To learn how to read a {{az-proposed-action}} and then run it, do it yourself, or dismiss it, refer to [](../decide-proposed-action.md). To learn how to take a confirmed attack through to containment, refer to [](../respond-to-attack.md).

## When to turn on the {{az-triage-watch}} [alertzero-triage-watch-when]

Turn on the {{az-triage-watch}} when your team spends more time sorting alerts than investigating them. Turn on both {{az-workers}} together, because the {{az-alert-triage}} {{az-worker}} closes false positives and leaves the {{az-attack-discovery}} {{az-worker}} fewer, more meaningful alerts to analyze. To learn whether each {{az-worker}} fits your environment and has the data it needs, refer to [when to use {{az-alert-triage}}](alert-triage-worker.md#alertzero-alert-triage-when-to-use) and [when to use {{az-attack-discovery}}](attack-discovery-worker.md#alertzero-attack-discovery-when-to-use).
