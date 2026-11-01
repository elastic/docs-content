---
description: "Review the false-positive alerts that the AlertZero Alert Triage Worker proposes to close in Elastic Security, approve or decline each batch, and reopen any closures you disagree with."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Close false-positive alerts [alertzero-decide]

The {{az-alert-triage}} {{az-worker}} reviews your open and acknowledged alerts and proposes closing the ones it judges to be false positives. It groups alerts that share a pattern into one {{az-proposed-action}}, so you can close a batch of noise in one decision instead of alert by alert.

By default, the {{az-alert-triage}} {{az-worker}} proposes closing an alert only when it's at least 85% confident that the alert is a false positive. It tags alerts below that score `az:inconclusive` and leaves them open for you to triage.

## Review a proposed closure [alertzero-decide-review]

1. In the navigation menu, select **{{alertzero}}**. The **{{az-proposed-actions-cap}}** page opens.
2. In the **Investigate** section, select the {{az-proposed-action}}'s card. Its {{az-investigation}} opens in a flyout.
3. In the flyout's **{{az-proposed-actions-cap}}** section, select the {{az-proposed-action}}.
4. Check that the reasoning holds for every alert in the batch:
    - **Scope:** How many alerts the closure covers, which rule they came from, and which hosts and users they involve. Look for a host or user you don't expect for that rule.
    - **Reasoning:** Why the {{az-alert-triage}} {{az-worker}} judged them false positives. It adds a note to each alert that explains why. Look for a note whose reasoning doesn't match what the alert shows. To ask follow-up questions, select **Open in chat**.

    Your decision covers the whole batch. If even one alert looks wrong, decline and triage the alerts yourself.
5. Select **Approve** or **Decline**. You can't change a decision after you make it, but you can [reopen alerts](#alertzero-decide-reopen) that it closed.
    - **If you approve:** The alerts close as false positives, and the closure runs under your account. The {{az-attack-discovery}} {{az-worker}} skips closed alerts, so closing a real threat by mistake might hide part of an attack.
    - **If you decline:** The {{az-alert-triage}} {{az-worker}} tags the alerts `az:inconclusive` and leaves them open.

    By default, a {{az-proposed-action}} expires after 72 hours. If nobody decides before then, the {{az-alert-triage}} {{az-worker}} tags its alerts `az:inconclusive` and leaves them open, as it does when you decline.

## Reopen alerts closed by mistake [alertzero-decide-reopen]

If a closure turns out to be wrong, reopen its alerts, whether you approved the closure or the {{az-alert-triage}} {{az-worker}} made it on its own. Reopened alerts are back in your queue, and the {{az-attack-discovery}} {{az-worker}} considers them again.

If your team sets the {{az-alert-triage}} {{az-worker}} to {{az-supervised}} {{az-autonomy}}, it closes false positives without waiting for approval. Check its closures regularly, especially soon after the change.

1. On the **{{az-proposed-actions-cap}}** page, expand **Closed Actions**. It lists decisions from the last 72 hours, and **Auto** marks the ones the {{az-alert-triage}} {{az-worker}} made on its own. For older closures, find the alerts on the **Alerts** page.
2. Select a closure's card to see the evidence behind it.
3. If you disagree with the closure, reopen the alerts. Refer to [](/solutions/security/detect-and-alert/manage-detection-alerts.md#detection-alert-status).

## Related pages [alertzero-decide-related]

- [](respond-to-attack.md): Decide what happens next when the {{az-attack-discovery}} {{az-worker}} finds an attack.
- [](use-alertzero.md): Find other work that {{az-workers}} bring you.
