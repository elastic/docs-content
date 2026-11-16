---
description: Generate PDF, PNG, and CSV reports automatically, either on demand with a POST URL from a script or Watcher, or on a schedule in Kibana.
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/automating-report-generation.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Automatically generate reports [automating-report-generation]

Generate PDF, PNG, and CSV reports automatically instead of exporting them by hand each time. Available methods and export formats vary by deployment type. Use the approach that fits your workflow:

* {applies_to}`serverless: unavailable` **[Trigger reports with a POST URL](#trigger-reports-post-url)**: Generate a report on demand from a script or {{watcher}}.
* **[Schedule and share reports](#schedule-report-generation)**: Set up a recurring schedule in {{kib}} that generates and emails reports at an interval you choose.

## Trigger reports with a POST URL [trigger-reports-post-url]
```{applies_to}
serverless: unavailable
```

To generate a report on demand from outside {{kib}}, such as from a script or {{watcher}}, create a POST URL for the report and send a request to it. {{kib}} queues the report, and you download it when it's ready.

### Prerequisites [post-url-prerequisites]

To trigger reports with a POST URL, you need the following:

* A role with [access to reporting](../../deploy-manage/kibana-reporting-configuration.md#grant-user-access).
* For PDF and PNG reports, a {{kib}} instance with a minimum of 2 GB of RAM. CSV reports have no minimum requirement.
* {applies_to}`stack: ga 9.1+` (Optional) If you generate reports from remote clusters in a cross-cluster search environment, the appropriate cluster and index privileges on both the remote cluster and the local cluster. For example, the API key that authenticates your request needs certain privileges on the local cluster that contains the local index, in addition to the remote. For more information and examples, refer to [Configure privileges for cross-cluster search](/explore-analyze/cross-cluster-search.md#configure-privileges-for-ccs).

{applies_to}`stack: ga 9.1+` {{kib}} authenticates report generation requests with API keys instead of session cookies. API keys capture your role privileges, whereas session cookies are based on your user credentials. API keys are also longer-lived than session cookies.

### Create a POST URL [create-a-post-url]

Create the POST URL from the dashboard, visualization, workpad, or Discover session that you want to generate reports for. The steps depend on the report type.

#### PDF and PNG reports [pdf-png-post-url]

To create the POST URL for PDF and PNG reports:

1. Go to **Dashboards**, **Visualize Library**, or **Canvas**.
2. Open the dashboard, visualization, or **Canvas** workpad you want to view as a report. From the toolbar, do one of the following:

    * {applies_to}`stack: ga 9.1+` Select the **Export** icon, then **PDF** or **PNG**. In the export flyout, copy the POST URL.
    * {applies_to}`stack: ga =9.0` If you are using **Dashboard** or **Visualize Library**, select **Share** → **Export**, select the **PDF** or **PNG** option, then select **Copy POST URL**.
    * {applies_to}`stack: ga =9.0` If you are using **Canvas**, select **Share** → **PDF Reports**, then select **Advanced options** → **Copy POST URL**.

#### CSV reports [csv-post-url]

To create the POST URL for CSV reports:

1. Go to **Discover**.
2. Open the saved Discover session you want to share, so the POST URL keeps working. If the session has unsaved changes, the export flyout warns that the link might not be permanent.
3. Copy the POST URL:

    * {applies_to}`stack: ga 9.1+` Open the CSV export, as described in [Export Discover session results as CSV](/explore-analyze/discover/export-discover-session.md#export-discover-session-csv). In the export flyout, copy the POST URL.
    * {applies_to}`stack: ga =9.0` Select **Share** → **Export** → **Copy POST URL**.

### Use Watcher [use-watcher]

To configure a watch to email reports, use the `reporting` attachment type in an `email` action. {{watcher}} integrates with reporting only through this email attachment type. For more information, refer to [Configuring email accounts](../alerting/watcher/actions-email.md#configuring-email).

For example, the following watch generates a PDF report and emails the report every hour:

```console
PUT _watcher/watch/error_report
{
  "trigger" : {
    "schedule": {
      "interval": "1h"
    }
  },
  "actions" : {
    "email_admin" : { <1>
      "email": {
        "to": "'Recipient Name <recipient@example.com>'",
        "subject": "Error Monitoring Report",
        "attachments" : {
          "error_report.pdf" : {
            "reporting" : {
              "url": "http://example.org:5601/api/reporting/generate/printablePdfV2?jobParams=...", <2>
              "retries":40, <3>
              "interval":"15s", <4>
              "auth":{ <5>
                "basic":{
                  "username":"elastic",
                  "password":"changeme"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

1. Configure at least one email account to enable {{watcher}} to send email. For more information, refer to [Configuring email accounts](../alerting/watcher/actions-email.md#configuring-email).
2. An example POST URL. You can copy and paste the URL for any report.
3. Optional, default is `40`.
4. Optional, default is `15s`.
5. User credentials for a user with permission to access {{kib}} and the {{report-features}}. For more information, refer to [Configure reporting](../report-and-share.md).

::::{note}
The report generation URL might contain date-math expressions that cause the watch to fail with a `parse_exception`. To avoid a failed watch, remove curly braces `{` `}` from date-math expressions and URL-encode characters. For example, `...(range:(%27@timestamp%27:(gte:now-15m%2Fd,lte:now%2Fd))))...`

For more information about configuring watches, refer to [How Watcher works](../alerting/watcher/how-watcher-works.md).

::::

### Use a script [use-a-script]

To generate reports from a script, send a request to the POST URL. The response is JSON with a `path` property, which holds the relative URL for downloading the report. Send a `GET` request to that path to download the report.

To queue a CSV report with cURL:

```bash
curl \
-XPOST \ <1>
-u elastic \ <2>
-H 'kbn-xsrf: true' \ <3>
'http://example.org:5601/api/reporting/generate/csv_searchsource?jobParams=...' <4>
```

1. The required `POST` method.
2. The user credentials for a user with permission to access {{kib}} and {{report-features}}.
3. The required `kbn-xsrf` header for all `POST` requests to {{kib}}. For more information, refer to [API request headers]({{kib-apis}}).
4. The POST URL. You can copy and paste the URL for any report.

A successfully queued report returns a response like this:

```js
{
  "path": "/api/reporting/jobs/download/4c8a1f6e-7d3b-4a52-9e0c-1b2f3d4e5a6b", <1>
  "job": {
    "id": "4c8a1f6e-7d3b-4a52-9e0c-1b2f3d4e5a6b",
    "index": ".ds-.kibana-reporting-2025.11.11-000001",
    "jobtype": "csv_searchsource",
    "created_at": "2025-11-11T10:15:00.000Z",
    "created_by": "elastic",
    "meta": {
      "objectType": "search"
    },
    "status": "pending",
    "attempts": 0,
    "migration_version": "7.14.0",
    "space_id": "default",
    "payload": ..., <2>
    "output": {}
  }
}
```

1. The relative path on the {{kib}} host for downloading the report.
2. (Not included in the example) Internal representation of the reporting job, as stored in the `.kibana-reporting` data stream.

### HTTP response codes [reporting-response-codes]

The response to a request to generate a report includes the path for downloading the report. The download API returns HTTP response codes that external systems can use to track the job state:

* **`200` (OK)**: {{kib}} returns a `200` status for successful requests to queue or download reports. A `200` response to a request that queues a report doesn't mean that the report succeeds. Report generation runs asynchronously, so the job can still fail after it is queued.
* **`400` (Bad Request)**: When sending requests to the POST URL, if your request is missing the `kbn-xsrf` header, {{kib}} returns a `400` status response.
* **`405` (Method Not Allowed)**: If you send a `GET` request to the POST URL, {{kib}} returns a `405` status response. Use the `POST` method to queue a report.
* **`500` (Internal Server Error)**: When you request the download by using the `path`, you get a `500` status if the report isn't available because of an error during generation. For details, go to **Stack Management** → **Alerts and Insights** → **Reporting**.
* **`503` (Service Unavailable)**: When you request the download by using the `path`, you get a `503` status if report generation hasn't completed yet. The response includes a `Retry-After` header. Set your script to wait that number of seconds, and then retry until the report is complete.

### Deprecated report URLs [deprecated-report-urls]

{{kib}} 8.0 and earlier also accepted report URLs that used the ID of a saved object. {{kib}} no longer supports these deprecated report URLs. If a script or watch still uses one after an upgrade, replace it with a POST URL, as described in [Create a POST URL](#create-a-post-url). The deprecated URL formats were:

* **Dashboard** reports: `/api/reporting/generate/dashboard/<dashboard-id>`
* **Visualize Library** reports: `/api/reporting/generate/visualization/<visualization-id>`
* **Discover** reports: `/api/reporting/generate/search/<discover-session-id>`

Earlier {{kib}} versions also let you add the `&sync` parameter to a report URL to hold the request open until the document was fully generated. {{kib}} no longer supports `&sync`. If a watch still uses it, update the watch to stop using the parameter.

## Schedule and share reports [schedule-report-generation]

```{applies_to}
stack: ga 9.3+, preview 9.1-9.2
serverless: ga
```

Save time by setting up a recurring task that automatically generates reports and shares them on a schedule that you choose. Which report formats you can schedule depends on your deployment type:

* {applies_to}`serverless: ga` CSV reports for Discover sessions
* {applies_to}`stack: ga` CSV reports for Discover sessions, and PDF and PNG reports for dashboards and library visualizations

### Prerequisites [scheduled-reports-reqs]

* {applies_to}`serverless: unavailable` To generate PDF and PNG reports, your {{kib}} instance needs a minimum of 2 GB of RAM. There is no minimum requirement for CSV reports.
* To use the scheduled reports feature, your role needs [access to reporting](../../deploy-manage/kibana-reporting-configuration.md#grant-user-access).
* (Optional) To view and manage other users' reports and schedules, your role needs `All` privileges for the **Manage Scheduled Reports** feature. You can set this by configuring your role's {{kib}} privileges. To learn how, refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-feature-privileges), or to [{{kib}} privileges in project custom roles](/deploy-manage/users-roles/serverless-custom-roles.md#custom-roles-kib-privileges) for {{serverless-short}}. If your role doesn't have the **Manage Scheduled Reports** feature privilege, you can only share reports with yourself.
* {applies_to}`serverless: unavailable` (Optional) The **Manage Scheduled Reports** feature must be enabled in the [**Feature visibility** settings](/deploy-manage/manage-spaces.md#spaces-managing) of the space.
* Sharing reports outside of {{kib}} requires a default preconfigured email connector.

   * **{{ech}} or {{serverless-short}} users**: You don't need to set up a default preconfigured email connector. {{kib}} provides a built-in preconfigured email connector that uses SMTP to send emails. To view it, go to the **Connectors** page and find the `Elastic-Cloud-SMTP` connector.
   * **Self-managed users**: You must set up a default preconfigured email connector to send notifications outside of {{kib}}. To do this:

     1. Open your `kibana.yml` file.
     2. Add the `xpack.actions.preconfigured` {{kib}} setting. This setting specifies configuration details for the preconfigured connector that you're defining.
     3. Under the `xpack.actions.preconfigured` setting, define the email connector. Define it in `kibana.yml`, because you can't create a preconfigured email connector from the {{kib}} UI. Refer to [Email connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md#preconfigured-email-configuration) to learn about requirements for different email services and providers.
     4. Add the `notifications.connectors.default.email` {{kib}} setting, and provide the name of your email connector. The `notifications.connectors.default.email` setting specifies the default email connector to use when sending notifications. This is especially useful if you have multiple email connectors and want to set a default one.

     The following example shows a modified `kibana.yml` file with a preconfigured email connector that's set as the default connector for email notifications:

     ```yaml
     xpack.actions.preconfigured:
       my-email:
         name: preconfigured-email-connector-type
         actionTypeId: .email
         config:
           service: other
           from: sender@example.com
           host: smtp.example.com
           port: 8080
           secure: false
           hasAuth: true
         secrets:
           user: testuser
           password: passwordkeystorevalue

     notifications.connectors.default.email: my-email
     ```

* (Optional) To control who can receive email notifications from {{kib}}, add the [`xpack.actions.email.domain_allowlist` setting](kibana://reference/configuration-reference/alerting-settings.md) to your `kibana.yml` file. To learn more about configuring this setting, refer to [Notifications domain allowlist](../alerting/alerts/notifications-domain-allowlist.md).

### Create a schedule [create-scheduled-report]

1. Open the saved Discover session, dashboard, or visualization you want to share.
2. Look for the **Schedule export** action. In **Discover**, it's in the same menu as the CSV export action. In other apps, select the **Export** icon, then **Schedule export**.
3. Enter a **Report name** and select the **File type**. For PDF reports, you can turn on **Print format** to generate a multi-page report that shows at most two visualizations per page.
4. Set up a schedule for generating the report.

    * **Date**: Select when to start generating reports.
    * **Timezone**: Set the time zone for the schedule.
    * **Repeat**: Select how often to generate reports.

5. (Optional) To share generated reports outside of {{kib}}, turn on **Send by email** and enter a list of email addresses. Recipients receive emails with the generated reports attached, on the schedule that you set.

   {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3+` (Optional) Enter additional details for email notifications:

    * **Cc**: Enter one or more email addresses. Recipients get a copy of the report, are included on all replies, and can see the other recipients' addresses.
    * **Bcc**: Enter one or more email addresses. Recipients get a copy of the report, but aren't included on replies and can't see the other recipients' addresses.
    * **Subject**: Keep the default email subject, or enter your own.
    * **Message**: Keep the default email message, or enter your own. You can format the message with Markdown.

       ::::{note}
       In the subject and message, you can also use [Mustache](https://mustache.github.io/mustache.5.html) template syntax (`{{variable name}}`) to insert values from data sources when {{kib}} generates the email. You can also enhance the values that Mustache variables pass. Refer to [](../../explore-analyze/alerting/alerts/rule-action-variables.md#enhance-mustache-variables) to learn more.
       ::::

6. Select **Schedule exports** to save the schedule.

A message confirms that the schedule is available on the **Reporting** page. From the **Reporting** page, select the **Schedules** tab to view details for the newly created schedule.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.3+` From the **Schedules** tab, use the search field to find schedules.

### Download generated reports [download-scheduled-reports]

Each time a schedule runs, the generated report appears on the **Exports** tab of the **Reporting** page, with **Scheduled** in the **Export type** column. From there, you can download the report, whether or not you chose to send it by email. Disabling or deleting a schedule doesn't remove the reports that it already generated.

### Manage schedules [manage-report-schedules]

From the **Schedules** tab on the **Reporting** page, you can manage a schedule with these actions:

::::{applies-switch}

:::{applies-item} {serverless: ga, stack: ga 9.3+}
* **Disable schedule**: Stop a schedule from generating future reports, but keep a record of it on the **Reporting** page.
* **Enable schedule**: Restart a disabled schedule.
* **Edit schedule config**: Change the configuration of an existing schedule.
* **Delete schedule**: Permanently stop a schedule and remove its record from the **Reporting** page. You can't recover a deleted schedule.
:::

:::{applies-item} stack: ga 9.1-9.2
* **Disable schedule**: Permanently stop a schedule from generating reports, but keep a record of it on the **Reporting** page. To restart the schedule, create a new one.
:::

::::

### Scheduled reports limitations [scheduled-reports-limitations]

Scheduled reports are meant for analyzing data in external tools. They aren't intended for bulk export or for backing up {{es}} data. Keep the following limitations in mind:

* {{kib}} doesn't email reports that are larger than 10 MB, and the email service that you use can set a lower limit. The built-in email service on {{ech}} and {{serverless-short}} limits a message to 10 MB after Base64 encoding, which makes an attachment about one third larger. It can send reports of up to about 7 MB. For all limits, refer to [Email service limits](/deploy-manage/deploy/elastic-cloud/tools-apis.md#email-service-limits).

  When {{kib}} can't send the email, the report is still generated. You can download it from the **Exports** tab, where it shows the status **Done, warnings detected**.
* If you schedule too many reports at the same time, reports might be shared late or on an inconsistent schedule. Each {{kib}} instance runs one reporting task at a time.
* If your cluster runs many tasks in general, reports might be delayed.
* You can't schedule reports of Canvas workpads, because Canvas workpads are in maintenance mode.
* You can't schedule CSV reports of Lens visualizations.
* {applies_to}`serverless: ga` {{serverless-full}} supports scheduling only CSV exports of Discover sessions. Other formats and other applications aren't supported.
