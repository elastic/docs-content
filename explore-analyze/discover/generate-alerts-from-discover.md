---
navigation_title: Create an alert rule
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Turn the query and filters of a Discover session into an alert rule that checks when your data goes above or below a threshold.
---

# Create an alert rule from Discover

From **Discover**, you can create a rule to periodically check when data goes above or below a certain threshold within a given time interval.

1. Ensure that your data view, query, and filters fetch the data for which you want an alert.
2. In the application menu, select **Create alert rule** (or **Alerts** in earlier versions), then select **Create search threshold rule**.

    The **Create rule** form is pre-filled with the latest query sent to {{es}}.

3. [Configure your query](../alerting/alerts/rule-type-es-query.md) and [select a connector type](../../deploy-manage/manage-connectors.md).
4. Select **Save**.

## Related pages

- [Create a {{alerting-v2-system}} rule from Discover](../alerting/esql/rules/create-rule-from-discover.md)
- [Alerting](../alerting/alerts.md)
