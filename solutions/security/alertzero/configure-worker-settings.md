---
description: "Turn AlertZero Workers on or off in Elastic Security, set how much each one does without you, and change their other settings."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Configure {{az-workers}} [alertzero-configure-workers]

You configure {{az-workers}} on the page for their {{az-watch}}. There, you can turn each {{az-worker}} on or off, set how much it does without you, and change its other settings. To learn what each {{az-watch}} and {{az-worker}} does, refer to [](watches-and-workers.md).

## Before you begin [alertzero-configure-before]

To change a {{az-worker}}'s settings, you need **All** for **{{alertzero}}** and the `manage_security` cluster privilege. To turn {{az-workers}} on or off, you also need the **Workflows** sub-feature privileges **Update** and **Update managed workflows**. Without `manage_security`, the {{az-watch}} pages are read-only, and you can ask an administrator to apply your changes. For where to grant these privileges, refer to [](alertzero-privileges.md).

% After elastic/docs-content#9115 merges, link the privileges reference above to alertzero-privileges.md#alertzero-privileges-configure.

## Change a {{az-worker}}'s settings [alertzero-change-worker-settings]

1. Find **Watches** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the {{az-watch}} that the {{az-worker}} belongs to, such as **{{az-triage-watch}}**.
3. Find the {{az-worker}}. On a {{az-watch}} with more than one {{az-worker}}, expand the {{az-worker}}'s section.
4. Make your changes:

    - To turn the {{az-worker}} on or off, use the **Enabled** switch. Refer to [](#alertzero-worker-on-off).
    - To change how much it does without you, select an **{{az-autonomy-cap}}** level. Refer to [](#alertzero-worker-autonomy).
    - To change how often it runs or its other settings, refer to the {{az-worker}}'s page.

5. Select **Save**. To undo your changes instead, select **Discard**.

Your changes don't take effect until you save. If you leave the page with unsaved changes, {{alertzero}} asks you to confirm.

## What happens when you turn a {{az-worker}} on or off [alertzero-worker-on-off]

Some {{az-workers}} depend on work from others. Before you turn off a {{az-worker}}, check whether [other {{az-workers}} need it](set-up-alertzero.md). If another {{az-worker}} needs the one you turn off, {{alertzero}} asks you to confirm and then shows a warning on both {{az-workers}}. After setup, {{alertzero}} never turns {{az-workers}} on or off for you.

Turning on the {{az-continuous-threat-hunt}} {{az-worker}} also turns on the [{{az-threat-intel-supply}}](glossary.md#alertzero-glossary-threat-intel-supply) workflows that provide its {{az-threat-reports}}. These are workflows, not {{az-workers}}. When you turn {{az-continuous-threat-hunt}} off, {{alertzero}} turns off the space's **Attribute alerts to reports** workflow. It turns off the shared **Ingest** and **Enrich** workflows only if no other space still uses them.

## Select an {{az-autonomy}} level [alertzero-worker-autonomy]

Decide each {{az-worker}}'s level based on what it does without you. Every {{az-worker}} starts at **{{az-manual}}**, and each one offers at most one other level. You always approve changes to detection rules yourself, because the {{az-rule-tuning}} and {{az-rule-coverage}} {{az-workers}} don't offer **{{az-supervised}}**.

### {{az-workers}} that offer {{az-supervised}} [alertzero-autonomy-supervised]

| {{az-worker}} | At {{az-manual}} | At {{az-supervised}} |
| --- | --- | --- |
| [{{az-alert-triage}}](watches/alert-triage-worker.md) | It closes alerts only after you approve. | It closes false positives itself, and you can reopen any you disagree with. |
| [{{az-attack-discovery}}](watches/attack-discovery-worker.md) | It hands an attack to the {{az-forensics-watch}} only after you approve. When it judges an attack a false positive, it acknowledges the open alerts and closes the attack and the {{az-investigation}} on its own. | It also hands attacks off without asking you first. |

### {{az-workers}} that offer {{az-assisted}} [alertzero-autonomy-assisted]

| {{az-worker}} | At {{az-manual}} | At {{az-assisted}} |
| --- | --- | --- |
| [{{az-rule-tuning}}](watches/rule-tuning-worker.md) | You approve each rule before it analyzes the rule, and you approve each change before it reaches the rule. | It analyzes every rule that qualifies without asking, but you still approve each change before it reaches the rule. |
| [{{az-rule-coverage}}](watches/rule-coverage-worker.md) | You approve each gap before it drafts a rule, and you approve each rule before it takes effect. | It drafts a rule for every gap without asking, but you still approve each rule before it takes effect. |

% When the Continuous Threat Hunt and Endpoint Analysis pages are written, add each Worker to the table for the level it offers besides Manual: Supervised or Assisted. If a Worker offers only Manual, add a sentence after the tables instead. If it offers a level not covered here, add a new subsection and table for that level.

% After elastic/docs-content#9114 merges, link the Set up AlertZero reference above to set-up-alertzero.md#alertzero-requirements-dependencies.
