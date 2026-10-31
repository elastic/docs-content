---
description: "Find what each AlertZero Worker in Elastic Security does, what starts it, what it needs, its settings, and where its work appears."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-watches}} and {{az-workers}} [alertzero-watches-and-workers]

Each {{az-watch}} groups the {{az-workers}} for one area of work. Use this page to look up what each {{az-worker}} does, what starts it, what it needs, its settings, and where its work appears.

On its {{az-watch}} page, every {{az-worker}} has three settings: The {{az-autonomy}} level, the **Trigger** that sets how often it runs, and the **Models** it uses from **Feature Settings**. Some {{az-workers}} have more settings, which their entries list. To change settings, refer to [](configure-worker-settings.md).

## {{az-triage-watch}} [alertzero-triage-watch]

The {{az-triage-watch}} reviews incoming alerts so your analysts see only the ones that need their attention. Its {{az-alert-triage}} {{az-worker}} classifies alerts, and its {{az-attack-discovery}} {{az-worker}} groups related alerts into attacks.

### {{az-alert-triage}} [alertzero-worker-alert-triage]

The {{az-alert-triage}} {{az-worker}} classifies detection alerts as true or false positives, so false positives stop reaching your analysts and the {{az-attack-discovery}} {{az-worker}}.

- **What it does:** It analyzes open and acknowledged alerts in batches and tags each one as a true positive, false positive, or inconclusive, with a note explaining why. It proposes closing the alerts it's confident are false positives. Alerts with the same pattern share one {{az-investigation}} and one {{az-proposed-action}}.
- **What starts it:** A schedule, every 15 minutes by default.
- **What it needs:** Detection alerts, and Alert Analysis turned on in the space. Refer to [](/solutions/security/detect-and-alert/turn-on-detections.md).
- **Settings:**
  - **Minimum confidence score:** How confident it must be that an alert is a false positive before it proposes closing the alert. If its confidence is lower, it tags the alert inconclusive. Default 85%.
  - **Minimum severity:** The lowest alert severity it triages. Default **Low**, which triages every alert.
  - **Exclude building-block alerts:** Skips alerts from building block rules. Default off.
  - **Excluded rule tags:** Skips alerts from rules with any of these tags. Tags must match exactly, including case. Up to 50 tags.
- **{{az-autonomy-cap}}:** {{az-manual}} or {{az-supervised}}. At {{az-manual}}, every closure waits for your approval. At {{az-supervised}}, it closes false positives itself, and you can reopen any you disagree with.
- **Where its work appears:** The **Investigate** section of the **{{az-proposed-actions-cap}}** page, as a {{az-proposed-action}} to close the alerts as false positives. If you decline, {{az-alert-triage}} tags the alerts inconclusive. Refer to [](decide-proposed-action.md).

### {{az-attack-discovery}} [alertzero-worker-attack-discovery]

The {{az-attack-discovery}} {{az-worker}} groups related alerts into candidate attacks, then checks each one before it reaches you. It runs the [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) feature of {{elastic-sec}} on a schedule.

- **What it does:** It opens one {{az-investigation}} for each candidate attack, or adds the attack to an open {{az-investigation}} for the same attack, then judges whether the attack is a false positive. For a false positive, it acknowledges the open alerts and closes the {{az-investigation}}. For an attack it confirms or can't rule out, it proposes handing the attack to the {{az-forensics-watch}} for forensics.
- **What starts it:** A schedule, every 24 hours by default. Each run picks up where the last one ended. You can't run it on demand.
- **What it needs:** Detection alerts. To hand attacks off, {{context-engine}} must be on in the space (the `contextEngine:enabled` advanced setting). To get those attacks analyzed, turn on the {{az-endpoint-analysis}} {{az-worker}} too. Refer to [{{az-worker}} dependencies](requirements.md).
- **Settings:** None beyond the three that every {{az-worker}} has.
- **{{az-autonomy-cap}}:** {{az-manual}} or {{az-supervised}}. At {{az-manual}}, every handoff to the {{az-forensics-watch}} waits for your approval. At {{az-supervised}}, it hands attacks off without waiting for you.
- **Where its work appears:** The **Investigate** section of the **{{az-proposed-actions-cap}}** page. Refer to [](respond-to-attack.md).
- **Limits:** Each run retrieves up to 10,000 alerts for every 24 hours it covers.

