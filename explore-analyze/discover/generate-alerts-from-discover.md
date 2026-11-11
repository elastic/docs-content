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

If you want to be notified when your data goes above or below a threshold within a time interval, turn the query and filters of a **Discover** session into an alert rule. The rule then checks your data on a schedule.

{applies_to}`observability: ga` {applies_to}`stack: ga 9.6+` In {{esql}} mode, **Discover** can also create a {{alerting-v2-system}} rule. This option appears when the **Universal Alerting** advanced setting is on, you work in a space with the Classic or Observability solution view, and your role can create {{alerting-v2-system}} rules. Refer to [Create a {{alerting-v2-system}} rule from Discover](../alerting/esql/rules/create-rule-from-discover.md).

## Before you begin

To create rules, you need a role that grants access to at least one rule type that **Discover** can create. If you don't have one, **Discover** hides the **Create alert rule** menu. To use **Create search threshold rule**, your role also needs access to rules in {{stack-manage-app}} and privileges for the {{es}} query rule type. For the privileges that rules need, refer to [Alerting security and privileges](../alerting/alerts/alerting-setup.md#alerting-security).

## Create the alert rule

1. Check that your data, query, and filters return the results you want an alert for.
2. In the application menu, select **Create alert rule** (or **Alerts** before 9.4), then select **Create search threshold rule**. If the {{data-source}} has no time field, this option is unavailable. In {{esql}} mode, a date field in the {{data-source}} is enough.

    The **Create rule** form is pre-filled with the latest query sent to {{es}}.

3. In the **Create rule** form, set the threshold and how often the rule runs. Refer to [{{es}} query rule](../alerting/alerts/rule-type-es-query.md).
4. Select the connector that sends the notification. Refer to [Connectors](../../deploy-manage/manage-connectors.md).
5. Select **Save**.

**Result:** The rule is saved and starts checking your data on its schedule.

## Next steps

- [Alerting](../alerting/alerts.md): Manage your rules and learn about the other rule types.

## Related pages

- [Create a {{alerting-v2-system}} rule from Discover](../alerting/esql/rules/create-rule-from-discover.md)
