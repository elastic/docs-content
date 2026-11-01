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

The {{az-triage-watch}} reviews incoming alerts so your analysts see only the ones that need their attention. Its two {{az-workers}} build on each other:

- The [{{az-alert-triage}} {{az-worker}}](alert-triage-worker.md) classifies alerts and proposes closing the false positives, so they don't reach the {{az-attack-discovery}} {{az-worker}}.
- The [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md) groups related alerts into attacks, and proposes handing the attacks it confirms or can't rule out to the [{{az-forensics-watch}}](forensics-watch.md).

You decide their work in the **Investigate** section of the **{{az-proposed-actions-cap}}** page. Refer to [](../decide-proposed-action.md) and [](../respond-to-attack.md).
