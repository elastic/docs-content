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
The Infrastructure UI only supports {{k8s}} pod metric data from the [{{k8s}}](integration-docs://reference/kubernetes.md) integration.
:::


|  |  |
| --- | --- |
| **CPU Usage** | Average of `kubernetes.pod.cpu.usage.node.pct`. |
| **Memory Usage** | Average of `kubernetes.pod.memory.usage.node.pct`. |
| **Inbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.rx.bytes` scaled to a 1 second rate. |
| **Outbound Traffic** | Derivative of the maximum of `kubernetes.pod.network.tx.bytes` scaled to a 1 second rate. |

For information about the fields used by the Infrastructure UI to display {{k8s}} pod metrics, see the [Infrastructure app fields](/reference/observability/fields-and-object-schemas.md).

## Infrastructure UI filtering logic [k8s-pod-metrics-filtering]
```{applies_to}
stack: ga 9.3
```

The Infrastructure UI requires the following attributes to work correctly. Data that does not include them will not appear in these views:

* Inventory UI searches - Kubernetes Pods: `event.module : kubernetes`
* Inventory Rule - Kubernetes Pods: `event.module : kubernetes`