---
description: "The AlertZero Hunt Watch proactively hunts your Elastic Security environment for threats, without waiting for an alert."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-hunt-watch}}

The {{az-hunt-watch}} proactively hunts your environment for threats, without waiting for an alert.

| {{az-worker}} | What it does | Works with |
| --- | --- | --- |
| [{{az-continuous-threat-hunt}}](continuous-threat-hunt-worker.md) | Searches your data for activity that matches {{az-threat-reports}} and for detection coverage gaps. | The [{{az-rule-coverage}} {{az-worker}}](rule-coverage-worker.md) in the [{{az-detection-watch}}](detection-watch.md), which proposes rules for the detection gaps this {{az-worker}} finds. |

## When to turn on the {{az-hunt-watch}} [alertzero-hunt-watch-when]

Turn on the {{az-hunt-watch}} when you want to search for threats proactively, without waiting for an alert. Turn it on together with the [{{az-rule-coverage}} {{az-worker}}](rule-coverage-worker.md), so the detection gaps it finds become rules.

% Placeholder. Above the "When to turn on" section, add a paragraph like the one on detection-watch.md: where you review its work on the Proposed Actions page, and a link to the page that explains how, with a reason to follow the link (not just "Refer to").
