---
description: "Find what the AlertZero Alert Triage Worker does, what it needs, its settings, and where its work appears in Elastic Security."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-alert-triage}} {{az-worker}}

The {{az-alert-triage}} {{az-worker}} belongs to the [{{az-triage-watch}}](triage-watch.md). It classifies detection alerts as true or false positives, so false positives stop reaching your analysts and the [{{az-attack-discovery}} {{az-worker}}](attack-discovery-worker.md).

It analyzes open and acknowledged alerts in batches and tags each one as a true positive, false positive, or inconclusive, with a note explaining why. It proposes closing the alerts it's confident are false positives. Alerts with the same pattern share one {{az-investigation}} and one {{az-proposed-action}}.

## Requirements [alertzero-alert-triage-requirements]

The {{az-alert-triage}} {{az-worker}} needs detection alerts, and it needs the [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) turned on in the space. The workflow is off by default.

## Settings [alertzero-alert-triage-settings]

Find these settings on the {{az-triage-watch}} page. To change them, refer to [](../configure-worker-settings.md).

**{{az-autonomy-cap}}**
:   How much it does without waiting for you. Default: {{az-manual}}.

    * **{{az-manual}}**: Every closure waits for your approval.
    * **{{az-supervised}}**: It closes false positives itself, and you can reopen any you disagree with.

**Trigger**
:   How often it runs, in minutes, hours, or days.

    Default: every 15 minutes.

**Models**
:   A link to **Feature Settings**, where you select the models that {{alertzero}} uses in the space.

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

## Where its work appears [alertzero-alert-triage-work]

Its {{az-proposed-actions}} appear in the **Investigate** section of the **{{az-proposed-actions-cap}}** page, each proposing to close alerts as false positives. If you decline, {{az-alert-triage}} tags the alerts inconclusive. Refer to [](../decide-proposed-action.md).
