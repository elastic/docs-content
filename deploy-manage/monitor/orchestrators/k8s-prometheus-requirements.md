---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-prometheus-requirements.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Prometheus requirements [k8s-prometheus-requirements]

If you're using [Prometheus](https://prometheus.io/), then you need to perform additional configuration to scrape the metrics endpoint using the configuration you set in [](/deploy-manage/monitor/orchestrators/k8s-enabling-metrics-endpoint.md) and [](/deploy-manage/monitor/orchestrators/k8s-securing-metrics-endpoint.md).

## RBAC settings for scraping the metrics [k8s_rbac_settings_for_scraping_the_metrics]

Configure the RBAC settings for the Prometheus instance to access the metrics endpoint. These typically will be set automatically when using the Prometheus operator.

Your settings should look similar to the following:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus
rules:
- nonResourceURLs:
  - /metrics
  verbs:
  - get
```

## Helm settings: Allow the Prometheus operator to read across namespaces[k8s_optional_prometheus_operator_helm_settings_to_allow_reading_podmonitor_and_servicemonitor_across_namespaces]

If you're using the Prometheus operator and your Prometheus instance is not in the same namespace as the ECK operator, then configure the Prometheus operator with the following Helm values. These values allow reading PodMonitor and ServiceMonitor across namespaces.

```yaml
prometheus:
  prometheusSpec:
    podMonitorNamespaceSelector: {}
    podMonitorSelectorNilUsesHelmValues: false
    serviceMonitorNamespaceSelector: {}
    serviceMonitorSelectorNilUsesHelmValues: false
```


## Allow full TLS verification when using a custom TLS certificate [k8s_optional_settings_to_allow_full_tls_verification_when_using_a_custom_tls_certificate]

If you are using a custom TLS certificate and you need to set `insecureSkipVerify` to `false`, then you need to do the following:

1. Create a Kubernetes secret within the Prometheus namespace that contains the Certificate Authority in PEM format.

    The easiest way to create the CA secret within the Prometheus namespace is to use the `kubectl create secret generic` command. For example:

    ```sh
    kubectl create secret generic eck-metrics-tls-ca -n monitoring --from-file=ca.crt=/path/to/ca.pem
    ```

2. Ensure that the CA secret is mounted within the Prometheus Pod.

    Steps will vary between Prometheus installations. If you're using the Prometheus operator, you can set the `spec.secrets` field of the `Prometheus` custom resource to the name of the previously created Kubernetes Secret. See the [ECK Helm chart values file](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/deploy/eck-operator/values.yaml) for more information.


