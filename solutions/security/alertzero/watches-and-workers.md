---
description: "Learn how AlertZero Watches group Workers in Elastic Security, how the Workers compare, and how Watches pass work to each other."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-watches}} and {{az-workers}} [alertzero-watches-and-workers]

Each {{az-watch}} groups the {{az-workers}} for one area of work. {{alertzero}} includes four {{az-watches}}: the [{{az-triage-watch}}](watches/triage-watch.md), the [{{az-detection-watch}}](watches/detection-watch.md), the [{{az-hunt-watch}}](watches/hunt-watch.md), and the [{{az-forensics-watch}}](watches/forensics-watch.md). Each {{az-worker}} has its own page that covers what it does, its settings, and its limits.

To turn {{az-workers}} on or off and change their settings, refer to [](configure-worker-settings.md).

## Compare {{az-workers}} [alertzero-compare-workers]

The following table lists each {{az-worker}}'s default schedule and the section of the **{{az-proposed-actions-cap}}** page where its work appears.

| {{az-worker}} | {{az-watch}} | Runs by default | {{az-proposed-actions-cap}} section |
| --- | --- | --- | --- |
| [{{az-alert-triage}}](watches/alert-triage-worker.md) | {{az-triage-watch}} | Every 15 minutes | Investigate |
| [{{az-attack-discovery}}](watches/attack-discovery-worker.md) | {{az-triage-watch}} | Every 24 hours | Investigate |
| [{{az-rule-tuning}}](watches/rule-tuning-worker.md) | {{az-detection-watch}} | Every 2 hours | Configure |
| [{{az-rule-coverage}}](watches/rule-coverage-worker.md) | {{az-detection-watch}} | Every hour | Configure |

% Add rows for the Hunt Watch and Forensics Watch Workers when their pages are written.

## How {{az-watches}} pass work to each other [alertzero-context-engine]

Some {{az-workers}} pick up work that {{az-workers}} in other {{az-watches}} started. They pass it through [{{context-engine}}](/explore-analyze/ai-features/context-engine.md), which stores information that AI features share:

- **Detection gaps:** The {{az-hunt-watch}} records each detection gap it finds. The [{{az-rule-coverage}} {{az-worker}}](watches/rule-coverage-worker.md) picks up each gap and proposes a rule for it.
- **Forensics handoffs:** When the [{{az-attack-discovery}} {{az-worker}}](watches/attack-discovery-worker.md) hands an attack to the {{az-forensics-watch}}, it records the handoff. The [{{az-endpoint-analysis}} {{az-worker}}](watches/endpoint-analysis-worker.md) picks up the handoff and investigates the affected hosts.

For these handoffs to work, {{context-engine}} must be on in each space where the {{az-workers}} run. {{alertzero}} stores the work they pass in an index, which you might notice in **Index Management**. For everything {{alertzero}} needs to run, refer to [](set-up-alertzero.md). To learn more about the index, refer to [](manage-alertzero.md).

% After elastic/docs-content#9114 merges, link the Set up AlertZero reference above to set-up-alertzero.md#alertzero-requirements-dependencies, and the Manage AlertZero reference to manage-alertzero.md#alertzero-indexes.
