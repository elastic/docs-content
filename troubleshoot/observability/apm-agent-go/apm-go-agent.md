---
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/go/current/troubleshooting.html
---

# APM Go Agent

Is something not working as expected? Don’t worry if you can’t figure out what the problem is; we’re here to help! First, ensure your app is compatible with the agent’s [supported technologies](https://www.elastic.co/guide/en/apm/agent/go/current/supported-tech.html).

If you’re an existing Elastic customer with a support contract, please create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm).

::::{important}
**Please upload your complete debug logs** to a service like [GitHub Gist](https://gist.github.com) so that we can analyze the problem. Logs should include everything from when the application starts up until the first request executes. Instructions for enabling logging are below.
::::



## Logging [agent-logging]

Agent logs are critical to the debugging process. By default, this logging is disabled. To enable it, set a log output file with [`ELASTIC_APM_LOG_FILE`](https://www.elastic.co/guide/en/apm/agent/go/current/configuration.html#config-log-file). Alternatively, if you’re using Docker or Kubernetes and are okay with mixing agent and application logs, you can set `ELASTIC_APM_LOG_FILE=stderr`.

::::{note}
The agent does not rotate log files. Log rotation must be handled externally.
::::


With logging enabled, use [`ELASTIC_APM_LOG_LEVEL`](https://www.elastic.co/guide/en/apm/agent/go/current/configuration.html#config-log-level) to increase the granularity of the agent’s logging. For example: `ELASTIC_APM_LOG_LEVEL=debug`.

Be sure to execute a few requests to your application before posting your log files. Each request should add lines similar to these in the logs:

```log
{"level":"debug","time":"2020-07-23T11:46:32+08:00","message":"sent request with 100 transactions, 0 spans, 0 errors, 0 metricsets"}
```

If you don’t see lines like these, it’s likely that you haven’t instrumented your application correctly.


## Disable the Agent [disable-agent]

In the unlikely event the agent causes disruptions to a production application, you can disable the agent while you troubleshoot.

If you have access to [dynamic configuration](https://www.elastic.co/guide/en/apm/agent/go/current/configuration.html#dynamic-configuration), you can disable the recording of events by setting [`ELASTIC_APM_RECORDING`](https://www.elastic.co/guide/en/apm/agent/go/current/configuration.html#config-recording) to `false`. When changed at runtime from a supported source, there’s no need to restart your application.

If that doesn’t work, or you don’t have access to dynamic configuration, you can disable the agent by setting [`ELASTIC_APM_ACTIVE`](https://www.elastic.co/guide/en/apm/agent/go/current/configuration.html#config-active) to `false`. Restart your application for the changes to apply.

