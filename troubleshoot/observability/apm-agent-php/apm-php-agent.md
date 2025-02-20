---
navigation_title: "APM PHP Agent"
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/php/current/troubleshooting.html
---

# Troubleshoot APM PHP Agent [troubleshooting]

Is something not working as expected? Don’t worry if you can’t figure out what the problem is; we’re here to help! As a first step, ensure your app is compatible with the agent’s [supported technologies](asciidocalypse://docs/apm-agent-php/docs/reference/ingestion-tools/apm-agent-php/supported-technologies.md).

If you’re an existing Elastic customer with a support contract, please create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm).

::::{important} 
**Please upload your complete debug logs** to a service like [GitHub Gist](https://gist.github.com) so that we can analyze the problem. Logs should include everything from when the application starts up until the first request executes.
::::



## Disable the Agent [disable-agent] 

In the unlikely event the agent causes disruptions to a production application, you can disable the agent while you troubleshoot.

Disable the agent by setting [`enabled`](asciidocalypse://docs/apm-agent-php/docs/reference/ingestion-tools/apm-agent-php/configuration-reference.md#config-enabled) to `false`. You’ll need to restart your application for the changes to apply.


## Disclaimer for `dev_internal_*` configuration options [dev-internal-config-disclaimer] 

Configuration options starting with `dev_internal_` should be used only for supportability. It’s recommended to have these options in the configuration for the short periods of time while resolving an issue with the agent. There is no backward compatability guarantee for these options so any one can be changed and/or removed even in a minor or patch release.


## Enable verbose log for backend communication [enable-verbose-log-backend-comm] 

Configuration option `dev_internal_backend_comm_log_verbose` can be used to enable verbose log for the agent’s communication with Elastic APM Server.

| Environment variable name | Option name in `php.ini` |
| --- | --- |
| `ELASTIC_APM_DEV_INTERNAL_BACKEND_COMM_LOG_VERBOSE` | `elastic_apm.dev_internal_backend_comm_log_verbose` |

| Default | Type |
| --- | --- |
| `false` | Boolean |

The log is written under `INFO` level - see [Logging](asciidocalypse://docs/apm-agent-php/docs/reference/ingestion-tools/apm-agent-php/configuration.md#configure-logging).

Also see [Disclaimer for `dev_internal_*` configuration options](#dev-internal-config-disclaimer).



