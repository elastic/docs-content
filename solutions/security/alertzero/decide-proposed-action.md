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

{{alertzero}} {{az-workers}} recommend actions, such as closing false-positive alerts, isolating a host, or changing a detection rule. Each {{az-proposed-action}} waits for one decision: approve it to run the action, or decline it. These steps are the same for every {{az-worker}}. For what to check before you decide a specific kind of action, refer to [](decide-detection-change.md), [](respond-to-attack.md), and [](act-on-hunt-finding.md).

## Before you begin [alertzero-decide-before]

- To approve or decline, you need the **{{alertzero}}** privilege set to **Read** and the **Proposed Actions** privilege set to **All**.
- An approved action runs as you, so you also need the privileges for the action itself, such as **Alerts**: **All** to close alerts. Refer to [](alertzero-privileges.md).
- To open {{az-investigation}} details, you need the **Agent Builder** privilege set to **Read**.

## Review the {{az-proposed-action}} [alertzero-decide-review]

1. On the **{{az-proposed-actions-cap}}** page, select the card for the {{az-investigation}}. Its details open in a flyout.
2. In the **{{az-proposed-actions-cap}}** section, select the {{az-proposed-action}} you want to review.
3. Check what the action does before you decide. The {{az-worker}}'s description explains the action and why it proposes it. The {{az-proposed-action}} also shows:
    - Whether the action is **Reversible** or **Irreversible**.
    - How much impact it has.
    - When the {{az-proposed-action}} expires.

## Approve it [alertzero-decide-approve]

Select **Approve**. The action starts right away, and runs as you. It's **Applying** while it runs, then **Applied** when it finishes, or **Failed** if it doesn't.

## Decline it [alertzero-decide-decline]

1. Select **Decline**.
2. Optionally, select a reason. The default is **Decline without a reason**. The other reasons are:
    - **Already reported elsewhere (duplicate)**
    - **Not a real issue (false positive)**
    - **Handled elsewhere**
    - **No actions needed (risk is acceptable)**
    - **Other**, which requires a description
3. Select **Decline** again.

## What happens after you decide [alertzero-decide-after]

- **Decisions are final.** After anyone decides, nobody can change the decision or decide the {{az-proposed-action}} again.
- **Undecided {{az-proposed-actions}} expire.** If nobody decides within 72 hours, the {{az-proposed-action}} expires and can't be approved anymore.
- **Some {{az-workers}} approve their own {{az-proposed-actions}}.** At {{az-supervised}} {{az-autonomy}}, {{az-workers}} approve their own {{az-proposed-actions}}, and the actions run as their service accounts. To review those decisions afterward, refer to [](review-closed-proposed-actions.md). To change {{az-autonomy}} levels, refer to [](configure-worker-settings.md).

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
