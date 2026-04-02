---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-container-metrics.html
  - https://www.elastic.co/guide/en/observability/current/container-metrics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Container metrics [observability-container-metrics]

Learn about key container metrics displayed in the Infrastructure UI:

* [Docker](#key-metrics-docker)
* [Kubernetes](#key-metrics-kubernetes)

## Docker container metrics [key-metrics-docker]

These are the key metrics displayed for Docker containers.

:::{note}
:applies_to: stack: ga 9.3
For Docker container metrics, the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support metric data collected by the [Docker integration](integration-docs://reference/docker.md).
:::

### Entity definition [monitor-docker-container-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |  |
| --- | --- | --- |
| **Filter** | `event.module : "docker"` | Used to filter relevant data. |
| **Identifier** | `container.id` | Used to identify each entity. |
| **Display value** | `container.name` | Used as a display friendly value. |

### CPU usage metrics [key-metrics-docker-cpu]

| Metric | Description |
| --- | --- |
| **CPU Usage (%)** | Average CPU for the container.<br><br>**Field Calculation:** `average(docker.cpu.total.pct)`<br> |


### Memory metrics [key-metrics-docker-memory]

| Metric | Description |
| --- | --- |
| **Memory Usage (%)** | Average memory usage for the container.<br><br>**Field Calculation:** `average(docker.memory.usage.pct)`<br> |


### Network metrics [key-metrics-docker-network]

| Metric | Description |
| --- | --- |
| **Inbound Traffic (RX)** | Derivative of the maximum of `docker.network.in.bytes` scaled to a 1 second rate.<br><br>**Field Calculation:** `average(docker.network.inbound.bytes) * 8 / (max(metricset.period, kql='docker.network.inbound.bytes: *') / 1000)`<br> |
| **Outbound Traffic (TX)** | Derivative of the maximum of `docker.network.out.bytes` scaled to a 1 second rate.<br><br>**Field Calculation:** `average(docker.network.outbound.bytes) * 8 / (max(metricset.period, kql='docker.network.outbound.bytes: *') / 1000)`<br> |


### Disk metrics [observability-container-metrics-disk-metrics]

| Metric | Description |
| --- | --- |
| **Disk Read IOPS** | Average count of read operations from the device per second.<br><br>**Field Calculation:**  `counter_rate(max(docker.diskio.read.ops), kql='docker.diskio.read.ops: *')`<br> |
| **Disk Write IOPS** | Average count of write operations from the device per second.<br><br>**Field Calculation:**  `counter_rate(max(docker.diskio.write.ops), kql='docker.diskio.write.ops: *')`<br> |


## {{k8s}} container metrics [key-metrics-kubernetes]

These are the key metrics displayed for {{k8s}} (containerd) containers.

:::{note}
:applies_to: stack: ga 9.3
For {{k8s}} container metrics, the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support metric data collected by the [{{k8s}} integration](integration-docs://reference/kubernetes.md).
:::

### Entity definition [monitor-k8s-container-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |  |
| --- | --- | --- |
| **Filter** | `event.module : "kubernetes"` | Used to filter relevant data. |
| **Identifier** | `container.id` | Used to identify each entity. |
| **Display value** | `container.name` | Used as a display friendly value. |

### CPU usage metrics [key-metrics-kubernetes-cpu]

| Metric | Description |
| --- | --- |
| **CPU Usage (%)** | Average CPU for the container.<br><br>**Field Calculation:** `average(kubernetes.container.cpu.usage.limit.pct)`<br> |


### Memory metrics [key-metrics-kubernetes-memory]

| Metric | Description |
| --- | --- |
| **Memory Usage (%)** | Average memory usage for the container.<br><br>**Field Calculation:** `average(kubernetes.container.memory.usage.limit.pct)`<br> |