## {{az-detection-watch}} [alertzero-detection-watch]

The {{az-detection-watch}} improves your detection rules at the source, instead of handling the alerts they produce one by one. Every change it proposes waits for your approval, because neither of its {{az-workers}} offers {{az-supervised}} {{az-autonomy}}.

### {{az-rule-tuning}} [alertzero-worker-rule-tuning]

The {{az-rule-tuning}} {{az-worker}} finds rules that produce too many false positives and proposes one change per rule to reduce them.

- **What it does:** It checks how many false positives each enabled rule produced in its analysis window. For each rule that meets both false positive thresholds, it opens an {{az-investigation}}, diagnoses the cause, and proposes one change to the rule's exceptions, query, risk score, threshold, or schedule. Most changes come with a backtest that compares the alerts the rule produced with the alerts it would have produced after the change.
- **What starts it:** A schedule, every 2 hours by default.
- **What it needs:** Alerts closed as false positives, by people or by the {{az-alert-triage}} {{az-worker}}.
- **Settings:**
  - **Analysis window (days):** How many days of alerts it checks. From 1 to 30, default 7.
  - **False positive count:** How many false positives a rule needs in the window. From 2 to 100, default 10.
  - **False positive rate:** What share of a rule's alerts must be false positives. From 0 to 100%, default 50%.
- **{{az-autonomy-cap}}:** {{az-manual}} or {{az-assisted}}. At {{az-manual}}, you approve each rule before it analyzes the rule. At {{az-assisted}}, it analyzes every rule that qualifies without asking. Either way, every change waits for your approval.
- **Where its work appears:** The **Configure** section of the **{{az-proposed-actions-cap}}** page, in an {{az-investigation}} named **Rule tuning: _rule name_**. Refer to [](decide-detection-change.md).
- **Limits:** Each run reviews up to 10 rules and uses each rule's newest 100 false positives. It doesn't backtest changes to saved query or {{ml}} rules, or exceptions on {{esql}} rules.

### {{az-rule-coverage}} [alertzero-worker-rule-coverage]

The {{az-rule-coverage}} {{az-worker}} proposes rules to close the detection gaps that the {{az-hunt-watch}} finds.

- **What it does:** It opens one {{az-investigation}} for each gap and checks whether a rule already covers it. Depending on what it finds, it proposes turning on an existing rule, installing a prebuilt rule, or creating a new {{esql}} rule with a backtest of how often the rule would have matched. If a rule already covers the gap, it asks you to confirm that instead.
- **What starts it:** A schedule, every hour by default.
- **What it needs:** The {{az-continuous-threat-hunt}} {{az-worker}}, which is the only source of the gaps it works on. Refer to [{{az-worker}} dependencies](requirements.md).
- **Settings:**
  - **Lookback (days):** How far back it looks for gaps. From 8 to 90, default 14.
  - **Max gaps per run:** The most gaps it works on in one run. From 1 to 50, default 5.
- **{{az-autonomy-cap}}:** {{az-manual}} or {{az-assisted}}. At {{az-manual}}, you approve each gap before it drafts a rule. At {{az-assisted}}, it drafts a rule for every gap without asking. Either way, every rule waits for your approval.
- **Where its work appears:** The **Configure** section of the **{{az-proposed-actions-cap}}** page, in an {{az-investigation}} named **Detection coverage: _gap_**. Refer to [](decide-detection-change.md).
- **Limits:** Up to 100 gaps can be under review in a space at once.

## Hunt Watch [alertzero-hunt-watch]


## Forensics Watch [alertzero-forensics-watch]
