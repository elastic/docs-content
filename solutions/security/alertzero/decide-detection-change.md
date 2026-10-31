---
description: "Approve or decline an AlertZero detection change in Elastic Security: a tuned rule from Rule Tuning, or a new, installed, or turned-on rule from Rule Coverage."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Decide a detection change [alertzero-decide-detection-change]

The {{az-detection-watch}} proposes two kinds of changes to your detection rules. The {{az-rule-tuning}} {{az-worker}} tunes rules that produce too many false positives, and the {{az-rule-coverage}} {{az-worker}} proposes rules for detection gaps. Every detection change waits for your approval, so no rule changes without a person deciding. Learn what to check before you approve each kind of change, and what happens to the rule after you decide.

To learn what starts each kind of change, refer to the [{{az-detection-watch}}](watches-and-workers.md#alertzero-detection-watch).

## Before you begin [alertzero-detection-change-before]

- You need the **{{alertzero}}** and **Agent Builder** privileges set to **Read**, and the **Proposed Actions** privilege set to **All**.
- An approved change runs as you, so you also need the **Rules and Exceptions** privilege set to **All**. Refer to [](alertzero-privileges.md).

## Decide a tuning change [alertzero-detection-change-tuning]

The {{az-rule-tuning}} {{az-worker}} proposes one change for each noisy rule.

1. In the **Configure** section of the **{{az-proposed-actions-cap}}** page, select the rule's card. Its name starts with **Rule tuning:**.
2. In the **{{az-proposed-actions-cap}}** section, select the change.
3. Before you decide, check these sections:
    - **Why this rule was picked** explains why the rule qualified for tuning.
    - **Proposed change** shows the rule before and after the change.
    - **Backtest** compares **Alerts with the current rule** with **Alerts with the proposed change**. Use it to check that the change drops the false positives without hiding real threats.
4. Select **Approve** to change the rule, or **Decline** to keep it unchanged.

When you approve, {{alertzero}} changes the rule in place or adds the exception. To undo the change later, edit the rule. Refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md). If someone edited the rule after {{az-rule-tuning}} proposed the change, the approval fails, so decline the change instead.

When you decline, the rule doesn't change and the {{az-investigation}} closes.

To tune a rule by hand instead, refer to [](/solutions/security/detect-and-alert/tune-detection-rules.md).

## Decide a rule for a detection gap [alertzero-detection-change-coverage]

The {{az-rule-coverage}} {{az-worker}} proposes a rule for each gap that the {{az-hunt-watch}} finds.

1. In the **Configure** section of the **{{az-proposed-actions-cap}}** page, select the gap's card. Its name starts with **Detection coverage:**.
2. In the **{{az-proposed-actions-cap}}** section, select the proposed rule.
3. Check what the {{az-proposed-action}} does, then select **Approve** or **Decline**.

What happens when you approve depends on the kind of {{az-proposed-action}}:

| {{az-proposed-action-cap}} | When you approve |
| --- | --- |
| Create a new {{esql}} rule | {{alertzero}} creates the rule, turned off. Review the rule, then turn it on. Before you approve, check the **Proposed rule** query and the **Backtest**, which shows how often the rule would have matched. |
| Install a prebuilt rule | {{alertzero}} installs the rule and turns it on. |
| Turn on an existing rule | {{alertzero}} turns the rule on. |
| Confirm rule coverage | Nothing runs. You confirm that an existing rule already covers the gap. |

When you decline, no rule changes, and {{alertzero}} discards any draft rule.

To manage rules by hand, refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md) and [](/solutions/security/detect-and-alert/install-prebuilt-rules.md).

## Related pages [alertzero-detection-change-related]

- [](decide-proposed-action.md): The steps every decision shares, and what each status means.
- [](watches-and-workers.md): What each {{az-worker}} needs, and its settings.
