---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-config-file.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---

# Configuration file of the Universal Profiling Agent [profiling-config-file]

The Universal Profiling Agent can be configured using a configuration file. Specify the path to the configuration file using the CLI argument `-config`. The default path for the configuration file is `/etc/Elastic/universal-profiling/pf-host-agent.conf`.

The expected format of the configuration file is a plaintext file, where each line holds one option.

Example:

```
project-id: 73
secret-token: abc123
collection-agent: example.com:443
```

::::{warning}
Command line arguments to the Universal Profiling Agent take precedence over environment variables, and environment variables take precedence over the configuration file.
::::


| Config file option | Type | Example | Description |
| --- | --- | --- | --- |
| `verbose` | `bool` | `verbose: true` | Run the Universal Profiling Agent in verbose mode. |
| `no-kernel-version-check` | `bool` | `no-kernel-version-check: true` | Disable the kernel version check. See [Override kernel version check ](override-kernel-version-check.md) for more details. |
| `tags` | `string` | `tags: 'cloud_region:us-central1;env:staging'` | Set specific tags. See [Tag data for querying](tag-data-for-querying.md) for more details. |
| `project-id` | `uint` | `project-id: 73` | Splits profiling data into logical groups that you control. You can assign any non-zero, unsigned integer ⇐ 4095. |
| `secret-token` | `string` | `secret-token: abc123` | Set the secret token for communicating with the Universal Profiling Collector to `abc123`. |
| `collection-agent` | `string` | `collection-agent: example.com:443` | Set the destination for reporting profiling information to `example.com:443`. |
| `probabilistic-interval` | `duration` | `probabilistic-interval: 2m30s` | Set the probabilistic interval to `2m30s`. See [Probabilistic profiling](configure-probabilistic-profiling.md) for more details. |
| `probabilistic-threshold` | `uint` | `probabilistic-threshold: 50` | Set the probabilistic threshold to `50`. See [Probabilistic profiling](configure-probabilistic-profiling.md) for more details. |

