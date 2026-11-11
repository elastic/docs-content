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

Both {{az-workers}} offer only {{az-manual}} and {{az-assisted}} {{az-autonomy}}, so every rule change waits for your approval. Approving a change doesn't give you the [privileges to make it](alertzero-privileges.md).

## How the {{az-detection-watch}} proposes a change [alertzero-detection-change-how]

These are the default schedules and thresholds:

- **{{az-rule-tuning}} {{az-worker}}:** Runs every 2 hours. It picks a rule when, over the last 7 days, at least 10 of the rule's alerts that it hasn't reviewed yet are false positives, and at least half of the rule's alerts are false positives.
- **{{az-rule-coverage}} {{az-worker}}:** Runs every hour, and reviews up to 5 detection gaps from the last 14 days in each run.

To change these defaults, refer to [{{az-detection-watch}} settings](configure-worker-settings.md#configure-worker-settings-detection-watch). For more about what each {{az-worker}} checks, refer to [](watches-and-workers.md#alertzero-detection-watch).

With **{{az-manual}}** {{az-autonomy}} (the default), each {{az-worker}} asks before it starts work on a change:

- **{{az-rule-tuning}} {{az-worker}}:** Proposes **Review rule for tuning** for a noisy rule. If you decline, the {{az-worker}} doesn't review those false positives again, but new ones can start a new review.
- **{{az-rule-coverage}} {{az-worker}}:** Proposes **Review detection gap** for a gap. If you decline, the {{az-worker}} leaves that gap out of future coverage checks.

When you approve either one, the {{az-worker}} drafts the change and proposes it for your review. With **{{az-assisted}}** {{az-autonomy}}, the {{az-workers}} skip this question and draft each change on their own.

If a {{az-proposed-action}} [expires](work-in-alertzero.md) before anyone decides, your rules stay as they are, and the {{az-worker}} can ask again on a later run.

## Review a tuning change for a noisy rule [alertzero-detection-change-tuning]

Open the tuning change on the **{{az-proposed-actions-cap}}** page, and check that it drops the false positives without hiding real threats. Start with why the {{az-rule-tuning}} {{az-worker}} picked the rule, based on how many of its recent alerts analysts or the {{az-alert-triage}} {{az-worker}} judged false positives. Then compare the rule before and after the change, and make sure an exception or query change is no broader than the noise it targets. If the change includes a backtest, check that it cuts only noise from the alerts on your past data.

If someone edited the rule after the {{az-worker}} proposed the change, decline the change, because approving it fails. Otherwise, approve or decline the change:

- **If you approve:** {{alertzero}} changes the rule in place or adds the exception.
- **If you decline:** The rule stays as it is, and the {{az-investigation}} closes.

To tune a rule by hand instead, refer to [](/solutions/security/detect-and-alert/tune-detection-rules.md).

## Decide how to fill a detection gap [alertzero-detection-change-coverage]

Open the {{az-proposed-action}} for the gap on the **{{az-proposed-actions-cap}}** page. What the {{az-rule-coverage}} {{az-worker}} proposes, and what happens when you approve it, depends on what the {{az-worker}} finds:

- **A new rule:** Check the rule's query and its backtest, which shows how often the rule matches your past data. A rule that matches often in the backtest is likely to be noisy once it's on. If you approve, {{alertzero}} creates the {{esql}} rule and turns it on under your account. The rule starts running at its next scheduled interval.
- **A prebuilt rule:** If you approve, {{alertzero}} installs the prebuilt rule and turns it on.
- **An existing rule that's turned off:** If you approve, {{alertzero}} turns on the rule. The rule starts creating alerts at its next scheduled run.
- **Existing coverage:** A rule that's already on covers the gap. The check doesn't look at rule exceptions, so make sure that no exception narrows the rule's coverage before you approve. Approving records the coverage and leaves your rules as they are.
- **A gap that needs follow-up:** The {{az-worker}} has no change to propose, for example because it can't find the rule it checked. Follow up by hand. Approving doesn't run anything.

If you decline, your rules stay as they are, and {{alertzero}} discards any draft rule.

To manage rules by hand, refer to [](/solutions/security/detect-and-alert/manage-detection-rules.md) and [](/solutions/security/detect-and-alert/install-prebuilt-rules.md).

## Undo a rule change [alertzero-detection-change-undo]

To see or undo an approved change later, refer to [](/solutions/security/detect-and-alert/view-rule-changes-history.md).

## Next steps [alertzero-detection-change-next-steps]

- [Find out how hunts pass detection gaps](act-on-hunt-finding.md#alertzero-hunt-finding-outcomes) to the {{az-rule-coverage}} {{az-worker}}.
- [Find other work that {{az-workers}} bring you](work-in-alertzero.md).
