---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-envs.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---

# Environment variables to configure the Universal Profiling Agent [profiling-envs]

The Universal Profiling Agent can be configured with environment variables.

::::{warning}
Command line arguments to the Universal Profiling Agent take precedence over environment variables, and environment variables take precedence over the configuration file.
::::


| Environment variable | Example | Description |
| --- | --- | --- |
| `PRODFILER_VERBOSE` | `PRODFILER_VERBOSE=true` | Run the Universal Profiling Agent in verbose mode. |
| `PRODFILER_NO_KERNEL_VERSION_CHECK` | `PRODFILER_NO_KERNEL_VERSION_CHECK=true` | Disable the kernel version check. See [Override kernel version check ](override-kernel-version-check.md) for more details. |
| `PRODFILER_TAGS` | `PRODFILER_TAGS="cloud_region:us-central1;env:staging"` | Set specific tags. See [Tag data for querying](tag-data-for-querying.md) for more details. |
| `PRODFILER_PROJECT_ID` | `PRODFILER_PROJECT_ID=73` | Set project ID to 73. |
| `PRODFILER_SECRET_TOKEN` | `PRODFILER_SECRET_TOKEN=my_secret_token` | Set the secret token to `my_secret_token`. |
| `PRODFILER_COLLECTION_AGENT` | `PRODFILER_COLLECTION_AGENT=example.com:443` | Set the destination for reporting profiling information to `example.com:443`. |
| `PRODFILER_PROBABILISTIC_THRESHOLD` | `PRODFILER_PROBABILISTIC_THRESHOLD=50` | Set the probabilistic threshold to `50`. See [Probabilistic profiling](configure-probabilistic-profiling.md) for more details. |
| `PRODFILER_PROBABILISTIC_INTERVAL` | `PRODFILER_PROBABILISTIC_INTERVAL=2m30s` | Set the probabilistic interval to `2m30s`. See [Probabilistic profiling](configure-probabilistic-profiling.md) for more details. |
| `PRODFILER_CONFIG` | `PRODFILER_CONFIG=/etc/Elastic/universal-profiling/pf-host-agent.conf` | Set the path for the configuration file of the Universal Profiling Agent. See [Configuration file of the Universal Profiling Agent](configuration-file-of-universal-profiling-agent.md) for more details. |

