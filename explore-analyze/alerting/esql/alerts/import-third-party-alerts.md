---
navigation_title: Import third-party alerts
applies_to:
  serverless:
    observability: experimental
  stack: experimental 9.6+
products:
  - id: kibana
description: "Import alerts from Datadog and other third-party monitoring tools into Kibana Universal Alerting with webhooks and workflows. Imported alerts appear on the Alerts page alongside alerts from rules."
---

# Import third-party alerts into {{alerting-v2-system}} [import-third-party-alerts]

{{alerting-v2-system-short}} can import alerts from your other monitoring tools, so you can review them in one place with the alerts that your rules create. Each imported alert opens, updates, and closes as the tool reports changes.

:::{note}
To import third-party alerts, your role needs the [import privileges](/explore-analyze/alerting/esql/manage/configure-access.md#alerting-import-privileges), and your subscription must include workflows. Refer to the subscriptions for [{{ecloud}}]({{subscriptions}}/cloud) and [self-managed]({{subscriptions}}) deployments.
:::

## Import alerts from Datadog [import-alerts-datadog]

The [managed workflow](/explore-analyze/workflows/managed-workflows.md) **Datadog alert translation** creates alerts from the monitor webhooks that Datadog connectors receive.

The managed workflow creates one alert for each monitor and scope, which is the group that triggered it, such as a host. A monitor that fires for two hosts creates two alerts. Transitions that start with `Recovered` close the alert, and every other transition opens it or keeps it open. The alerts have no severity, but their data includes the monitor's priority as `priority`.

To import alerts from Datadog:

1. Set up a Datadog connector to [receive events](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-events).
2. In Datadog, [create a webhook](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-webhook) that sends monitor alerts to {{kib}}, then add it to your monitors.
3. To check the setup, trigger a monitor or send a test from the Datadog webhook integration. An alert named after the title of the Datadog event appears on the **Alerts** page. If no alert appears, [check the response](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-confirm) that Datadog received from {{kib}}.

After setup, the import runs on its own. It doesn't include alerts that fired before you added the webhook.

## Import alerts from other tools [import-alerts-other-tools]

Any tool that can send a webhook with a JSON body, such as Zabbix, can send alerts to an Inbound Webhook connector.

:::{include} /explore-analyze/alerting/esql/_snippets/import-third-party-alerts.md
:::

## Stop importing alerts [stop-importing-alerts]

How you stop importing alerts depends on the tool:

- **Datadog**: Open the Datadog connector, turn off **Receive events**, and save. {{kib}} stops accepting Datadog's requests immediately, so the managed workflow and any other workflows that the connector starts stop running.
- **Other tools**: Turn off the workflow that the tool's connector starts. To also reject the tool's requests, delete the connector.

{applies_to}`{stack: experimental 9.6+, ess: unavailable, serverless: unavailable}` To stop importing alerts from every tool at once, set `xpack.actions.inboundEvents.enabled: false` in `kibana.yml` and restart {{kib}}. This turns off incoming requests for every connector, including connectors that start other workflows.
% For details about this setting, refer to [`xpack.actions.inboundEvents.enabled`](kibana://reference/configuration-reference/alerting-settings.md#xpack-actions-inboundevents-enabled)
