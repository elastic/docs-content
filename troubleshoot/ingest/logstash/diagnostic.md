---
navigation_title: Diagnostics
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: logstash
---

# Capture {{ls}} diagnostics [diagnostic]

The {{ls}} [Support Diagnostic](https://github.com/elastic/support-diagnostics) tool captures a point-in-time snapshot of its statistics and most settings. It works against all {{ls}} versions.

This information can be used to troubleshoot problems with your data pipeline. For examples of issues that you can troubleshoot using Support Diagnostic tool output, refer to [the Elastic blog](https://www.elastic.co/blog/why-does-elastic-support-keep-asking-for-diagnostic-files).

You can generate diagnostic information using this tool before you contact [Elastic Support](https://support.elastic.co) or [Elastic Discuss](https://discuss.elastic.co) to minimize turnaround time.

See this [this video](https://www.youtube.com/watch?v=0a1I5yPmoOk) for a walkthrough of capturing a {{ls}} diagnostic.

## Requirements [diagnostic-tool-requirements]

* Java Runtime Environment or Java Development Kit v1.8 or higher


## Access the tool [diagnostic-tool-access]

You can directly download the `diagnostics-X.X.X-dist.zip` file for the latest Support Diagnostic release from [the `support-diagnostic` repo](https://github.com/elastic/support-diagnostics/releases/latest).


## Capture diagnostic information [diagnostic-capture]

To capture a {{ls}} diagnostic:

1. In a terminal, verify that your network access is sufficient to connect to your {{ls}} node by polling its root endpoint.

    For example, with [the parameters](https://www.elastic.co/docs/reference/logstash/logstash-settings-file) `api.http.host: 127.0.0.1` and `api.http.port: 9600` without authentication (default), you’d use the following curl request:

    ```sh
    curl -X GET -k http://127.0.0.1:9600?pretty
    ```

    If you receive a an HTTP 200 `OK` response, you can proceed to the next step. If you receive a different response code, [diagnose the issue](#diagnostic-non-200) before proceeding.

2. Using the same environment parameters, run the diagnostic tool script.

    For information about the parameters that you can pass to the tool, refer to the [diagnostic parameter reference](https://github.com/elastic/support-diagnostics#standard-options).

    The following command options are recommended:

    * Unix-based systems

        ```sh
        sudo ./diagnostics.sh --type logstash-local --host 127.0.0.1 --port 9600 --bypassDiagVerify
        ```
        
    *  Windows

        ```sh
        .\diagnostics.bat --type logstash-local --host 127.0.0.1 --port 9600 --bypassDiagVerify
        ```

    ::::{tip}
  
    You can run the script in three [modes](https://github.com/elastic/support-diagnostics#diagnostic-types):
  
    * `local` (default, recommended): Polls the [{{ls}} API](https://www.elastic.co/docs/api/doc/logstash/), gathers operating system info, and captures node logs.
    * `remote`: Establishes an ssh session to the applicable target server to pull the same information as `local`.
    * `api`: Polls the [{{ls}} API](https://www.elastic.co/docs/api/doc/logstash/). All other data must be collected manually.
  
    ::::

3. When the script has completed, verify that no errors were logged to `diagnostic.log`. If the log file contains errors, refer to [Diagnose errors in `diagnostic.log`](#diagnostic-log-errors).

4. If the script completed without errors, an archive with the format `<diagnostic type>-diagnostics-<DateTimeStamp>.zip` is created in the working directory, or an output directory you have specified. You can review or share the diagnostic archive as needed.


## Diagnose a non-200 node response [diagnostic-non-200]

When you poll your node, if you receive any response other than `200 0K`, the diagnostic tool might not work as intended. The following are possible error codes and their resolutions:

HTTP 401 `UNAUTHENTICATED`
:   Your team has setup [{{ls}} API Security](https://www.elastic.co/docs/reference/logstash/monitoring-logstash#monitoring-api-security) and one/both of your `api.auth.basic.username` or `api.auth.basic.password` pair is invalid.

HTTP 504 `BAD_GATEWAY`
:   Your network is experiencing issues reaching the node. You might be using a proxy or firewall. Consider running the diagnostic tool from a different location, confirming your port, or using an IP instead of a URL domain.


## Diagnose errors in `diagnostic.log` [diagnostic-log-errors]

The following are common errors that you might encounter when running the diagnostic tool:

* `Error: Could not find or load main class com.elastic.support.diagnostics.DiagnosticApp`

    This indicates that you accidentally downloaded the source code file instead of `diagnostics-X.X.X-dist.zip` from the releases page.

* `Could not retrieve the {{ls}} version due to a system or network error - unable to continue.`

    This indicates that the diagnostic couldn’t run commands against the node. Poll the root endpoint again, and ensure that you’re using the same parameters when you run the dianostic batch or shell file.
