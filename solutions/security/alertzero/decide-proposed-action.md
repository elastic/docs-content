---
description: "Review an AlertZero proposed action in Elastic Security, then approve it to run the action or decline it, optionally with a reason. Status definitions explain each outcome."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Decide a {{az-proposed-action}} [alertzero-decide]

Approve or decline a {{az-proposed-action}} from a {{az-worker}}, such as closing false-positive alerts, isolating a host, or changing a detection rule. These steps are the same for every {{az-worker}}. For what to check on a specific kind of action, refer to [](decide-detection-change.md), [](respond-to-attack.md), and [](act-on-hunt-finding.md).

## Before you begin [alertzero-decide-before]

- You need the privileges to decide {{az-proposed-actions}}. Approving an action doesn't give you the privileges to run it. An approved action runs as you, so if you don't have the privileges for the action itself, it fails. Refer to [](alertzero-privileges.md).
- Decisions are final. After someone approves or declines, nobody can change the decision.
- By default, {{az-proposed-actions}} expire after 72 hours without a decision. After that, nobody can approve them.

## Review the {{az-proposed-action}} [alertzero-decide-review]

1. In the navigation menu, select **{{alertzero}}**. The **{{az-proposed-actions-cap}}** page opens.
2. Select the {{az-investigation}}'s card. Its details open in a flyout.
3. In the **{{az-proposed-actions-cap}}** section, select the {{az-proposed-action}} you want to review.
4. Before you decide, check:
    - The {{az-worker}}'s description of the action and why it proposes it.
    - Whether the action is **Reversible** or **Irreversible**.
    - How much impact the action has.
    - When the {{az-proposed-action}} expires.

## Approve the {{az-proposed-action}} [alertzero-decide-approve]

Select **Approve**. The action starts immediately and runs as you. The status changes to **Applying**, then to **Applied** when the action finishes, or **Failed** if it doesn't.

If the action fails, {{alertzero}} can offer it again as a new {{az-proposed-action}} with the same expiry.

## Decline the {{az-proposed-action}} [alertzero-decide-decline]

1. Select **Decline**.
2. Optionally, select a reason, such as **Not a real issue (false positive)**. If you select **Other**, enter a description.
3. Select **Decline** again.

## Decide whether to close false-positive alerts [alertzero-decide-close-alerts]

The {{az-alert-triage}} {{az-worker}} proposes closing alerts it's confident are false positives, with one {{az-proposed-action}} for alerts that share a pattern. These {{az-proposed-actions}} appear in the **Investigate** section.

- If you approve, the alerts close.
- If you decline, {{az-alert-triage}} tags the alerts inconclusive.

At {{az-supervised}} {{az-autonomy}}, {{az-alert-triage}} closes false positives without waiting for you, and you can reopen any you disagree with.

## When {{az-workers}} decide for you [alertzero-decide-after]

At {{az-supervised}} {{az-autonomy}}, {{az-workers}} approve their own {{az-proposed-actions}}. To check those decisions afterward, refer to [](review-closed-proposed-actions.md). To change {{az-autonomy}} levels, refer to [](configure-worker-settings.md).

## {{az-proposed-action-cap}} statuses [alertzero-decide-statuses]

| Status | What it means |
| --- | --- |
| **Needs review** | Waiting for a decision. |
| **Applying** | Approved, and the action is running. |
| **Applied** | Approved, and the action finished. |
| **Failed** | Approved, but the action didn't finish. |
| **Approved** | Approved, with no action to run. |
| **Declined** | Someone declined it. |
| **Expired** | Nobody decided it in time. |
