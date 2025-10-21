---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/automating-report-generation.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Automatically generate reports [automating-report-generation]

To automatically generate PDF and CSV reports, generate a POST URL, then submit an HTTP `POST` request using {{watcher}} or a script. In {{stack}} 9.1 and Serverless, you can use {{kib}} to generate reports on a recurring schedule and share them with a list of emails that you specify.

:::{note}
:applies_to: {stack: ga, serverless: unavailable}
API keys are used to authenticate requests to generate reports. If you have a cross-cluster search environment and want to generate reports from remote clusters, you must have the appropriate cluster and index privileges on the remote cluster and local cluster. For example, if requests are authenticated with an API key, the API key requires certain privileges on the local cluster that contains the leader index, instead of the remote. For more information and examples, refer to [Configure roles and users for remote clusters](../../deploy-manage/remote-clusters/remote-clusters-cert.md#remote-clusters-privileges-cert).
:::

## Create a POST URL [create-a-post-url]

Create the POST URL that triggers a report to generate PDF and CSV reports.

### PDF and PNG reports [pdf-png-post-url]

To create the POST URL for PDF reports:

1. Go to **Dashboards**, **Visualize Library**, or **Canvas**.
2. Open the dashboard, visualization, or **Canvas** workpad you want to view as a report. From the toolbar, do one of the following:

    * {applies_to}`stack: ga 9.0` If you are using **Dashboard** or **Visualize Library**, click **Share > Export**, select the PDF or PNG option, then click **Copy POST URL**.
    * {applies_to}`stack: ga 9.0` If you are using **Canvas**, click **Share > PDF Reports**, then click **Advanced options > Copy POST URL**.
    * {applies_to}`stack: ga 9.1` Click the **Export** icon, then **PDF** or **PNG**. In the export flyout, copy the POST URL.

### CSV reports [csv-post-url]

To create the POST URL for CSV reports:

1. Go to **Discover**.
2. Open the saved Discover session you want to share.
3. In the toolbar, do one of the following:
  
   * {applies_to}`stack: ga 9.0` Click **Share > Export > Copy POST URL**.
   * {applies_to}`stack: ga 9.1` Click the **Export** icon, then **CSV**. In the export flyout, copy the POST URL.


## Use Watcher [use-watcher]

To configure a watch to email reports, use the `reporting` attachment type in an `email` action. For more information, refer to [Configuring email accounts](../alerts-cases/watcher/actions-email.md#configuring-email).

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
              "url": "http://0.0.0.0:5601/api/reporting/generate/printablePdfV2?jobParams=...", <2>
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

1. Configure at least one email account to enable Watcher to send email. For more information, refer to [Configuring email accounts](../alerts-cases/watcher/actions-email.md#configuring-email).
2. An example POST URL. You can copy and paste the URL for any report.
3. Optional, default is `40`.
4. Optional, default is `15s`.
5. User credentials for a user with permission to access {{kib}} and the {{report-features}}. For more information, refer to [Configure reporting](../report-and-share.md).


::::{note}
**Reporting** is integrated with Watcher only as an email attachment type.

The report generation URL might contain date-math expressions that cause the watch to fail with a `parse_exception`. To avoid a failed watch, remove curly braces `{`  `}` from date-math expressions and URL-encode characters. For example, `...(range:(%27@timestamp%27:(gte:now-15m%2Fd,lte:now%2Fd))))...`

For more information about configuring watches, refer to [How Watcher works](../alerts-cases/watcher/how-watcher-works.md).

::::



## Use a script [use-a-script]

To automatically generate reports from a script, make a request to the `POST` URL. The request returns a JSON and contains a `path` property with a URL that you use to download the report. Use the `GET` method in the HTTP request to download the report.

To queue CSV report generation using the `POST` URL with cURL:

```bash
curl \
-XPOST \ <1>
-u elastic \ <2>
-H 'kbn-xsrf: true' \ <3>
'http://0.0.0.0:5601/api/reporting/generate/csv?jobParams=...' <4>
```

1. The required `POST` method.
2. The user credentials for a user with permission to access {{kib}} and {{report-features}}.
3. The required `kbn-xsrf` header for all `POST` requests to {{kib}}. For more information, refer to [API Request Headers](https://www.elastic.co/docs/api/doc/kibana/).
4. The POST URL. You can copy and paste the URL for any report.


An example response for a successfully queued report:

```js
{
  "path": "/api/reporting/jobs/download/jxzaofkc0ykpf4062305t068", <1>
  "job": {
    "id": "jxzaofkc0ykpf4062305t068",
    "index": ".reporting-2018.11.11",
    "jobtype": "csv",
    "created_by": "elastic",
    "payload": ..., <2>
    "timeout": 120000,
    "max_attempts": 3
  }
}
```

1. The relative path on the {{kib}} host for downloading the report.
2. (Not included in the example) Internal representation of the reporting job, as found in the `.reporting-*` storage.



## HTTP response codes [reporting-response-codes]

The response payload of a request to generate a report includes the path to download a report. The API to download a report uses HTTP response codes to give feedback. In automation, this helps external systems track the various possible job states:

* **`200` (OK)**: As expected, Kibana returns `200` status in the response for successful requests to queue or download reports.

  ::::{note}
  Kibana will send a `200` response status for successfully queuing a Reporting job via the POST URL. This is true even if the job somehow fails later, since report generation happens asynchronously from queuing.
  ::::

* **`400` (Bad Request)**: When sending requests to the POST URL, if you don’t use `POST` as the HTTP method, or if your request is missing the `kbn-xsrf` header, Kibana will return a code `400` status response for the request.
* **`503` (Service Unavailable)**: When using the `path` to request the download, you will get a `503` status response if report generation hasn’t completed yet. The response will include a `Retry-After` header. You can set the script to wait the number of seconds in the `Retry-After` header, and then repeat if needed, until the report is complete.
* **`500` (Internal Server Error)**: When using the `path` to request the download, you will get a `500` status response if the report isn’t available due to an error when generating the report. More information is available at **Management > Kibana > Reporting**.


## Deprecated report URLs [deprecated-report-urls]

If you experience issues with the deprecated report URLs after you upgrade {{kib}}, regenerate the POST URL for your reports.

* **Dashboard** reports:  `/api/reporting/generate/dashboard/<dashboard-id>`
* **Visualize Library** reports:  `/api/reporting/generate/visualization/<visualization-id>`
* **Discover** reports: `/api/reporting/generate/search/<discover-session-id>`

:::{important}
In earlier {{kib}} versions, you could use the `&sync` parameter to append to report URLs that held the request open until the document was fully generated. The `&sync` parameter is now unsupported. If you use the `&sync` parameter in Watcher, you must update the parameter.
:::

## Schedule and share reports [schedule-report-generation]

```{applies_to}
stack: preview 9.1
serverless: preview
```

Save time by setting up a recurring task that automatically generates reports and shares them on a schedule that you choose. 

### Prerequisites [scheduled-reports-reqs]

* To generate PDF and PNG reports, your {{kib}} instance needs a minimum of 2GB of RAM. There is no minimum requirement for CSV reports.
* To use the scheduled reports feature, your role needs [access to reporting](../../deploy-manage/kibana-reporting-configuration.md#grant-user-access).
* (Optional) To view and manage other users’ reports and schedules, your role needs `All` privileges for the **Manage Scheduled Reports** feature. You can set this by configuring your role's {{kib}} privileges. If your role doesn't have the **Manage Scheduled Reporting** feature privilege, you can only share reports with yourself. 
* Sharing reports outside of {{kib}} requires a default preconfigured email connector.

   * **{{ech}} or {{serverless-short}} users**: You do not need to set up a default preconfigured email connector. Kibana provides you with a built-in preconfigured email connector that uses the SMTP protocol to send emails. To view it, go to the **Connectors** page and find the Elastic-Cloud-SMTP connector.
   * **Self-managed users**: You must set up a default preconfigured email connector to send notifications outside of {{kib}}. To do this:
     
     1. Open your `kibana.yml` file.
     2. Add the `xpack.actions.preconfigured` {{kib}} setting. This setting specifies configuration details for the preconfigured connector that you're defining. 
     3. Under the `xpack.actions.preconfigured` setting, define the email connector. Refer to [Email connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md#preconfigured-email-configuration) to learn about requirements for different email services and providers.

         :::{note} 
         You must define preconfigured email connector details in the `kibana.yml` file. You cannot create a preconfigured email connector from the {{kib}} UI. 
         :::

     4. Add the `notifications.connectors.default.email` {{kib}} setting, and provide the name of your email connector. The `notifications.connectors.default.email` setting specifies the default email connector to use when sending notifications. This is especially useful if you have multiple email connectors and want to set a default one. 

     The following example shows a modified `kibana.yml` file with a preconfigured email connector that's set as the default connector for email notifications:

      ```
        xpack.actions.preconfigured:
          my-email:
            name: preconfigured-email-connector-type
            actionTypeId: .email
            config:
              service: other
              from: testsender@test.com
              host: validhostname
              port: 8080
              secure: false
              hasAuth: true
            secrets:
              user: testuser
              password: passwordkeystorevalue

        notifications.connectors.default.email: my-email
     ```

* (Optional) To control who can receive email notifications from {{kib}}, add the [`xpack.actions.email.domain_allowlist` setting](kibana://reference/configuration-reference/alerting-settings.md) to your `kibana.yml` file. To learn more about configuring this setting, refer to [Notifications domain allowlist](../alerts-cases/alerts/notifications-domain-allowlist.md).

### Create a schedule [create-scheduled-report]

1. Open the saved Discover session, dashboard, or visualization you want to share. 
2. Click the **Export** icon, then **Schedule export**.
3. Enter the requested details, and (optional) enable **Print format** to generate the report in a printer-friendly format.
4. Set up a schedule for generating the report.

    * **Date**: Choose when to start generating reports.
    * **Timezone**: Specify a timezone for the schedule.
    * **Repeat**: Choose how often you want to generate reports.  

5. (Optional) To share generated reports outside of Kibana, enable **Send by email** and enter a list of email addresses. Recipients will receive emails with the generated reports attached and on the schedule that you specified.

   ::::{note} 
   If your role doesn't have the **Manage Scheduled Reporting** feature privilege, you can only send reports to yourself. 
   ::::

6. Click **Schedule exports** to save the schedule. 

A message appears, indicating that the schedule is available on the **Reporting** page. From the **Reporting** page, click on the **Schedules** tab to view details for the newly-created schedule. 

::::{important} 
Note that you cannot edit or delete a schedule after you create it. To stop the schedule from running, you must disable it. Disabling a schedule permanently stops it from running. To restart it, you must create a new schedule. 
::::

### Scheduled reports limitations [scheduled-reports-limitations]

The feature enables analysis of data in external tools, but it is not intended for bulk export or to backup Elasticsearch data. Issues with report generation and sharing are likely to happen in the following scenarios:

* The limit for email attachments is 10 MB. {{kib}} might fail to attach reports that are larger than this size.
* Scheduling too many reports at the same time might cause reports to be shared late or at an inconsistent schedule. {{kib}} Task Manager runs reporting tasks one at a time.
* If your cluster is running many tasks in general, reports may be delayed.
* Scheduling reports of Canvas workpads is not supported since Canvas workpads are in maintenance mode. 
* Scheduling CSV reports of Lens visualizations is not supported. 