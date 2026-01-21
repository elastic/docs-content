---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/alert-suppression.html
  - https://www.elastic.co/guide/en/serverless/current/security-alert-suppression.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Suppress detection alerts [security-alert-suppression]

Alert suppression allows you to reduce the number of repeated or duplicate detection alerts created by [detection rules](/solutions/security/detect-and-alert/about-detection-rules.md). Normally, when a rule meets its criteria repeatedly, it creates multiple alerts, one for each time the rule’s criteria are met. When alert suppression is configured, alerts for duplicate events are not created. Instead, the qualifying events are grouped, and only one alert is created for each group. 

Depending on the rule type, you can configure alert suppression to create alerts each time the rule runs, or once within a specified time window. You can also specify multiple fields to group events by unique combinations of values.

The {{security-app}} displays several indicators in the Alerts table and the alert details flyout when a detection alert is created with alert suppression enabled. You can view the original events associated with suppressed alerts by investigating the alert in Timeline.

## Configure alert suppression [security-alert-suppression-configure-alert-suppression]

::::{admonition} Requirements and notices
* To use alert suppression in {{stack}} and {{serverless-short}}, you must have the appropriate [subscription](https://www.elastic.co/pricing). 
* {{ml-cap}} rules have [additional requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md) for alert suppression.

::::

You can configure alert suppression when [creating](/solutions/security/detect-and-alert/create-detection-rule.md) or editing a rule.  

1. When configuring the rule (the **Define rule** step for a new rule, or the **Definition** tab for an existing rule), specify how you want to group alerts for alert suppression:

    * **All rule types except the threshold rule:** In **Suppress alerts by**, enter 1 or more field names to group alerts by the fields' values. The maximum limit of fields that you can enter is as follows:
       * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Enter up to 5 fields.
       * {applies_to}`stack: ga 9.0-9.1` Enter up to 3 fields.


    * **Threshold rule only:** In **Group by**, enter up to 3 field names to group events by the fields' values, or leave the setting empty to group all qualifying events together. 


    ::::{tip}
    
    Refer to [Suppression for fields with an array of values](/solutions/security/detect-and-alert/suppress-detection-alerts.md#security-alert-suppression-fields-with-multiple-values) to learn how fields with multiple values are handled.

    ::::


2. Choose how often to create alerts for qualifying events:

    * **Per rule execution**: Create an alert each time the rule runs and an event meets its criteria.
    * **Per time period**: Create one alert for all qualifying events that occur within a specified time window, beginning from when an event first meets the rule criteria and creates the alert. This is the only option available when configuring alert suppression for threshold rules.

        For example, if a rule runs every 5 minutes but you don’t need alerts that frequently, you can set the suppression time period to a longer time, such as 1 hour. If the rule meets its criteria, it creates an alert at that time, and for the next hour, it’ll suppress any subsequent qualifying events.

        :::{image} /solutions/images/security-alert-suppression-options.png
        :alt: Alert suppression options
        :width: 450px
        :::

3. Under **If a suppression field is missing**, choose how to handle events with missing suppression fields (events in which one or more of the **Suppress alerts by** fields don’t exist):

    ::::{note}
    These options are available for all rule types except threshold rules.
    ::::

    * **Suppress and group alerts for events with missing fields**: Create one alert for each group of events with missing fields. Missing fields get a `null` value, which is used to group and suppress alerts.
    * **Do not suppress alerts for events with missing fields**: Create a separate alert for each matching event. This basically falls back to normal alert creation for events with missing suppression fields.

4. Configure other rule settings, then save and enable the rule.

::::{tip}
* Use the **Rule preview** before saving the rule to visualize how alert suppression will affect the alerts created, based on historical data.
* If a rule times out while suppression is turned on, try shortening the rule’s [look-back](/solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule) time or turn off suppression to improve the rule’s performance.

::::


### Suppression for fields with an array of values [security-alert-suppression-fields-with-multiple-values]

When specifying fields to suppress alerts by, you can select fields that have multiple values. When alerts for those fields are generated, they're handled as follows:

* **Custom query or threshold rules:** Alerts are grouped by each unique value and an alert is created for each group. For example, if you suppress alerts by `destination.ip` of `[127.0.0.1, 127.0.0.2, 127.0.0.3]`, alerts are grouped separately for each value of `127.0.0.1`, `127.0.0.2`, and `127.0.0.3` and an alert is created for each group.

* **Indicator match, event correlation (non-sequence queries only), new terms, {{esql}}, or {{ml}} rules:** Alerts with identical array values are grouped together. For example, if you suppress alerts by `destination.ip` of `[127.0.0.1, 127.0.0.2, 127.0.0.3]`, alerts with the entire array are grouped and only one alert is created for the group.
           
* **Event correlation (sequence queries only) rules:** Alerts that are an exact match are grouped. To be an exact match, array values must be identical and in the same order. For example, if you specify the field `myips` and one sequence alert has `[1.1.1.1, 0.0.0.0]` and another sequence alert has `[1.1.1.1, 192.168.0.1]`, neither of those alerts is suppressed, despite sharing an array element.

## Confirm suppressed alerts [security-alert-suppression-confirm-suppressed-alerts]

The {{security-app}} displays several indicators of whether a detection alert was created with alert suppression enabled, and how many qualifying alerts were suppressed.

::::{important}
Changing an alert's status to `Closed` can affect suppression. Refer to [Impact of closing suppressed alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md#security-alert-suppression-impact-close-alerts) to learn more.
::::


* **Alerts** table — Icon in the **Rule** column. Hover to display the number of suppressed alerts:

    :::{image} /solutions/images/security-suppressed-alerts-table.png
    :alt: Suppressed alerts icon and tooltip in Alerts table
    :screenshot:
    :width: 650px
    :::

* **Alerts** table — Column for suppressed alerts count. Select **Fields** to open the fields browser, then add `kibana.alert.suppression.docs_count` to the table.

    :::{image} /solutions/images/security-suppressed-alerts-table-column.png
    :alt: Suppressed alerts count field column in Alerts table
    :screenshot:
    :width: 750px
    :::

* Alert details flyout — **Insights** → **Correlations** section:

    :::{image} /solutions/images/security-suppressed-alerts-details.png
    :alt: Suppressed alerts in the Correlations section within the alert details flyout
    :screenshot:
    :width: 450px
    :::


## Investigate events for suppressed alerts [security-alert-suppression-investigate-events-for-suppressed-alerts]

With alert suppression, detection alerts aren’t created for the grouped source events, but you can still retrieve the events for further analysis or investigation. Do one of the following to open Timeline with the original events associated with both the created alert and the suppressed alerts:

* **Alerts** table — Select **Investigate in timeline** in the **Actions** column.

    :::{image} /solutions/images/security-timeline-button.png
    :alt: Investigate in timeline button
    :width: 250px
    :screenshot:
    :::

* Alert details flyout — Select **Take action** → **Investigate in timeline**.


## Impact of closing suppressed alerts [security-alert-suppression-impact-close-alerts]

By default, if you close a suppressed alert while a suppression window is still active, suppression resets. Subsequently, any new qualifying alerts are suppressed and added to a new alert for suppression.

For example, say you set the suppression time period to 5 minutes and specify to group alerts by the `host.name` field. The first time an event meets the rule's criteria, an alert is created. Over the next 5 minutes, any subsequent qualifying alerts are suppressed and grouped by unique `host.name` value. If you close that first alert before the active suppression window ends (the 5 minute suppression time period), alert suppression stops and restarts when the next qualifying alert meets the suppression criteria. 


:::{image} /solutions/images/security-alert-suppression-close-alert-example.png
:alt: Example of suppression configuration for a rule
:screenshot:
:width: 450px
:::

{applies_to}`stack: ga 9.2` You can change the default behavior and continue suppressing alerts until the end of suppression window after you close an investigated alert. To do this, change the `securitySolution:suppressionBehaviorOnAlertClosure` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#suppression-window-behavior) to **Continue until suppression window ends**.

## Alert suppression limit by rule type [security-alert-suppression-alert-suppression-limit-by-rule-type]

Some rule types have a maximum number of alerts that can be suppressed (custom query rules don’t have a suppression limit):

* **Threshold, event correlation, {{esql}}, and {{ml}}:** The maximum number of alerts is the value you choose for the rule’s **Max alerts per run** [advanced setting](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params), which is `100` by default.
* **Indicator match and new terms:** The maximum number is five times the value you choose for the rule’s **Max alerts per run** [advanced setting](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params). The default value is `100`, which means the default maximum limit for indicator match rules and new terms rules is `500`.

## Bulk apply and remove alert suppression [security-alert-suppression-bulk-apply]

```{applies_to}
   stack: ga 9.1 
```

From the Rules table, use the **Bulk actions** menu to apply or remove alert suppression to multiple rules. The **Apply alert suppression** option can be used for all rules types except for the threshold rule type. To bulk-apply alert suppression to threshold rules, use the bulk menu option that's labeled for threshold rules only.