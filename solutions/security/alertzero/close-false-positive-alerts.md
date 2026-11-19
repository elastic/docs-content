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

# Close false-positive alerts [alertzero-close-false-positives]

The {{az-alert-triage}} {{az-worker}} reviews your open and acknowledged alerts and finds the ones it judges to be false positives. Its [{{az-autonomy}}](configure-worker-settings.md#configure-worker-settings-alert-triage) controls what it does with them.

- With **{{az-manual}}** {{az-autonomy}} (the default), the {{az-worker}} proposes closing the false positives and waits for you to [review](#alertzero-close-false-positives-review) and [approve or decline](#alertzero-close-false-positives-decide) each proposed closure.
- With **{{az-supervised}}** {{az-autonomy}}, the {{az-worker}} closes the false positives on its own. You [check its closures](#alertzero-close-false-positives-past-closures) afterward and reopen any that you disagree with.

## How the {{az-alert-triage}} {{az-worker}} picks alerts to close [alertzero-close-false-positives-how]

By default, the {{az-alert-triage}} {{az-worker}} runs every 15 minutes and triages alerts of every severity. It proposes closing an alert only when it's at least 85% confident that the alert is a false positive. It tags alerts with a lower score `az:inconclusive` and leaves them open for you to triage.

The {{az-worker}} groups false positives from the same rule that share a pattern into one {{az-proposed-action}}. For example, if a backup agent on many hosts runs from the same folder, with the same publisher signature and the same parent process, its alerts become one {{az-proposed-action}}.

To change how often the {{az-worker}} runs, which alerts it triages, or how confident it must be before it proposes a closure, refer to [{{az-alert-triage}} settings](configure-worker-settings.md#configure-worker-settings-alert-triage).

## Review a proposed closure [alertzero-close-false-positives-review]

Open the proposed closure on the **{{az-proposed-actions-cap}}** page, and check that the reasoning holds for every alert in the batch. Start with how many alerts the closure covers, which rule they came from, and which hosts and users they involve. A host or user you don't expect for that rule is a reason to look closer. The {{az-worker}} also adds a note to each alert that explains why it judged the alert a false positive, so look for a note whose reasoning doesn't match what the alert shows.

You decide the batch as a whole. If some alerts need a closer look, ask in the {{az-investigation}}'s chat to remove them from the closure, or decline the closure and handle the alerts one by one.

## Approve or decline a proposed closure [alertzero-close-false-positives-decide]

After you review a closure, approve or decline it.

- **If you approve:** The alerts close as false positives. The closure runs under your account, so you need the [privileges to close alerts](alertzero-privileges.md#alertzero-action-privileges). Without them, the closure fails.
- **If you decline:** The alerts stay open, tagged `az:inconclusive`. The same happens if the {{az-proposed-action}} [expires](work-in-alertzero.md) before anyone decides.

:::{important}
You can't change your decision on a proposed closure. If you approve one by mistake, [reopen its alerts](#alertzero-close-false-positives-past-closures). Until you do, the {{az-attack-discovery}} {{az-worker}} skips them, so it might miss part of an attack.
:::

## Check and reopen past closures [alertzero-close-false-positives-past-closures]

Check closures regularly, especially soon after your team switches the {{az-alert-triage}} {{az-worker}} to {{az-supervised}} {{az-autonomy}}.

**Closed Actions** on the **{{az-proposed-actions-cap}}** page lists decisions from the last 72 hours, with the evidence behind each one. A closure that the {{az-worker}} made on its own names the {{az-worker}}.

If you disagree with a closure, [reopen its alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md#detection-alert-status) on the **Alerts** page, where you can also find alerts from older closures. The {{az-attack-discovery}} {{az-worker}} then considers the reopened alerts again.

## Next steps [alertzero-close-false-positives-next-steps]

- [Respond to an attack](respond-to-attack.md) that the {{az-attack-discovery}} {{az-worker}} finds.
- [Find other work that {{az-workers}} bring you](work-in-alertzero.md).
