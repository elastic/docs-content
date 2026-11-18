---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-kubernetes-pod-metrics.html
  - https://www.elastic.co/guide/en/observability/current/kubernetes-pod-metrics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# {{k8s}} pod metrics [observability-kubernetes-pod-metrics]

Learn about key {{k8s}} pod metrics displayed in the Infrastructure UI:

* [{{k8s}} integration pod metrics](#ecs-k8s-pod-metrics)
* [OpenTelemetry pod metrics](#otel-k8s-pod-metrics)

To analyze {{k8s}} pod metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

## {{k8s}} integration pod metrics [ecs-k8s-pod-metrics]

Refer to the following sections for pod metrics and field calculation formulas for {{k8s}} integration data:

* [Entity definition](#monitor-k8s-pods-entity)
* [Metrics](#monitor-k8s-pods-metrics)

:::{note}
:applies_to: {"stack": "ga 9.3, removed 9.6", "serverless": "removed"}
For {{k8s}} pod metrics, the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support {{k8s}} pod metric data collected by the [{{k8s}} integration](integration-docs://reference/kubernetes.md). If you're using {{edot}} and these views appear empty, refer to [{{k8s}} Pods and Docker Containers views empty when using {{edot}}](/troubleshoot/observability/troubleshooting-infrastructure-monitoring/kubernetes-pods-docker-containers-empty-otel.md).
:::

### Entity definition [monitor-k8s-pods-entity]
```{applies_to}
stack: ga 9.3
```

The following table lists the fields used to filter, identify, and display each pod entity.

|  |  |  |
| --- | --- | --- |
| **Filter** | `event.module: "kubernetes"` | Used to filter relevant data. |
| **Identifier** | `kubernetes.pod.uid` | Used to identify each entity. |
| **Display value** | `kubernetes.pod.name` | Used as a display friendly value. |

### Metrics [monitor-k8s-pods-metrics]

The following table lists each predefined pod metric and its field calculation formula.

| Metric | Description |
| --- | --- |
| **CPU Usage** | Percentage of CPU used, measured against the pod's CPU limit. When the pod has no CPU limit, the percentage is measured against the capacity of the node instead.<br><br>**Field Calculation**: `average(kubernetes.pod.cpu.usage.limit.pct)`, falling back to `average(kubernetes.pod.cpu.usage.node.pct)`<br> |
| **Memory Usage** | Percentage of memory used, measured against the pod's memory limit. Pods without a memory limit report no value.<br><br>**Field Calculation**: `average(kubernetes.pod.memory.usage.limit.pct)`<br> |
| **Inbound Traffic** | Number of bytes received per second.<br><br>**Field Calculation**: `derivative(max(kubernetes.pod.network.rx.bytes))` scaled to a 1 second rate<br> |
| **Outbound Traffic** | Number of bytes sent per second.<br><br>**Field Calculation**: `derivative(max(kubernetes.pod.network.tx.bytes))` scaled to a 1 second rate<br> |

## OpenTelemetry pod metrics [otel-k8s-pod-metrics]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

The Infrastructure UI and inventory rules also support pod metrics collected using OpenTelemetry semantic conventions, through the `kubeletstats` receiver. To choose which pods you want to see, use the **Schema** menu described in [Select the data collection schema](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#pod-schema-selector).

Refer to the following sections for pod metrics and field calculation formulas for OpenTelemetry data:

* [Entity definition](#opentelemetry-k8s-pod-entity)
* [Metrics](#otel-k8s-pod-metrics-list)

### OpenTelemetry Collector configuration [k8s-pod-otel-collector-configuration]

By default, when {{agent}} is configured as an OTel Collector, it collects {{k8s}} node, pod, and container metrics using the `kubeletstats` receiver. Refer to the [default {{k8s}} configuration](elastic-agent://reference/edot-collector/config/default-config-k8s.md) for the receiver settings.

If you're using a different Collector distribution or the upstream Contrib Collector, refer to the [{{k8s}} OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md) for the equivalent Collector configuration.

### Entity definition [opentelemetry-k8s-pod-entity]

The following table lists the fields used to filter, identify, and display each pod entity.

|  |  |  |
| --- | --- | --- |
| **Filter** | `data_stream.dataset: 'kubeletstatsreceiver.otel'` | Used to filter relevant data. |
| **Identifier** | `k8s.pod.uid` | Used to identify each entity. |
| **Display value** | `k8s.pod.name` | Used as a display friendly value. |

### Metrics [otel-k8s-pod-metrics-list]

The following table lists each predefined pod metric and its field calculation formula.

| Metric | Description |
| --- | --- |
| **CPU Usage** | Percentage of CPU used, measured against the pod's CPU limit. When the pod has no CPU limit, the percentage is measured against the capacity of the node instead.<br><br>**Field Calculation**: `average(metrics.k8s.pod.cpu_limit_utilization)`, falling back to `average(metrics.k8s.pod.cpu.node.utilization)`<br> |
| **Memory Usage** | Percentage of memory used, measured against the pod's memory limit. When the pod has no memory limit, the percentage is measured against the capacity of the node instead. If neither value is available, no value is reported.<br><br>**Field Calculation**: `average(metrics.k8s.pod.memory_limit_utilization)`, falling back to `average(metrics.k8s.pod.memory.node.utilization)`<br> |
| **Inbound Traffic** | Number of bytes received per second. The maximum is taken for each network interface, then summed across interfaces.<br><br>**Field Calculation**: `derivative(sum(max(metrics.k8s.pod.network.io, kql='direction: receive')))` scaled to a 1 second rate<br> |
| **Outbound Traffic** | Number of bytes sent per second. The maximum is taken for each network interface, then summed across interfaces.<br><br>**Field Calculation**: `derivative(sum(max(metrics.k8s.pod.network.io, kql='direction: transmit')))` scaled to a 1 second rate<br> |

For information about the fields used by the Infrastructure UI to display {{k8s}} pod metrics, see the [{{infrastructure-app}} fields](/reference/observability/fields-and-object-schemas.md).
