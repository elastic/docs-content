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

To analyze {{k8s}} pod metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

:::{note}
:applies_to: stack: ga 9.3
For {{k8s}} pod metrics, the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support metric data collected by the [{{k8s}} integration](integration-docs://reference/kubernetes.md).
:::

## Entity definition [monitor-k8s-pods-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |  |
| --- | --- | --- |
| **Filter** | `event.module: "kubernetes"` | Used to filter relevant data. |
| **Identifier** | `kubernetes.pod.uid` | Used to identify each entity. |
| **Display value** | `kubernetes.pod.name` | Used as a display friendly value. |

## Metrics [monitor-k8s-pods-metrics]

|  |  |
| --- | --- |
| **CPU Usage** | Average of `kubernetes.pod.cpu.usage.node.pct`. |
| **Memory Usage** | Average of `kubernetes.pod.memory.usage.node.pct`. |
| **Inbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.rx.bytes` scaled to a 1 second rate. |
| **Outbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.tx.bytes` scaled to a 1 second rate. |

For information about the fields used by the Infrastructure UI to display {{k8s}} pod metrics, see the [Infrastructure app fields](/reference/observability/fields-and-object-schemas.md).