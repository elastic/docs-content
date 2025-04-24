---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-configuring-alerts.html
---

# Generating alerts for anomaly detection jobs [ml-configuring-alerts]

{{kib}} {{alert-features}} include support for {{ml}} rules, which run scheduled checks for anomalies in one or more {{anomaly-jobs}} or check the health of the job with certain conditions. If the conditions of the rule are met, an alert is created and the associated action is triggered. For example, you can create a rule to check an {{anomaly-job}} every fifteen minutes for critical anomalies and to notify you in an email. To learn more about {{kib}} {{alert-features}}, refer to [Alerting](../../alerts-cases/alerts/alerting-getting-started.md).

The following {{ml}} rules are available:

{{anomaly-detect-cap}} alert
:   Checks if the {{anomaly-job}} results contain anomalies that match the rule conditions.

{{anomaly-jobs-cap}} health
:   Monitors job health and alerts if an operational issue occurred that may prevent the job from detecting anomalies.

::::{tip}
If you have created rules for specific {{anomaly-jobs}} and you want to monitor whether these jobs work as expected, {{anomaly-jobs}} health rules are ideal for this purpose.
::::

In **{{stack-manage-app}} > {{rules-ui}}**, you can create both types of {{ml}} rules. In the **{{ml-app}}** app, you can create only {{anomaly-detect}} alert rules; create them from the {{anomaly-job}} wizard after you start the job or from the {{anomaly-job}} list.

## {{anomaly-detect-cap}} alert rules [creating-anomaly-alert-rules]

When you create an {{anomaly-detect}} alert rule, you must select the job that
the rule applies to.

You must also select a type of {{ml}} result. In particular, you can create rules
based on bucket, record, or influencer results.

:::{image} /explore-analyze/images/ml-anomaly-alert-severity.png
:alt: Selecting result type, severity, and test interval
:screenshot:
:::

For each rule, you can configure the `anomaly_score` that triggers the action. 
The `anomaly_score` indicates the significance of a given anomaly compared to 
previous anomalies. The default severity threshold is 75 which means every 
anomaly with an `anomaly_score` of 75 or higher triggers the associated action.

You can select whether you want to include interim results. Interim results are 
created by the {{anomaly-job}}  before a bucket is finalized. These results might 
disappear after the bucket is fully processed. Include interim results if you 
want to be notified earlier about a potential anomaly even if it might be a 
false positive. If you want to get notified only about anomalies of fully 
processed buckets, do not include interim results.

