---
navigation_title: EDOT PHP
description: Troubleshooting the Elastic Distribution of OpenTelemetry PHP agent.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_php: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the EDOT PHP agent

Use the information on this page to troubleshoot issues using EDOT PHP.

If you need help and you're an existing Elastic customer with a support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-node/issues).

As a first step, review the [supported technologies](elastic-otel-php://reference/edot-php/supported-technologies.md) to ensure your application is supported by the agent. Are you using a PHP version that EDOT PHP supports? Are the versions of your dependencies in the supported version range to be instrumented?

## Turn on logging

When diagnosing issues with the agent's operation, logs play a key role. You can find a detailed explanation of the logging configuration options in [Configuration](elastic-otel-php://reference/edot-php/configuration.md#logging-configuration).

In most cases, setting the logging level to `debug` is sufficient. You can also use `trace` can be used, but keep in mind that the amount of generated data might be significant.

Additionally, turn on logging for OpenTelemetry components, for example as shown in the following example . Logs from OpenTelemetry components are directed to the same output configured for EDOT logs.

```
export OTEL_LOG_LEVEL=DEBUG
```

:::{note}
Upload your complete debug logs to a service like [GitHub Gist](https://gist.github.com) so that Elastic support can analyze the problem. Logs should include everything from when the application starts up until the first request executes. Logs might contain sensitive data: make sure to review and sanitize them before sharing.
:::


## Turn off the agent

If you suspect that the agent might be causing disruptions to a production application, you can deactivate the agent while you troubleshoot.

To deactivate the agent, set the [`elastic_otel.enabled`](elastic-otel-php://reference/edot-php/configuration.md#general-configuration) setting to `false`.

:::{note}
You need to restart your application for the changes to apply.
:::

## Agent is not instrumenting code

If the agent doesn't seem to be instrumenting code from your application, try the following actions.

### Native OTLP serializer issues

If you're experiencing issues where no spans, logs, or metrics are being sent, or if you encounter log messages like the following:

```bash
Failed to serialize spans/logs/metrics batch...
```

This might be due to a failure in the native OTLP Protobuf serializer. The native serializer is activated by default for maximum performance, but in rare cases it might encounter incompatibilities with certain environments or data. To confirm whether this is the cause, try turning off the native serializer using the following environment variable:

```bash
export ELASTIC_OTEL_NATIVE_OTLP_SERIALIZER_ENABLED=false
```

Restart your application and check if spans, logs, or metrics start appearing correctly.

:::{note}
When turned off, the agent falls back to a PHP-based serializer, which has lower performance.
:::


### `open_basedir` PHP configuration option

If you see a similar entry in the agent log, this indicates an incorrect `open_basedir` configuration. For more details, refer to [Limitations](elastic-otel-php://reference/edot-php/setup/limitations.md#open_basedir-php-configuration-option).

```
EDOT PHP bootstrap file (...php/bootstrap_php_part.php) is located outside of paths allowed by open_basedir ini setting.
```

## Collection of diagnostic information

For a more detailed analysis of issues, you might need to collect diagnostic information. The agent allows for the automatic collection of such information: all data is saved to the file specified in the configuration.

There are two possible ways to turn on diagnostic information:

- By editing the `php.ini` file: Modify the `php.ini` file, or `99-elastic.ini`, to provide the path to the file where the data will be saved, For example:

   ```
   elastic_otel.debug_diagnostic_file=/tmp/php_diags_%p_%t.txt
   ```

- By setting an environment variable. The `ELASTIC_OTEL_DEBUG_DIAGNOSTIC_FILE` environment variable must be exported or directly specified when running PHP process. For example:

   ```bash
   ELASTIC_OTEL_DEBUG_DIAGNOSTIC_FILE=/tmp/php_diags_%p_%t.txt php test.php
   ```

   The provided file path must be writable by the PHP process. If there are multiple PHP processes in your system, you can specify directives in the diagnostic file name. This way, the files remain unique and won't be overwritten.

   - `%p` - In this place, the agent substitutes the process identifier.
   - `%t` - In this place, the agent substitutes the UNIX timestamp.

:::{warning}
After setting the path, remember to fully restart the process for which you are collecting diagnostic information. This might vary depending on the context, such as PHP, PHP-FPM, Apache, or PHP-CGI. Diagnostic information will be recorded after the first HTTP request is made or at the beginning of script execution for PHP-CLI. Also be aware that the information contained in the output file may include sensitive data, such as passwords, security tokens or environment variables from your system. After collecting diagnostic information, remember to disable this feature and restore the previous configuration in php.ini or the environment variable.
:::

The following information is collected:

- Process identifier and parent process identifier
- User identifier of the worker process
- List of loaded PHP extensions
- Result from the `phpinfo()` function
- Process memory information and memory maps (`/proc/{id}/maps` and `/proc/{id}/smaps_rollup`)
- Process status information (`/proc/{id}/status`)

## Turn on debugging for instrumented functions

EDOT can collect detailed diagnostics of arguments passed to instrumented functions. Use them to verify whether the data used by the instrumented application is correctly analyzed by the instrumentation code.

To turn on debugging for instrumented function, set the following environment variable:

```bash
ELASTIC_OTEL_DEBUG_PHP_HOOKS_ENABLED=true
```


## Turn on instrumentation of all the application code

For diagnostic purposes outside of production environments, EDOT allows instrumenting the entire code of your application. This allows tracking function calls throughout the processing of an entire request or script and provides better insight into the application's behavior.

To turn on debugging for instrumented function, set the following environment variable:

```bash
ELASTIC_OTEL_DEBUG_INSTRUMENT_ALL=true
```

