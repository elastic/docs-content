::::{tab-set}
:group: import-alert-source

:::{tab-item} Datadog
:sync: datadog

1. Set up a Datadog connector to receive events, then add a Datadog webhook to your monitors. Follow [Receive Datadog webhook events](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-events) and [Start a workflow from Datadog events](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-howto).
2. To test the setup, trigger a monitor or send a test from the Datadog webhook integration. The alert appears on the **Alerts** page.

You don't need to write a workflow. {{kib}} includes a [managed workflow](/explore-analyze/workflows/managed-workflows.md) called **Datadog alert translation**, which turns monitor webhooks from every Datadog connector into alerts. The workflow follows these rules.

- Each combination of monitor and scope gets its own alert. A monitor that fires for two hosts creates two alerts.
- A `Recovered` transition in Datadog closes the alert. Any other transition opens it or keeps it open.
- The alert has no severity. Datadog's priority is in the alert data, as `priority`.
:::

:::{tab-item} Other tools
:sync: other

Any tool that can send a webhook with a JSON body, such as Zabbix or PagerDuty, can send alerts to an Inbound Webhook connector. You write a workflow that turns the tool's payload into alerts.

1. Create an **Inbound Webhook** connector on the **{{connectors-ui}}** page, which you can open from the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Turn on **Receive events**, then save the connector.
2. Copy the **Webhook URL** and the **Ingest token**. {{kib}} shows the token only once. If you lose it, select **Rotate ingest token** to get a new one. The old token stops working right away.
3. Create a workflow that the connector's events trigger. In it, add an `alerting.create_alert` step that maps the tool's payload to alert fields, as in the example after these steps.
4. In the tool, send each alert as a POST request with a JSON body to the webhook URL. Add the ingest token in an `Authorization: Bearer <ingest-token>` header. If the tool can't set headers, append `?token=<ingest-token>` to the URL.

The following workflow handles a tool that sends one alert per request, with a body such as `{"id": "disk-web-1", "name": "Disk almost full", "state": "firing", "severity": "high", "url": "https://monitoring.example.com/alerts/disk-web-1"}`. Replace `<connector-id>` with the ID of your connector, which is the last part of the webhook URL.

```yaml
name: Import alerts from my monitoring tool
enabled: true
triggers:
  - type: inboundWebhook.received
    connector-id: "<connector-id>"
steps:
  - name: create_alert_from_webhook
    type: alerting.create_alert
    with:
      source: my-monitoring-tool
      fingerprint: "{{ event.body.id }}"
      alert_status: '{% if event.body.state == "resolved" %}inactive{% else %}active{% endif %}'
      severity: "{{ event.body.severity }}"
      data:
        rule_name: "{{ event.body.name }}"
        source_alert_url: "{{ event.body.url }}" # On Elastic Stack 9.6, name this field alert_url
```

The request body is available to the workflow as `event.body`. To run one workflow for every Inbound Webhook connector, set `connector-id` to `"*"`. If the tool sends several alerts in one request, loop over them with a [`foreach` step](/explore-analyze/workflows/steps/foreach.md).

When you map the payload, the following fields decide which alert an event updates, when that alert opens and closes, and how it appears.

Identity
:   The step identifies the alert by the first of these fields that the event includes: `fingerprint`, then `fingerprint_fields`, then `rule_id`. Each event needs at least one of them. `fingerprint_fields` lists field names under `data` whose values together identify the alert. The identity also includes `source` and the {{kib}} space, so the same fingerprint from two tools, or in two spaces, creates separate alerts. Choose a value that stays the same while one problem lasts, such as a check ID together with a host name. Otherwise, each update creates a new alert instead of updating the open one.

Lifecycle
:   An event with `alert_status: active` opens an alert, or updates the open alert that has the same identity. An event with `inactive` closes that alert. If the same identity becomes `active` again later, a new alert opens in the same [series](/explore-analyze/alerting/esql/alerts.md#series-overview). If you leave out `alert_status`, the step uses `active`.

Display
:   `source` names the tool and can't start with `elastic`. `severity` accepts `info`, `low`, `medium`, `high`, or `critical`, and the step fails on any other value, so map the tool's values when they differ. Put any other payload fields under `data`, up to 100 keys. `data.rule_name` is the alert's name in the alerts table. A URL in `data.source_alert_url` {applies_to}`{stack: preview 9.7+, serverless: preview}` or `data.alert_url` {applies_to}`stack: preview =9.6` adds a link back to the tool.
:::

::::
