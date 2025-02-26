---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/automating-report-generation.html
---

# Automatically generate reports [automating-report-generation]

To automatically generate PDF and CSV reports, generate a POST URL, then submit the HTTP `POST` request using {{watcher}} or a script.


## Create a POST URL [create-a-post-url]

Create the POST URL that triggers a report to generate PDF and CSV reports.

To create the POST URL for PDF reports:

1. Go to **Dashboards**, **Visualize Library**, or **Canvas**.
2. Open the dashboard, visualization, or **Canvas** workpad you want to view as a report.

    * If you are using **Dashboard** or **Visualize Library**, from the toolbar, click **Share > Export**, select the PDF option then click **Copy POST URL**.
    * If you are using **Canvas**, from the toolbar, click **Share > PDF Reports**, then click **Advanced options > Copy POST URL**.


To create the POST URL for CSV reports:

1. Go to **Discover**.
2. Open the saved Discover session you want to share.
3. In the toolbar, click **Share > Export > Copy POST URL**.


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
3. The required `kbn-xsrf` header for all `POST` requests to {{kib}}. For more information, refer to [API Request Headers](https://www.elastic.co/guide/en/kibana/current/api.html#api-request-headers).
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

IMPORTANT: In earlier {{kib}} versions, you could use the `&sync` parameter to append to report URLs that held the request open until the document was fully generated. The `&sync` parameter is now unsupported. If you use the `&sync` parameter in Watcher, you must update the parameter.
