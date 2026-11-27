---
navigation_title: OpenTelemetry profiling
description: Diagnose and fix common OpenTelemetry profiling problems in Elastic Observability, including missing profiles, eBPF and tracefs errors, data stream permissions, and empty Profiling views in Kibana.
type: troubleshooting
applies_to:
  stack: preview 9.6+
  serverless: preview
products:
  - id: observability
---

# Troubleshoot OpenTelemetry profiling [profiling-otel-troubleshoot]

Use this page when OpenTelemetry profiling doesn't deliver profiles to the **Profiling** app. Start with the symptom that matches what you see in the {{agent}} logs or in {{kib}}. For the requirements and the deployment steps, refer to [Get started with OpenTelemetry profiling](/solutions/observability/infra-and-hosts/get-started-with-otel-profiling.md).

## The agent is healthy but no profiles arrive

The profiler can't load its eBPF programs when it lacks privileges or runs on an unsupported kernel, and {{fleet}} doesn't always report this as an error. Check the {{agent}} logs for messages such as:

```txt
failed to load eBPF tracer: failed to read kernel symbols: unable to read kallsyms addresses - check capabilities
```

Run the agent as root, or grant the `CAP_SYS_ADMIN` capability, and confirm that the host meets the [kernel requirements](/solutions/observability/infra-and-hosts/get-started-with-otel-profiling.md#profiling-otel-requirements-hosts).

## The receiver reports that neither `debugfs` nor `tracefs` is mounted

The profiler needs access to scheduler tracepoints. Mount `tracefs` on the Linux host:

```bash
sudo mount -t tracefs tracefs /sys/kernel/tracing
```

For a container deployment, expose that directory at `/sys/kernel/tracing` in the container. The Helm profiling preset configures this container mount for you.

## The receiver fails with `system analysis request was not handled` on a local kind cluster

kind runs its nodes in containers, so the profiler runs in a nested PID namespace. With {{agent}} 9.6, enable PID namespace translation by adding the following receiver setting to your Helm values:

```yaml
config:
  receivers:
    profiling:
      pid_namespace_translation_mode: auto
```

## Agents cannot create profiling data streams

{{agent}} logs show an error like this one:

```txt
action [indices:admin/auto_create] is unauthorized for API key id [...] of user [elastic/fleet-server] on indices [profiling-stacktraces.otel-default]
```

If the agent's API key lacks permission to create these data streams, ingestion fails even when the templates are installed. As a user with the `superuser` role, create the missing data streams before the agents start sending data. The event streams include the full stream and downsampled streams from `5pow01` through `5pow11`. Run only the requests for streams that do not already exist:

```console
PUT _data_stream/profiling-events-all.otel-default
PUT _data_stream/profiling-events-5pow01.otel-default
PUT _data_stream/profiling-events-5pow02.otel-default
PUT _data_stream/profiling-events-5pow03.otel-default
PUT _data_stream/profiling-events-5pow04.otel-default
PUT _data_stream/profiling-events-5pow05.otel-default
PUT _data_stream/profiling-events-5pow06.otel-default
PUT _data_stream/profiling-events-5pow07.otel-default
PUT _data_stream/profiling-events-5pow08.otel-default
PUT _data_stream/profiling-events-5pow09.otel-default
PUT _data_stream/profiling-events-5pow10.otel-default
PUT _data_stream/profiling-events-5pow11.otel-default
PUT _data_stream/profiling-stacktraces.otel-default
PUT _data_stream/profiling-stackframes.otel-default
PUT _data_stream/profiling-executables.otel-default
PUT _data_stream/profiling-hosts.otel-default
```

## {{kib}} reports that no profiling data was found

Check that the schema selector is set to **OpenTelemetry** and widen the time range. Run the event count query in [Verify that profiles are flowing](/solutions/observability/infra-and-hosts/get-started-with-otel-profiling.md#profiling-otel-verify). If the count is `0`, check the agent's health and logs in {{fleet}}. The `resources.has_data` field from `GET /_profiling/status` covers both profiling schemas, so `true` does not by itself confirm OpenTelemetry ingestion. In an OpenTelemetry-only deployment, `resource_management.enabled` and `resources.created` can both be `false`: those fields describe Universal Profiling resources.
