---
navigation_title: Diagnostics
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-diagnostic.html
applies_to:
  deployment:
    ess: all
    ece: all
    self: all
    eck: all
products:
  - id: kibana
---



# Capture {{kib}} diagnostics [kibana-diagnostic]


The {{kib}} [Support Diagnostic](https://github.com/elastic/support-diagnostics) tool captures a point-in-time snapshot of {{kib}} and its Task Manager health. It works on {{kib}} versions 7.11.0 and above.

You can use the information captured by the tool to troubleshoot problems with {{kib}} instances. Check the [Troubleshooting Kibana Health blog](https://www.elastic.co/blog/troubleshooting-kibana-health) for examples.

You can generate diagnostic information using this tool before you contact [Elastic Support](https://support.elastic.co) or [Elastic Discuss](https://discuss.elastic.co) to help get a timely answer.

See this [this video](https://www.youtube.com/watch?v=t0J32qBKlIU) for a walkthrough of capturing a {{kib}} diagnostic.

## Requirements [kibana-diagnostic-tool-requirements]

* Java Runtime Environment or Java Development Kit v1.8 or higher.


## Access the tool [kibana-diagnostic-tool-access]

The Support Diagnostic tool is included out-of-the-box as a sub-library in:

* {{ece}} - Find the tool under **{{ece}}** > **Deployment** > **Operations** > **Prepare Bundle** > **{{kib}}**.
* {{eck}} - Run the tool with [`eck-diagnostics`](/troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md).

You can also get the latest version of the tool by downloading the `diagnostics-X.X.X-dist.zip` file from [the `support-diagnostic` repo](https://github.com/elastic/support-diagnostics/releases/latest).


## Capture diagnostic information [kibana-diagnostic-capture]

To run a {{kib}} diagnostic:

1. In a terminal, verify that your network and user permissions are sufficient to connect by polling {{kib}}'s [Task Manager health](https://www.elastic.co/docs/api/doc/kibana/operation/operation-task-manager-health).

    For example, with the parameters `host:localhost`, `port:5601`, and `username:elastic`, you’d use the following curl request. Adapt these parameters to your context.

    ```sh
    curl -X GET -k -H 'kbn-xsrf: true' -u elastic -p https://localhost:5601/api/task_manager/_health
    ```

    If you receive an HTTP 200 `OK` response, you can proceed to the next step. If you receive a different response code, you must [diagnose the issue](#kibana-diagnostic-non-200) before proceeding.

2. Using the same environment parameters, run the diagnostic tool script.

    For information about the parameters that you can pass to the tool, refer to the [diagnostic parameter reference](https://github.com/elastic/support-diagnostics#standard-options).

    The following command options are recommended:

    **Unix-based systems**

    ```sh
    sudo ./diagnostics.sh --type kibana-local --host localhost --port 5601 -u elastic -p --bypassDiagVerify --ssl --noVerify
    ```

    **Windows**

    ```sh
    .\diagnostics.bat --type kibana-local --host localhost --port 5601 -u elastic -p --bypassDiagVerify --ssl --noVerify
    ```

    ::::{tip}

    You can execute the script in three [modes](https://github.com/elastic/support-diagnostics#diagnostic-types):

    * `kibana-local` (default, recommended): Polls the [{{kib}} API](https://www.elastic.co/docs/api/doc/kibana/), gathers operating system info, and captures cluster and garbage collection (GC) logs.
    * `kibana-remote`: Establishes an SSH session to the applicable target server to pull the same information as `kibana-local`.
    * `kibana-api`: Polls the [{{kib}} API](https://www.elastic.co/docs/api/doc/kibana/). All other data must be collected manually.

    ::::

3. When the script has completed, verify that no errors were logged to `diagnostic.log`. If the log file contains errors, refer to [Diagnose errors in `diagnostic.log`](#kibana-diagnostic-log-errors).
4. If the script completed without errors, an archive with the format `<diagnostic type>-diagnostics-<DateTimeStamp>.zip` is created in the working directory or the output directory that you have specified. You can review or share the diagnostic archive as needed.


## Diagnose a non-200 response [kibana-diagnostic-non-200]

When you poll your Task Manager health, if you receive any response other than `200 0K`, then the diagnostic tool might not work as intended. Check the possible resolutions based on the error code that you get:

HTTP 401 `UNAUTHENTICATED`
:   Additional information in the error will usually indicate that your `username:password` pair is invalid, or that your {{es}} `.security` index is unavailable and you need to setup a temporary {{es}} [file-based realm](../../deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md) user with `role:superuser` to authenticate.

HTTP 403 `UNAUTHORIZED`
:   Your `username` is recognized but has insufficient permissions to run the diagnostic. Either use a different username or increase the user’s privileges.

HTTP 429 `TOO_MANY_REQUESTS` (for example, `circuit_breaking_exception`)
:   The authentication and authorization were successful, but the {{es}} cluster isn’t responding to requests. This issue is usually intermittent and can happen when the cluster is overwhelmed. In this case, resolve {{es}}'s health first before returning to {{kib}}.

HTTP 504 `BAD_GATEWAY`
:   Your network has trouble reaching {{kib}}. You might be using a proxy or firewall. Consider running the diagnostic tool from a different location, confirming your port, or using an IP instead of a URL domain.


## Diagnose errors in `diagnostic.log` [kibana-diagnostic-log-errors]

The following are common errors that you might encounter when running the diagnostic tool:

* `Error: Could not find or load main class com.elastic.support.diagnostics.DiagnosticApp`

    This indicates that you accidentally downloaded the source code file instead of `diagnostics-X.X.X-dist.zip` from the releases page.

* A `security_exception` that includes `is unauthorized for user`:

    The provided user has insufficient admin permissions to run the diagnostic tool. Use another user, or grant the user `role:superuser` privileges.

* `Kibana Server is not Ready yet`

    This indicates issues with {{kib}}'s dependencies blocking full start-up. To investigate, check [Error: {{kib}} server is not ready yet](/troubleshoot/kibana/error-server-not-ready.md).
