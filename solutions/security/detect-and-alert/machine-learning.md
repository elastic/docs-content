---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create detection rules that trigger on machine learning anomaly detection job results.
---

# {{ml-cap}} rules [ml-rule-type]

## Overview

{{ml-cap}} rules generate alerts when a {{ml}} {{anomaly-job}} discovers an anomaly that exceeds a defined score threshold. Unlike other rule types, {{ml}} rules do not require you to write a query. Instead, they rely on {{ml}} jobs that continuously model normal behavior and flag deviations.

### When to use a {{ml}} rule

{{ml-cap}} rules are the right fit when:

* You want to detect **behavioral anomalies** that are difficult to express as static queries, such as unusual login times, atypical data transfer volumes, or rare process executions for a given user or host.
* A {{ml}} job is already active (or you plan to enable one) that models the relevant behavior.
* You want **adaptive detection** that automatically adjusts to changing baselines without manual threshold tuning.

{{ml}} rules are **not** the best fit when:

* You can define the exact pattern you're looking for. Use a [custom query rule](/solutions/security/detect-and-alert/custom-query.md) or [EQL rule](/solutions/security/detect-and-alert/eql.md) instead.
* You need a count-based threshold. Use a [threshold rule](/solutions/security/detect-and-alert/threshold.md) instead.
* You need to compare events against threat intelligence. Use an [indicator match rule](/solutions/security/detect-and-alert/indicator-match.md) instead.

## Requirements

{{ml-cap}} rules require the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md), and you must have the [`machine_learning_admin`](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-ml-admin) role in {{stack}} or the appropriate [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md) in {{serverless-short}}. You also need at least one {{ml}} {{anomaly-job}} active or configured to start.

For an overview of using {{ml}} with {{elastic-sec}}, refer to [{{anomaly-detect-cap}}](/solutions/security/advanced-entity-analytics/anomaly-detection.md).

## Manage {{ml}} jobs for detection rules

{{ml-cap}} rules depend on their associated {{ml}} jobs running continuously. If a job stops, the rule cannot evaluate anomaly results and won't generate alerts. You can manage job status in two ways: from the {{ml}} jobs setting UI or the rule's details page.

### ML job settings interface

{{ml-cap}} jobs created for {{elastic-sec}} detection rules are managed separately from jobs you create in the {{ml-app}} app:

1. Find **Detection rules (SIEM)** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the settings menu in the upper-right corner of the page, then select **ML job settings**.

From there you can view, start, and stop all {{ml}} jobs associated with your detection rules.

::::{note}
{{ml-cap}} jobs created through {{elastic-sec}} detection rules do not appear in the standard {{ml-app}} job management UI. Use the {{rules-ui}} page settings menu to manage them.
::::

### Rule's details page

You can also check and control job status for a specific rule:

1. Find **Detection rules (SIEM)** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and select the rule name in the Rules table.
2. In the **Definition** section of the rule's details page, check whether the required {{ml}} jobs are running.
3. Use the toggles to start or stop each job.

If a required {{ml}} job isn't running, an error indicator appears in the **Last response** column of the Rules table. Select the indicator to see which jobs are affected.

<!-- CRAFT LAYER - COMMENTED OUT FOR REVIEW
## Configuring effective {{ml}} rules [craft-ml]

### Selecting {{ml}} jobs

Select one or more {{ml}} jobs that model the behavior you want to detect. {{elastic-sec}} ships with prebuilt jobs covering common use cases:

* **Unusual login activity.** Detects logins at unusual times or from unusual locations.
* **Rare process execution.** Surfaces processes that rarely execute on a given host.
* **DNS tunneling.** Identifies unusually high DNS query volumes or rare query patterns.

If a selected job is not currently active, it starts automatically when you enable the rule.

### Setting the anomaly score threshold

The anomaly score ranges from 0 to 100, where higher scores indicate stronger deviations from normal behavior. Guidelines for setting the threshold:

| Threshold range | Effect |
|---|---|
| 25-50 | Casts a wide net. Generates more alerts, including moderate anomalies. Suitable for initial exploration of a new job. |
| 50-75 | Balanced. Surfaces significant anomalies while filtering out low-confidence results. A good starting point for most rules. |
| 75-100 | High confidence only. Generates fewer alerts but each one represents a strong deviation. Best for mature jobs with well-understood baselines. |

### Tuning and noise reduction

{{ml}} rules can be noisy when a job is newly deployed or the underlying data shifts. Use these techniques to reduce false positives:

* **Raise the anomaly score threshold** if the job is generating too many low-confidence alerts.
* **Add [rule exceptions](/solutions/security/detect-and-alert/rule-exceptions.md)** to suppress alerts from known-benign anomalies, such as scheduled maintenance windows or expected batch processes.
* **Allow the job time to learn.** Most jobs need at least two weeks of data before their baselines stabilize. Anomalies flagged during the initial learning period are less reliable.

### Understanding {{ml}} alerts

{{ml}} alerts differ from other alert types:

* Alerts are generated from **anomaly results**, not raw source events. The alert contains anomaly metadata (score, job ID, influencers, bucket time) rather than the original event fields.
* When configuring **alert suppression**, only anomaly fields are available because source event fields are not present in the anomaly results.
* **Severity and risk score overrides** based on source event fields are not applicable. Consider mapping the anomaly score to severity using severity override on anomaly-specific fields.

::::{tip}
**See it in practice.** These prebuilt rules use {{ml}} detection:

* **Anomalous Process For a Linux Population.** Uses a rare-process {{ml}} job to surface processes that are unusual across a fleet of Linux hosts.
* **Unusual Login Activity.** Triggers when a user logs in at unusual times or from unusual source IPs, based on a login-activity {{ml}} job.
* **Spike in Network Traffic To a Country.** Detects sudden increases in outbound network traffic to a specific country, useful for identifying data exfiltration.
::::
END CRAFT LAYER -->

## {{ml-cap}} field reference [ml-fields]

The following settings are specific to {{ml}} rules. For settings shared across all rule types, refer to [Rule settings reference](/solutions/security/detect-and-alert/common-rule-settings.md).

**{{ml-cap}} jobs**
:   The {{anomaly-jobs}} whose results the rule evaluates. Select one or more jobs. If a selected job is not active, it starts automatically when the rule is enabled.

**Anomaly score threshold**
:   The minimum anomaly score (0-100) above which the rule generates alerts. Only anomalies that meet or exceed this score trigger alerts.

**Suppress alerts by** (optional)
:   Reduce repeated or duplicate alerts by grouping them on one or more fields. Only anomaly fields are available for suppression because {{ml}} alerts do not contain source event fields. For details, refer to [Alert suppression](/solutions/security/detect-and-alert/alert-suppression.md).

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/prebuilt-rules.md#rule-prerequisites).
