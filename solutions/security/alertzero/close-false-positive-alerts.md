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

The {{az-alert-triage}} {{az-worker}} reviews your open and acknowledged alerts and finds the ones it judges to be false positives. Its [{{az-autonomy}}](configure-worker-settings.md) controls what it does with them.

- With **{{az-manual}}** {{az-autonomy}} (the default) the {{az-worker}} proposes closing the false positives and waits for you to [approve or decline](#alertzero-decide-review) each proposed closure.
- With **{{az-supervised}}** {{az-autonomy}}, the {{az-worker}} closes the false positives on its own. You [check its closures](#alertzero-decide-autonomy) afterward and reopen any that you disagree with.

## How the {{az-alert-triage}} {{az-worker}} picks alerts to close [alertzero-decide-how]

By default, the {{az-alert-triage}} {{az-worker}} runs every 15 minutes and triages alerts of every severity. It proposes closing an alert only when it's at least 85% confident that the alert is a false positive. It tags alerts with a lower score `az:inconclusive` and leaves them open for you to triage.

The {{az-worker}} groups false positives from the same rule that share a pattern into one {{az-proposed-action}}, so you can close a batch of noise in one decision instead of alert by alert. For example, if a backup agent on many hosts runs from the same folder, is signed by the same publisher, and is started by the same parent process, its alerts become one {{az-proposed-action}}.

To change these defaults, edit the {{az-alert-triage}} settings in the {{az-triage-watch}}. For example, you can raise the **Minimum confidence score**, skip less severe alerts with **Minimum severity**, or skip alerts from rules that carry certain tags with **Excluded rule tags**. Refer to [](configure-worker-settings.md).

% For docs writers: After elastic/docs-content#9144 merges, point both links to configure-worker-settings.md on this page at its configure-worker-settings-alert-triage anchor.

## Review a proposed closure [alertzero-decide-review]

1. Find **{{alertzero}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). The **{{az-proposed-actions-cap}}** page opens.
2. In the **Investigate** section, select the card for the proposed closure. This section also lists attacks from the {{az-attack-discovery}} {{az-worker}}, so make sure that the card is for closing alerts. The {{az-investigation}} opens in a flyout.
3. In the flyout's **{{az-proposed-actions-cap}}** section, select the {{az-proposed-action}}.
4. Check that the reasoning holds for every alert in the batch:
    - **Scope:** How many alerts the closure covers, which rule they came from, and which hosts and users they involve. Look for a host or user you don't expect for that rule.
    - **Reasoning:** Why the {{az-alert-triage}} {{az-worker}} judged them false positives. The {{az-worker}} adds a note to each alert that explains why. Look for a note whose reasoning doesn't match what the alert shows. To ask follow-up questions, select **Open chat**.

        :::{note}
        You approve or decline the batch as a whole. If some alerts need a closer look, ask in the chat to remove them from the closure, and then decide the revised closure. You can also decline the closure and handle the alerts individually.
        :::

5. Select **Approve** or **Decline**. You can't change your decision afterward.
    - **If you approve:** The alerts close as false positives. The closure runs under your account, so you need the privileges to close alerts. Without them, the closure fails. Refer to [](alertzero-privileges.md).
    - **If you decline:** The {{az-alert-triage}} {{az-worker}} tags the alerts `az:inconclusive` and leaves them open.

    :::{important}
    The {{az-attack-discovery}} {{az-worker}} skips closed alerts. If you close a real threat by mistake, {{az-attack-discovery}} might miss part of an attack.
    :::

    Each {{az-proposed-action}} expires after 72 hours. If nobody decides before then, the alerts stay open, tagged `az:inconclusive`.

% For docs writers: After elastic/docs-content#9158 merges, point the link to alertzero-privileges.md in step 5 at its alertzero-action-privileges anchor.

## Check past closures [alertzero-decide-autonomy]

You can check any closure, whether someone approved it or the {{az-alert-triage}} {{az-worker}} closed the alerts on its own. If your team sets the {{az-worker}} to {{az-supervised}} {{az-autonomy}}, it closes false positives without waiting for approval, so check its closures regularly, especially soon after the change.

1. On the **{{az-proposed-actions-cap}}** page, expand **Closed Actions**. It lists decisions from the last 72 hours. For older closures, find the alerts on the **Alerts** page.
2. Find the {{az-alert-triage}} closures. To narrow the list to a host or user, filter it by impacted entity.
3. Check who decided each closure. Each closure shows whether a person approved it or the {{az-alert-triage}} {{az-worker}} closed the alerts on its own.

If a closure looks wrong, [reopen its alerts](#alertzero-decide-reopen).

## Reopen alerts closed by mistake [alertzero-decide-reopen]

If a closure turns out to be wrong, reopen its alerts. You can reopen them whether you approved the closure or the {{az-alert-triage}} {{az-worker}} closed them on its own. The {{az-attack-discovery}} {{az-worker}} then considers the reopened alerts again.

1. In **Closed Actions**, select the closure's card to see the evidence behind it.
2. If you disagree with the closure, reopen the alerts. Refer to [](/solutions/security/detect-and-alert/manage-detection-alerts.md#detection-alert-status).

## Next steps [alertzero-decide-next-steps]

- [Respond to an attack](respond-to-attack.md) that the {{az-attack-discovery}} {{az-worker}} finds.
- [Find other work that {{az-workers}} bring you](work-in-alertzero.md).
