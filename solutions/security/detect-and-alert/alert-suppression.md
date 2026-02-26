---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/alert-suppression.html
  - https://www.elastic.co/guide/en/serverless/current/security-alert-suppression.html
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Use alert suppression to reduce duplicate detection alerts by grouping qualifying events and creating a single alert per group.
---

# Suppress detection alerts [security-alert-suppression]

When a detection rule runs, it can generate many alerts for similar events—sometimes hundreds of near-identical alerts for the same threat. Alert suppression helps you cut through this noise by grouping related events and creating a single representative alert instead of one alert per event.

::::{admonition} Requirements
* Alert suppression requires the appropriate [subscription](https://www.elastic.co/pricing) for {{stack}} and {{serverless-short}}.
* {{ml-cap}} rules have [additional requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md) for alert suppression.
::::

## When to use alert suppression

Alert suppression is useful when:

* A rule generates too many alerts for the same activity (for example, repeated failed login attempts from the same IP address)
* You want to focus analyst attention on unique threats rather than duplicates
* You need to reduce alert volume without weakening your detection coverage

Alert suppression doesn't ignore events—it groups them. You can still investigate all the original events associated with a suppressed alert.


## How alert suppression works

Without suppression, a rule creates one alert for every event that matches its criteria. With suppression enabled:

1. You specify one or more fields to group events by (for example, `host.name` or `source.ip`).
2. When multiple events share the same field values, they're grouped together.
3. Instead of creating separate alerts for each event, the rule creates one alert per group.
4. For some rule types, you can also control *how often* alerts are created:
   * **Per rule execution**: A new alert is created each time the rule runs (if matching events exist).
   * **Per time period**: One alert is created for all matching events within a time window you specify.


## Configure alert suppression [security-alert-suppression-configure-alert-suppression]

You can configure alert suppression when [creating](/solutions/security/detect-and-alert/using-the-rule-builder.md) or editing a rule.

::::::{stepper}

::::{step} Choose fields to group by
When configuring the rule (the **Define rule** step for a new rule, or the **Definition** tab for an existing rule), specify how you want to group alerts:

:::{dropdown} For all rule types except threshold rules
In **Suppress alerts by**, enter one or more field names to group alerts by. Events with the same values for these fields are grouped together.

* {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` You can enter up to 5 fields.
* {applies_to}`stack: ga 9.0-9.1` You can enter up to 3 fields.

For {{esql}} rules, fields created in the {{esql}} query (for example, with the `EVAL` command) are available to select in **Suppress alerts by**.
:::

:::{dropdown} For threshold rules only
In **Group by**, enter up to 3 field names to group events by, or leave the setting empty to group all qualifying events together.
:::

:::{tip}
If you're suppressing by fields that contain arrays, refer to [Suppression for fields with an array of values](#security-alert-suppression-fields-with-multiple-values) for details on how different rule types handle them.
:::
::::

::::{step} Choose suppression frequency
Choose how often to create alerts for qualifying events:

* **Per rule execution**: Create an alert each time the rule runs and finds matching events.
* **Per time period**: Create one alert for all matching events that occur within a specified time window. The window starts when an event first matches and creates an alert.

    For example, if a rule runs every 5 minutes but you don't need alerts that frequently, you can set the suppression time period to 1 hour. The rule creates an alert when it first matches, then suppresses any subsequent matching events for the next hour.

   :::{note}
   **Per time period** is the only option available for threshold rules.
   :::

::::

::::{step} Handle missing fields
Under **If a suppression field is missing**, choose how to handle events where one or more suppression fields don't exist:

* **Suppress and group alerts for events with missing fields**: Treat missing fields as having a `null` value. Events with missing fields are grouped together and suppressed.
* **Do not suppress alerts for events with missing fields**: Create a separate alert for each event with missing fields. This falls back to normal alert behavior for those events.

:::{note}
These options are available for all rule types except threshold rules.
:::
::::

::::{step} Save and enable the rule
Configure any other rule settings, then save and enable the rule.

:::{tip}
* Use the **Rule preview** before saving to visualize how alert suppression will affect alerts based on historical data.
* If a rule times out while suppression is enabled, try shortening the rule's [look-back](/solutions/security/detect-and-alert/common-rule-settings.md#rule-schedule) time or turning off suppression to improve performance.
:::
::::

::::::


## Suppression for fields with an array of values [security-alert-suppression-fields-with-multiple-values]

When you suppress alerts by fields that contain multiple values (arrays), the behavior depends on the rule type:

| Rule type | Behavior |
|-----------|----------|
| Custom query or threshold | Alerts are grouped by each unique value separately. For example, if `destination.ip` contains `[127.0.0.1, 127.0.0.2, 127.0.0.3]`, three separate alert groups are created—one for each IP address. |
| Indicator match, event correlation (non-sequence), new terms, {{esql}}, or {{ml}} | Alerts with identical arrays are grouped together. The entire array must match exactly. |
| Event correlation (sequence queries) | Alerts are grouped only if arrays are an exact match *and* in the same order. For example, `[1.1.1.1, 0.0.0.0]` and `[1.1.1.1, 192.168.0.1]` are not grouped together, even though they share an element. |


## Confirm suppressed alerts [security-alert-suppression-confirm-suppressed-alerts]

The {{security-app}} shows several indicators when an alert was created with suppression enabled.

::::{important}
Closing a suppressed alert can affect suppression behavior. Refer to [Impact of closing suppressed alerts](#security-alert-suppression-impact-close-alerts) for details.
::::

### Alerts table

- **Icon in the Rule column**: Hover over the icon to see the number of suppressed alerts.

   :::{image} /solutions/images/security-suppressed-alerts-table.png
   :alt: Suppressed alerts icon and tooltip in Alerts table
   :screenshot:
   :width: 650px
   :::

- **Suppressed alerts count column**: Select **Fields** to open the fields browser, then add `kibana.alert.suppression.docs_count` to the table.

   :::{image} /solutions/images/security-suppressed-alerts-table-column.png
   :alt: Suppressed alerts count field column in Alerts table
   :screenshot:
   :width: 750px
   :::

### Alert details flyout

Open the **Insights** → **Correlations** section to see suppression details.

:::{image} /solutions/images/security-suppressed-alerts-details.png
:alt: Suppressed alerts in the Correlations section within the alert details flyout
:screenshot:
:width: 450px
:::


## Investigate events for suppressed alerts [security-alert-suppression-investigate-events-for-suppressed-alerts]

Even though suppressed events don't generate their own alerts, you can still access the original events for analysis. Open Timeline with all the events associated with a suppressed alert using one of these methods:

* Alerts table— select **Investigate in timeline** in the **Actions** column.
* Alert details flyout— select **Take action > Investigate in timeline**.


## Impact of closing suppressed alerts [security-alert-suppression-impact-close-alerts]

By default, closing a suppressed alert while the suppression window is still active resets suppression. The next qualifying event starts a new suppression window and creates a new alert.

For example, say you set suppression to 5 minutes, grouped by `host.name`. When an event matches, an alert is created. For the next 5 minutes, matching events are suppressed and grouped with that alert. If you close the alert before the 5-minute window ends, suppression stops. The next matching event creates a new alert and starts a new 5-minute window.

{applies_to}`stack: ga 9.2` You can change this default behavior to continue suppressing alerts until the suppression window ends, even after you close the alert. To do this, change the `securitySolution:suppressionBehaviorOnAlertClosure` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#suppression-window-behavior) to **Continue until suppression window ends**.


## Alert suppression limits [security-alert-suppression-alert-suppression-limit-by-rule-type]

Some rule types limit the number of alerts that can be suppressed. Custom query rules have no suppression limit.

| Rule type | Maximum suppressed alerts |
|-----------|---------------------------|
| Threshold, event correlation, {{esql}}, and {{ml}} | Equal to the rule's **Max alerts per run** [advanced setting](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) (default: `100`) |
| Indicator match and new terms | Five times the rule's **Max alerts per run** setting (default: `500`) |


## Bulk apply or remove alert suppression [security-alert-suppression-bulk-apply]

```{applies_to}
stack: ga 9.1
```

You can apply or remove alert suppression from multiple rules at once using the **Bulk actions** menu in the Rules table.

* For most rule types, use the **Apply alert suppression** option.
* For threshold rules, use the bulk menu option labeled specifically for threshold rules.