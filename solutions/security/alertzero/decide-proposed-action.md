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

{{alertzero}} {{az-workers}} bring you {{az-proposed-actions}}, such as closing false-positive alerts, isolating a host, or changing a detection rule. Each one waits for you to approve or decline it. Learn what to check before you decide, what happens after, and what each status means.

These steps are the same for every {{az-worker}}. For what to check on a specific kind of action, refer to [](decide-detection-change.md), [](respond-to-attack.md), and [](act-on-hunt-finding.md).

## Before you begin [alertzero-decide-before]

- You need the **{{alertzero}}** and **Agent Builder** privileges set to **Read**, and the **Proposed Actions** privilege set to **All**.
- An approved action runs as you, so you also need the privileges for the action itself, such as **Alerts**: **All** to close alerts. Without them, the action fails. Refer to [](alertzero-privileges.md).
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

## When {{az-workers}} decide for you [alertzero-decide-after]

At {{az-supervised}} {{az-autonomy}}, {{az-workers}} approve their own {{az-proposed-actions}}, and the actions run as each {{az-worker}}'s service account instead of as you. To check those decisions afterward, refer to [](review-closed-proposed-actions.md). To change {{az-autonomy}} levels, refer to [](configure-worker-settings.md).

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
