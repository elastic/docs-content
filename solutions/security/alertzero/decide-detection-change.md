---
description: "Approve or decline an AlertZero detection change in Elastic Security: a tuned rule from Rule Tuning, or a new, installed, or turned-on rule from Rule Coverage."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Decide a detection change [alertzero-decide-detection-change]

The {{az-detection-watch}} proposes changes to your detection rules: tuning a rule that produces too many false positives, or adding a rule for a detection gap. Every detection change waits for your approval, so a rule never changes without someone deciding. To learn what starts each kind of change, refer to the [{{az-detection-watch}}](watches-and-workers.md#alertzero-detection-watch).

## Before you begin [alertzero-detection-change-before]

- You need the **{{alertzero}}** and **Agent Builder** privileges set to **Read**, the **Proposed Actions** privilege set to **All**, and the **Rules and Exceptions** privilege set to **All**, because an approved change runs as you. Refer to [](alertzero-privileges.md).
- Detection changes appear in the **Configure** section of the **{{az-proposed-actions-cap}}** page.

## Decide a tuning change [alertzero-detection-change-tuning]

The {{az-rule-tuning}} {{az-worker}} proposes one change per rule: an exception, a query edit, or a new risk score, threshold, or schedule.

1. On the **{{az-proposed-actions-cap}}** page, select the card for the rule's {{az-investigation}}. Its name starts with **Rule tuning:**.
2. In the **{{az-proposed-actions-cap}}** section, select the change.
3. Check the change before you decide:
    - **Why this rule was picked** explains why the rule qualified for tuning.
    - **Proposed change** shows what changes, before and after.
    - **Backtest** compares **Alerts with the current rule** with **Alerts with the proposed change**, so you can check that the change drops the false positives without hiding real threats.
4. Select **Approve** to change the rule, or **Decline** to leave it as it is.

When you approve, {{alertzero}} changes the rule in place or adds the exception. You can change it back later. Refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md). If someone edited the rule after the change was proposed, the approval fails, and you can decline it instead. When you decline, the rule stays as it is and the {{az-investigation}} closes.

To tune a rule by hand instead, refer to [](/solutions/security/detect-and-alert/tune-detection-rules.md).

## Decide a rule for a detection gap [alertzero-detection-change-coverage]

The {{az-rule-coverage}} {{az-worker}} proposes a rule for each gap that the {{az-hunt-watch}} finds.

1. On the **{{az-proposed-actions-cap}}** page, select the card for the gap's {{az-investigation}}. Its name starts with **Detection coverage:**.
2. In the **{{az-proposed-actions-cap}}** section, select the proposed rule.
3. Check what the {{az-proposed-action}} would do, and select **Approve** or **Decline**:

| Proposed action | When you approve |
| --- | --- |
| **Create a new {{esql}} detection rule** | {{alertzero}} creates the rule, turned off. Before you approve, check its query and its **Backtest**, which shows how many matches it would have had. After you approve, review the rule and turn it on. |
| Install a prebuilt rule | {{alertzero}} installs the rule and turns it on. |
| Turn on an existing rule | {{alertzero}} turns the rule on. |
| **Confirm rule coverage** | Nothing runs. You confirm that an existing rule already covers the gap. |

When you decline, {{alertzero}} discards the draft rule, or the rule stays off or uninstalled.

To manage rules by hand, refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md) and [](/solutions/security/detect-and-alert/install-prebuilt-rules.md).

## Related pages [alertzero-detection-change-related]

- [](decide-proposed-action.md): The steps every decision shares, and what each status means.
- [](watches-and-workers.md): What each {{az-worker}} needs, and its settings.
