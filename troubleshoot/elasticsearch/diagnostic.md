---
navigation_title: Diagnostics
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnostic.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Capture {{es}} diagnostics [diagnostic]


The {{es}} [Support Diagnostic](https://github.com/elastic/support-diagnostics) tool captures a point-in-time snapshot of cluster statistics and most settings. It works against all {{es}} versions.

This information can be used to troubleshoot problems with your cluster. For examples of issues that you can troubleshoot using Support Diagnostic tool output, refer to [the Elastic blog](https://www.elastic.co/blog/why-does-elastic-support-keep-asking-for-diagnostic-files).

You can generate diagnostic information using this tool before you contact [Elastic Support](https://support.elastic.co) or [Elastic Discuss](https://discuss.elastic.co) to minimize turnaround time.

Watch [this video](https://www.youtube.com/watch?v=Bb6SaqhqYHw) for a walkthrough of capturing an {{es}} diagnostic.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::



## Requirements [diagnostic-tool-requirements]

* Java Runtime Environment or Java Development Kit v1.8 or higher


## Access the tool [diagnostic-tool-access]

The Support Diagnostic tool is included as a sub-library in some Elastic deployments:

* {{ece}}: Located under **{{ece}}** > **Deployment** > **Operations** > **Prepare Bundle** > **{{es}}**.
* {{eck}}: Run as [`eck-diagnostics`](/troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md).

You can also directly download the `diagnostics-X.X.X-dist.zip` file for the latest Support Diagnostic release from [the `support-diagnostic` repo](https://github.com/elastic/support-diagnostics/releases/latest).


## Capture diagnostic information [diagnostic-capture]

To capture an {{es}} diagnostic:

1. In a terminal, verify that your network and user permissions are sufficient to connect to your {{es}} cluster by polling the cluster’s [health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health).

    For example, with the parameters `host:localhost`, `port:9200`, and `username:elastic`, you’d use the following curl request:

    ```sh
    curl -X GET -k -u elastic -p https://localhost:9200/_cluster/health
    ```

    If you receive a an HTTP 200 `OK` response, then you can proceed to the next step. If you receive a different response code, then [diagnose the issue](#diagnostic-non-200) before proceeding.

2. Using the same environment parameters, run the diagnostic tool script.

    For information about the parameters that you can pass to the tool, refer to the [diagnostic parameter reference](https://github.com/elastic/support-diagnostics#standard-options).

    The following command options are recommended:

    **Unix-based systems**

    ```sh
    sudo ./diagnostics.sh --type local --host localhost --port 9200 -u elastic -p --bypassDiagVerify --ssl --noVerify
    ```

    **Windows**

    ```sh
    .\diagnostics.bat --type local --host localhost --port 9200 -u elastic -p --bypassDiagVerify --ssl --noVerify
    ```

    ::::{tip}

    You can execute the script in three [modes](https://github.com/elastic/support-diagnostics#diagnostic-types):

    * `local` (default, recommended): Polls the [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md), gathers operating system info, and captures cluster and GC logs.
    * `remote`: Establishes an ssh session to the applicable target server to pull the same information as `local`.
    * `api`: Polls the [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md). All other data must be collected manually.

    ::::

3. When the script has completed, verify that no errors were logged to `diagnostic.log`. If the log file contains errors, then refer to [Diagnose errors in `diagnostic.log`](#diagnostic-log-errors).
4. If the script completed without errors, then an archive with the format `<diagnostic type>-diagnostics-<DateTimeStamp>.zip` is created in the working directory, or an output directory you have specified. You can review or share the diagnostic archive as needed.


## Diagnose a non-200 cluster health response [diagnostic-non-200]

When you poll your cluster health, if you receive any response other than `200 0K`, then the diagnostic tool might not work as intended. The following are possible error codes and their resolutions:

HTTP 401 `UNAUTHENTICATED`
:   Additional information in the error will usually indicate either that your `username:password` pair is invalid, or that your `.security` index is unavailable and you need to setup a temporary [file-based realm](../../deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md) user with `role:superuser` to authenticate.

HTTP 403 `UNAUTHORIZED`
:   Your `username` is recognized but has insufficient permissions to run the diagnostic. Either use a different username or elevate the user’s privileges.

HTTP 429 `TOO_MANY_REQUESTS` (for example, `circuit_breaking_exception`)
:   Your username authenticated and authorized, but the cluster is under sufficiently high strain that it’s not responding to API calls. These responses are usually intermittent. You can proceed with running the diagnostic, but the diagnostic results might be incomplete.

HTTP 504 `BAD_GATEWAY`
:   Your network is experiencing issues reaching the cluster. You might be using a proxy or firewall. Consider running the diagnostic tool from a different location, confirming your port, or using an IP instead of a URL domain.

HTTP 503 `SERVICE_UNAVAILABLE` (for example, `master_not_discovered_exception`)
:   Your cluster does not currently have an elected master node, which is required for it to be API-responsive. This might be temporary while the master node rotates. If the issue persists, then [investigate the cause](../../deploy-manage/distributed-architecture/discovery-cluster-formation/cluster-fault-detection.md) before proceeding.


## Diagnose errors in `diagnostic.log` [diagnostic-log-errors]

The following are common errors that you might encounter when running the diagnostic tool:

* `Error: Could not find or load main class com.elastic.support.diagnostics.DiagnosticApp`

    This indicates that you accidentally downloaded the source code file instead of `diagnostics-X.X.X-dist.zip` from the releases page.

* `Could not retrieve the {{es}} version due to a system or network error - unable to continue.`

    This indicates that the diagnostic couldn’t run commands against the cluster. Poll the cluster’s health again, and ensure that you’re using the same parameters when you run the dianostic batch or shell file.

* A `security_exception` that includes `is unauthorized for user`:

    The provided user has insufficient admin permissions to run the diagnostic tool. Use another user, or grant the user `role:superuser` privileges.
