---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/host-metrics.html
---

# Host metrics [host-metrics]

Learn about key host metrics displayed in the {{infrastructure-app}}:

* [Hosts](#key-metrics-hosts)
* [CPU usage](#key-metrics-cpu)
* [Memory](#key-metrics-memory)
* [Log](#key-metrics-log)
* [Network](#key-metrics-network)
* [Disk](#key-metrics-network)
* [Legacy metrics](#legacy-metrics)


## Hosts metrics [key-metrics-hosts]

| Metric | Description |
| --- | --- |
| **Hosts** | Number of hosts returned by your search criteria.<br>**Field Calculation:** `count(system.cpu.cores)` |


## CPU usage metrics [key-metrics-cpu]

| Metric | Description |
| --- | --- |
| **CPU Usage (%)** | Average of percentage of CPU time spent in states other than Idle and IOWait, normalized by the number of CPU cores. Includes both time spent on user space and kernel space. 100% means all CPUs of the host are busy.<br>**Field Calculation**: `average(system.cpu.total.norm.pct)`<br>For legacy metric calculations, refer to [Legacy metrics](#legacy-metrics). |
| **CPU Usage - iowait (%)** | The percentage of CPU time spent in wait (on disk).<br>**Field Calculation:** `average(system.cpu.iowait.pct) / max(system.cpu.cores)` |
| **CPU Usage - irq (%)** | The percentage of CPU time spent servicing and handling hardware interrupts.<br>**Field Calculation:** `average(system.cpu.irq.pct) / max(system.cpu.cores)` |
| **CPU Usage - nice (%)** | The percentage of CPU time spent on low-priority processes.<br>**Field Calculation:** `average(system.cpu.nice.pct) / max(system.cpu.cores)` |
| **CPU Usage - softirq (%)** | The percentage of CPU time spent servicing and handling software interrupts.<br>**Field Calculation:** `average(system.cpu.softirq.pct) / max(system.cpu.cores)` |
| **CPU Usage - steal (%)** | The percentage of CPU time spent in involuntary wait by the virtual CPU while the hypervisor was servicing another processor. Available only on Unix.<br>**Field Calculation:** `average(system.cpu.steal.pct) / max(system.cpu.cores)` |
| **CPU Usage - system (%)** | The percentage of CPU time spent in kernel space.<br>**Field Calculation:** `average(system.cpu.system.pct) / max(system.cpu.cores)` |
| **CPU Usage - user (%)** | The percentage of CPU time spent in user space. On multi-core systems, you can have percentages that are greater than 100%. For example, if 3 cores are at 60% use, then the system.cpu.user.pct will be 180%.<br>**Field Calculation:** `average(system.cpu.user.pct) / max(system.cpu.cores)` |
| **Load (1m)** | 1 minute load average.<br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br>**Field Calculation:** average(system.load.1) |
| **Load (5m)** | 5 minute load average.<br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br>**Field Calculation:** `average(system.load.5)` |
| **Load (15m)** | 15 minute load average.<br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br>**Field Calculation:** `average(system.load.15)` |
| **Normalized Load** | 1 minute load average normalized by the number of CPU cores.<br>Load average gives an indication of the number of threads that are runnable (either busy running on CPU, waiting to run, or waiting for a blocking IO operation to complete).<br>100% means the 1 minute load average is equal to the number of CPU cores of the host.<br>Taking the example of a 32 CPU cores host, if the 1 minute load average is 32, the value reported here is 100%. If the 1 minute load average is 48, the value reported here is 150%.<br>**Field Calculation:**  `average(system.load.1) / max(system.load.cores)` |


## Memory metrics [key-metrics-memory]

| Metric | Description |
| --- | --- |
| **Memory Cache** | Memory (page) cache.<br>**Field Calculation:** `average(system.memory.used.bytes ) - average(system.memory.actual.used.bytes)` |
| **Memory Free** | Total available memory.<br>**Field Calculation:** `max(system.memory.total) - average(system.memory.actual.used.bytes)` |
| **Memory Free (excluding cache)** | Total available memory excluding the page cache.<br>**Field Calculation:** `system.memory.free` |
| **Memory Total** | Total memory capacity.<br>**Field Calculation:** `avg(system.memory.total)` |
| **Memory Usage (%)** | Percentage of main memory usage excluding page cache.<br>This includes resident memory for all processes plus memory used by the kernel structures and code apart from the page cache.<br>A high level indicates a situation of memory saturation for the host. For example, 100% means the main memory is entirely filled with memory that can’t be reclaimed, except by swapping out.<br>**Field Calculation:** `average(system.memory.actual.used.pct)` |
| **Memory Used** | Main memory usage excluding page cache.<br>**Field Calculation:** `average(system.memory.actual.used.bytes)` |


## Log metrics [key-metrics-log]

| Metric | Description |
| --- | --- |
| **Log Rate** | Derivative of the cumulative sum of the document count scaled to a 1 second rate. This metric relies on the same indices as the logs.<br>**Field Calculation:** `cumulative_sum(doc_count)` |


## Network metrics [key-metrics-network]

| Metric | Description |
| --- | --- |
| **Network Inbound (RX)** | Number of bytes that have been received per second on the public interfaces of the hosts.<br>**Field Calculation**: `sum(host.network.ingress.bytes) * 8 / 1000`<br>For legacy metric calculations, refer to [Legacy metrics](#legacy-metrics). |
| **Network Outbound (TX)** | Number of bytes that have been sent per second on the public interfaces of the hosts.<br>**Field Calculation**: `sum(host.network.egress.bytes) * 8 / 1000`<br>For legacy metric calculations, refer to [Legacy metrics](#legacy-metrics). |


## Disk metrics [key-metrics-disk]

| Metric | Description |
| --- | --- |
| **Disk Latency** | Time spent to service disk requests.<br>**Field Calculation:**  `average(system.diskio.read.time + system.diskio.write.time) / (system.diskio.read.count + system.diskio.write.count)` |
| **Disk Read IOPS** | Average count of read operations from the device per second.<br>**Field Calculation:**  `counter_rate(max(system.diskio.read.count), kql='system.diskio.read.count: *')` |
| **Disk Read Throughput** | Average number of bytes read from the device per second.<br>**Field Calculation:**  `counter_rate(max(system.diskio.read.bytes), kql='system.diskio.read.bytes: *')` |
| **Disk Usage - Available (%)** | Percentage of disk space available.<br>**Field Calculation:**  `1-average(system.filesystem.used.pct)` |
| **Disk Usage - Max (%)** | Percentage of disk space used. A high percentage indicates that a partition on a disk is running out of space.<br>**Field Calculation:**  `max(system.filesystem.used.pct)` |
| **Disk Write IOPS** | Average count of write operations from the device per second.<br>**Field Calculation:**  `counter_rate(max(system.diskio.write.count), kql='system.diskio.write.count: *')` |
| **Disk Write Throughput** | Average number of bytes written from the device per second.<br>**Field Calculation:**  `counter_rate(max(system.diskio.write.bytes), kql='system.diskio.write.bytes: *')` |


## Legacy metrics [legacy-metrics]

Over time, we may change the formula used to calculate a specific metric. To avoid affecting your existing rules, instead of changing the actual metric definition, we create a new metric and refer to the old one as "legacy."

The UI and any new rules you create will use the new metric definition. However, any alerts that use the old definition will refer to the metric as "legacy."

| Metric | Description |
| --- | --- |
| **CPU Usage (legacy)** | Percentage of CPU time spent in states other than Idle and IOWait, normalized by the number of CPU cores. This includes both time spent on user space and kernel space. 100% means all CPUs of the host are busy.<br>**Field Calculation:** `(average(system.cpu.user.pct) + average(system.cpu.system.pct)) / max(system.cpu.cores)` |
| **Network Inbound (RX) (legacy)** | Number of bytes that have been received per second on the public interfaces of the hosts.<br>**Field Calculation:**  `average(host.network.ingress.bytes) * 8 / (max(metricset.period, kql='host.network.ingress.bytes: *') / 1000)` |
| **Network Outbound (TX) (legacy)** | Number of bytes that have been sent per second on the public interfaces of the hosts.<br>**Field Calculation:**  `average(host.network.egress.bytes) * 8 / (max(metricset.period, kql='host.network.egress.bytes: *') / 1000)` |
