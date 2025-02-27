---
navigation_title: "Connect to an external cluster"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_connect_to_an_external_monitoring_elasticsearch_cluster.html
applies_to:
  deployment:
    eck: all
---

# Connect to an external monitoring Elasticsearch cluster [k8s_connect_to_an_external_monitoring_elasticsearch_cluster]

If you want to connect to a monitoring Elasticsearch cluster not managed by ECK, you can reference a Secret instead of an Elastisearch cluster in the `monitoring` section through the `secretName` attribute:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: monitored-sample
  namespace: production
spec:
  version: 8.16.1
  monitoring:
    metrics:
      elasticsearchRefs:
      - secretName: monitoring-metrics-es-ref <1>
    logs:
      elasticsearchRefs:
      - name: monitoring-logs
        namespace: observability <2>
        serviceName: monitoring-logs-es-coordinating-nodes <2>
  nodeSets:
  - name: default
    count: 1
    config:
      node.store.allow_mmap: false
```

1. The `secretName` and `name` attributes are mutually exclusive, you have to choose one or the other.
2. The `namespace` and `serviceName` attributes can only be used in conjunction with `name`, not with `secretName`.


The referenced Secret must contain the following connection information:

* `url`: the URL to reach the Elasticsearch cluster
* `username`: the username of the user to be authenticated to the Elasticsearch cluster
* `password`: the password of the user to be authenticated to the Elasticsearch cluster
* `ca.crt`: the contents of the CA certificate in PEM format to secure communication to the Elasticsearch cluster (optional)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: monitoring-metrics-es-ref
stringData:
  url: https://mon1.es.abcd-42.xyz.elastic-cloud.com:9243
  username: monitoring-user
  password: REDACTED
```

The user referenced in the Secret must have been created beforehand.

