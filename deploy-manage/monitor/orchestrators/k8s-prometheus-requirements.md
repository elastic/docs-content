---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-prometheus-requirements.html
applies:
  eck: all
---

# Prometheus requirements [k8s-prometheus-requirements]

The previous options requires the following settings within Prometheus to function properly:

## RBAC settings for scraping the metrics [k8s_rbac_settings_for_scraping_the_metrics]

Configure the RBAC settings for the Prometheus instance to access the metrics endpoint similar to the following: (These typically will be set automatically when using the Prometheus operator)

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


## Optional Prometheus operator Helm settings to allow reading PodMonitor and ServiceMonitor across namespaces [k8s_optional_prometheus_operator_helm_settings_to_allow_reading_podmonitor_and_servicemonitor_across_namespaces]

* If using the Prometheus operator and your Prometheus instance is not in the same namespace as the ECK operator you will need the Prometheus operator configured with the following Helm values:

```yaml
prometheus:
  prometheusSpec:
    podMonitorNamespaceSelector: {}
    podMonitorSelectorNilUsesHelmValues: false
    serviceMonitorNamespaceSelector: {}
    serviceMonitorSelectorNilUsesHelmValues: false
```


## Optional settings to allow full TLS verification when using a custom TLS certificate [k8s_optional_settings_to_allow_full_tls_verification_when_using_a_custom_tls_certificate]

If you are using a custom TLS certificate and you need to set `insecureSkipVerify` to `false` you will need to do the following:

* Create a Kubernetes secret within the Prometheus namespace that contains the Certificate Authority in PEM format.

The easiest way to create the CA secret within the Prometheus namespace is to use the `kubectl create secret generic` command. For example:

```sh
kubectl create secret generic eck-metrics-tls-ca -n monitoring --from-file=ca.crt=/path/to/ca.pem
```

* Ensure that the CA secret is mounted within the Prometheus Pod.

This will vary between Prometheus installations, but if using the Prometheus operator you can set the `spec.secrets` field of the `Prometheus` custom resource to the name of the previously created Kubernetes Secret. See the [ECK Helm chart values file](https://github.com/elastic/cloud-on-k8s/tree/2.16/deploy/eck-operator/values.yaml) for more information.


