---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/kubernetes-pod-metrics.html
---

# Kubernetes pod metrics [kubernetes-pod-metrics]

Learn about Kubernetes pod metrics displayed in the {{infrastructure-app}}.

|     |     |
| --- | --- |
| **CPU Usage** | Average of `kubernetes.pod.cpu.usage.node.pct`. |
| **Memory Usage** | Average of `kubernetes.pod.memory.usage.node.pct`. |
| **Inbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.rx.bytes` scaled to a 1 second rate. |
| **Outbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.tx.bytes` scaled to a 1 second rate. |

For information about which required fields the {{infrastructure-app}} uses to display Kubernetes pods metrics, see the [{{infrastructure-app}} field reference](asciidocalypse://docs/docs-content/docs/reference/observability/fields-and-object-schemas/metrics-app-fields.md).

