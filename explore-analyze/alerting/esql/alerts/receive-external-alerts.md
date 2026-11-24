---
navigation_title: Receive external alerts
applies_to:
  serverless:
    observability: experimental
  stack: experimental 9.6+
products:
  - id: kibana
description: "Receive alerts from Datadog and other external monitoring tools in Kibana Universal Alerting with webhooks and workflows. The alerts appear on the Alerts page alongside alerts from rules."
---

# Receive alerts from external sources in {{alerting-v2-system}} [receive-external-alerts]

Send alerts from Datadog or another monitoring tool to the **Alerts** page, where you can triage them and include them in action policies like the alerts from your rules.

If you already monitor your services with another tool, you can keep its monitors and still work with their alerts in {{kib}}. For [Datadog](#receive-alerts-datadog), you set up a connector and a webhook, and a managed workflow creates the alerts. For [other tools](#receive-alerts-other-sources) that can send a JSON webhook, such as Zabbix, you also create the workflow that turns each request into an alert.

:::{note}
To receive alerts from external sources, your role needs the [privileges for external alerts](/explore-analyze/alerting/esql/manage/configure-access.md#alerting-external-alerts-privileges), and your subscription must include workflows. Refer to the subscriptions for [{{ecloud}}]({{subscriptions}}/cloud) and [self-managed]({{subscriptions}}) deployments.
:::

## Receive alerts from Datadog [receive-alerts-datadog]

The [managed workflow](/explore-analyze/workflows/managed-workflows.md) **Datadog alert translation** creates alerts from the monitor webhooks that Datadog connectors receive.

The managed workflow creates one alert for each monitor and scope, which is the group that triggered it, such as a host. A monitor that fires for two hosts creates two alerts. Transitions that start with `Recovered` close the alert, and every other transition opens it or keeps it open. The alerts have no severity, but their data includes the monitor's priority as `priority`.

To receive alerts from Datadog:

1. Set up a Datadog connector to [receive events](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-events).
2. In Datadog, [create a webhook](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-webhook) that sends monitor alerts to {{kib}}, then add it to your monitors.
3. To check the setup, trigger a monitor or send a test from the Datadog webhook integration. An alert appears on the **Alerts** page, with the title of the Datadog event in the **Rule** column. If no alert appears, [check the response](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-confirm) that Datadog received from {{kib}}.

After setup, {{kib}} creates or updates an alert each time Datadog sends one. You don't receive alerts that fired before you added the webhook.

## Receive alerts from other sources [receive-alerts-other-sources]

Any source that can send a webhook with a JSON body, such as Zabbix, can send alerts to an Inbound Webhook connector.

:::{include} /explore-analyze/alerting/esql/_snippets/receive-external-alerts.md
:::

## Stop receiving alerts [stop-receiving-alerts]

How you stop receiving alerts depends on the source:

- **Datadog**: Open the Datadog connector, turn off **Receive events**, and save. {{kib}} stops accepting Datadog's requests immediately, so the managed workflow and any other workflows that the connector starts stop running.
- **Other sources**: Turn off the workflow that the source's connector starts. To also reject the source's requests, delete the connector.

{applies_to}`{stack: experimental 9.6+, ess: unavailable, serverless: unavailable}` To stop receiving alerts from every source at once, set `xpack.actions.inboundEvents.enabled: false` in `kibana.yml` and restart {{kib}}. This turns off incoming requests for every connector, including connectors that start other workflows. For details about this setting, refer to [`xpack.actions.inboundEvents.enabled`](kibana://reference/configuration-reference/alerting-settings.md#xpack-actions-inboundevents-enabled).
