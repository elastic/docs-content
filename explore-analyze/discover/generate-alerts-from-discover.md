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

If you want to be notified when your data goes above or below a certain threshold within a given time interval, you can turn the query and filters of a **Discover** session into an alert rule. The rule then checks the data periodically.

## Before you begin

You need a role that lets you create rules. **Discover** shows the **Create alert rule** menu only if your role grants access to at least one rule type that **Discover** can create. For the privileges that rules need, refer to [Security](../alerting/alerts/alerting-setup.md#alerting-security).

## Create the alert rule

1. Check that your data, query, and filters return the results you want an alert for.
2. In the application menu, select **Create alert rule** (or **Alerts** in earlier versions), then select **Create search threshold rule**.

    The **Create rule** form is pre-filled with the latest query sent to {{es}}.

3. [Configure your query](../alerting/alerts/rule-type-es-query.md) and [select a connector type](../../deploy-manage/manage-connectors.md).
4. Select **Save**.

## Related pages

- [Create a {{alerting-v2-system}} rule from Discover](../alerting/esql/rules/create-rule-from-discover.md)
- [Alerting](../alerting/alerts.md)
