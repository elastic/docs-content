---
description: "Find what the AlertZero Alert Triage Worker does in Elastic Security, and the settings that control which alerts it triages and closes."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-alert-triage}} {{az-worker}}

The {{az-alert-triage}} {{az-worker}} classifies detection alerts as true or false positives, so false positives stop reaching your analysts and the [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md). It's part of the [{{az-triage-watch}}](triage-watch.md).

It analyzes open and acknowledged alerts in batches and tags each one as a true positive, false positive, or inconclusive, with a note explaining why. It proposes closing the alerts it's confident are false positives. Alerts with the same pattern share one {{az-investigation}} and one {{az-proposed-action}}.

By default, it runs every 15 minutes. It offers {{az-manual}} and {{az-supervised}} {{az-autonomy}}. Refer to [what it does at each level](../watches-and-workers.md#alertzero-worker-autonomy-levels).

## Settings [alertzero-alert-triage-settings]

Besides the [settings every {{az-worker}} has](../watches-and-workers.md#alertzero-shared-worker-settings), {{az-alert-triage}} has these settings:

**Minimum confidence score**
:   How confident it must be that an alert is a false positive before it proposes closing the alert. If its confidence is lower, it tags the alert inconclusive.

    Default: 85%. Range: 0–100%, in whole numbers.

**Minimum severity**
:   The lowest alert severity it triages: **Low**, **Medium**, **High**, or **Critical**.

    Default: **Low**, which triages every alert.

**Exclude building-block alerts**
:   Skips alerts from building block rules.

    Default: off.

**Excluded rule tags**
:   Skips alerts from rules with any of these tags. Tags must match exactly, including case.

    Default: none. You can add up to 50 tags.

## Work with this {{az-worker}} [alertzero-alert-triage-tasks]

- **Before you turn it on:** Check [what it needs](../requirements.md).
- **Decide its work:** Its {{az-proposed-actions}} appear in the **Investigate** section of the **{{az-proposed-actions-cap}}** page. Refer to [](../decide-proposed-action.md).
- **Change its settings:** Refer to [](../configure-worker-settings.md).
