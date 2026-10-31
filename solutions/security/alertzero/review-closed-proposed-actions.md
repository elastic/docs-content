---
description: "Audit AlertZero proposed actions that closed in the last 72 hours in Elastic Security, including ones Workers approved on their own and ones that expired."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Review closed {{az-proposed-actions}} [alertzero-review-closed]

Use the **Closed Actions** section of the **{{az-proposed-actions-cap}}** page to audit recent decisions. It shows who approved or declined each {{az-proposed-action}}, which ones {{az-workers}} approved on their own, which ones expired, and whether approved actions finished.

## Before you begin [alertzero-review-closed-before]

To view **Closed Actions**, you need the **{{alertzero}}** and **Proposed Actions** privileges set to **Read**. To open a card's details, you also need the **Agent Builder** privilege set to **Read**. Refer to [](alertzero-privileges.md).

## Find recently closed {{az-proposed-actions}} [alertzero-review-closed-find]

1. In the navigation menu, select **{{alertzero}}**. The **{{az-proposed-actions-cap}}** page opens.
2. Expand **Closed Actions**.
3. To see a closed {{az-proposed-action}}'s details, select its card.

**Closed Actions** lists the {{az-proposed-actions}} that closed in the last 72 hours, newest first. After that, they stay in their {{az-investigation}}'s details. If {{alertzero}} offered a failed action again, only the latest attempt appears. To show only one host, user, or service, select it in the **Impact** filter.

## What each outcome means [alertzero-review-closed-outcomes]

| Outcome | What happened |
| --- | --- |
| **Approved by _name_** | That person approved it. |
| **Declined by _name_** | That person declined it. |
| **Auto** | The {{az-worker}} approved it at {{az-supervised}} {{az-autonomy}}. Refer to [](configure-worker-settings.md). |
| **Declined** | Someone declined it, but {{alertzero}} can't show who. |
| **Expired** | Nobody decided it in time. |
| **Failed** | The approved action didn't finish. |
