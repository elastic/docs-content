---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-configuring-alerts.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Generating alerts for anomaly detection jobs [ml-configuring-alerts]

This guide explains how to create alerts that notify you automatically when an anomaly is detected in a [{{anomaly-job}}](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md), or when issues occur that affect job performance.

{{kib}}'s {{alert-features}} support two types of {{ml}} rules, which run scheduled checks on your {{anomaly-jobs}}:

[{{anomaly-detect-cap}} alert](#creating-anomaly-alert-rules)
:   Checks job results for anomalies that match your defined conditions and raises an alert when found.

[{{anomaly-jobs-cap}} health](#creating-anomaly-jobs-health-rules)
:   Monitors the operational status of a job and alerts you if issues occur (such as a stopped datafeed or memory limit errors). 
    
:::{tip}
If you have created rules for specific {{anomaly-jobs}} and you want to monitor whether these jobs work as expected, {{anomaly-jobs}} health rules are ideal for this purpose.
:::

If the conditions of a rule are met, an alert is created, and any associated actions (such as sending an email or Slack message) are triggered. For example, you can configure a rule that checks a job every 15 minutes for anomalies with a high score and sends a notification when one is found.

In **{{stack-manage-app}} > {{rules-ui}}**, you can create both types of {{ml}} rules. In the **{{ml-app}}** app, you can create only {{anomaly-detect}} alert rules; create them from the {{anomaly-job}} wizard after you start the job or from the {{anomaly-job}} list.

## Prerequisites [prerequisites]

Before you begin, make sure that:

- You have at least one running [{{anomaly-job}}](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md).
- You have appropriate [user permissions](/deploy-manage/users-roles.md) to create and manage alert rules.
-  If you would like to send notifications about alerts (such as Slack messages, emails, or webhooks), make sure you have configured the necessary [connectors](https://www.elastic.co/docs/reference/kibana/connectors-kibana).

## {{anomaly-detect-cap}} alert rules [creating-anomaly-alert-rules]

{{anomaly-detect-cap}} alert rules monitor if the {{anomaly-job}} results contain anomalies that match the rule conditions.

To set up an {{anomaly-detect}} alert rule:

1. Open **{{rules-ui}}**: find **{{stack-manage-app}} > {{rules-ui}}** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **{{anomaly-detect-cap}}** rule type.

:::{image} /explore-analyze/images/ml-anomaly-create-anomaly-detection.png
:alt: Selecting Anomaly detection rule type
:screenshot:
:::

3. Select the [{{anomaly-job}}](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) that the rule applies to.
4. Select a type of {{ml}} result. You can create rules based on bucket, record, or influencer results.
5. (Optional) Configure the `anomaly_score` that triggers the action. 
The `anomaly_score` indicates the significance of a given anomaly compared to 
previous anomalies. The default severity threshold is 75 which means every 
anomaly with an `anomaly_score` of 75 or higher triggers the associated action.
6. {applies_to}`stack: ga 9.3`{applies_to}`serverless: ga` (Optional) To narrow down the list of anomalies that the rule monitors for, add an **Anomaly filter**. This filtering capability uses KQL and is only available for the Record and Influencer result types. 
    
    In the **Anomaly filter** field, enter a KQL query that specifies to only alert when either or both happen:
    
    * Certain partitioning or influencers fields in the anomaly results match specified conditions
    * The actual or typical scores in the anomalies match specified conditions

    For example, say you've set up alerting for an anomaly detection job that has `partition_field = "response.keyword"` as the detector. If you were only interested in being alerted on `response.keyword = 404`, enter `partition_field_value: "404"` into the **Anomaly filter** field. When the rule runs, it will only alert on anomalies with ``partition_field_value: "404"`.

    ::::{note}
    When creating the KQL query, you're given suggestions for the most relevant fields to filter by. To compare actual and typical values, use operators such as `>` (greater than), `<` (less than), or `=` (equal to).
    ::::

7. Select whether you want to include interim results. Interim results are created before a bucket is finalized and might disappear after full processing.
    - Include interim results if you 
want to be notified earlier about a potential anomaly even if it might be a 
false positive. 
    - Don't include interim results if you want to get notified only about anomalies of fully 
processed buckets.

:::{image} /explore-analyze/images/ml-anomaly-alert.png
:alt: Selecting result type, severity, and interim results
:screenshot:
:::

8. (Optional) Configure **Advanced settings**:
   - Configure the _Lookback interval_ to define how far back to query previous anomalies during each condition check. Its value is derived from the bucket span of the job and the query delay of the {{dfeed}} by default. It is not recommended to set the lookback interval lower than the default value, as it might result in missed anomalies.
   - Configure the _Number of latest buckets_ to specify how many buckets to check to obtain the highest anomaly score found during the _Lookback interval_. The alert is created based on the highest scoring anomaly from the most anomalous bucket.

::::{tip}
You can preview how the rule would perform on existing data:

 - Define the _check interval_ to specify how often the rule conditions are evaluated. It’s recommended to set this close to the job’s bucket span. 
 - Click **Test**.
 
 The preview shows how many alerts would have been triggered during the selected time range.
::::

:::{image} /explore-analyze/images/ml-anomaly-alert-advanced.jpg 
:alt: Advanced settings and testing the rule condition
:screenshot:
:::

9. Set how often to check the rule conditions by selecting a time value and unit under **Rule schedule**.
10. (Optional) Configure **Advanced options**:
   - Define the number of consecutive matches required before an alert is triggered under **Alert delay**.
   - Enable or disable **Flapping Detection** to reduce noise from frequently changing alerts. You can customize the flapping detection settings if you need different thresholds for detecting flapping behavior.

:::{image} /explore-analyze/images/ml-anomaly-rule-schedule-advanced.jpg
:alt: Rule schedule and advanced settings
:screenshot:
:::

Next, define the [actions](#ml-configuring-alert-actions) that occur when the rule conditions are met.

## {{anomaly-jobs-cap}} health rules [creating-anomaly-jobs-health-rules]

{{anomaly-jobs-cap}} health rules monitor job health and alerts if an operational issue occurred that may prevent the job from detecting anomalies. 

To set up an {{anomaly-jobs}} alert rule:

1. Open **{{rules-ui}}**: find **{{stack-manage-app}} > {{rules-ui}}** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **{{anomaly-jobs-cap}}** rule type.

:::{image} /explore-analyze/images/ml-anomaly-create-anomaly-job-health.png
:alt: Selecting Anomaly detection jobs health rules type
:screenshot:
:::

3. Include jobs and groups:
   - Select the job or group that the rule applies to. If you add more jobs to the selected group later, they are automatically included the next time the rule conditions are checked. To apply the rule to all your jobs, you can use a special character (`*`). This ensures that any jobs created after the rule is saved are automatically included.
   - (Optional) To exclude jobs that are not critically important, use the **Exclude** field.

4. Enable the health check types you want to apply. All checks are enabled by default. At least one check needs to be enabled to create the rule. The following health checks are available:

   - **Datafeed is not started:** Notifies if the corresponding {{dfeed}} of the job is not started but the job is 
  in an opened state. The notification message recommends the necessary 
  actions to solve the error.

   - **Model memory limit reached**: Notifies if the model memory status of the job reaches the soft or hard model 
   memory limit. Optimize your job by following [these guidelines](/explore-analyze/machine-learning/anomaly-detection/anomaly-detection-scale.md) or consider [amending the model memory limit](/explore-analyze/machine-learning/anomaly-detection/anomaly-detection-scale.md#set-model-memory-limit).

   - **Data delay has occurred:** Notifies when the job missed some data. You can define the threshold for the 
   amount of missing documents you get alerted on by setting _Number of documents_. You can control the lookback interval for checking delayed data with _Time interval_. Refer to the [Handling delayed data](/explore-analyze/machine-learning/anomaly-detection/ml-delayed-data-detection.md) page to see what to do about delayed data.

   - **Errors in job messages:** Notifies when the job messages contain error messages. Review the 
   notification; it contains the error messages, the corresponding job IDs and recommendations on how to fix the issue. This check looks for job errors that occur after the rule is created; it does not look at historic behavior.

:::{image} /explore-analyze/images/ml-health-check-config.jpg
:alt: Selecting health checkers
:screenshot:
:::

5. Set how often to check the rule conditions by selecting a time value and unit under **Rule schedule**. It is recommended to select an interval that is close to the bucket span of the job.

6. (Optional) Configure **Advanced options**:
   - Define the number of consecutive matches required before an alert is triggered under **Alert delay**.
   - Enable or disable **Flapping Detection** to reduce noise from frequently changing alerts. You can customize the flapping detection settings if you need different thresholds for detecting flapping behavior.

:::{image} /explore-analyze/images/ml-anomaly-rule-schedule-advanced.jpg
:alt: Rule schedule and advanced settings
:screenshot:
:::

Next, define the [actions](#ml-configuring-alert-actions) that occur when the rule conditions are met.

## Actions [ml-configuring-alert-actions]

You can send notifications when the rule conditions are met and when they are no longer met. These rules support:

* **Alert summaries:** Combine multiple alerts into a single notification, sent at regular intervals.
* **Per-alert actions for anomaly detection:** Trigger an action when an anomaly score meets the defined condition.
* **Per-alert actions for job health:** Trigger an action when an issue is detected in a job’s health status (for example, a stopped datafeed or memory issue).
* **Recovery actions:** Notify when a previously triggered alert returns to a normal state.

To set up an action:

1. Select a connector. 

:::{important}
Each action uses a connector, which stores connection information for a {{kib}}
service or supported third-party integration, depending on where you want to
send the notifications. For example, you can use a Slack connector to send a
message to a channel. Or you can use an index connector that writes a JSON
object to a specific index. For details about creating connectors, refer to
[Connectors](/deploy-manage/manage-connectors.md#creating-new-connector).
:::

2. Set the action frequency. Choose whether you want to send:

   * **Summary of alerts**: Groups multiple alerts into a single notification at each check interval or on a custom schedule.
   * **A notification for each alert**: Sends individual alerts as they are triggered, recovered, or change state.


::::{dropdown} Example: Summary of alerts
You can choose to create a summary of alerts on:
  * **Each check interval**: Sends a summary every time the rule runs (for example, every 5 minutes).
  * **Custom interval**: Sends a summary less often, on a schedule you define (for example, every hour), which helps reduce notification noise. A custom action interval cannot be shorter than the rule's check interval.

For example, send slack notifications that summarize the new, ongoing, and recovered alerts:

:::{image} /explore-analyze/images/ml-anomaly-alert-action-summary.png
:alt: Adding an alert summary action to the rule
:screenshot:
:::
::::

::::{dropdown} Example: For each alert

Choose how often the action runs: 

 * at each check interval, 
 * only when the alert status changes, or 
 * at a custom action interval. 
 
For *{{anomaly-detect}} alert rules*, you must also choose whether the action runs when the anomaly score
matches the condition or when the alert recovers:

:::{image} /explore-analyze/images/ml-anomaly-alert-action-score-matched.png
:alt: Adding an action for each alert in the rule
:screenshot:
:::

For *{{anomaly-jobs}} health rules*, choose whether the action runs when the issue is
detected or when it is recovered:

:::{image} /explore-analyze/images/ml-health-check-action.png
:alt: Adding an action for each alert in the rule
:screenshot:
:::

::::

3. Specify that actions run only when they match a KQL query or occur within a specific time frame.

4. Use variables to customize the notification message. Click the icon above the message field to view available variables, or refer to [action variables](#action-variables). For example:

:::{image} /explore-analyze/images/ml-anomaly-alert-messages.png
:alt: Customizing your message
:screenshot:
:::

After you save the configurations, the rule appears in the
*{{stack-manage-app}} > {{rules-ui}}* list; you can check its status and see the
overview of its configuration information.

When an alert occurs for an {{anomaly-detect}} alert rule, it is always the same
name as the job ID of the associated {{anomaly-job}} that triggered it. You can
review how the alerts that are occured correlate with the {{anomaly-detect}}
results in the **Anomaly explorer** by using the **Anomaly timeline** swimlane
and the **Alerts** panel.

If necessary, you can snooze rules to prevent them from generating actions. For
more details, refer to
[Snooze and disable rules](/explore-analyze/alerts-cases/alerts/create-manage-rules.md#controlling-rules).

## Action variables [action-variables]

The following variables are specific to the {{ml}} rule types. An asterisk (`*`)
marks the variables that you can use in actions related to recovered alerts.

You can also specify [variables common to all rules](/explore-analyze/alerts-cases/alerts/rule-action-variables.md).

### {{anomaly-detect-cap}} alert action variables [anomaly-alert-action-variables]

Every {{anomaly-detect}} alert has the following action variables:

`context.anomalyExplorerUrl`^*^
:   URL to open in the Anomaly Explorer.

`context.isInterim`
:   Indicates if top hits contain interim results.

`context.jobIds`^*^
:   List of job IDs that triggered the alert.

`context.message`^*^
:   A preconstructed message for the alert.

`context.score`
:   Anomaly score at the time of the notification action.

`context.timestamp`
:   The bucket timestamp of the anomaly.

`context.timestampIso8601`
:   The bucket timestamp of the anomaly in ISO8601 format.

`context.topInfluencers`
:   The list of top influencers. Limited to a maximum of 3 documents.

:::{dropdown} Properties of `context.topInfluencers`
`influencer_field_name`
:   The field name of the influencer.

`influencer_field_value`
:   The entity that influenced, contributed to, or was to blame for the anomaly.

`score`
:   The influencer score. A normalized score between 0–100 which shows the influencer’s overall contribution to the anomalies.
:::

`context.topRecords`
:   The list of top records. Limited to a maximum of 3 documents.

:::{dropdown} Properties of `context.topRecords`
`actual`
:   The actual value for the bucket.

`by_field_value`
:   The value of the by field.

`field_name`
:   Certain functions require a field to operate on, for example, `sum()`. For those functions, this value is the name of the field to be analyzed.

`function`
:   The function in which the anomaly occurs, as specified in the detector configuration. For example, `max`.

`over_field_name`
:   The field used to split the data.

`partition_field_value`
:   The field used to segment the analysis.

`score`
:   A normalized score between 0–100, which is based on the probability of the anomalousness of this record.

`typical`
:   The typical value for the bucket, according to analytical modeling.
:::

### {{anomaly-detect-cap}} health action variables [anomaly-jobs-health-action-variables]

Every health check has two main variables: `context.message` and 
`context.results`. The properties of `context.results` may vary based on the 
type of check. You can find the possible properties for all the checks below.

####  Datafeed is not started

`context.message`^*^
:   A preconstructed message for the alert.

`context.results`
:   Contains the following properties:

:::{dropdown} Properties of `context.results`
`datafeed_id`^*^
:   The datafeed identifier.

`datafeed_state`^*^
:   The state of the datafeed. It can be `starting`, `started`, `stopping`, or `stopped`.

`job_id`^*^
:   The job identifier.

`job_state`^*^
:   The state of the job. It can be `opening`, `opened`, `closing`, `closed`, or `failed`.
:::

####  Model memory limit reached

`context.message`^*^
:   A preconstructed message for the rule.

`context.results`
:   Contains the following properties:

:::{dropdown} Properties of `context.results`
`job_id`^*^
:   The job identifier.

`memory_status`^*^
:   The status of the mathematical model. It can have one of the following values:  
    - `soft_limit`: The model used more than 60% of the configured memory limit and older unused models will be pruned to free up space. In categorization jobs, no further category examples will be stored.  
    - `hard_limit`: The model used more space than the configured memory limit. As a result, not all incoming data was processed.  
    The `memory_status` is `ok` for recovered alerts.

`model_bytes`^*^
:   The number of bytes of memory used by the models.

`model_bytes_exceeded`^*^
:   The number of bytes over the high limit for memory usage at the last allocation failure.

`model_bytes_memory_limit`^*^
:   The upper limit for model memory usage.

`log_time`^*^
:   The timestamp of the model size statistics according to server time. Time formatting is based on the Kibana settings.

`peak_model_bytes`^*^
:   The peak number of bytes of memory ever used by the model.
:::

####  Data delay has occurred

`context.message`^*^
:   A preconstructed message for the rule.

`context.results`
:   For recovered alerts, `context.results` is either empty (when there is no delayed data) or the same as for an active alert (when the number of missing documents is less than the *Number of documents* threshold set by the user).  
    Contains the following properties:

:::{dropdown} Properties of `context.results`
`annotation`^*^
:   The annotation corresponding to the data delay in the job.

`end_timestamp`^*^
:   Timestamp of the latest finalized buckets with missing documents. Time formatting is based on the Kibana settings.

`job_id`^*^
:   The job identifier.

`missed_docs_count`^*^
:   The number of missed documents.
:::

####  Error in job messages

`context.message`^*^
:   A preconstructed message for the rule.

`context.results`
:   Contains the following properties:

:::{dropdown} Properties of `context.results`
`timestamp`
:   Timestamp of the latest finalized buckets with missing documents.

`job_id`
:   The job identifier.

`message`
:   The error message.

`node_name`
:   The name of the node that runs the job.
:::


