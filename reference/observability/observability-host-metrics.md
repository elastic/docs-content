---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-host-metrics.html
  - https://www.elastic.co/guide/en/observability/current/host-metrics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Host metrics [observability-host-metrics]

Learn about key host metrics displayed in the Infrastructure UI:

* [Elastic System integration host metrics](#ecs-host-metrics)
* [OpenTelemetry host metrics](#open-telemetry-host-metrics)


## Elastic System integration host metrics [ecs-host-metrics]

Refer to the following sections for host metrics and field calculation formulas for the Elastic System integration data:

* [Hosts](#key-metrics-hosts)
* [CPU usage](#key-metrics-cpu)
* [Memory](#key-metrics-memory)
* [Log](#key-metrics-log)
* [Network](#key-metrics-network)
* [Disk](#key-metrics-network)
* [Legacy](#legacy-metrics)

### Entity definition [monitor-rds-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |
| --- | --- |
| **Filter** | `event.module: 'system'` or `metricset.module: 'system'` | Used to filter relevant data. |
| **Identifier** | `host.name` | Used to identify each entity. |
| **Display value** | `host.name` | Used as a display friendly value. |

### Hosts metrics [key-metrics-hosts]

| Metric | Description |
| --- | --- |
| **Hosts** | Number of hosts returned by your search criteria.<br><br>**Field Calculation**: `unique_count(host.name)`<br> |


### CPU usage metrics [key-metrics-cpu]

| Metric | Description |
| --- | --- |
| **CPU Usage (%)** | Average of percentage of CPU time spent in states other than Idle and IOWait, normalized by the number of CPU cores. Includes both time spent on user space and kernel space. 100% means all CPUs of the host are busy.<br><br>**Field Calculation**: `average(system.cpu.total.norm.pct)`<br><br>For legacy metric calculations, refer to [Legacy metrics](#legacy-metrics).<br> |
| **CPU Usage - iowait (%)** | The percentage of CPU time spent in wait (on disk).<br><br>**Field Calculation**: `average(system.cpu.iowait.pct) / max(system.cpu.cores)`<br> |
| **CPU Usage - irq (%)** | The percentage of CPU time spent servicing and handling hardware interrupts.<br><br>**Field Calculation**: `average(system.cpu.irq.pct) / max(system.cpu.cores)`<br> |
| **CPU Usage - nice (%)** | The percentage of CPU time spent on low-priority processes.<br><br>**Field Calculation**: `average(system.cpu.nice.pct) / max(system.cpu.cores)`<br> |
| **CPU Usage - softirq (%)** | The percentage of CPU time spent servicing and handling software interrupts.<br><br>**Field Calculation**: `average(system.cpu.softirq.pct) / max(system.cpu.cores)`<br> |
| **CPU Usage - steal (%)** | The percentage of CPU time spent in involuntary wait by the virtual CPU while the hypervisor was servicing another processor. Available only on Unix.<br><br>**Field Calculation**: `average(system.cpu.steal.pct) / max(system.cpu.cores)`<br> |
| **CPU Usage - system (%)** | The percentage of CPU time spent in kernel space.<br><br>**Field Calculation**: `average(system.cpu.system.pct) / max(system.cpu.cores)`<br> |
| **CPU Usage - user (%)** | The percentage of CPU time spent in user space. On multi-core systems, you can have percentages that are greater than 100%. For example, if 3 cores are at 60% use, then the system.cpu.user.pct will be 180%.<br><br>**Field Calculation**: `average(system.cpu.user.pct) / max(system.cpu.cores)`<br> |
| **Load (1m)** | 1 minute load average.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>**Field Calculation**: `average(system.load.1)`<br> |
| **Load (5m)** | 5 minute load average.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>**Field Calculation**: `average(system.load.5)`<br> |
| **Load (15m)** | 15 minute load average.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>**Field Calculation**: `average(system.load.15)`<br> |
| **Normalized Load** | 1 minute load average normalized by the number of CPU cores.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>100% means the 1 minute load average is equal to the number of CPU cores of the host.<br><br>Taking the example of a 32 CPU cores host, if the 1 minute load average is 32, the value reported here is 100%. If the 1 minute load average is 48, the value reported here is 150%.<br><br>**Field Calculation**: `average(system.load.1) / max(system.load.cores)`<br> |


### Memory metrics [key-metrics-memory]

| Metric | Description |
| --- | --- |
| **Memory Cache** | Memory (page) cache.<br><br>**Field Calculation**: `average(system.memory.used.bytes ) - average(system.memory.actual.used.bytes)`<br> |
| **Memory Free** | Total available memory.<br><br>**Field Calculation**: `max(system.memory.total) - average(system.memory.actual.used.bytes)`<br> |
| **Memory Free (excluding cache)** | Total available memory excluding the page cache.<br><br>**Field Calculation**: `system.memory.free`<br> |
| **Memory Total** | Total memory capacity.<br><br>**Field Calculation**: `avg(system.memory.total)`<br> |
| **Memory Usage (%)** | Percentage of main memory usage excluding page cache.<br><br>This includes resident memory for all processes plus memory used by the kernel structures and code apart from the page cache.<br><br>A high level indicates a situation of memory saturation for the host. For example, 100% means the main memory is entirely filled with memory that can’t be reclaimed, except by swapping out.<br><br>**Field Calculation**: `average(system.memory.actual.used.pct)`<br> |
| **Memory Used** | Main memory usage excluding page cache.<br><br>**Field Calculation**: `average(system.memory.actual.used.bytes)`<br> |


### Log metrics [key-metrics-log]

| Metric | Description |
| --- | --- |
| **Log Rate** | Derivative of the cumulative sum of the document count scaled to a 1 second rate. This metric relies on the same indices as the logs.<br><br>**Field Calculation**: `cumulative_sum(doc_count)`<br> |


### Network metrics [key-metrics-network]

| Metric | Description |
| --- | --- |
| **Network Inbound (RX)** | Number of bytes that have been received per second on the public interfaces of the hosts.<br><br>**Field Calculation**: `sum(host.network.ingress.bytes) * 8 / 1000`<br><br>For legacy metric calculations, refer to [Legacy metrics](#legacy-metrics).<br> |
| **Network Outbound (TX)** | Number of bytes that have been sent per second on the public interfaces of the hosts.<br><br>**Field Calculation**: `sum(host.network.egress.bytes) * 8 / 1000`<br><br>For legacy metric calculations, refer to [Legacy metrics](#legacy-metrics).<br> |


### Disk metrics [observability-host-metrics-disk-metrics]

| Metric | Description |
| --- | --- |
| **Disk Latency** | Time spent to service disk requests.<br><br>**Field Calculation**: `average(system.diskio.read.time + system.diskio.write.time) / (system.diskio.read.count + system.diskio.write.count)`<br> |
| **Disk Read IOPS** | Average count of read operations from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.diskio.read.count), kql='system.diskio.read.count: *')`<br> |
| **Disk Read Throughput** | Average number of bytes read from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.diskio.read.bytes), kql='system.diskio.read.bytes: *')`<br> |
| **Disk Usage - Available (%)** | Percentage of disk space available.<br><br>**Field Calculation**: `1-average(system.filesystem.used.pct)`<br> |
| **Disk Usage - Max (%)** | Percentage of disk space used.  A high percentage indicates that a partition on a disk is running out of space.<br><br>**Field Calculation**: `max(system.filesystem.used.pct)`<br> |
| **Disk Write IOPS** | Average count of write operations from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.diskio.write.count), kql='system.diskio.write.count: *')`<br> |
| **Disk Write Throughput** | Average number of bytes written from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.diskio.write.bytes), kql='system.diskio.write.bytes: *')`<br> |

### Legacy metrics [legacy-metrics]

Over time, we may change the formula used to calculate a specific metric. To avoid affecting your existing rules, instead of changing the actual metric definition, we create a new metric and refer to the old one as "legacy".

The UI and any new rules you create will use the new metric definition. However, any alerts that use the old definition will refer to the metric as "legacy".

| Metric | Description |
| --- | --- |
| **CPU Usage (legacy)** | Percentage of CPU time spent in states other than Idle and IOWait, normalized by the number of CPU cores. This includes both time spent on user space and kernel space. 100% means all CPUs of the host are busy.<br><br>**Field Calculation**: `(average(system.cpu.user.pct) + average(system.cpu.system.pct)) / max(system.cpu.cores)`<br> |
| **Network Inbound (RX) (legacy)** | Number of bytes that have been received per second on the public interfaces of the hosts.<br><br>**Field Calculation**: `average(host.network.ingress.bytes) * 8 / (max(metricset.period, kql='host.network.ingress.bytes: *') / 1000)`<br> |
| **Network Outbound (TX) (legacy)** | Number of bytes that have been sent per second on the public interfaces of the hosts.<br><br>**Field Calculation**: `average(host.network.egress.bytes) * 8 / (max(metricset.period, kql='host.network.egress.bytes: *') / 1000)`<br> |

## OpenTelemetry host metrics [open-telemetry-host-metrics]

Refer to the following sections for host metrics and field calculation formulas for OpenTelemetry data:

* [Hosts](#otel-metrics-hosts)
* [CPU usage](#otel-metrics-cpu)
* [Memory](#otel-metrics-memory)
* [Log](#otel-metrics-log)
* [Network](#otel-metrics-network)
* [Disk](#otel-metrics-network)

### Entity definition [opentelemetry-host-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |
| --- | --- |
| **Filter** | `data_stream.dataset: 'hostmetricsreceiver.otel'` | Used to filter relevant data. |
| **Identifier** | `host.name` | Used to identify each entity. |
| **Display value** | `host.name` | Used as a display friendly value. |

### OpenTelemetry hosts metrics [otel-metrics-hosts]

| Metric | Description |
| --- | --- |
| **Hosts** | Number of hosts returned by your search criteria.<br><br>**Field Calculation**: `unique_count(host.name)`<br> |

### OpenTelemetry CPU usage metrics [otel-metrics-cpu]

| Metric | Description |
| --- | --- |
| **CPU Usage (%)** | Average percentage of CPU time spent in states other than Idle and IOWait, normalized by the number of CPU cores. Includes both time spent on user space and kernel space. 100% means all CPUs of the host are busy.<br><br>**Field Calculation**: `1-(average(metrics.system.cpu.utilization,kql='state: idle') + average(metrics.system.cpu.utilization,kql='state: wait'))`<br> |
| **CPU Usage - iowait (%)** | The percentage of CPU time spent in wait (on disk).<br><br>**Field Calculation**: `average(metrics.system.cpu.utilization,kql='state: wait') / max(metrics.system.cpu.logical.count)`<br> |
| **CPU Usage - irq (%)** | The percentage of CPU time spent servicing and handling hardware interrupts.<br><br>**Field Calculation**: `average(metrics.system.cpu.utilization,kql='state: interrupt') / max(metrics.system.cpu.logical.count)`<br> |
| **CPU Usage - nice (%)** | The percentage of CPU time spent on low-priority processes.<br><br>**Field Calculation**: `average(metrics.system.cpu.utilization,kql='state: nice') / max(metrics.system.cpu.logical.count)`<br> |
| **CPU Usage - softirq (%)** | The percentage of CPU time spent servicing and handling software interrupts.<br><br>**Field Calculation**: `average(metrics.system.cpu.utilization,kql='state: softirq') / max(metrics.system.cpu.logical.count)`<br> |
| **CPU Usage - steal (%)** | The percentage of CPU time spent in involuntary wait by the virtual CPU while the hypervisor was servicing another processor. Available only on Unix.<br><br>**Field Calculation**: `average(metrics.system.cpu.utilization,kql='state: steal') / max(metrics.system.cpu.logical.count)`<br> |
| **CPU Usage - system (%)** | The percentage of CPU time spent in kernel space.<br><br>**Field Calculation**: `average(metrics.system.cpu.utilization,kql='state: system') / max(metrics.system.cpu.logical.count)`<br> |
| **CPU Usage - user (%)** | The percentage of CPU time spent in user space. On multi-core systems, you can have percentages that are greater than 100%. For example, if 3 cores are at 60% use, then the system.cpu.user.pct will be 180%.<br><br>**Field Calculation**: `average(metrics.system.cpu.utilization,kql='state: user') / max(metrics.system.cpu.logical.count)`<br> |
| **Load (1m)** | 1 minute load average.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>**Field Calculation**: `average(metrics.system.cpu.load_average.1m)`<br> |
| **Load (5m)** | 5 minute load average.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>**Field Calculation**: `average(metrics.system.cpu.load_average.5m)`<br> |
| **Load (15m)** | 15 minute load average.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>**Field Calculation**: `average(metrics.system.cpu.load_average.15m)`<br> |
| **Normalized Load** | 1 minute load average normalized by the number of CPU cores.<br><br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br><br>100% means the 1 minute load average is equal to the number of CPU cores of the host.<br><br>Taking the example of a 32 CPU cores host, if the 1 minute load average is 32, the value reported here is 100%. If the 1 minute load average is 48, the value reported here is 150%.<br><br>**Field Calculation**: `average(metrics.system.cpu.load_average.1m) / max(metrics.system.cpu.logical.count)`<br> |

### OpenTelemetry memory metrics [otel-metrics-memory]

| Metric | Description |
| --- | --- |
| **Memory Cache** | Memory (page) cache.<br><br>**Field Calculation**: `average(metrics.system.memory.usage, kql='state: cache') / average(metrics.system.memory.usage, kql='state: slab_reclaimable') + average(metrics.system.memory.usage, kql='state: slab_unreclaimable')`<br> |
| **Memory Free** | Total available memory.<br><br>**Field Calculation**: `(max(metrics.system.memory.usage, kql='state: free') + max(metrics.system.memory.usage, kql='state: cached')) - (average(metrics.system.memory.usage, kql='state: slab_unreclaimable') + average(metrics.system.memory.usage, kql='state: slab_reclaimable'))`<br> |
| **Memory Free (excluding cache)** | Total available memory excluding the page cache.<br><br>**Field Calculation**: `average(metrics.system.memory.usage, kql='state: free')`<br> |
| **Memory Total** | Total memory capacity.<br><br>**Field Calculation**: `avg(system.memory.total)`<br> |
| **Memory Usage (%)** | Percentage of main memory usage excluding page cache.<br><br>This includes resident memory for all processes plus memory used by the kernel structures and code apart from the page cache.<br><br>A high level indicates a situation of memory saturation for the host. For example, 100% means the main memory is entirely filled with memory that can’t be reclaimed, except by swapping out.<br><br>**Field Calculation**: `average(system.memory.utilization, kql='state: used') + average(system.memory.utilization, kql='state: buffered') + average(system.memory.utilization, kql='state: slab_reclaimable') + average(system.memory.utilization, kql='state: slab_unreclaimable')`<br> |
| **Memory Used** | Main memory usage excluding page cache.<br><br>**Field Calculation**: `average(metrics.system.memory.usage, kql='state: used') + average(metrics.system.memory.usage, kql='state: buffered') + average(metrics.system.memory.usage, kql='state: slab_reclaimable') + average(metrics.system.memory.usage, kql='state: slab_unreclaimable')`<br> |

### OpenTelemetry log metrics [otel-metrics-log]

| Metric | Description |
| --- | --- |
| **Log Rate** | Derivative of the cumulative sum of the document count scaled to a 1 second rate. This metric relies on the same indices as the logs.<br><br>**Field Calculation**: `cumulative_sum(doc_count)`<br> |

### OpenTelemetry network metrics [otel-metrics-network]

| Metric | Description |
| --- | --- |
| **Network Inbound (RX)** | Number of bytes that have been received per second on the public interfaces of the hosts.<br><br>**Field Calculation**: `8 * counter_rate(max(metrics.system.network.io, kql='direction: receive')))`<br> |
| **Network Outbound (TX)** | Number of bytes that have been sent per second on the public interfaces of the hosts.<br><br>**Field Calculation**: `8 * counter_rate(max(metrics.system.network.io, kql='direction: transmit'))`<br> |

### OpenTelemetry disk metrics [otel-metrics-disk]

| Metric | Description |
| --- | --- |
| **Disk Latency** | Time spent to service disk requests.<br><br>**Field Calculation**: `average(system.diskio.read.time + system.diskio.write.time) / (system.diskio.read.count + system.diskio.write.count)`<br> |
| **Disk Read IOPS** | Average count of read operations from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.disk.operations, kql='attributes.direction: read'))`<br> |
| **Disk Read Throughput** | Average number of bytes read from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.disk.io, kql='attributes.direction: read'))`<br> |
| **Disk Usage - Available (%)** | Percentage of disk space available.<br><br>**Field Calculation**: `average(system.filesystem.usage, kql='state: free')`<br> |
| **Disk Usage - Used (%)** | Percentage of disk space used. <br><br>**Field Calculation**: `1 - sum(metrics.system.filesystem.usage, kql='state: free') / sum(metrics.system.filesystem.usage)`<br> |
| **Disk Write IOPS** | Average count of write operations from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.disk.operations, kql='attributes.direction: write'))`<br> |
| **Disk Write Throughput** | Average number of bytes written from the device per second.<br><br>**Field Calculation**: `counter_rate(max(system.disk.io, kql='attributes.direction: write'))')`<br> |