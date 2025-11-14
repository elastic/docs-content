---
navigation_title: Generate alerts from Discover
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html#alert-from-Discover
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Create alerting rules from Discover searches to monitor data conditions. Get notified when values exceed thresholds or match specific criteria in your data.
---

# Create alerts from Discover searches [alert-from-Discover]

Create alerting rules directly from **Discover** to monitor your data automatically. Set up rules that check your data at regular intervals and send notifications when values exceed thresholds, match specific conditions, or deviate from expected patterns.

## Prerequisites

* You must have the appropriate privileges to create rules. Refer to [Alerting setup](../alerts-cases/alerts/alerting-setup.md).
* Your query should be tested and refined to return the data you want to monitor.

## Create a search threshold rule

1. In **Discover**, ensure that your {{data-source}}, query, and filters fetch the data for which you want an alert.
2. Test your search to confirm it returns the expected results.
3. In the application menu bar, click **Alerts > Create search threshold rule**.

   The **Create rule** form opens, pre-filled with the latest query sent to {{es}}.

4. [Configure your query](../alerts-cases/alerts/rule-type-es-query.md) by setting:
   * **Threshold conditions**: Define when the alert should fire (for example, when the count is above, below, or between certain values)
   * **Time window**: Specify the time interval to check (for example, last 5 minutes)
   * **Check frequency**: How often to run the query (for example, every 1 minute)

5. [Select a connector type](../../deploy-manage/manage-connectors.md) to determine how you'll be notified when the rule fires. Options include:
   * Email
   * Slack
   * PagerDuty
   * {{webhook}}
   * Other notification methods

6. Configure the action details for your chosen connector.
7. Click **Save** to create the rule.

The rule now runs in the background at the specified frequency, checking your data against the threshold conditions you defined.

## Manage your rules

After creating a rule from **Discover**, you can manage it in the {{rules-ui}} interface:

1. Go to **{{stack-manage-app}} > Alerts and Insights > {{rules-ui}}**.
2. Find your rule in the list.
3. Click on it to view details, edit conditions, or disable/enable it.

You can also view the history of when the rule fired and what actions were taken.

## Usage example

Suppose you're monitoring application logs and want to be alerted when error rates spike:

1. In **Discover**, create a query that filters for error-level logs:
   ```
   log.level : "error" AND service.name : "checkout"
   ```

2. Click **Alerts > Create search threshold rule**.
3. Configure the threshold to fire when the count is above 50 in the last 5 minutes.
4. Set it to check every 1 minute.
5. Configure an email or Slack connector to notify your team.
6. Save the rule.

Now your team will be notified whenever the checkout service logs more than 50 errors in a 5-minute window.

## Learn more

* [Alerting](../alerts-cases/alerts.md) - Complete guide to {{alert-features}}
* [{{es}} query rule](../alerts-cases/alerts/rule-type-es-query.md) - Detailed configuration options
* [{{connectors-ui}}](../../deploy-manage/manage-connectors.md) - Available notification methods

