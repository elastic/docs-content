---
description: "Review the detection rule changes that AlertZero proposes in Elastic Security: tuning changes for noisy rules from Rule Tuning, and new, installed, or turned-on rules for detection gaps from Rule Coverage."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Tune noisy rules and fill detection gaps [alertzero-decide-detection-change]

The {{az-detection-watch}} proposes two kinds of changes to your detection rules. The {{az-rule-tuning}} {{az-worker}} proposes tuning changes that cut noise from rules with too many false positives. The {{az-rule-coverage}} {{az-worker}} proposes rules that cover the detection gaps that the {{az-hunt-watch}} finds. No rule changes until you approve, so you can check that each change does what it says without hiding real threats.

% After elastic/docs-content#9118 merges, link to watches/detection-watch.md for what starts each kind of change.

## Tune a noisy rule [alertzero-detection-change-tuning]

The {{az-rule-tuning}} {{az-worker}} proposes one change for each noisy rule. By default, it first asks whether to analyze the rule, with a {{az-proposed-action}} named **Review rule for tuning**. Approve that one to get the tuning change.

1. In the **Configure** section of the **{{az-proposed-actions-cap}}** page, select the rule's card. Its name starts with **Rule tuning:**.
2. In the flyout's **{{az-proposed-actions-cap}}** section, select the change.
3. Check that the change drops the false positives without hiding real threats:
    - **Why this rule was picked** explains why the rule qualified for tuning.
    - **Proposed change** shows the rule before and after the change. Make sure an exception or query change is no broader than the noise it targets.
    - **Backtest**, when the change includes one, compares **Alerts with the current rule** with **Alerts with the proposed change**.

    If someone edited the rule after the {{az-rule-tuning}} {{az-worker}} proposed the change, decline the change. Approving a change to an edited rule fails.
4. Select **Approve** or **Decline**.
    - **If you approve:** {{alertzero}} changes the rule in place or adds the exception.
    - **If you decline:** The rule doesn't change, and the {{az-investigation}} closes.

To see or undo an approved change later, refer to [](/solutions/security/detect-and-alert/view-rule-changes-history.md). To tune a rule by hand instead, refer to [](/solutions/security/detect-and-alert/tune-detection-rules.md).

## Fill a detection gap [alertzero-detection-change-coverage]

The {{az-rule-coverage}} {{az-worker}} proposes a rule for each gap that the {{az-hunt-watch}} finds. By default, it first asks whether to work on the gap, with a {{az-proposed-action}} named **Review detection gap**. Approve that one to get the proposed rule.

1. In the **Configure** section of the **{{az-proposed-actions-cap}}** page, select the gap's card. Its name starts with **Detection coverage:**.
2. In the flyout's **{{az-proposed-actions-cap}}** section, select the proposed rule.
3. For a new rule, check the **Proposed rule** query and the **Backtest**, which shows how often the rule matches your past data. A rule that matches often in the backtest is likely to be noisy once it's on.
4. Select **Approve** or **Decline**.
    - **If you approve:** What happens depends on the kind of {{az-proposed-action}}:
        - **Create a new {{esql}} rule:** {{alertzero}} creates the rule, turned off. Review it, then turn it on.
        - **Install a prebuilt rule:** {{alertzero}} installs the rule and turns it on.
        - **Turn on an existing rule:** {{alertzero}} turns the rule on.
        - **Confirm rule coverage:** Nothing runs. You confirm that an existing rule already covers the gap.
    - **If you decline:** No rule changes, and {{alertzero}} discards any draft rule.

To manage rules by hand, refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md) and [](/solutions/security/detect-and-alert/install-prebuilt-rules.md).

## Related pages [alertzero-detection-change-related]

- [](use-alertzero.md): Find other work that {{az-workers}} bring you.
