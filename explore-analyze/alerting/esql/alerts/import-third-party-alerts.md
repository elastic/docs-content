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

For Datadog, you set up a [Datadog connector](kibana://reference/connectors-kibana/datadog-action-type.md), and Elastic provides a [managed workflow](/explore-analyze/workflows/managed-workflows.md) that creates the alerts. For any other tool that can send a webhook, you set up an Inbound Webhook connector and write a short workflow that turns each request from the tool into an alert.

## Before you begin [import-third-party-alerts-requirements]

Make sure that your role has the [privileges to import alerts](/explore-analyze/alerting/esql/manage/configure-access.md#alerting-import-privileges) and that your deployment or project meets the [license and project requirements](/explore-analyze/alerting/esql/setup.md#alerting-setup-requirements). On {{stack}}, you also need the following settings:

- {applies_to}`stack: experimental 9.6+` [`server.publicBaseUrl`](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) set in `kibana.yml` to a URL that the tool can reach. If it isn't set, {{kib}} shows a relative webhook URL that external tools can't use.
- {applies_to}`stack: experimental 9.6+` `xpack.actions.inboundEvents.enabled` left at its default, `true`. If it's `false`, connectors can't receive events.

## Import alerts from Datadog [import-alerts-datadog]

Elastic provides a [managed workflow](/explore-analyze/workflows/managed-workflows.md) called **Datadog alert translation** that turns monitor webhooks from every Datadog connector into alerts, so you don't need to write your own.

The managed workflow follows these rules:

- Each combination of monitor and scope gets its own alert. A monitor that fires for two hosts creates two alerts.
- A `Recovered` transition in Datadog closes the alert. Any other transition opens it or keeps it open.
- The alert has no severity. Datadog's monitor priority is in the alert data, as `priority`.

To import alerts from Datadog:

1. Set up a Datadog connector to receive events, as described in [Receive Datadog webhook events](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-events).
2. In Datadog, create a webhook that sends monitor alerts to {{kib}}, then add it to your monitors, as described in [Create the Datadog webhook](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-webhook).
3. To check the setup, trigger a monitor or send a test from the Datadog webhook integration. An alert named after the title of the Datadog event appears on the [**Alerts** page](/explore-analyze/alerting/esql/alerts/view-and-manage-alerts.md). If no alert appears, check the response that Datadog received from {{kib}}, as described in [Confirm that Datadog calls {{kib}}](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-confirm).

After that, the import runs on its own. Each time a monitor that uses the webhook changes state, Datadog notifies {{kib}}, and the managed workflow opens, updates, or closes the matching alert. The import doesn't include alerts that fired before you added the webhook.

Imported Datadog alerts appear on the **Alerts** page with the alerts from your rules. To open the page, go to **Alerting** → **Alerts** in the {{observability}} navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

% TODO: PMs need to provide why analysts and SREs look for imported alerts. Use the reason to open the next paragraph with the reader's goal.

To find Datadog alerts among your other alerts, look for `datadog` in the **Source** column.

{applies_to}`{serverless: {observability: experimental}, stack: experimental 9.7+}` To list only Datadog alerts, filter the page by **Source** and select `datadog`.

% Unconfirmed: To view an alert in Datadog, open its details flyout and select **View in source system**. 

To stop importing alerts from Datadog, open the connector, turn off **Receive events**, and save. The webhook URL stops working right away, and workflows subscribed to the connector stop receiving events. The connector's outbound actions keep working.

:::{include} /explore-analyze/alerting/esql/_snippets/import-third-party-alerts.md
:::

## Stop importing alerts from every tool [stop-importing-alerts]

```yaml {applies_to}
stack: experimental 9.6+
```

Set `xpack.actions.inboundEvents.enabled: false` in `kibana.yml` and restart {{kib}}. Connectors then no longer accept incoming events from any tool.
