---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-advanced-configuration.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
navigation_title: Advanced configuration
---

# Advanced configuration for Elastic Universal Profiling [profiling-advanced-configuration]

After completing the steps in the [Get started](get-started-with-universal-profiling.md) documentation, you may need to continue to more advanced configuration for your deployment. See the following sections for more information:

* [Tag data for querying](tag-data-for-querying.md): Tag data collected by the Universal Profiling Agent into multiple logical groups so they can be queried in Kibana.
* [Add symbols for native frames](add-symbols-for-native-frames.md): Push symbols to your cluster so you can see function names and line numbers in traces of applications written in programming languages that compile to native code (C, C++, Rust, Go, etc.).
* [Use a proxy](use-proxy-with-universal-profiling-agent.md):  Set up an HTTP proxy if your infrastructure Universal Profiling Agent installation needs one to reach {{ecloud}}.
* [Override kernel version check ](override-kernel-version-check.md): Configure the Universal Profiling Agent to bypass the kernel version compatibility check.
* [Environment variables for the Universal Profiling Agent ](environment-variables-to-configure-universal-profiling-agent.md): Configure the Universal Profiling Agent using the environment.

::::{warning}
Command line arguments to the Universal Profiling Agent take precedence over environment variables, and environment variables take precedence over the configuration file.
::::


The Universal Profiling Agent accepts the following CLI arguments:

| CLI argument | Type | Example | Description |
| --- | --- | --- | --- |
| `-v` | `bool` | `-v` | Run the Universal Profiling Agent in verbose mode. |
| `-no-kernel-version-check` | `bool` | `-no-kernel-version-check` | Disable the kernel version check. See [Override kernel version check ](override-kernel-version-check.md) for more details. |
| `-tags` | `string` | `-tags='cloud_region:us-central1;env:staging'` | Set specific tags. See [Tag data for querying](tag-data-for-querying.md) for more details. |
| `-project-id` | `uint` | `-project-id 73` | Splits profiling data into logical groups that you control. You can assign any non-zero, unsigned integer ⇐ 4095. |
| `-secret-token` | `string` | `-secret-token=abc123` | Set the secret token for communicating with the Universal Profiling Collector to `abc123`. |
| `-collection-agent` | `string` | `-collection-agent=example.com:443` | Set the destination for reporting profiling information to `example.com:443`. |
| `-probabilistic-interval` | `duration` | `-probabilistic-interval=2m30s` | Set the probabilistic interval to `2m30s`. See [Probabilistic profiling](configure-probabilistic-profiling.md) for more details. |
| `-probabilistic-threshold` | `uint` | `-probabilistic-threshold=50` | Set the probabilistic threshold to `50`. See [Probabilistic profiling](configure-probabilistic-profiling.md) for more details. |
| `-config` | `string` | `-config=/etc/Elastic/universal-profiling/pf-host-agent.conf` | Set the path for the configuration file of the Universal Profiling Agent. See [Configuration file of the Universal Profiling Agent](configuration-file-of-universal-profiling-agent.md) for more details. |







