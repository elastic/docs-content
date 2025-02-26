---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-configure-operator-metrics.html
applies_to:
  deployment:
    eck: all
---

# ECK metrics configuration [k8s-configure-operator-metrics]

The ECK operator provides a metrics endpoint that can be used to monitor the operator’s performance and health. By default, the metrics endpoint is not enabled and is not secured. The following sections describe how to enable it, secure it and the associated Prometheus requirements:

* [Enabling the metrics endpoint](k8s-enabling-metrics-endpoint.md)
* [Securing the metrics endpoint](k8s-securing-metrics-endpoint.md)
* [Prometheus requirements](k8s-prometheus-requirements.md)

::::{note} 
The ECK operator metrics endpoint will be secured by default beginning in version 3.0.0.
::::





