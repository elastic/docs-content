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

The {{az-detection-watch}} proposes two kinds of detection rule changes. The {{az-rule-tuning}} {{az-worker}} proposes changes that cut false positives from noisy rules. The {{az-rule-coverage}} {{az-worker}} proposes rules that cover the detection gaps that the {{az-hunt-watch}} finds.

Rule changes always wait for your approval, because the {{az-rule-tuning}} and {{az-rule-coverage}} {{az-workers}} offer only {{az-manual}} and {{az-assisted}} {{az-autonomy}}. Approving a change doesn't give you the privileges to make it. Refer to [](alertzero-privileges.md).

To learn what starts each kind of change, refer to [](watches-and-workers.md).

% After the Watches and Workers reference (elastic/docs-content-internal#1814) merges, link to its Detection Watch section instead of the whole page.

## How the {{az-detection-watch}} proposes a change [alertzero-detection-change-how]

By default, each {{az-worker}} asks before it starts work on a change:

- **The {{az-rule-tuning}} {{az-worker}}:** Asks whether to analyze a noisy rule, with the {{az-proposed-action}} **Review rule for tuning**.
- **The {{az-rule-coverage}} {{az-worker}}:** Asks whether to work on a gap, with the {{az-proposed-action}} **Review detection gap**.

After you approve, the {{az-worker}} drafts the change and proposes it for your review. If you decline **Review rule for tuning**, the {{az-rule-tuning}} {{az-worker}} doesn't review those false positives again, but new ones can start a new review. If you decline **Review detection gap**, the {{az-rule-coverage}} {{az-worker}} leaves that gap out of future coverage checks.

% The proposal text inside the UI tells people to "dismiss," but the button says Decline. The flyout also has a separate Dismiss button that acts on the whole investigation. The docs say Decline to match the button, but users might find the mix confusing.

## Review a tuning change for a noisy rule [alertzero-detection-change-tuning]

The {{az-rule-tuning}} {{az-worker}} proposes one change for each noisy rule.

1. In the **Configure** section of the **{{az-proposed-actions-cap}}** page, select the rule's card. Its name starts with **Rule tuning:**.
2. In the flyout's **{{az-proposed-actions-cap}}** section, select the change.
3. Check that the change drops the false positives without hiding real threats:
    - **Why this rule was picked:** How many of the rule's recent alerts were judged false positives, either closed by analysts or classified by the {{az-alert-triage}} {{az-worker}}.
    - **Proposed change:** Compare the rule before and after the change. Make sure an exception or query change is no broader than the noise it targets.
    - **Backtest:** If the change includes one, compare **Alerts with the current rule** with **Alerts with the proposed change** to see how the change affects alerts on your past data.
4. If someone edited the rule after the {{az-rule-tuning}} {{az-worker}} proposed the change, decline the change. Approving a change to an edited rule fails.
5. Select **Approve** or **Decline**.
    - **If you approve:** {{alertzero}} changes the rule in place or adds the exception.
    - **If you decline:** The rule stays as it is, and the {{az-investigation}} closes.

To tune a rule by hand instead, refer to [](/solutions/security/detect-and-alert/tune-detection-rules.md).

## Review a rule for a detection gap [alertzero-detection-change-coverage]

The {{az-rule-coverage}} {{az-worker}} proposes a rule for each gap that the {{az-hunt-watch}} finds.

1. In the **Configure** section of the **{{az-proposed-actions-cap}}** page, select the gap's card. Its name starts with **Detection coverage:**.
2. In the flyout's **{{az-proposed-actions-cap}}** section, select the proposed rule.
3. For a new rule, check the **Proposed rule** query and the **Backtest**, which shows how often the rule matches your past data. A rule that matches often in the backtest is likely to be noisy once it's on.
4. Select **Approve** or **Decline**.
    - **If you approve:** What happens depends on the kind of {{az-proposed-action}}:
        - **Create detection rule:** {{alertzero}} creates the {{esql}} rule and turns it on under your account. The rule starts running at its next scheduled interval.
        - **Install prebuilt detection rule:** {{alertzero}} installs the prebuilt rule and turns it on.
        - **Enable detection rule:** {{alertzero}} turns on the existing rule. The rule starts creating alerts at its next scheduled run.
        - **Confirm rule coverage:** Your approval records that a rule that's already on covers the gap. Your rules stay as they are. The check doesn't look at rule exceptions, so make sure that no exception narrows the rule's coverage before you approve.
        - **Coverage check needs follow-up:** The {{az-rule-coverage}} {{az-worker}} has no change to propose, for example because it can't find the rule it checked. Nothing runs when you approve. Follow up by hand.
    - **If you decline:** Your rules stay as they are, and {{alertzero}} discards any draft rule.

To manage rules by hand, refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md) and [](/solutions/security/detect-and-alert/install-prebuilt-rules.md).

## Undo a rule change [alertzero-detection-change-undo]

To see or undo an approved change later, refer to [](/solutions/security/detect-and-alert/view-rule-changes-history.md).

## Related pages [alertzero-detection-change-related]

- [](act-on-hunt-finding.md): Find out how hunts pass detection gaps to the {{az-rule-coverage}} {{az-worker}}.
- [](use-alertzero.md): Find other work that {{az-workers}} bring you.
