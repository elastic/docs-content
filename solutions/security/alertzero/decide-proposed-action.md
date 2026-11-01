---
description: "Review an AlertZero proposed action in Elastic Security, approve or decline it, and check what happened to recent decisions, including ones Workers made on their own."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Decide a {{az-proposed-action}} [alertzero-decide]

Approve or decline the {{az-proposed-actions}} that {{az-workers}} bring you, such as closing false-positive alerts, isolating a host, or changing a detection rule. These steps are the same for every {{az-worker}}. For what to check on a specific kind of action, refer to [](respond-to-attack.md), [](act-on-hunt-finding.md), and [](decide-detection-change.md).

## Review the {{az-proposed-action}} [alertzero-decide-review]

1. In the navigation menu, select **{{alertzero}}**. The **{{az-proposed-actions-cap}}** page opens.
2. Select the {{az-proposed-action}}'s card. Its {{az-investigation}} opens in a flyout.
3. In the **{{az-proposed-actions-cap}}** section, select the {{az-proposed-action}}.
4. Before you decide, check:
    - What the {{az-worker}} wants to do, and why.
    - Whether the action is **Reversible** or **Irreversible**.
    - How much impact the action has.
    - When the {{az-proposed-action}} expires. By default, nobody can approve it after 72 hours.

## Approve or decline [alertzero-decide-approve]

- **To approve:** Select **Approve**. The action starts immediately and runs as you. Its status changes to **Applying**, then to **Applied** when the action finishes, or **Failed** if it doesn't. If your role doesn't allow the action, it fails, and {{alertzero}} can offer it again so someone else can approve it.
- **To decline:** Select **Decline**, optionally select a reason, such as **Not a real issue (false positive)**, then select **Decline** again.

You can't change a decision after you make it.

## Decide whether to close false-positive alerts [alertzero-decide-close-alerts]

The {{az-alert-triage}} {{az-worker}} proposes closing alerts it's confident are false positives, with one {{az-proposed-action}} for alerts that share a pattern. These {{az-proposed-actions}} appear in the **Investigate** section.

- If you approve, the alerts close.
- If you decline, {{az-alert-triage}} tags the alerts inconclusive.

At {{az-supervised}} {{az-autonomy}}, {{az-alert-triage}} closes false positives without waiting for you, and you can reopen any you disagree with.

## Check recent decisions [alertzero-decide-closed]

To see what happened to {{az-proposed-actions}} decided in the last 72 hours, expand **Closed Actions** at the bottom of the **{{az-proposed-actions-cap}}** page. Each card shows who decided it and how it turned out. **Auto** means a {{az-worker}} at {{az-supervised}} {{az-autonomy}} approved it without a person. To check its evidence, select the card.

After 72 hours, closed {{az-proposed-actions}} stay in their {{az-investigation}}'s details.
