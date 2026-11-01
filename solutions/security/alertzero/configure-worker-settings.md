---
description: "Learn what each AlertZero Watch and Worker does in Elastic Security, turn Workers on or off, and decide what needs your approval."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Configure {{az-watches}} and {{az-workers}} [alertzero-configure-watches-workers]

{{alertzero}} groups its {{az-workers}} by area of expertise into the [{{az-triage-watch}}](watches/triage-watch.md), [{{az-detection-watch}}](watches/detection-watch.md), [{{az-hunt-watch}}](watches/hunt-watch.md), and [{{az-forensics-watch}}](watches/forensics-watch.md). From each {{az-watch}}'s page, you can turn its {{az-workers}} on or off and change their settings.

## {{az-workers}} at a glance [alertzero-compare-workers]

Use the following table to find each {{az-worker}}'s {{az-watch}}, how often it runs by default, and where on the **{{az-proposed-actions-cap}}** page you review its work.

| {{az-worker}} | {{az-watch}} | Runs by default | {{az-proposed-actions-cap}} section |
| --- | --- | --- | --- |
| [{{az-alert-triage}}](watches/alert-triage-worker.md) | {{az-triage-watch}} | Every 15 minutes | Investigate |
| [{{az-attack-discovery}}](watches/attack-discovery-worker.md) | {{az-triage-watch}} | Every 24 hours | Investigate |
| [{{az-rule-tuning}}](watches/rule-tuning-worker.md) | {{az-detection-watch}} | Every 2 hours | Configure |
| [{{az-rule-coverage}}](watches/rule-coverage-worker.md) | {{az-detection-watch}} | Every hour | Configure |

% Add rows for the Hunt Watch and Forensics Watch Workers when their pages are written.

## How {{az-workers}} depend on each other [alertzero-worker-on-off]

Some {{az-workers}} depend on another {{az-worker}}'s results. If you turn off the {{az-worker}} they depend on, they stay on, but they get less to work on, or nothing:

- If you turn off {{az-continuous-threat-hunt}}, {{az-rule-coverage}} gets no new detection gaps to propose rules for.
- If you turn off {{az-attack-discovery}}, {{az-endpoint-analysis}} gets no attacks to investigate.
- If you turn off {{az-alert-triage}}, false positives stay open until someone closes them. {{az-attack-discovery}} analyzes them along with your other open alerts, and {{az-rule-tuning}} counts only the false positives that people close.

These {{az-workers}} also depend on [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) to pass results to each other. If {{context-engine}} is off in a space, {{az-rule-coverage}} and {{az-endpoint-analysis}} get nothing to work on, even when {{az-continuous-threat-hunt}} and {{az-attack-discovery}} are on. For everything {{alertzero}} needs to run, refer to [](set-up-alertzero.md).

% After elastic/docs-content#9114 merges, link the "everything AlertZero needs to run" reference in the Context Engine paragraph to set-up-alertzero.md#alertzero-turn-on-workers.

## What you approve for {{az-workers}} [alertzero-worker-autonomy]

To control which steps wait for your approval, set each {{az-worker}}'s **{{az-autonomy-cap}}** level. Every {{az-worker}} starts at **{{az-manual}}**, where you approve every action it proposes. Some {{az-workers}} also ask you before they start analyzing. Each {{az-worker}} offers at most one other level, where you approve less:

- **{{az-assisted}}**: The {{az-worker}} starts its analysis without asking you, but it still waits for you before it makes any change.
- **{{az-supervised}}**: The {{az-worker}} approves its own {{az-proposed-actions}}, and you review the results afterward.

The following table shows what you approve for each {{az-worker}} at each level it offers.

| {{az-worker}} | {{az-manual}} | {{az-assisted}} | {{az-supervised}} |
| --- | --- | --- | --- |
| [{{az-alert-triage}}](watches/alert-triage-worker.md) | Each closure it proposes | Not offered | Nothing. It closes false positives on its own, and you can reopen any you disagree with. |
| [{{az-attack-discovery}}](watches/attack-discovery-worker.md) | Each attack before it goes to the {{az-forensics-watch}}. It closes false-positive attacks on its own. | Not offered | Nothing. It hands attacks off on its own. |
| [{{az-rule-tuning}}](watches/rule-tuning-worker.md) | Each rule before the {{az-worker}} analyzes it, and each change before it reaches the rule | Each change before it reaches the rule | Not offered |
| [{{az-rule-coverage}}](watches/rule-coverage-worker.md) | Each gap before the {{az-worker}} drafts a rule, and each rule before it takes effect | Each rule before it takes effect | Not offered |

% When the Continuous Threat Hunt and Endpoint Analysis pages are written, add a row to the table for each Worker. If a Worker offers a level that isn't in the table, add a column for it and add the level to the list of levels in this section.

## Change {{az-worker}} settings [alertzero-change-worker-settings]

:::{note}
To change a {{az-worker}}'s settings, you need **All** for **{{alertzero}}** and the `manage_security` cluster privilege. To turn {{az-workers}} on or off, you also need the **Workflows** sub-feature privileges **Update** and **Update managed workflows**. To learn more, refer to [](alertzero-privileges.md).
:::

% After elastic/docs-content#9115 merges, link the privileges reference in the note to alertzero-privileges.md#alertzero-privileges-configure.

1. Find **Watches** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the {{az-watch}} that the {{az-worker}} belongs to, such as **{{az-triage-watch}}**.
3. Find the {{az-worker}}. On a {{az-watch}} with more than one {{az-worker}}, expand the {{az-worker}}'s section.
4. Make your changes:

    - To turn the {{az-worker}} on or off, use the **Enabled** switch. Before you turn it off, check [which {{az-workers}} depend on it](#alertzero-worker-on-off).
    - To change what needs your approval, select an **{{az-autonomy-cap}}** level. Refer to [what you approve at each level](#alertzero-worker-autonomy).
    - To change how often it runs or its other settings, refer to the {{az-worker}}'s page.

5. Select **Save**. To undo your changes instead, select **Discard**.
