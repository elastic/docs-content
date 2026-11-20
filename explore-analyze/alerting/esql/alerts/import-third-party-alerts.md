---
navigation_title: Import third-party alerts
applies_to:
  stack: preview 9.6+
  serverless:
    observability: preview
products:
  - id: kibana
description: "Show alerts from Datadog and other monitoring tools on the Kibana Universal Alerting Alerts page. Each tool sends its alerts to a Kibana webhook, and a workflow turns them into alerts."
---

# Import third-party alerts into {{alerting-v2-system}} [import-third-party-alerts]

{{alerting-v2-system}} can show alerts from your other monitoring tools on the **Alerts** page, next to the alerts that your rules create. Each tool sends its alerts to a {{kib}} webhook URL, and a workflow turns each request into an alert that opens, updates, and closes as the tool reports changes.

Datadog works without a workflow to write. For any other tool that can send a webhook, you write a short workflow that maps the tool's payload to alert fields.

## Before you begin [import-third-party-alerts-requirements]

- Privileges to create connectors, and the workflow privileges described in [Set up Workflows](/explore-analyze/workflows/get-started/setup.md).
- **Alerts: All** under **Universal Alerting** for the user who saves the connector. Workflows that the connector starts run as that user, and creating an alert needs the same privilege as [triaging one](/explore-analyze/alerting/esql/manage/configure-access.md#alerting-triage-privileges).
- {applies_to}`stack: preview 9.6+` An Enterprise license for the Datadog connector, or a Gold license or higher for the Inbound Webhook connector.
- {applies_to}`stack: preview 9.6+` `server.publicBaseUrl` set in `kibana.yml` to a URL that the tool can reach. If it isn't set, {{kib}} shows a relative webhook URL that external tools can't use.
- {applies_to}`stack: preview 9.6+` `xpack.actions.inboundEvents.enabled` left at its default, `true`. If it's `false`, connectors don't show the **Receive events** option.

## Import alerts [import-third-party-alerts-steps]

:::{include} /explore-analyze/alerting/esql/_snippets/import-third-party-alerts.md
:::

## Find imported alerts [find-imported-alerts]

Imported alerts appear on the **Alerts** page with your other alerts. To open it, go to **Alerting** → **Alerts** in the {{observability}} navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

When an imported alert includes a URL to the tool, its details show **Alert URL**. Select **View in source system** to open the alert in the tool. Only URLs that start with `http://` or `https://` become links.

For working with alerts on this page, refer to [View and manage alerts](view-and-manage-alerts.md).

## Stop importing alerts [stop-importing-alerts]

To stop importing alerts from one tool, open its connector, turn off **Receive events**, and save. The webhook URL stops working right away, and workflows subscribed to the connector stop receiving events. The connector's outbound actions keep working.

{applies_to}`stack: preview 9.6+` To stop importing alerts from every tool, set `xpack.actions.inboundEvents.enabled: false` in `kibana.yml` and restart {{kib}}. Connectors then no longer accept or offer incoming events.

## Related pages [import-third-party-alerts-related]

- [Datadog connector](kibana://reference/connectors-kibana/datadog-action-type.md): Set up the Datadog side of the webhook and test it with a sample event.
- [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md): Start workflows from events in {{kib}}.
- [Alerts in {{alerting-v2-system}}](/explore-analyze/alerting/esql/alerts.md): How alerts move through their lifecycle and belong to a series.
