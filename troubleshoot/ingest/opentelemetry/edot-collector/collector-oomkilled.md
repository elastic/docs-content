---
navigation_title: Collector out of memory
description: Diagnose and resolve out-of-memory issues in the EDOT Collector using Go’s Performance Profiler.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Troubleshoot an out-of-memory EDOT Collector

If your EDOT Collector pods terminate with an `OOMKilled` status, this usually indicates sustained memory pressure or potentially a memory leak due to an introduced regression or a bug. You can use the Performance Profiler (`pprof`) extension to collect and analyze memory profiles, helping you identify the root cause of the issue.

If you're running the Collector in Kubernetes and experiencing resource allocation issues, refer to [Insufficient resources in Kubernetes](/troubleshoot/ingest/opentelemetry/edot-collector/insufficient-resources-kubestack.md) for troubleshooting steps.

## Symptoms

These symptoms typically indicate that the EDOT Collector is experiencing a memory-related failure:

- EDOT Collector pod restarts with an `OOMKilled` status in Kubernetes.
- Memory usage steadily increases before the crash.
- The Collector's logs don't show clear errors before termination.

For more detailed diagnostics, refer to [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md).

## Resolution

Turn on runtime profiling using the `pprof` extension and then gather memory heap profiles from the affected pod:

::::::{stepper}

:::::{step} Enable `pprof` in the Collector

Edit the EDOT Collector Daemonset configuration and include the `pprof` extension:

```yaml
exporters:
  ...
processors:
  ...
receivers:
  ...
extensions:
  pprof:

service:
  extensions:
   - pprof
   - ...
  pipelines:
    metrics:
      receivers: [ ... ]
      processors: [ ... ]
      exporters: [ ... ]
```

Restart the Collector after applying these changes. When the Daemonset is deployed again, spot the pod that is getting restarted.
:::::

:::::{step} Access the affected pod and collect a heap dump

When a pod starts exhibiting high memory usage or restarts due to OOM, run the following to enter a debug shell:

```console
kubectl debug -it <collector-pod-name> --image=ubuntu:latest
```

In the debug container:

```console
apt update
apt install -y curl
curl http://localhost:1777/debug/pprof/heap > heap.out
```
:::::

:::::{step} Copy the heap file from the pod

From your local machine, copy the heap file using:

```bash
kubectl cp <collector-pod-name>:heap.out ./heap.out -c <debug-container-name>
```
::::{note}
Replace `<debug-container-name>` with the name assigned to the debug container. Without the `-c` flag, Kubernetes will show the list of available containers.
::::
:::::

:::::{step} Convert the heap profile for analysis

You can now generate a visual representation, for example PNG:

```bash
go tool pprof -png heap.out > heap.png
```
:::::
::::::

## Best practices

To improve the effectiveness of memory diagnostics and reduce investigation time, consider the following:

- Collect multiple heap profiles over time (for example, every few minutes) to observe memory trends before the crash.

- Automate heap profile collection at intervals to observe trends over time.

## Resources

- [Go's pprof documentation](https://pkg.go.dev/net/http/pprof)
- [OpenTelemetry Collector troubleshooting documentation](https://opentelemetry.io/docs/collector/troubleshooting/#performance-profiler-pprof)
