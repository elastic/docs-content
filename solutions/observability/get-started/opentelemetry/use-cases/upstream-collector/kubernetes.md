---
navigation_title: On Kubernetes
description: Deploy an EDOT Collector gateway on Kubernetes to receive telemetry from a contrib OpenTelemetry Collector and forward it to Elasticsearch.
applies_to:
  stack: ga 9.2+
products:
  - id: observability
  - id: edot-collector
---

# Deploy the EDOT gateway on {{k8s}} [upstream-collector-k8s]

This page extends [Send data from a contrib OpenTelemetry Collector](/solutions/observability/get-started/opentelemetry/use-cases/upstream-collector/index.md) with {{k8s}}-specific deployment steps. If you haven't read that page, start there for context on the architecture and components.

In {{k8s}}, you deploy the EDOT gateway as a `Deployment` and expose it as a `Service` so contrib Collectors can reach it using cluster DNS.

The EDOT Collector image for standalone use is `docker.elastic.co/elastic-agent/elastic-otel-collector`. Unlike the full {{agent}} image, this image's entrypoint unconditionally starts in `otel` mode — no extra environment variables are required.

## Prerequisites

* A running {{k8s}} cluster
* `kubectl` configured to access the cluster
* A running self-managed {{es}} cluster reachable from the {{k8s}} cluster

::::{stepper}

:::{step} Create a secret for credentials

```bash
kubectl create secret generic elastic-secret-otel \
  --from-literal=elastic_endpoint='https://your-elasticsearch:9200' \
  --from-literal=elastic_api_key='your-encoded-api-key'
```

:::

:::{step} Deploy the EDOT gateway

Apply the following manifest. The `ConfigMap` holds the gateway configuration, the `Deployment` runs the EDOT Collector, and the `Service` exposes port 4317 for contrib Collectors inside the cluster.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: edot-gateway-config
data:
  gateway.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
    connectors:
      elasticapm: {}
    processors:
      batch:
        send_batch_size: 1000
        timeout: 1s
        send_batch_max_size: 1500
      batch/metrics:
        send_batch_max_size: 0
        timeout: 1s
      elasticapm: {}
    exporters:
      elasticsearch/otel:
        endpoints:
          - ${env:ELASTIC_ENDPOINT}
        api_key: ${env:ELASTIC_API_KEY}
        mapping:
          mode: otel
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch, elasticapm]
          exporters: [elasticapm, elasticsearch/otel]
        metrics:
          receivers: [otlp]
          processors: [batch/metrics]
          exporters: [elasticsearch/otel]
        metrics/aggregated-otel-metrics:
          receivers: [elasticapm]
          processors: []
          exporters: [elasticsearch/otel]
        logs:
          receivers: [otlp]
          processors: [batch]
          exporters: [elasticsearch/otel]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: edot-gateway
  labels:
    app: edot-gateway
spec:
  replicas: 2
  selector:
    matchLabels:
      app: edot-gateway
  template:
    metadata:
      labels:
        app: edot-gateway
    spec:
      containers:
        - name: edot-gateway
          image: docker.elastic.co/elastic-agent/elastic-otel-collector:{{version.edot_collector}}
          args: ["--config", "/etc/edot/gateway.yaml"]
          env:
            - name: ELASTIC_ENDPOINT
              valueFrom:
                secretKeyRef:
                  name: elastic-secret-otel
                  key: elastic_endpoint
            - name: ELASTIC_API_KEY
              valueFrom:
                secretKeyRef:
                  name: elastic-secret-otel
                  key: elastic_api_key
          ports:
            - containerPort: 4317  # gRPC
            - containerPort: 4318  # HTTP
          volumeMounts:
            - name: config
              mountPath: /etc/edot
      volumes:
        - name: config
          configMap:
            name: edot-gateway-config
---
apiVersion: v1
kind: Service
metadata:
  name: edot-gateway
spec:
  selector:
    app: edot-gateway
  ports:
    - name: otlp-grpc
      port: 4317
      targetPort: 4317
    - name: otlp-http
      port: 4318
      targetPort: 4318
```

:::

:::{step} Configure the contrib Collector

Point the contrib Collector's OTLP exporter at the gateway `Service`:

```yaml
exporters:
  otlp:
    endpoint: "edot-gateway:4317"
    tls:
      insecure: true  # Set to `false` and configure `ca_file` for production
```

:::

:::{step} Verify data in {{kib}}

After the gateway pods are running and your contrib Collectors point to the `edot-gateway` Service, confirm that data flows in:

1. Check your services in **{{observability}}** → **{{product.apm}}**.
2. Check the `traces-generic.otel-default`, `logs-generic.otel-default`, and `metrics-generic.otel-default` data streams in **Discover**.

If no data appears, refer to [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md).

:::

::::

:::{note}
For comprehensive {{k8s}} observability (including host metrics, pod logs, {{k8s}} events, and cluster metrics), use the `opentelemetry-kube-stack` Helm chart with the Elastic values instead. Refer to [{{k8s}} observability](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/index.md) for more information.
:::
