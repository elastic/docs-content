---
navigation_title: "Troubleshoot the backend"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-self-managed-troubleshooting.html
applies_to:
  stack: all
---



# Troubleshoot the Universal Profiling backend [profiling-self-managed-troubleshooting]


Refer to the following sections to troubleshoot any issues you encounter when setting up or operating the Universal Profiling backend services.


## Application behavior [_application_behavior] 


### Missing stack traces in the UI [_missing_stack_traces_in_the_ui] 

If there is a sudden drop in the number of stack traces in the UI, or if the UI is displaying none at all, the collector service may be having trouble and thus data ingestion is impacted.

The status of the collector can be inferred from the health checks and the metrics exposed.

Most notable causes of an impaired collector are:

* collector is not able to connect to the Elasticsearch cluster: the connection or authentication details may be wrong
* collector is not starting up properly: the collector may be crashing on startup, or it may be stuck in a loop (when deployed through an orchestration system): check the logs for any errors


### Missing symbols [_missing_symbols] 

One of the most useful features of Universal Profiling is the ability to display the source code file and line number of the stack trace frames. This is only possible if the symbols are processed correctly in the backend services.

When the symbols are missing, the UI will display the stack trace frames of native applications with an hexadecimal addresses, in the form `0x1234abcd`. If this is happening for most of the native frames, including public OS package files, this is a sign that the debug symbols are not being processed correctly.

It is possible to verify that the symbolizer is working correctly by using the health check endpoint and the metrics exposed.

The most notable causes of an impaired symbolizer are:

1. symbolizer is not able to connect to the debug symbol endpoint: this is an internet-exposed endpoint, so it may be blocked by a firewall
2. symbolizer is not starting up properly: the symbolizer may be crashing on startup, possibly due to misconfigurations, or it may be stuck in a loop (when deployed through an orchestration system): check the logs for any errors


## General troubleshooting [_general_troubleshooting] 


### Capacity planning [_capacity_planning] 

When deploying Universal Profiling Agents on a new set of machines, it is possible that the backend services will not be able to handle the load. This is especially true if the number of Universal Profiling Agents is large, or if the Universal Profiling Agents are deployed on machines with a large number of cores.

The traffic pattern of the Universal Profiling Agents is prone to bursts on startup, and the backend services may not be able to handle the burst of traffic coming from a large number of Universal Profiling Agents at the same time.

Even if the capacity of the backend services was planned based on the number of Universal Profiling Agents as suggested in [Sizing guidance](../../../solutions/observability/infra-and-hosts/operate-universal-profiling-backend.md#profiling-self-managed-ops-sizing-guidance), we recommend deploying Universal Profiling Agents are in batches. For example, deploy 20% of the fleet at a time. After deploying a batch of Universal Profiling Agents, pause for at least 30 to 60 seconds before deploying the next batch to allow the backend services to stabilize. When the Universal Profiling Agent starts fresh on a new machine, it scans all the existing processes and sends the executable’s metadata to the backend services. This can cause a burst of traffic that can overwhelm the backend services.


### Inspecting the metrics [_inspecting_the_metrics] 

Once metrics are exposed by the backend services, it is possible to inspect them to understand the behavior of the services. Refer to [Metrics](../../../solutions/observability/infra-and-hosts/operate-universal-profiling-backend.md#profiling-self-managed-ops-monitoring-metrics) for instructions on how to expose metrics.

We don’t yet provide pre-built Kibana dashboards to monitor the services, but we have compiled a list of the most useful metrics to monitor. The prominent peak of goroutines or memory usage is a sign that the service is under stress and may be having trouble. If there’s the possibility of having access to Linux kernel telemetry for the hosts running the backend services, the most important metrics to monitor are the CPU throttling and the network usage.


### Reading debug logs [_reading_debug_logs] 

The backend services can be configured to log at debug level, which can be useful for troubleshooting issues. To do so, there’s a `verbose` config entry in each YAML configuration file, which can be set to `true` to enable debug logging. The same configuration option can be set through the CLI flags, as detailed in [Use CLI flags to override configuration file values"](../../../solutions/observability/infra-and-hosts/operate-universal-profiling-backend.md#profiling-self-managed-ops-configuration-cli-overrides).

When running the backend services in verbose mode, the logs will be helpful to troubleshoot issues.

::::{important} 
Debug logs create an output that is unsuited for long-running production deployments. The verbose mode should only be enabled on a single replica at a time, and only for a short period of time, as it reduces performance and increases the CPU usage of the service.
::::


When verbose mode is enabled, there will be fine-grained information logged about the operations of the service. In the case of collectors, the component responsible for ingesting data in Elasticsearch will be the most frequent. For symbolizers most of the logs will be related to the processing of native frames, initially detected by the collector.

If you are troubleshooting startup issues for both services, logs are the most useful source of information. On startup, each service generates logs indicating whether it was able or unable to parse configurations and begin processing incoming requests. Any startup errors will be logged using the `log.level=error` field. Use these error logs to find misconfigurations or other issues that could prevent the service from starting. Errors will be logged using the `log.level=error` field: they can be used to spot misconfigurations or other issues that prevent the service from starting up.

