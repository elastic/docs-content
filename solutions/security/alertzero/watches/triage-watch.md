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

The {{az-triage-watch}} reviews incoming alerts so your analysts see only the ones that need their attention. Its {{az-alert-triage}} {{az-worker}} classifies alerts, and its {{az-attack-discovery}} {{az-worker}} groups related alerts into attacks.

| {{az-worker}} | What it does |
| --- | --- |
| [{{az-alert-triage}}](alert-triage-worker.md) | Classifies detection alerts as true or false positives, and proposes closing the false positives. |
| [{{az-attack-discovery}}](attack-discovery-worker.md) | Groups related alerts into candidate attacks, and proposes handing the attacks it confirms or can't rule out to the {{az-forensics-watch}}. |

Their work appears in the **Investigate** section of the **{{az-proposed-actions-cap}}** page.
