---
description: "Find the AlertZero Watches and Workers in Elastic Security, the settings every Worker has, and how the Workers compare."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-watches}} and {{az-workers}} [alertzero-watches-and-workers]

Each {{az-watch}} groups the {{az-workers}} for one area of work. {{alertzero}} includes four {{az-watches}}: the [{{az-triage-watch}}](watches/triage-watch.md), the [{{az-detection-watch}}](watches/detection-watch.md), the [{{az-hunt-watch}}](watches/hunt-watch.md), and the [{{az-forensics-watch}}](watches/forensics-watch.md). Each {{az-worker}} has its own page that covers what it does, what it needs, its settings, and where its work appears.

## Settings every {{az-worker}} has [alertzero-shared-worker-settings]

Each {{az-watch}} has its own page in {{alertzero}}, where you turn its {{az-workers}} on or off and change their settings. On that page, every {{az-worker}} has these settings:

- **{{az-autonomy-cap}}**: Its [{{az-autonomy}}](glossary.md#alertzero-glossary-autonomy) level. Each {{az-worker}} offers only the levels that suit its work, and starts at {{az-manual}}.
- **Models**: A link to **Feature Settings**, where you select the models that {{alertzero}} uses in the space. A {{az-worker}} has no model setting of its own.

{{az-workers}} that run on a schedule also have a **Trigger** that sets how often they run. Some {{az-workers}} have more settings, which their pages list. To change settings, refer to [](configure-worker-settings.md).

## Compare {{az-workers}} [alertzero-compare-workers]

The following table lists each {{az-worker}}'s default schedule, the {{az-autonomy}} levels it offers, and the section of the **{{az-proposed-actions-cap}}** page where its work appears.

| {{az-worker}} | {{az-watch}} | Runs by default | {{az-autonomy-cap}} levels | {{az-proposed-actions-cap}} section |
| --- | --- | --- | --- | --- |
| [{{az-alert-triage}}](watches/alert-triage-worker.md) | {{az-triage-watch}} | Every 15 minutes | {{az-manual}}, {{az-supervised}} | **Investigate** |
| [{{az-attack-discovery}}](watches/attack-discovery-worker.md) | {{az-triage-watch}} | Every 24 hours | {{az-manual}}, {{az-supervised}} | **Investigate** |
| [{{az-rule-tuning}}](watches/rule-tuning-worker.md) | {{az-detection-watch}} | Every 2 hours | {{az-manual}}, {{az-assisted}} | **Configure** |
| [{{az-rule-coverage}}](watches/rule-coverage-worker.md) | {{az-detection-watch}} | Every hour | {{az-manual}}, {{az-assisted}} | **Configure** |

% Add rows for the Hunt Watch and Forensics Watch Workers when their pages are written.
