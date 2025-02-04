---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-enabling-the-metrics-endpoint.html
---

# Enabling the metrics endpoint [k8s-enabling-the-metrics-endpoint]

The metrics endpoint is not enabled by default. To enable the metrics endpoint, follow the instructions in the next sections depending on whether you installed ECK through the Helm chart or the manifests.

## Using the operator Helm chart [k8s_using_the_operator_helm_chart]

If you installed ECK through the Helm chart commands listed in [Install ECK using the Helm chart](../../deploy/cloud-on-k8s/install-using-helm-chart.md), you can now set  `config.metrics.port` to a value greater than 0 in your values file and the metrics endpoint will be enabled.


## Using the operator manifests [k8s_using_the_operator_manifests]

If you installed ECK using the manifests using the commands listed in [*Deploy ECK in your Kubernetes cluster*](../../deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md) some additional changes will be required to enable the metrics endpoint.

Enable the metrics endpoint in the `ConfigMap`.

```shell
cat <<EOF | kubectl apply -f -
kind: ConfigMap
apiVersion: v1
metadata:
  name: elastic-operator
  namespace: elastic-system
data:
  eck.yaml: |-
    log-verbosity: 0
    metrics-port: 8080
    metrics-host: 0.0.0.0
    container-registry: docker.elastic.co
    max-concurrent-reconciles: 3
    ca-cert-validity: 8760h
    ca-cert-rotate-before: 24h
    cert-validity: 8760h
    cert-rotate-before: 24h
    disable-config-watch: false
    exposed-node-labels: [topology.kubernetes.io/.*,failure-domain.beta.kubernetes.io/.*]
    set-default-security-context: auto-detect
    kube-client-timeout: 60s
    elasticsearch-client-timeout: 180s
    disable-telemetry: false
    distribution-channel: all-in-one
    validate-storage-class: true
    enable-webhook: true
    webhook-name: elastic-webhook.k8s.elastic.co
    webhook-port: 9443
    operator-namespace: elastic-system
    enable-leader-election: true
    elasticsearch-observation-interval: 10s
    ubi-only: false
EOF
```

Patch the `StatefulSet` to expose the metrics port.

```shell
kubectl patch sts -n elastic-system elastic-operator --patch-file=/dev/stdin <<-EOF
spec:
  template:
    spec:
      containers:
        - name: manager
          ports:
          - containerPort: 9443
            name: https-webhook
            protocol: TCP
          - containerPort: 8080
            protocol: TCP
            name: metrics
EOF
```

The ECK operator will be recreated after applying the patch.

If using the Prometheus operator, install a `PodMonitor` to allow scraping of the metrics endpoint by Prometheus.

```shell
cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: elastic-operator
  namespace: elastic-system
  labels:
    control-plane: elastic-operator
    app.kubernetes.io/component: metrics
spec:
  podMetricsEndpoints:
    - port: metrics
      path: /metrics
      interval: 1m
      scrapeTimeout: 30s
  namespaceSelector:
    matchNames:
      - elastic-system
  selector:
    matchLabels:
      control-plane: elastic-operator
EOF
```


