---
description: "Turn an AlertZero Worker on or off, and set its autonomy and other settings."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Configure {{az-worker}} settings

When you turn on {{az-workers}} during setup, they start with their default settings. You can change these defaults on the **{{az-watches}}** page.

Each {{az-worker}} has its own settings, and the {{az-autonomy}} levels control different things for each {{az-worker}}. This page describes each {{az-worker}}'s settings, grouped by {{az-watch}}.

## Before you begin [configure-worker-settings-before-you-begin]

To change these settings, you need a privilege that lets you manage {{alertzero}}. Refer to [](alertzero-privileges.md).

## Change a Worker's settings [configure-worker-settings-change]

1. Find **{{az-watches}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the {{az-watch}} that contains the {{az-worker}}.
3. Change the settings for the {{az-worker}}.
4. Select **Save**.

## Turn a Worker on or off and view its runs [configure-worker-settings-enabled]

These two settings apply to every {{az-worker}}. The sections that follow cover the other settings of each {{az-worker}}.

**Enabled**
:   Turns the {{az-worker}} on or off.

**View executions**
:   Opens the {{az-worker}}'s execution history in the workflow editor, where you can check what it did and whether each run succeeded. Refer to [](view-execution-history.md).

## {{az-triage-watch}} [configure-worker-settings-triage-watch]

The {{az-triage-watch}} includes the {{az-alert-triage}} and {{az-attack-discovery}} {{az-workers}}. You configure each {{az-worker}} separately.

### {{az-alert-triage}} [configure-worker-settings-alert-triage]

{{az-alert-triage}} has the following settings.

**{{az-autonomy-cap}}**
:   Sets whether {{az-alert-triage}} needs your approval to close false positives.

    * **{{az-manual}}**: {{az-alert-triage}} classifies new alerts and proposes closing the false positives. You approve or decline each proposed closure.
    * **{{az-supervised}}**: {{az-alert-triage}} classifies new alerts and closes false positives on its own. You can reopen closed alerts that you disagree with.

**Schedule**
:   How often {{az-alert-triage}} checks for alerts that are waiting to be triaged.

:::{include} /solutions/security/alertzero/_snippets/worker-models-setting.md
:::

**Minimum confidence score**
:   How confident {{az-alert-triage}} must be that an alert is a false positive before it proposes closing the alert or closes it. A false positive below this score is classified as inconclusive and stays open. A higher score means fewer alerts are closed, so it's the safer choice if you want to review more alerts yourself. A lower score means more alerts are closed.

**Minimum severity**
:   The lowest alert severity to triage. Alerts below this severity are skipped. To triage every alert, select **Low**.

**Exclude building block alerts**
:   Skips the alerts that any rule configured as a [building block rule](/solutions/security/detect-and-alert/about-building-block-rules.md) generates.

**Excluded rule tags**
:   Skips alerts from rules that carry any of these tags. Press **Enter** after each tag to add more than one. Tags are case-sensitive.

### {{az-attack-discovery}} [configure-worker-settings-attack-discovery]

{{az-attack-discovery}} has the following settings.

**{{az-autonomy-cap}}**
:   Sets whether {{az-attack-discovery}} needs your approval to hand an attack to the {{az-forensics-watch}}.

    * **{{az-manual}}**: {{az-attack-discovery}} opens an {{az-investigation}} for each potential attack. For each attack it confirms or can't rule out, it proposes handing the attack to the {{az-forensics-watch}}. You approve or decline each handoff.
    * **{{az-supervised}}**: {{az-attack-discovery}} opens an {{az-investigation}} for each potential attack and hands the attacks it confirms or can't rule out to the {{az-forensics-watch}} on its own.

**Schedule**
:   How often {{az-attack-discovery}} looks for potential attacks.

:::{include} /solutions/security/alertzero/_snippets/worker-models-setting.md
:::

## {{az-hunt-watch}} [configure-worker-settings-hunt-watch]

The {{az-hunt-watch}} includes the {{az-continuous-threat-hunt}} {{az-worker}}.

### {{az-continuous-threat-hunt}} [configure-worker-settings-continuous-threat-hunt]

{{az-continuous-threat-hunt}} has the following settings.

**{{az-threat-intel-supply-cap}}**
:   The workflows that build the {{az-threat-reports}} that {{az-continuous-threat-hunt}} hunts: **Ingest threat feeds**, **Enrich threat report**, and **Attribute alerts to reports**. {{alertzero}} turns them on when you turn on {{az-continuous-threat-hunt}}, but only if your deployment meets the [requirements](threat-reports.md#alertzero-threat-reports-requirements). Otherwise, the settings show what's missing. To learn what each workflow does, refer to [](threat-reports.md#alertzero-threat-reports). To learn which ones all spaces share, refer to [](threat-reports.md#alertzero-threat-reports-spaces).

    If a workflow is off while {{az-continuous-threat-hunt}} is on, select **Restore threat intel supply** in the callout to turn it back on. You can also turn these workflows on or off from the **Workflows** page after you turn on [**Show managed workflows**](/explore-analyze/workflows/get-started/setup.md#workflows-managed-visibility). Refer to [Manage and organize workflows](/explore-analyze/workflows/authoring-techniques/manage-workflows.md).

**{{az-autonomy-cap}}**
:   {{az-continuous-threat-hunt}} always uses **{{az-manual}}** {{az-autonomy}}. It hunts each {{az-threat-report}}, opens an {{az-investigation}} for it, and proposes response actions for the threats it finds. You approve or decline each {{az-proposed-action}}.

**Schedule**
:   How often {{az-continuous-threat-hunt}} searches your data for activity that matches {{az-threat-reports}}. The interval is fixed, so you can't change it. It runs every 4 hours.

:::{include} /solutions/security/alertzero/_snippets/worker-models-setting.md
:::

## {{az-detection-watch}} [configure-worker-settings-detection-watch]

The {{az-detection-watch}} includes the {{az-rule-tuning}} and {{az-rule-coverage}} {{az-workers}}. You configure each {{az-worker}} separately.

### {{az-rule-tuning}} [configure-worker-settings-rule-tuning]

{{az-rule-tuning}} has the following settings.

**{{az-autonomy-cap}}**
:   Sets whether {{az-rule-tuning}} needs your approval before it analyzes a rule. Applying a tuning change always waits for your approval.

    * **{{az-manual}}**: {{az-rule-tuning}} finds each qualifying rule, but waits for your approval before it analyzes the rule. You also approve or decline each proposed tuning change.
    * **{{az-assisted}}**: {{az-rule-tuning}} analyzes each qualifying rule on its own and proposes a tuning change. You approve or decline each proposed change.

**Schedule**
:   How often {{az-rule-tuning}} looks for rules to analyze.

:::{include} /solutions/security/alertzero/_snippets/worker-models-setting.md
:::

**Analysis window (days)**
:   The period of alerts {{az-rule-tuning}} considers when it checks the qualifying thresholds and analyzes a rule. Alerts older than this period don't count toward either threshold.

**Qualifying thresholds**
:   When a rule qualifies for analysis. A rule qualifies only when both thresholds are met within the analysis window. Both count alerts closed as false positives.

    * **False positive count**: The number of false positive alerts.
    * **False positive rate**: The percentage of alerts that are false positives.

### {{az-rule-coverage}} [configure-worker-settings-rule-coverage]

{{az-rule-coverage}} has the following settings.

**{{az-autonomy-cap}}**
:   Sets whether {{az-rule-coverage}} needs your approval before it checks a detection gap. The proposed next step always waits for your approval.

    * **{{az-manual}}**: {{az-rule-coverage}} reviews the detection gaps that the {{az-hunt-watch}} finds, but waits for your approval before it checks a gap. You also approve or decline each proposed next step.
    * **{{az-assisted}}**: {{az-rule-coverage}} checks each gap on its own and proposes a next step, such as drafting a new rule or installing a prebuilt rule. You approve or decline each proposed next step.

**Schedule**
:   How often {{az-rule-coverage}} picks up new detection gaps to review.

:::{include} /solutions/security/alertzero/_snippets/worker-models-setting.md
:::

**Lookback (days)**
:   How many days back each run looks for coverage gaps that haven't been reviewed. Older gaps are not reviewed.

**Max gaps per run**
:   The maximum number of detection gaps {{az-rule-coverage}} reviews in a single run.

## {{az-forensics-watch}} [configure-worker-settings-forensics-watch]

The {{az-forensics-watch}} includes the {{az-endpoint-analysis}} {{az-worker}}.

### {{az-endpoint-analysis}} [configure-worker-settings-endpoint-analysis]

{{az-endpoint-analysis}} has the following settings.

**{{az-autonomy-cap}}**
:   Sets whether response actions need your approval.

    * **{{az-manual}}**: {{az-endpoint-analysis}} adds an attack timeline, indicators of compromise, and its rationale to the {{az-investigation}}, and proposes response actions, such as isolating a host, terminating a process, or suspending a process. You approve or decline each proposed response action.
    * **{{az-supervised}}**: {{az-endpoint-analysis}} adds the same details to the {{az-investigation}} and runs those response actions on its own. You review the results afterward.

    ::::{warning}
    With **{{az-supervised}}** {{az-autonomy}}, {{az-endpoint-analysis}} isolates hosts, terminates processes, or suspends processes without waiting for your approval. Isolating a host blocks its communication with other hosts on your network, and killing or suspending a process interrupts whatever that process is doing. Use **{{az-supervised}}** only if you're confident in your response procedures.
    ::::

<!-- Keeps the Models snippet below from merging into the Autonomy list. -->

:::{include} /solutions/security/alertzero/_snippets/worker-models-setting.md
:::

## Related pages [configure-worker-settings-related]

* [](run-worker-on-demand.md)
* [](view-execution-history.md)
* [](watches-and-workers.md)
* [](alertzero-privileges.md)
