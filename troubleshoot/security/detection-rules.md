---
navigation_title: "Detection rules"
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ts-detection-rules.html
  - https://www.elastic.co/guide/en/serverless/current/security-ts-detection-rules.html
  - https://www.elastic.co/guide/en/security/current/alerts-ui-monitor.html#troubleshoot-signals
  - https://www.elastic.co/guide/en/serverless/current/security-alerts-ui-monitor.html#troubleshoot-signals
---

# Troubleshoot detection rules [ts-detection-rules]


This topic covers common troubleshooting issues when creating or managing [detection rules](../../solutions/security/detect-and-alert/create-detection-rule.md).


## {{ml-cap}} rules [ML-rules-ts]

::::{dropdown} {{ml-cap}} rule is failing and a required {{ml}} job is stopped
:name: start-ML-jobs-ts

If a {{ml}} rule is failing, check to make sure the required {{ml}} jobs are running and start any jobs that have stopped.

1. Go to **Rules** → **Detection rules (SIEM)**, then select the {{ml}} rule. The required {{ml}} jobs and their statuses are listed in the **Definition** section.

   :::{image} ../../images/security-rules-ts-ml-job-stopped.png
   :alt: Rule details page with ML job stopped
   :class: screenshot
   :::

2. If a required {{ml}} job isn’t running, turn on the **Run job** toggle next to it.
3. Rerun the {{ml}} detection rule.
::::


## Indicator match rules [IM-match-rules-ts]

::::{dropdown} Rules are failing due to number of alerts
:name: IM-rule-failure

If you receive the following rule failure: `"Bulk Indexing of signals failed: [parent] Data too large"`, this indicates that the alerts payload was too large to process.

This can be caused by bad indicator data, a misconfigured rule, or too many event matches. Review your indicator data or rule query. If nothing obvious is misconfigured, try executing the rule against a subset of the original data and continue diagnosis.
::::


::::{dropdown} Indicator match rules are timing out
:name: IM-rule-timeout

If you receive the following rule failure: `"An error occurred during rule execution: message: "Request Timeout after 90000ms"`, this indicates that the query phase is timing out. Try refining the time frame or dividing the data defined in the query into multiple rules.
::::


::::{dropdown} Indicator match rules are failing because the `maxClauseCount` limit is too low
:name: IM-rule-heap-memory

