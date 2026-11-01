---
description: "Learn what each AlertZero Watch and Worker does in Elastic Security, turn Workers on or off, and decide how much each one does without you."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Configure {{az-watches}} and {{az-workers}} [alertzero-configure-watches-workers]

Each {{az-watch}} groups the {{az-workers}} for one area of work. {{alertzero}} includes four {{az-watches}}: the [{{az-triage-watch}}](watches/triage-watch.md), the [{{az-detection-watch}}](watches/detection-watch.md), the [{{az-hunt-watch}}](watches/hunt-watch.md), and the [{{az-forensics-watch}}](watches/forensics-watch.md). Each {{az-watch}} has its own page in {{alertzero}}, where you turn its {{az-workers}} on or off and change their settings.

## Before you begin [alertzero-configure-before]

- Changing {{az-workers}}, including turning them on or off, needs the `manage_security` cluster privilege. That privilege also lets a user manage users and roles across the cluster, so don't grant it only for {{alertzero}}. Refer to [](alertzero-privileges.md).
- Without `manage_security`, the {{az-watch}} pages are read-only. If you decide which {{az-workers}} run and how much they do without you, but don't have this privilege, ask an administrator to apply your choices.

## Turn {{az-workers}} on or off [alertzero-worker-on-off]

Before you turn off {{az-workers}}, check whether [other {{az-workers}} need them](set-up-alertzero.md). If another {{az-worker}} needs the one you turn off, {{alertzero}} asks you to confirm first and shows a warning on both {{az-workers}}. It never turns {{az-workers}} on or off for you.

When you turn on the {{az-continuous-threat-hunt}} {{az-worker}}, {{alertzero}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that provide its {{az-threat-reports}}. Turning off {{az-continuous-threat-hunt}} turns those workflows off.

## Set {{az-autonomy}} levels [alertzero-worker-autonomy]

Decide each {{az-worker}}'s level based on what it does without you. Every {{az-worker}} starts at {{az-manual}}, and each one offers at most one other level. Changes to detection rules always wait for you, because the {{az-rule-tuning}} and {{az-rule-coverage}} {{az-workers}} don't offer {{az-supervised}}.

| {{az-worker}} | At {{az-manual}} | At its other level |
| --- | --- | --- |
| [{{az-alert-triage}}](watches/alert-triage-worker.md) | Every closure waits for your approval. | {{az-supervised}}: It closes false positives itself, and you can reopen any you disagree with. |
| [{{az-attack-discovery}}](watches/attack-discovery-worker.md) | Every handoff to the {{az-forensics-watch}} waits for your approval. It closes false positives on its own. | {{az-supervised}}: It also hands attacks off without waiting for you. |
| [{{az-rule-tuning}}](watches/rule-tuning-worker.md) | You approve each rule before it analyzes the rule. Every change waits for your approval. | {{az-assisted}}: It analyzes every rule that qualifies without asking. Every change still waits for your approval. |
| [{{az-rule-coverage}}](watches/rule-coverage-worker.md) | You approve each gap before it drafts a rule. Every rule waits for your approval. | {{az-assisted}}: It drafts a rule for every gap without asking. Every rule still waits for your approval. |

% Add rows for Continuous Threat Hunt and Endpoint Analysis when their pages are written.

## Settings every {{az-worker}} has [alertzero-shared-worker-settings]

On its {{az-watch}} page, every {{az-worker}} has these settings:

- **{{az-autonomy-cap}}**: Its [{{az-autonomy}}](glossary.md#alertzero-glossary-autonomy) level. Refer to [](#alertzero-worker-autonomy).
- **Models**: A link to **Feature Settings**, where you select the models that {{alertzero}} uses in the space. {{az-workers}} have no model setting of their own.

{{az-workers}} that run on a schedule also have a **Trigger** that sets how often they run. Some {{az-workers}} have more settings, which their pages list.

## Compare {{az-workers}} [alertzero-compare-workers]

The following table lists each {{az-worker}}'s default schedule and the section of the **{{az-proposed-actions-cap}}** page where its work appears.

| {{az-worker}} | {{az-watch}} | Runs by default | {{az-proposed-actions-cap}} section |
| --- | --- | --- | --- |
| [{{az-alert-triage}}](watches/alert-triage-worker.md) | {{az-triage-watch}} | Every 15 minutes | **Investigate** |
| [{{az-attack-discovery}}](watches/attack-discovery-worker.md) | {{az-triage-watch}} | Every 24 hours | **Investigate** |
| [{{az-rule-tuning}}](watches/rule-tuning-worker.md) | {{az-detection-watch}} | Every 2 hours | **Configure** |
| [{{az-rule-coverage}}](watches/rule-coverage-worker.md) | {{az-detection-watch}} | Every hour | **Configure** |

% Add rows for the Hunt Watch and Forensics Watch Workers when their pages are written.

## How {{az-watches}} pass work to each other [alertzero-context-engine]

Some {{az-workers}} pick up work that {{az-workers}} in other {{az-watches}} started. They pass it through [{{context-engine}}](/explore-analyze/ai-features/context-engine.md), which stores information that AI features share:

- **Detection gaps:** The {{az-hunt-watch}} records each detection gap it finds. The [{{az-rule-coverage}} {{az-worker}}](watches/rule-coverage-worker.md) picks up each gap and proposes a rule for it.
- **Forensics handoffs:** When the [{{az-attack-discovery}} {{az-worker}}](watches/attack-discovery-worker.md) hands an attack to the {{az-forensics-watch}}, it records the handoff. The [{{az-endpoint-analysis}} {{az-worker}}](watches/endpoint-analysis-worker.md) picks up the handoff and investigates the affected hosts.

You don't work in {{context-engine}} directly, but it must be on in each space where these {{az-workers}} run. If it's off, they can't pass work to each other, and their {{az-watch}} page shows **Worker setup needs attention**. Refer to [](set-up-alertzero.md).

{{alertzero}} keeps this shared work in an index that you might notice in **Index Management**. Refer to [](manage-alertzero.md).

% After elastic/docs-content#9114 merges, link the Set up AlertZero references above to set-up-alertzero.md#alertzero-requirements-dependencies and set-up-alertzero.md#alertzero-requirements-worker-settings, and the Manage AlertZero reference to manage-alertzero.md#alertzero-indexes.
