---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/debug-standalone-agents.html
---

# Debug standalone Elastic Agents [debug-standalone-agents]

When you run standalone {{agent}}s, you are responsible for monitoring the status of your deployed {{agent}}s. You cannot view the status or logs in {{fleet}}.

Use the following tips to help identify potential issues.

Also refer to [Troubleshoot common problems](/troubleshoot/ingest/fleet/common-problems.md) for guidance on specific problems.

::::{note}
You might need to log in as a root user (or Administrator on Windows) to run these commands.
::::



## Check the status of the running {{agent}} [_check_the_status_of_the_running_agent]

To check the status of the running {{agent}} daemon and other processes managed by {{agent}}, run the `status` command. For example:

```shell
elastic-agent status
```

Returns something like:

```yaml
State: HEALTHY
Message: Running
Fleet State: STOPPED
Fleet Message: (no message)
Components:
  * log           (HEALTHY)
                  Healthy: communicating with pid '25423'
  * filestream    (HEALTHY)
                  Healthy: communicating with pid '25424'
```

By default, this command returns the status in human-readable format. Use the `--output` flag to change it to `json` or `yaml`.

For more information about this command, refer to [elastic-agent status](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-status-command).


## Inspect {{agent}} and related logs [inspect-standalone-agent-logs]

If the {{agent}} status is unhealthy, or behaving unexpectedly, inspect the logs of the running {{agent}}.

The log location varies by platform. {{agent}} logs are in the folders described in [Installation layout](/reference/ingestion-tools/fleet/installation-layout.md). {{beats}} and {{fleet-server}} logs are in folders named for the output (for example, `default`).

Start by investigating any errors you see in the {{agent}} and related logs. Also look for repeated lines that might indicate problems like connection issues. If the {{agent}} and related logs look clean, check the host operating system logs for out of memory (OOM) errors related to the {{agent}} or any of its processes.


## Increase the log level of the running {{agent}} [increase-log-level]

The log level of the running agent is set to `info` by default. At this level, {{agent}} will log informational messages, including the number of events that are published. It also logs any warnings, errors, or critical errors.

To increase the log level, set it to `debug` in the `elastic-agent.yml` file.

The `debug` setting configures {{agent}} to log debug messages, including a detailed printout of all flushed events, plus all the information collected at other log levels.

Set other options if you want write logs to a file. For example:

```yaml
agent.logging.level: debug
agent.logging.to_files: true
agent.logging.files:
  path: /var/log/elastic-agent
  name: elastic-agent
  keepfiles: 7
  permissions: 0600
```

For other log settings, refer to [Logging](/reference/ingestion-tools/fleet/elastic-agent-standalone-logging-config.md).


## Expose /debug/pprof/ endpoints with the monitoring endpoint [expose-debug-endpoint]

Profiling data produced by the `/debug/pprof/` endpoints can be useful for debugging, but presents a security risk. Do not expose these endpoints if the monitoring endpoint is accessible over a network. (By default, the monitoring endpoint is bound to a local Unix socket or Windows npipe and not accessible over a network.)

To expose the `/debug/pprof/` endpoints, set `agent.monitoring.pprof: true` in the `elastic-agent.yml` file. For more information about monitoring settings, refer to [Monitoring](/reference/ingestion-tools/fleet/elastic-agent-monitoring-configuration.md).

After exposing the endpoints, you can access the HTTP handler bound to a socket for {{beats}} or the {{agent}}. For example:

```shell
sudo curl --unix-socket /Library/Elastic/Agent/data/tmp/default/filebeat/filebeat.sock http://socket/ | json_pp
```

Returns something like:

```json
{
   "beat" : "filebeat",
   "binary_arch" : "amd64",
   "build_commit" : "93708bd74e909e57ed5d9bea3cf2065f4cc43af3",
   "build_time" : "2022-01-28T09:53:29.000Z",
   "elastic_licensed" : true,
   "ephemeral_id" : "421e2525-9360-41db-9395-b9e627fbbe6e",
   "gid" : "0",
   "hostname" : "My-MacBook-Pro.local",
   "name" : "My-MacBook-Pro.local",
   "uid" : "0",
   "username" : "root",
   "uuid" : "fc0cc98b-b6d8-4eef-abf5-2d5f26adc7e8",
   "version" : "7.17.0"
}
```

Likewise, the following request:

```shell
sudo curl --unix-socket /Library/Elastic/Agent/data/tmp/elastic-agent.sock http://socket/stats | json_pp
```

Returns something like:

```shell
{
   "beat" : {
      "cpu" : {
         "system" : {
            "ticks" : 16272,
            "time" : {
               "ms" : 16273
            }
         },
         "total" : {
            "ticks" : 42981,
            "time" : {
               "ms" : 42982
            },
            "value" : 42981
         },
         "user" : {
            "ticks" : 26709,
            "time" : {
               "ms" : 26709
            }
         }
      },
      "info" : {
         "ephemeral_id" : "ea8fec0d-f7dd-4577-85d7-a2c38583c9c6",
         "uptime" : {
            "ms" : 5885653
         },
         "version" : "7.17.0"
      },
      "memstats" : {
         "gc_next" : 13027776,
         "memory_alloc" : 7771632,
         "memory_sys" : 39666696,
         "memory_total" : 757970208,
         "rss" : 58990592
      },
      "runtime" : {
         "goroutines" : 101
      }
   },
   "system" : {
      "cpu" : {
         "cores" : 12
      },
      "load" : {
         "1" : 4.8892,
         "15" : 2.6748,
         "5" : 3.0537,
         "norm" : {
            "1" : 0.4074,
            "15" : 0.2229,
            "5" : 0.2545
         }
      }
   }
}
```


## Inspect the {{agent}} configuration [inspect-configuration]

To inspect the running {{agent}} configuration use the [elastic-agent inspect](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-inspect-command) command.

To analyze the current state of the agent, inspect log files, and see the configuration of {{agent}} and the sub-processes it starts, run the `diagnostics` command. For example:

```shell
elastic-agent diagnostics
```

For more information about this command, refer to [elastic-agent diagnostics](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-diagnostics-command).

