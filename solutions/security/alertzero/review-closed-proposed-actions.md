---
description: "Audit AlertZero proposed actions that closed in the last 72 hours in Elastic Security, including Worker auto-approvals and expired actions, and read each outcome."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Review closed {{az-proposed-actions}} [alertzero-review-closed]

The **Closed Actions** section of the **{{az-proposed-actions-cap}}** page shows what happened to recent {{az-proposed-actions}}, including the ones that {{az-workers}} approved on their own and the ones that nobody decided in time. Check it to confirm that approved actions finished and to see who decided what.

To view **Closed Actions**, you need the **{{alertzero}}** and **Proposed Actions** privileges set to **Read**. To open a card's details, you also need the **Agent Builder** privilege set to **Read**. Refer to [](alertzero-privileges.md).

## Find recently closed {{az-proposed-actions}} [alertzero-review-closed-find]

1. On the **{{az-proposed-actions-cap}}** page, expand **Closed Actions**. It starts collapsed.
2. To see the details of one, select its card.

**Closed Actions** lists the {{az-proposed-actions}} that closed in the last 72 hours, with the most recent decision first. The [entity filter](use-alertzero.md#alertzero-use-filter) applies to it too. When a failed action is retried, only the retry appears.

After 72 hours, {{az-proposed-actions}} leave **Closed Actions**, but they stay with their {{az-investigation}}. To find one, open the {{az-investigation}}'s details and check **{{az-proposed-actions-cap}}**.

## Read the outcome [alertzero-review-closed-outcomes]

Each closed {{az-proposed-action}} shows its outcome:

| Outcome | What happened |
| --- | --- |
| **Approved by** _name_ | That person approved it. |
| **Declined by** _name_ | That person declined it. |
| **Auto** | The {{az-worker}} approved it at {{az-supervised}} {{az-autonomy}}. Refer to [](configure-worker-settings.md). |
| **Declined** | It was declined, but {{alertzero}} can't show who declined it. |
| **Expired** | Nobody decided it in time. |
| **Failed** | It was approved, but the action didn't finish. |
