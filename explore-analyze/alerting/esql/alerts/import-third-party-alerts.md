---
navigation_title: Import third-party alerts
applies_to:
  stack: preview 9.6+
  serverless:
    observability: preview
products:
  - id: kibana
description: "Import alerts from Datadog and other third-party monitoring tools into Kibana Universal Alerting with webhooks and workflows. Imported alerts appear on the Alerts page alongside alerts from rules."
---

# Import third-party alerts into {{alerting-v2-system}} [import-third-party-alerts]

{{alerting-v2-system}} can import alerts from your other monitoring tools, so you can review them in one place with the alerts that your rules create. Each imported alert opens, updates, and closes as the tool reports changes.

For Datadog, you set up a Datadog connector, and {{kib}} provides the workflow that creates the alerts. For any other tool that can send a webhook, you set up an Inbound Webhook connector and write a short workflow that maps the tool's payload to alert fields.

## Before you begin [import-third-party-alerts-requirements]

To import alerts, you need the following.

- **Actions and Connectors: All** (under **Management**) to create the connector.
- For a tool other than Datadog, the privileges to create a workflow, as described in [](/explore-analyze/workflows/get-started/setup.md).
- **Alerts: All** (under **Universal Alerting**) for the last user to save the connector. Workflows that the connector starts run as that user, and creating an alert needs the same privilege as the [alert triage actions](/explore-analyze/alerting/esql/manage/configure-access.md#alerting-triage-privileges).
- {applies_to}`stack: preview 9.6+` An Enterprise license. Workflows and the Datadog connector both require it.
- {applies_to}`observability: preview` An {{obs-serverless}} Complete project. Logs Essentials projects don't include workflows.
- {applies_to}`stack: preview 9.6+` [`server.publicBaseUrl`](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) set in `kibana.yml` to a URL that the tool can reach. If it isn't set, {{kib}} shows a relative webhook URL that external tools can't use.
- {applies_to}`stack: preview 9.6+` `xpack.actions.inboundEvents.enabled` left at its default, `true`. If it's `false`, connectors can't receive events.

## Import alerts [import-third-party-alerts-steps]

:::{include} /explore-analyze/alerting/esql/_snippets/import-third-party-alerts.md
:::

## Find imported alerts [find-imported-alerts]

Imported alerts appear on the **Alerts** page with your other alerts. To open it, go to **Alerting** → **Alerts** in the {{observability}} navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

When an imported alert includes a URL to the tool, the alert details flyout shows **Alert URL**. To open the alert in the tool, select **View in source system**. Only URLs that start with `http://` or `https://` become links.

To learn what else the **Alerts** page shows, go to [](view-and-manage-alerts.md).

## Stop importing alerts [stop-importing-alerts]

How you stop importing alerts from one tool depends on its connector.

- **Datadog:** Open the connector, turn off **Receive events**, and save. The webhook URL stops working right away, and workflows subscribed to the connector stop receiving events. The connector's outbound actions keep working.
- **Inbound Webhook:** Turn off the workflow that the connector triggers. {{kib}} still accepts the tool's requests but creates no alerts. To have {{kib}} reject the requests too, delete the connector.

{applies_to}`stack: preview 9.6+` To stop importing alerts from every tool, set `xpack.actions.inboundEvents.enabled: false` in `kibana.yml` and restart {{kib}}. Connectors then no longer accept incoming events.

## Related pages [import-third-party-alerts-related]

- [Datadog connector](kibana://reference/connectors-kibana/datadog-action-type.md): Set up the Datadog side of the webhook and test it with a sample event.
- [](/explore-analyze/workflows/triggers/event-driven-triggers.md): Start workflows from events in {{kib}}.
- [](/explore-analyze/alerting/esql/alerts.md): Learn how alerts move through their lifecycle.