If you receive the following rule failure: `Bulk Indexing of signals failed: index: ".index-name" reason: "maxClauseCount is set to 1024" type: "too_many_clauses"`, this indicates that the limit for the total number of clauses that a query tree can have is too low. To update your maximum clause count, [increase the size of your {{es}} JVM heap memory](https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#set-jvm-heap-size). 1 GB of {{es}} JVM heap size or more is sufficient.
::::


::::{dropdown} General slowness
:name: IM-slowness

If you notice rule delays, review the suggestions above to troubleshoot, and also consider limiting the number of rules that run simultaneously, as this can cause noticeable performance implications in {{kib}}.
::::


## Rule exceptions [rule-exceptions-ts]

:::::{dropdown} No autocomplete suggestions
:name: rule-exceptions-autocomplete-ts

When you’re creating detection rule exceptions, autocomplete might not provide suggestions in the **Value** field if the values don’t exist in the current page’s time range.

You can resolve this by expanding the time range, or by configuring {{kib}}'s autocomplete feature to get suggestions from your full data set instead. Go to **{{kib}}** → **Stack Management** → **Advanced Settings**, then turn off `autocomplete:useTimeRange`.

::::{warning}
Turning off `autocomplete:useTimeRange` could cause performance issues if the data set is especially large.
::::

:::::


:::::{dropdown} Warning about type conflicts and unmapped fields
:name: rule-exceptions-field-conflicts

A warning icon (![Field conflict warning icon](../../images/security-field-warning-icon.png "")) and message appear for fields with [type conflicts](#fields-with-conflicting-types) across multiple indices or  fields that are [unmapped](#unmapped-field-conflict). You can learn more about the conflict by clicking the warning message.

::::{note}
A field can have type conflicts *and* be unmapped in specified indices.
::::


:::{image} ../../images/security-warning-icon-message.png
:alt: Shows the warning icon and message
:class: screenshot
:::


### Fields with conflicting types [fields-with-conflicting-types]

Type conflicts occur when a field is mapped to different types across multiple indices. To resolve this issue, you can create new indices with matching field type mappings and [reindex your data](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex). Otherwise, use the information about a field’s type mappings to ensure you’re entering compatible field values when defining exception conditions.

In the following example, the selected field has been defined as different types across five indices.

:::{image} ../../images/security-warning-type-conflicts.png
:alt: Warning for fields with type conflicts
:class: screenshot
:::


### Unmapped fields [unmapped-field-conflict]

Unmapped fields are undefined within an index’s mapping definition. Using unmapped fields to define an exception can prevent it from working as expected, and lead to false positives or unexpected alerts. To fix unmapped fields, [add them](../../manage-data/data-store/mapping/explicit-mapping.md#update-mapping) to your indices' mapping definitions.

In the following example, the selected field is unmapped across two indices.

:::{image} ../../images/security-warning-unmapped-fields.png
:alt: Warning for unmapped fields
:class: screenshot
:::

:::::


## Rule executions

:::::{dropdown} Troubleshoot missing alerts
:name: troubleshoot-signals

When a rule fails to run close to its scheduled time, some alerts may be missing. There are a number of ways to try to resolve this issue:

* [Troubleshoot gaps](#troubleshoot-gaps)
* [Troubleshoot ingestion pipeline delay](#troubleshoot-ingestion-pipeline-delay)
* [Troubleshoot missing alerts for {{ml}} jobs](#ml-job-compatibility)

You can also use Task Manager in {{kib}} to troubleshoot background tasks and processes that may be related to missing alerts:

* [Task Manager health monitoring](../../deploy-manage/monitor/kibana-task-manager-health-monitoring.md)
* [Task Manager troubleshooting](../../troubleshoot/kibana/task-manager.md)


### Troubleshoot maximum alerts warning [troubleshoot-max-alerts]

When a rule reaches the maximum number of alerts it can generate during a single rule execution, the following warning appears on the rule’s details page and in the rule execution log: `This rule reached the maximum alert limit for the rule execution. Some alerts were not created.`

If you receive this warning, go to the rule’s **Alerts** tab and check for anything unexpected. Unexpected alerts might be created from data source issues or queries that are too broadly scoped. To further reduce alert volume, you can also add [rule exceptions](../../solutions/security/detect-and-alert/add-manage-exceptions.md) or [suppress alerts](../../solutions/security/detect-and-alert/suppress-detection-alerts.md).


### Troubleshoot gaps [troubleshoot-gaps]

If you see values in the Gaps column in the Rule Monitoring table or on the Rule details page for a small number of rules, you can edit those rules and increase their additional look-back time.

It’s recommended to set the `Additional look-back time` to at least 1 minute. This ensures there are no missing alerts when a rule doesn’t run exactly at its scheduled time.

{{elastic-sec}} prevents duplication. Any duplicate alerts that are discovered during the `Additional look-back time` are *not* created.

::::{note}
If the rule that experiences gaps is an indicator match rule, see [how to tune indicator match rules](../../solutions/security/detect-and-alert/tune-detection-rules.md#tune-indicator-rules). Also please note that {{elastic-sec}} provides [limited support for indicator match rules](../../solutions/security/detect-and-alert.md#support-indicator-rules).
::::


If you see gaps for numerous rules:

* If you restarted {{kib}} when many rules were activated, try deactivating them and then reactivating them in small batches at staggered intervals. This ensures {{kib}} does not attempt to run all the rules at the same time.
* Consider adding another {{kib}} instance to your environment.


### Troubleshoot ingestion pipeline delay [troubleshoot-ingestion-pipeline-delay]

Even if your rule runs at its scheduled time, there might still be missing alerts if your ingestion pipeline delay is greater than your rule interval + additional look-back time. Prebuilt rules have a minimum interval + additional look-back time of 6 minutes in {{stack}} version >=7.11.0. To avoid missed alerts for prebuilt rules, use caution to ensure that ingestion pipeline delays remain below 6 minutes.

In addition, use caution when creating custom rule schedules to ensure that the specified interval + additional look-back time is greater than your deployment’s ingestion pipeline delay.

You can reduce the number of missed alerts due to ingestion pipeline delay by specifying the `Timestamp override` field value to `event.ingested` in [advanced settings](../../solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params) during rule creation or editing. The detection engine uses the value from the `event.ingested` field as the timestamp when executing the rule.

For example, say an event occurred at 10:00 but wasn’t ingested into {{es}} until 10:10 due to an ingestion pipeline delay. If you created a rule to detect that event with an interval + additional look-back time of 6 minutes, and the rule executes at 10:12, it would still detect the event because the `event.ingested` timestamp was from 10:10, only 2 minutes before the rule executed and well within the rule’s 6-minute interval + additional look-back time.

:::{image} ../../images/security-timestamp-override.png
:alt: timestamp override
:class: screenshot
:::


### Troubleshoot missing alerts for {{ml}} jobs [ml-job-compatibility]
```yaml {applies_to}
stack: all
```


{{ml-cap}} detection rules use {{ml}} jobs that have dependencies on data fields populated by the {{beats}} and {{agent}} integrations. In {{stack}} version 8.3, new {{ml}} jobs (prefixed with `v3`) were released to operate on the ECS fields available at that time.

If you’re using 8.2 or earlier versions of {{beats}} or {{agent}} with {{stack}} version 8.3 or later, you may need to duplicate prebuilt rules or create new custom rules *before* you update the Elastic prebuilt rules. Once you update the prebuilt rules, they will only use `v3` {{ml}} jobs. Duplicating the relevant prebuilt rules before updating them ensures continued coverage by allowing you to keep using `v1` or `v2` jobs (in the duplicated rules) while also running the new `v3` jobs (in the updated prebuilt rules).

::::{important}
* Duplicated rules may result in duplicate anomaly detections and alerts.
* Ensure that the relevant `v3` {{ml}} jobs are running before you update the Elastic prebuilt rules.

::::


* If you only have **8.3 or later versions of {{beats}} and {{agent}}**: You can download or update your prebuilt rules and use the latest `v3` {{ml}} jobs. No additional action is required.
* If you only have **8.2 or earlier versions of {{beats}} or {{agent}}**, or **a mix of old and new versions**: To continue using the `v1` and `v2` {{ml}} jobs specified by pre-8.3 prebuilt detection rules, you must duplicate affected prebuilt rules *before* updating them to the latest rule versions. The duplicated rules can continue using the same `v1` and `v2` {{ml}} jobs, and the updated prebuilt {{ml}} rules will use the new `v3` {{ml}} jobs.
* If you have **a non-Elastic data shipper that gathers ECS-compatible events**: You can use the latest `v3` {{ml}} jobs with no additional action required, as long as your data shipper uses the latest ECS specifications. However, if you’re migrating from {{ml}} rules using `v1`/`v2` jobs, ensure that you start the relevant `v3` jobs before updating the Elastic prebuilt rules.

The following Elastic prebuilt rules use the new `v3` {{ml}} jobs to generate alerts. Duplicate their associated `v1`/`v2` prebuilt rules *before* updating them if you need continued coverage from the `v1`/`v2` {{ml}} jobs:

* [Unusual Linux Network Port Activity](https://www.elastic.co/guide/en/security/current/unusual-linux-network-port-activity.html): `v3_linux_anomalous_network_port_activity`
* [Unusual Linux Network Connection Discovery](https://www.elastic.co/guide/en/security/current/unusual-linux-network-connection-discovery.html): `v3_linux_anomalous_network_connection_discovery`
* [Anomalous Process For a Linux Population](https://www.elastic.co/guide/en/security/current/anomalous-process-for-a-linux-population.html): `v3_linux_anomalous_process_all_hosts`
* [Unusual Linux Username](https://www.elastic.co/guide/en/security/current/unusual-linux-username.html): `v3_linux_anomalous_user_name`
* [Unusual Linux Process Calling the Metadata Service](https://www.elastic.co/guide/en/security/current/unusual-linux-process-calling-the-metadata-service.html): `v3_linux_rare_metadata_process`
* [Unusual Linux User Calling the Metadata Service](https://www.elastic.co/guide/en/security/current/unusual-linux-user-calling-the-metadata-service.html): `v3_linux_rare_metadata_user`
* [Unusual Process For a Linux Host](https://www.elastic.co/guide/en/security/current/unusual-process-for-a-linux-host.html): `v3_rare_process_by_host_linux`
* [Unusual Process For a Windows Host](https://www.elastic.co/guide/en/security/current/unusual-process-for-a-windows-host.html): `v3_rare_process_by_host_windows`
* [Unusual Windows Network Activity](https://www.elastic.co/guide/en/security/current/unusual-windows-network-activity.html): `v3_windows_anomalous_network_activity`
* [Unusual Windows Path Activity](https://www.elastic.co/guide/en/security/current/unusual-windows-path-activity.html): `v3_windows_anomalous_path_activity`
* [Anomalous Windows Process Creation](https://www.elastic.co/guide/en/security/current/anomalous-windows-process-creation.html): `v3_windows_anomalous_process_creation`
* [Anomalous Process For a Windows Population](https://www.elastic.co/guide/en/security/current/anomalous-process-for-a-windows-population.html): `v3_windows_anomalous_process_all_hosts`
* [Unusual Windows Username](https://www.elastic.co/guide/en/security/current/unusual-windows-username.html): `v3_windows_anomalous_user_name`
* [Unusual Windows Process Calling the Metadata Service](https://www.elastic.co/guide/en/security/current/unusual-windows-process-calling-the-metadata-service.html): `v3_windows_rare_metadata_process`
* [Unusual Windows User Calling the Metadata Service](https://www.elastic.co/guide/en/security/current/unusual-windows-user-calling-the-metadata-service.html): `v3_windows_rare_metadata_user`

:::::
