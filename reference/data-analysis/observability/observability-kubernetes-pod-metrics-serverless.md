---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-kubernetes-pod-metrics.html
---

# Kubernetes pod metrics [observability-kubernetes-pod-metrics]

To analyze Kubernetes pod metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|  |  |
| --- | --- |
| **CPU Usage** | Average of `kubernetes.pod.cpu.usage.node.pct`. |
| **Memory Usage** | Average of `kubernetes.pod.memory.usage.node.pct`. |
| **Inbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.rx.bytes` scaled to a 1 second rate. |
| **Outbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.tx.bytes` scaled to a 1 second rate. |

For information about the fields used by the Infrastructure UI to display Kubernetes pod metrics, see the [Infrastructure app fields](/reference/observability/serverless/infrastructure-app-fields.md).
