% Steps to import alerts into Universal Alerting from any tool that can send a webhook.

1. Create an **Inbound Webhook** connector. When you save it, {{kib}} generates a **Webhook URL** and an **Ingest token** for the connector and shows them in the flyout. Copy both before you close the flyout, because {{kib}} doesn't show the token again. If you lose the token, open the connector and select **Rotate ingest token** to get a new one.
   % For instructions, refer to [](kibana://reference/connectors-kibana/inbound-webhook-action-type.md)
2. Open **Workflows** from the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). If you already have workflows, select **Create workflow**. Then select **Start manually** to open the editor with a sample workflow.

3. Replace the sample workflow with the following one:

   ```yaml
   name: Import alerts from my monitoring tool
   enabled: true
   triggers:
     - type: inboundWebhook.received
       connector-id: "<connector-id>" <1>
   steps:
     - name: create_alert_from_webhook
       type: alerting.create_alert
       with:
         source: "<tool-name>" <2>
         fingerprint: "{{ event.body.<alert-id-field> }}" <3>
         alert_status: '{% if event.body.<status-field> == "<resolved-value>" %}inactive{% else %}active{% endif %}' <4>
         severity: "{{ event.body.<severity-field> | default: 'info' }}" <5>
         data:
           rule_name: "{{ event.body.<name-field> }}" <6>
           source_alert_url: "{{ event.body.<url-field> }}" <7>
   ```

   The `inboundWebhook.received` trigger runs this workflow for each request that your connector receives, and the `alerting.create_alert` step turns each request into an alert. Replace each placeholder, such as `<connector-id>`, with a value from your connector or your tool, as the following annotations describe:

   1. Replace `<connector-id>` with the value in your connector's **Connector ID** field. You can also remove `"<connector-id>"`, press {kbd}`ctrl+space`, and select the connector from the list. To run the workflow for every Inbound Webhook connector in the space, select **All connectors of this type** from that list, which sets the value to `"*"`.
   2. Replace `<tool-name>` with a name for your tool, such as `zabbix`. The name appears in the **Source** column on the **Alerts** page and can't start with `elastic`.
   3. Replace `<alert-id-field>` with the field that identifies the alert. Requests with the same `fingerprint` update the same alert, so use a field whose value stays the same while a problem lasts. If no single field identifies the alert, replace `fingerprint` with `fingerprint_fields`, a list of fields in `data` whose values together identify it. The step also accepts `rule_id`, the tool's own rule ID, as a last resort. It fails if you set none of the three. Alerts from different tools or spaces stay separate, even when their fingerprints match.
   4. Replace `<status-field>` with the field that holds the alert's state, and `<resolved-value>` with the value that marks the problem as resolved. `active` opens the alert, or updates it if it's already open, and `inactive` closes it. If the tool reports the problem again after the alert closes, a new alert opens. If you leave out `alert_status`, the step uses `active`. The step also accepts `pending` and `recovering`.
   5. Replace `<severity-field>` with the field that holds the alert's severity. The value must be `info`, `low`, `medium`, `high`, or `critical`. Any other value, including an empty one, makes the step fail, so map the tool's values when they differ. The `default` filter sets `info` when the request has no severity. If the tool never sends one, remove this line.
   6. Replace `<name-field>` with the field that holds the alert's name, which appears on the **Alerts** page. You can also add other fields from the request to `data`, up to 100 fields in total.
   7. Replace `<url-field>` with the field that holds a link to the alert in the tool. In the alert's details flyout, **View in source system** opens this link, so you can go straight to the alert in the tool. The link works only for URLs that start with `http://` or `https://`. If the tool doesn't send a link, remove this line.

      {applies_to}`stack: experimental =9.6` For **View in source system** to appear, name the field in this line `alert_url` instead of `source_alert_url`.

   The workflow reads each field in the tool's request body as `event.body.<field>`, so look at a request from your tool to find the field names. For example, a tool might send this body:

   ```json
   {
     "id": "disk-web-1",
     "name": "Disk almost full",
     "state": "firing",
     "severity": "high",
     "url": "https://monitoring.example.com/alerts/disk-web-1"
   }
   ```

   For that body, `<alert-id-field>` is `id`, `<status-field>` is `state`, `<severity-field>` is `severity`, `<name-field>` is `name`, and `<url-field>` is `url`. `<resolved-value>` is the value of `state` that marks the problem as resolved, such as `resolved`. If the tool sends several alerts in one request, use a [`foreach` step](/explore-analyze/workflows/steps/foreach.md) to create an alert for each one.

4. Select **Save**. The workflow sets `enabled: true`, so it runs for each request as soon as you save it.
5. In the tool's webhook settings, enter these values:

   - **URL**: The **Webhook URL** that you copied in step 1.
   - **Method**: Use `POST`.
   - **Body**: The alert as JSON, with a `Content-Type: application/json` header.
   - **Authentication**: An `Authorization: Bearer <ingest-token>` header, where `<ingest-token>` is the **Ingest token** that you copied from the connector in step 1. If the tool can't set headers, add `?token=<ingest-token>` to the end of the URL instead. Prefer the header, because URLs and logs can expose the token.

   Protect the ingest token like a password. Anyone who has it can start the connector's workflows.
6. To check that the connector and the workflow work, have the tool send an alert. Then open the workflow and select **Executions** to see its [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history). Each request that {{kib}} accepts starts a run:

   - If the run succeeded, the alert is on the [**Alerts** page](/explore-analyze/alerting/esql/alerts/view-and-manage-alerts.md).
   - If the run failed, open it to find the step that failed and why.
   - If no run appears, check the HTTP status that the tool received. A `202` status means that {{kib}} accepted the request, so make sure that the workflow is enabled, is in the same space as the connector, and has your connector's ID in `connector-id`. A `404` status means that {{kib}} rejected the URL or the ingest token.
   % For every status code, refer to [Troubleshoot webhook requests](kibana://reference/connectors-kibana/inbound-webhook-action-type.md#inbound-webhook-troubleshoot)