You can also configure advanced settings. _Lookback interval_ sets an interval 
that is used to query previous anomalies during each condition check. Its value 
is derived from the bucket span of the job and the query delay of the {{{dfeed}}  by 
default. It is not recommended to set the lookback interval lower than the 
default value as it might result in missed anomalies. _Number of latest buckets_ 
sets how many buckets to check to obtain the highest anomaly from all the 
anomalies that are found during the _Lookback interval_. An alert is created 
based on the anomaly with the highest anomaly score from the most anomalous 
bucket.

You can also test the configured conditions against your existing data and check 
the sample results by providing a valid interval for your data. The generated 
preview contains the number of potentially created alerts during the relative 
time range you defined.

::::{tip}
You must also provide a _check interval_ that defines how often to
evaluate the rule conditions. It is recommended to select an interval that is
close to the bucket span of the job.
::::

As the last step in the rule creation process, define its [actions](#ml-configuring-alert-actions).

## {{anomaly-jobs-cap}} health rules [creating-anomaly-jobs-health-rules]

When you create an {{anomaly-jobs}} health rule, you must select the job or group
that the rule applies to. If you assign more jobs to the group, they are
included the next time the rule conditions are checked.

You can also use a special character (`*`) to apply the rule to all your jobs. 
Jobs created after the rule are automatically included. You can exclude jobs 
that are not critically important by using the _Exclude_ field.

Enable the health check types that you want to apply. All checks are enabled by 
default. At least one check needs to be enabled to create the rule. The 
following health checks are available:

Datafeed is not started
:   Notifies if the corresponding {{dfeed}} of the job is not started but the job is 
  in an opened state. The notification message recommends the necessary 
  actions to solve the error.

Model memory limit reached
:   Notifies if the model memory status of the job reaches the soft or hard model 
  memory limit. Optimize your job by following 
  [these guidelines](/explore-analyze/machine-learning/anomaly-detection/anomaly-detection-scale.md) or consider 
  [amending the model memory limit](/explore-analyze/machine-learning/anomaly-detection/anomaly-detection-scale.md#set-model-memory-limit).

Data delay has occurred
:    Notifies when the job missed some data. You can define the threshold for the 
  amount of missing documents you get alerted on by setting 
  _Number of documents_. You can control the lookback interval for checking 
  delayed data with _Time interval_. Refer to the 
  [Handling delayed data](/explore-analyze/machine-learning/anomaly-detection/ml-delayed-data-detection.md) page to see what to do about delayed data.

Errors in job messages
:    Notifies when the job messages contain error messages. Review the 
  notification; it contains the error messages, the corresponding job IDs and 
  recommendations on how to fix the issue. This check looks for job errors 
  that occur after the rule is created; it does not look at historic behavior.

:::{image} /explore-analyze/images/ml-health-check-config.png
:alt: Selecting health checkers
:screenshot:
:::

::::{tip}
You must also provide a _check interval_ that defines how often to
evaluate the rule conditions. It is recommended to select an interval that is
close to the bucket span of the job.
::::

As the last step in the rule creation process, define its actions.

## Actions [ml-configuring-alert-actions]

You can optionally send notifications when the rule conditions are met and when
they are no longer met. In particular, these rules support:

* alert summaries
* actions that run when the anomaly score matches the conditions (for {{anomaly-detect}} alert rules)
* actions that run when an issue is detected (for {{anomaly-jobs}} health rules)
* recovery actions that run when the conditions are no longer met

Each action uses a connector, which stores connection information for a {{kib}}
service or supported third-party integration, depending on where you want to
send the notifications. For example, you can use a Slack connector to send a
message to a channel. Or you can use an index connector that writes a JSON
object to a specific index. For details about creating connectors, refer to
[Connectors](/deploy-manage/manage-connectors.md#creating-new-connector).

After you select a connector, you must set the action frequency. You can choose
to create a summary of alerts on each check interval or on a custom interval.
For example, send slack notifications that summarize the new, ongoing, and
recovered alerts:

:::{image} /explore-analyze/images/ml-anomaly-alert-action-summary.png
:alt: Adding an alert summary action to the rule
:screenshot:
:::

::::{tip}
If you choose a custom action interval, it cannot be shorter than the
rule's check interval.
::::

Alternatively, you can set the action frequency such that actions run for each
alert. Choose how often the action runs (at each check interval, only when the
alert status changes, or at a custom action interval). For {{anomaly-detect}}
alert rules, you must also choose whether the action runs when the anomaly score
matches the condition or when the alert recovers:

:::{image} /explore-analyze/images/ml-anomaly-alert-action-score-matched.png
:alt: Adding an action for each alert in the rule
:screenshot:
:::

In {{anomaly-jobs}} health rules, choose whether the action runs when the issue is
detected or when it is recovered:

:::{image} /explore-analyze/images/ml-health-check-action.png
:alt: Adding an action for each alert in the rule
:screenshot:
:::

You can further refine the rule by specifying that actions run only when they
match a KQL query or when an alert occurs within a specific time frame.

There is a set of variables that you can use to customize the notification
messages for each action. Click the icon above the message text box to get the
list of variables or refer to [action variables](#action-variables). For example:

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

**`context.anomalyExplorerUrl`^*^**
:   URL to open in the Anomaly Explorer.

**`context.isInterim`**
:   Indicates if top hits contain interim results.

**`context.jobIds`^*^**
:   List of job IDs that triggered the alert.

**`context.message`^*^**
:   A preconstructed message for the alert.

**`context.score`**
:   Anomaly score at the time of the notification action.

**`context.timestamp`**
:   The bucket timestamp of the anomaly.

**`context.timestampIso8601`**
:   The bucket timestamp of the anomaly in ISO8601 format.

**`context.topInfluencers`**
:   The list of top influencers. Limited to a maximum of 3 documents.

:::{dropdown} Properties of `context.topInfluencers`
**`influencer_field_name`**
:   The field name of the influencer.

**`influencer_field_value`**
:   The entity that influenced, contributed to, or was to blame for the anomaly.

**`score`**
:   The influencer score. A normalized score between 0–100 which shows the influencer’s overall contribution to the anomalies.
:::

**`context.topRecords`**
:   The list of top records. Limited to a maximum of 3 documents.

:::{dropdown} Properties of `context.topRecords`
**`actual`**
:   The actual value for the bucket.

**`by_field_value`**
:   The value of the by field.

**`field_name`**
:   Certain functions require a field to operate on, for example, `sum()`. For those functions, this value is the name of the field to be analyzed.

**`function`**
:   The function in which the anomaly occurs, as specified in the detector configuration. For example, `max`.

**`over_field_name`**
:   The field used to split the data.

**`partition_field_value`**
:   The field used to segment the analysis.

**`score`**
:   A normalized score between 0–100, which is based on the probability of the anomalousness of this record.

**`typical`**
:   The typical value for the bucket, according to analytical modeling.
:::

### {{anomaly-detect-cap}} health action variables [anomaly-jobs-health-action-variables]

Every health check has two main variables: `context.message` and 
`context.results`. The properties of `context.results` may vary based on the 
type of check. You can find the possible properties for all the checks below.

####  Datafeed is not started

**`context.message`^*^**
:   A preconstructed message for the alert.

**`context.results`**
:   Contains the following properties:

:::{dropdown} Properties of `context.results`
**`datafeed_id`^*^**
:   The datafeed identifier.

**`datafeed_state`^*^**
:   The state of the datafeed. It can be `starting`, `started`, `stopping`, or `stopped`.

**`job_id`^*^**
:   The job identifier.

**`job_state`^*^**
:   The state of the job. It can be `opening`, `opened`, `closing`, `closed`, or `failed`.
:::

####  Model memory limit reached

**`context.message`^*^**
:   A preconstructed message for the rule.

**`context.results`**
:   Contains the following properties:

:::{dropdown} Properties of `context.results`
**`job_id`^*^**
:   The job identifier.

**`memory_status`^*^**
:   The status of the mathematical model. It can have one of the following values:  
    - `soft_limit`: The model used more than 60% of the configured memory limit and older unused models will be pruned to free up space. In categorization jobs, no further category examples will be stored.  
    - `hard_limit`: The model used more space than the configured memory limit. As a result, not all incoming data was processed.  
    The `memory_status` is `ok` for recovered alerts.

**`model_bytes`^*^**
:   The number of bytes of memory used by the models.

**`model_bytes_exceeded`^*^**
:   The number of bytes over the high limit for memory usage at the last allocation failure.

**`model_bytes_memory_limit`^*^**
:   The upper limit for model memory usage.

**`log_time`^*^**
:   The timestamp of the model size statistics according to server time. Time formatting is based on the Kibana settings.

**`peak_model_bytes`^*^**
:   The peak number of bytes of memory ever used by the model.
:::

####  Data delay has occurred

**`context.message`^*^**
:   A preconstructed message for the rule.

**`context.results`**
:   For recovered alerts, `context.results` is either empty (when there is no delayed data) or the same as for an active alert (when the number of missing documents is less than the *Number of documents* threshold set by the user).  
    Contains the following properties:

:::{dropdown} Properties of `context.results`
**`annotation`^*^**
:   The annotation corresponding to the data delay in the job.

**`end_timestamp`^*^**
:   Timestamp of the latest finalized buckets with missing documents. Time formatting is based on the Kibana settings.

**`job_id`^*^**
:   The job identifier.

**`missed_docs_count`^*^**
:   The number of missed documents.
:::

####  Error in job messages

**`context.message`^*^**
:   A preconstructed message for the rule.

**`context.results`**
:   Contains the following properties:

:::{dropdown} Properties of `context.results`
**`timestamp`**
:   Timestamp of the latest finalized buckets with missing documents.

**`job_id`**
:   The job identifier.

**`message`**
:   The error message.

**`node_name`**
:   The name of the node that runs the job.
:::


