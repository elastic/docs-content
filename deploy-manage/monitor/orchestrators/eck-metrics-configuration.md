---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-configure-operator-metrics.html
applies_to:
  deployment:
    eck: all
---

# ECK operator metrics [k8s-configure-operator-metrics]

% todo: what metrics? what to watch for?

The ECK operator provides a metrics endpoint that can be used to monitor the operator’s performance and health. By default, the metrics endpoint is not enabled. In ECK version 2.16 and lower, the metrics endpoint is also not secured.

The following sections describe how to enable and secure the metrics endpoint. If you use [Prometheus](https://prometheus.io/) to consume the monitoring data, then you need to perform additional configurations within Prometheus.

* [Enabling the metrics endpoint](k8s-enabling-metrics-endpoint.md)
* [Securing the metrics endpoint](k8s-securing-metrics-endpoint.md) (ECK 2.16 and lower)
* [Prometheus requirements](k8s-prometheus-requirements.md)

::::{note} 
The ECK operator metrics endpoint is secured by default beginning in version 3.0.0.
::::
