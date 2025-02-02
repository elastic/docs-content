---
navigation_title: "Suppress alerts"
---

# Suppress detection alerts [security-alert-suppression]


::::{admonition} Requirements and notice
:class: important

* {{ml-cap}} rules have [additional requirements](../../../solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md) for alert suppression.
* Alert suppression is in technical preview for event correlation rules. The functionality may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.

::::


Alert suppression allows you to reduce the number of repeated or duplicate detection alerts created by these detection rule types:

* [Custom query](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-custom-rule)
* [Threshold](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-threshold-rule)
* [Indicator match](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-indicator-rule)
* [Event correlation](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-eql-rule)
* [New terms](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-new-terms-rule)
* [ES|QL](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-esql-rule)
* [Machine learning](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-ml-rule)

Normally, when a rule meets its criteria repeatedly, it creates multiple alerts, one for each time the rule’s criteria are met. When alert suppression is configured, duplicate qualifying events are grouped, and only one alert is created for each group. Depending on the rule type, you can configure alert suppression to create alerts each time the rule runs, or once within a specified time window. You can also specify multiple fields to group events by unique combinations of values.

The {{security-app}} displays several indicators in the Alerts table and the alert details flyout when a detection alert is created with alert suppression enabled. You can view the original events associated with suppressed alerts by investigating the alert in Timeline.

::::{note}
Alert suppression is not available for Elastic prebuilt rules. However, if you want to suppress alerts for a prebuilt rule, you can duplicate it, then configure alert suppression on the duplicated rule.

::::



## Configure alert suppression [security-alert-suppression-configure-alert-suppression]

You can configure alert suppression when you create or edit a supported rule type. Refer to documentation for creating [custom query](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-custom-rule), [threshold](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-threshold-rule), [indicator match](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-indicator-rule), [event correlation](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-eql-rule), [new terms](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-new-terms-rule), [ES|QL](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-esql-rule), or [machine learning](../../../solutions/security/detect-and-alert/create-detection-rule.md#create-ml-rule) rules for detailed instructions.

1. When configuring the rule type (the **Define rule** step for a new rule, or the **Definition** tab for an existing rule), specify how you want to group events for alert suppression:

    * **Custom query rule, indicator match, threshold, event correlation, new terms, {{esql}}, or {{ml}} rules:** In **Suppress alerts by**, enter 1-3 field names to group events by the fields' values.
    * **Threshold rule:** In **Group by**, enter up to 3 field names to group events by the fields' values, or leave the setting empty to group all qualifying events together.

        ::::{note}
        If you specify a field with multiple values, alerts with that field are handled as follows:

        * **Custom query or threshold rules:** Alerts are grouped by each unique value. For example, if you suppress alerts by `destination.ip` of `[127.0.0.1, 127.0.0.2, 127.0.0.3]`, alerts will be suppressed separately for each value of `127.0.0.1`, `127.0.0.2`, and `127.0.0.3`.
        * **Indicator match, event correlation (non-sequence queries only), new terms, {{esql}}, or {{ml}} rules:** Alerts with the specified field name and identical array values are grouped together. For example, if you suppress alerts by `destination.ip` of `[127.0.0.1, 127.0.0.2, 127.0.0.3]`, alerts with the entire array are grouped and only one alert is created for the group.
        * **Event correlation (sequence queries only) rules:** If the suppression field is an array of values, the suppressed alert will only suppress values that are an exact match. The values must be equivalent and be in the same position. For example, if you configure suppresson on the field `myips` and one sequence alert has [1.1.1.1, 0.0.0.0] and another sequence alert has [1.1.1.1, 192.168.0.1], neither of those alerts will be suppressed, despite sharing an array element.

        ::::

2. If available, select how often to create alerts for duplicate events:

    ::::{admonition} NOTE
    :class: note

    Both options are available for custom query, indicator match, event correlation, new terms, {{esql}}, and {{ml}} rules. Threshold rules only have the **Per time period** option.

    ::::


    * **Per rule execution**: Create an alert each time the rule runs and an event meets its criteria.
    * **Per time period**: Create one alert for all qualifying events that occur within a specified time window, beginning from when an event first meets the rule criteria and creates the alert.

        For example, if a rule runs every 5 minutes but you don’t need alerts that frequently, you can set the suppression time period to a longer time, such as 1 hour. If the rule meets its criteria, it creates an alert at that time, and for the next hour, it’ll suppress any subsequent qualifying events.

        ![Alert suppression options](../../../images/serverless--detections-alert-suppression-options.png "")

3. Under **If a suppression field is missing**, choose how to handle events with missing suppression fields (events in which one or more of the **Suppress alerts by** fields don’t exist):

    ::::{admonition} NOTE
    :class: note

    These options are not available for threshold rules.

    ::::


    * **Suppress and group alerts for events with missing fields**: Create one alert for each group of events with missing fields. Missing fields get a `null` value, which is used to group and suppress alerts.
    * **Do not suppress alerts for events with missing fields**: Create a separate alert for each matching event. This basically falls back to normal alert creation for events with missing suppression fields.

4. Configure other rule settings, then save and enable the rule.

::::{admonition} Tips
:class: tip

* Use the **Rule preview** before saving the rule to visualize how alert suppression will affect the alerts created, based on historical data.
* If a rule times out while suppression is turned on, try shortening the rule’s [look-back](../../../solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule) time or turn off suppression to improve the rule’s performance.

::::



## Confirm suppressed alerts [security-alert-suppression-confirm-suppressed-alerts]

The {{security-app}} displays several indicators of whether a detection alert was created with alert suppression enabled, and how many duplicate alerts were suppressed.

::::{important}
After an alert is moved to the `Closed` status, it will no longer suppress new alerts. To prevent interruptions or unexpected changes in suppression, avoid closing alerts before the suppression interval ends.

::::


* **Alerts** table — Icon in the **Rule** column. Hover to display the number of suppressed alerts:

    ![Suppressed alerts icon and tooltip in Alerts table](../../../images/serverless--detections-suppressed-alerts-table.png "")

* **Alerts** table — Column for suppressed alerts count. Select **Fields** to open the fields browser, then add `kibana.alert.suppression.docs_count` to the table.

    ![Suppressed alerts count field column in Alerts table](../../../images/serverless--detections-suppressed-alerts-table-column.png "")

* Alert details flyout — **Insights** section:

    ![Suppressed alerts Insights section in alert details flyout](../../../images/serverless--detections-suppressed-alerts-details.png "")



## Investigate events for suppressed alerts [security-alert-suppression-investigate-events-for-suppressed-alerts]

With alert suppression, detection alerts aren’t created for the grouped source events, but you can still retrieve the events for further analysis or investigation. Do one of the following to open Timeline with the original events associated with both the created alert and the suppressed alerts:

* **Alerts** table — Select **Investigate in timeline** in the **Actions** column.

    ![Investigate in timeline button](../../../images/serverless--detections-timeline-button.png "")

* Alert details flyout — Select **Take action** → **Investigate in timeline**.


## Alert suppression limit by rule type [security-alert-suppression-alert-suppression-limit-by-rule-type]

Some rule types have a maximum number of alerts that can be suppressed (custom query rules don’t have a suppression limit):

* **Threshold, event correlation, {{esql}}, and {{ml}}:** The maximum number is the value you choose for the rule’s **Max alerts per run** [advanced setting](../../../solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params), which is `100` by default.
* **Indicator match and new terms:** The maximum number is five times the value you choose for the rule’s **Max alerts per run** [advanced setting](../../../solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params). The default value is `100`, which means the default maximum limit for indicator match rules and new terms rules is `500`.
