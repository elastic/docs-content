---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/tuning-detection-signals.html
  - https://www.elastic.co/guide/en/serverless/current/security-tune-detection-signals.html
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Narrow a noisy detection rule's query, threshold, or other logic so it matches only suspicious activity, then test the change and keep track of it.
---

# Tune detection rules [security-tune-detection-signals]

When a detection rule creates alerts for activity that's normal in any environment, change the rule's logic so it matches only the behavior it's meant to detect. Tuning fixes noise at its source. Analysts get fewer false positives, and the rule keeps catching the activity that matters.

% Legacy anchors. Exception guidance moved to rule-exceptions.md, and indicator match guidance moved to indicator-match.md.

$$$filter-rule-process$$$
$$$tune-authorized-processes$$$
$$$tune-windows-rules$$$
$$$security-tune-detection-signals-noise-from-common-cloud-based-network-traffic$$$

Tuning changes what the rule detects across all the data it searches, so it doesn't fit every noisy rule. If the rule is correct but fires on activity that's safe only in your environment, such as a known admin tool, scanner, or service account, add an [exception](/solutions/security/detect-and-alert/rule-exceptions.md) instead. To compare tuning with exceptions, alert suppression, and snoozing, refer to [Reduce noise and false positives](/solutions/security/detect-and-alert/reduce-noise-and-false-positives.md).

## Before you begin [tune-rules-before-you-begin]

* To edit rules, you need the privileges described in [Manage rules](/solutions/security/detect-and-alert/detections-privileges.md#detections-privileges-manage-rules).
* You can edit Elastic prebuilt rules directly with an Enterprise subscription on {{stack}} or a Security Analytics Complete project on {{serverless-short}}. With other subscriptions, duplicate the prebuilt rule and tune the copy. A duplicate doesn't receive Elastic updates. Refer to [Customize Elastic prebuilt rules](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#customize-subscription-capabilities).

## Find out why the rule is noisy [find-noisy-rules]

Before you change a rule, find out what its false positives have in common. That tells you whether to tune the rule and which part of it to change.

1. Find the rules that create the most alerts. On the **Alerts** page, select **Group alerts by** → **Rule name**. To count alerts by rule over a longer period, [query the alerts index](/solutions/security/detect-and-alert/query-alert-indices.md#example_queries).
2. Open several alerts from a noisy rule and compare their details. Look for values the false positives share, such as the same parent process, command line, file path, or destination.
3. On the rule's details page, read the rule's **False positive examples** and investigation guide. For Elastic prebuilt rules, they describe activity that's known to trigger the rule.
4. Decide whether to tune the rule. If the false positives come from activity that's normal in any environment, tune the rule. If they come from hosts, users, or tools that are specific to your environment, add an [exception](/solutions/security/detect-and-alert/add-manage-exceptions.md) instead.

## Change the rule's logic [change-rule-logic]

$$$tune-indicator-rules$$$

What to change depends on the rule type and on what the false positives have in common.

1. Open the rule's details page, then select **Edit rule settings**.
2. Make the change that matches the cause of the false positives.

    | What the false positives have in common | What to change | Learn more |
    |---|---|---|
    | They match the query, but they aren't the behavior the rule is meant to detect | Add conditions to the query that describe the behavior more precisely | [Example of narrowing a query](#tune-example-narrow-query) |
    | A threshold rule fires on normal bursts of activity | Raise the **Threshold** value, or use **Count** to require a minimum number of unique values in another field | [Threshold rule field reference](/solutions/security/detect-and-alert/threshold.md#threshold-fields) |
    | A new terms rule fires on values that are new but expected | Increase the **History Window Size**, so the rule checks a longer period for earlier occurrences of each value | [New terms rule field reference](/solutions/security/detect-and-alert/new-terms.md#new-terms-fields) |
    | A {{ml}} rule fires on weak anomalies | Raise the **Anomaly score threshold** | [{{ml-cap}} rule field reference](/solutions/security/detect-and-alert/machine-learning.md#ml-fields) |
    | An indicator match rule fires on old or low-value indicators | Narrow the **Indicator index query**, for example to a shorter time range | [Indicator match rules](/solutions/security/detect-and-alert/indicator-match.md#indicator-match-limitations) |
    | The alerts are real, but they don't need urgent attention | Lower the **Default severity** and **Default risk score**, or use **Severity override** to lower the severity only for specific field values | [Basic settings](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-basic-params) |

## Test and save the change [test-tuned-rule]

Every condition you add to a rule can also hide an attack, so check what the tuned rule still detects before you save it.

1. While you edit the rule, use the rule preview to run the tuned rule against past data. Select a time range that includes the false positives you're removing. Refer to [Preview rules against historical data](/solutions/security/detect-and-alert/validate-and-test-rules.md#validate-historical-data).
2. Compare the preview results with the rule's recent alerts. The false positives you targeted no longer appear, and the alerts you'd still want to investigate do.
3. Select **Save changes**.
4. Check the rule's next alerts to confirm that the change works on new data.

## Example of narrowing a query [tune-example-narrow-query]

Administrators and management scripts run `whoami.exe` all the time, so a rule that matches every run of it creates alerts in any environment. Attackers run it too, often as soon as they get code execution through a web shell or a remote management tool, to check which account they're using.

This EQL query matches every run of `whoami.exe` on Windows hosts.

```eql
process where host.os.type == "windows" and event.type == "start" and
  process.name : "whoami.exe"
```

To match only the suspicious runs, add a condition on the process that started it. The following query matches `whoami.exe` only when an IIS worker process, a remote PowerShell session, the WMI provider host, `rundll32.exe`, or `regsvr32.exe` starts it. Legitimate tools rarely start it this way.

```eql
process where host.os.type == "windows" and event.type == "start" and
  process.name : "whoami.exe" and
  process.parent.name : ("w3wp.exe", "wsmprovhost.exe", "wmiprvse.exe", "rundll32.exe", "regsvr32.exe")
```

The tuned query no longer detects `whoami.exe` when other processes start it, such as a command shell that an attacker opened. Decide whether that gap is acceptable, or add a second condition that covers it. For example, the Elastic prebuilt [Whoami Process Activity](detection-rules://rules/windows/discovery_whoami_command_activity.md) rule also matches runs with SYSTEM privileges, and it excludes specific commands that monitoring tools run.

## Keep track of tuned rules [track-tuned-rules]

A tuned rule detects less than it did before, so make sure your team can find out what changed and why.

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` To find out who changed a rule and when, or to restore an earlier version, use the rule's changes history. Refer to [View rule changes history](/solutions/security/detect-and-alert/view-rule-changes-history.md).
* If you edited an Elastic prebuilt rule, an Elastic update that changes the same fields can conflict with your changes. Refer to [Resolve update conflicts](/solutions/security/detect-and-alert/update-prebuilt-rules.md#resolve-reduce-rule-conflicts).
* Record why you tuned the rule, for example in its **Investigation guide**, so analysts know which activity it no longer detects.
