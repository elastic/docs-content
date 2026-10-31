---
description: "Review an AlertZero proposed action in Elastic Security, then approve it to run the action or decline it, optionally with a reason. Status definitions explain each outcome."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Decide a {{az-proposed-action}} [alertzero-decide]

{{alertzero}} {{az-workers}} recommend actions, such as closing false-positive alerts, isolating a host, or changing a detection rule. Each {{az-proposed-action}} waits for one decision. Approve it to run the action, or decline it. These steps are the same for every {{az-worker}}. For what to check before you decide a specific kind of action, refer to [](decide-detection-change.md), [](respond-to-attack.md), and [](act-on-hunt-finding.md).

## Before you begin [alertzero-decide-before]

- You need the **{{alertzero}}** and **Agent Builder** privileges set to **Read**, and the **Proposed Actions** privilege set to **All**.
- An approved action runs as you, so you also need the privileges for the action itself, such as **Alerts**: **All** to close alerts. Refer to [](alertzero-privileges.md).
- Decisions are final. After anyone decides a {{az-proposed-action}}, nobody can change the decision or decide it again.
- By default, a {{az-proposed-action}} expires if nobody decides it within 72 hours. After that, nobody can approve it.

## Review the {{az-proposed-action}} [alertzero-decide-review]

1. Select **{{alertzero}}** in the navigation menu to open the **{{az-proposed-actions-cap}}** page.
2. Select the card for the {{az-investigation}}. Its details open in a flyout.
3. In the **{{az-proposed-actions-cap}}** section, select the {{az-proposed-action}} you want to review.
4. Check what the action does before you decide. The {{az-worker}}'s description explains the action and why the {{az-worker}} proposes it. The {{az-proposed-action}} also shows:
    - Whether the action is **Reversible** or **Irreversible**.
    - How much impact the action has.
    - When the {{az-proposed-action}} expires.

## Approve the {{az-proposed-action}} [alertzero-decide-approve]

Select **Approve**. The action starts right away and runs as you. While the action runs, the {{az-proposed-action}} shows **Applying**. It then shows **Applied** when the action finishes, or **Failed** if the action doesn't finish.

If an approved action fails, {{alertzero}} can offer it again as a new {{az-proposed-action}} that keeps the original expiry. You decide the new one the same way.

## Decline the {{az-proposed-action}} [alertzero-decide-decline]

1. Select **Decline**.
2. Optionally, select a reason. The default is **Decline without a reason**. The other reasons are:
    - **Already reported elsewhere (duplicate)**
    - **Not a real issue (false positive)**
    - **Handled elsewhere**
    - **No actions needed (risk is acceptable)**
    - **Other**, which requires a description
3. Select **Decline** again.

## When {{az-workers}} decide for you [alertzero-decide-after]

At {{az-supervised}} {{az-autonomy}}, {{az-workers}} approve their own {{az-proposed-actions}}, so those actions run as each {{az-worker}}'s service account, not as you. To review those decisions afterward, refer to [](review-closed-proposed-actions.md). To change {{az-autonomy}} levels, refer to [](configure-worker-settings.md).

## {{az-proposed-action-cap}} statuses [alertzero-decide-statuses]

| Status | What it means |
| --- | --- |
| **Needs review** | It's waiting for a decision. |
| **Applying** | It's approved, and the action is running. |
| **Applied** | It's approved, and the action finished. |
| **Approved** | It's approved, and it had no action to run. |
| **Declined** | Someone declined it. |
| **Failed** | It's approved, but the action didn't finish. |
| **Expired** | Nobody decided it in time. |
