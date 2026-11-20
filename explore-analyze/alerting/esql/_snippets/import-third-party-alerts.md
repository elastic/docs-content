% Include this snippet under a heading or page tagged stack: preview 9.6+ and serverless observability: preview.
% It has no heading of its own, and it doesn't list requirements, so the including page supplies both.

::::{tab-set}
:group: import-alert-source

:::{tab-item} Datadog
:sync: datadog

You don't need to write a workflow for Datadog. {{kib}} includes a [managed workflow](/explore-analyze/workflows/managed-workflows.md) called **Datadog alert translation**, which turns monitor webhooks from every Datadog connector into alerts.

1. Set up a Datadog connector to receive events, as described in [Receive Datadog webhook events](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-events).
2. In Datadog, create a webhook that sends monitor alerts to {{kib}}, then add it to your monitors, as described in [Create the Datadog webhook](kibana://reference/connectors-kibana/datadog-action-type.md#datadog-inbound-webhook).
3. To test the setup, trigger a monitor or send a test from the Datadog webhook integration. The alert appears on the [**Alerts** page](/explore-analyze/alerting/esql/alerts/view-and-manage-alerts.md).

The managed workflow follows these rules.

- Each combination of monitor and scope gets its own alert. A monitor that fires for two hosts creates two alerts.
- A `Recovered` transition in Datadog closes the alert. Any other transition opens it or keeps it open.
- The alert has no severity. Datadog's monitor priority is in the alert data, as `priority`.
:::

:::{tab-item} Other tools
:sync: other

Any tool that can send a webhook with a JSON body, such as Zabbix or PagerDuty, can send alerts to an Inbound Webhook connector. You write a workflow that turns each request into an alert.

1. Create an **Inbound Webhook** connector on the **{{connectors-ui}}** page, which you can open from the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). After you save it, {{kib}} shows the **Webhook URL** and the **Ingest token**.
2. Copy the webhook URL and the ingest token. {{kib}} shows the token only once. If you lose it, select **Rotate ingest token** to get a new one. The old token stops working right away.
3. [Create a workflow](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md) that the connector's events trigger, with an `alerting.create_alert` step that maps the tool's request body to alert fields. For example, a tool might send one alert per request with this body.

   ```json
   {
     "id": "disk-web-1",
     "name": "Disk almost full",
     "state": "firing",
     "severity": "high",
     "url": "https://monitoring.example.com/alerts/disk-web-1"
   }
   ```

   The following workflow turns each of those requests into an alert. Replace `<connector-id>` with the ID of your connector, which is the last part of the webhook URL.

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
           source_alert_url: "{{ event.body.url }}"
   ```

   {applies_to}`stack: preview =9.6` Name the URL field `alert_url` instead of `source_alert_url`.

   The workflow receives the request body as `event.body`. To run one workflow for every Inbound Webhook connector in the space, set `connector-id` to `"*"`. If the tool sends several alerts in one request, loop over them with a [`foreach` step](/explore-analyze/workflows/steps/foreach.md). The field descriptions after these steps explain how to map each field.
4. Configure the tool to send each alert as a `POST` request with a JSON body to the webhook URL. Add the ingest token in an `Authorization: Bearer <ingest-token>` header. If the tool can't set headers, append `?token=<ingest-token>` to the URL.
5. To test the setup, have the tool send an alert. The alert appears on the [**Alerts** page](/explore-analyze/alerting/esql/alerts/view-and-manage-alerts.md). If it doesn't, check the workflow's [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history) for a failed step.

The `alerting.create_alert` fields decide which alert each request updates, when that alert opens and closes, and how it appears.

Identity
:   The step uses `fingerprint` to identify the alert. If the event has no `fingerprint`, the step uses `fingerprint_fields`, a list of field names under `data` whose values together identify the alert. If neither is present, it uses `rule_id`. Each event needs at least one of the three.

    The identity also includes `source` and the {{kib}} space, so the same fingerprint from two tools, or in two spaces, creates separate alerts. Use a value that stays the same while one problem lasts, such as a check ID together with a host name. Otherwise, each update opens a new alert instead of updating the open one.

Lifecycle
:   An event with `alert_status: active` opens an alert or updates the open alert that has the same identity. An event with `alert_status: inactive` closes that alert. If the same identity becomes `active` again later, a new alert opens in the same series as the earlier ones. If you leave out `alert_status`, the step uses `active`. The step also accepts `pending` and `recovering`.

Display
:   `source` names the tool and can't start with `elastic`. Put any other request fields under `data`, up to 100 keys. `data.rule_name` is the alert's name in the alerts table.

    `severity` accepts `info`, `low`, `medium`, `high`, or `critical`. The step fails on any other value, including an empty one, so map the tool's values when they differ. If the tool doesn't always send a severity, add a Liquid `default` filter to the value.

    A URL in one of the following fields adds a link back to the tool.

    - {applies_to}`{stack: preview 9.7+, serverless: {observability: preview}}` `data.source_alert_url`
    - {applies_to}`stack: preview =9.6` `data.alert_url`
:::

::::
