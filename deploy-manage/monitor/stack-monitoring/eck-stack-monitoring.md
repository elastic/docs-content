---
navigation_title: "Elastic Cloud on Kubernetes (ECK)"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-monitoring.html
applies_to:
  deployment:
    eck: all
---

# Enable stack monitoring on ECK deployments [k8s-stack-monitoring]

You can enable [Stack Monitoring](/deploy-manage/monitor.md) on Elasticsearch, Kibana, Beats and Logstash to collect and ship their metrics and logs to a monitoring cluster. Although self-monitoring is possible, it is advised to use a [separate monitoring cluster](/deploy-manage/monitor/stack-monitoring.md).

To enable Stack Monitoring, simply reference the monitoring Elasticsearch cluster in the `spec.monitoring` section of their specification.

The following example shows how Elastic Stack components can be configured to send their monitoring data to a separate Elasticsearch cluster in the same Kubernetes cluster.

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
      - name: monitoring <1>
        namespace: observability <2>
    logs:
      elasticsearchRefs:
      - name: monitoring <1>
        namespace: observability <2>
  nodeSets:
  - name: default
    count: 1
    config:
      node.store.allow_mmap: false

apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: monitored-sample
spec:
  type: filebeat
  version: 8.16.1
  monitoring:
    metrics:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability <2>
    logs:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability <2>
---
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
    name: monitored-sample
spec:
  version: 8.16.1
  monitoring:
    metrics:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability <2>
    logs:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability <2>
```

1. The same monitoring cluster is used for metrics and logs, but separate clusters could be used.
2. The use of `namespace` is optional if the monitoring Elasticsearch cluster and the monitored Elastic Stack resource are running in the same namespace.


::::{note}
If Logs Stack Monitoring is configured for a Beat, and custom container arguments (`podTemplate.spec.containers[].args`) include `-e`, which enables logging to stderr and disables log file output, this argument will be removed from the Pod to allow the Filebeat sidecar to consume the Beat’s log files.
::::


You can also enable Stack Monitoring on a single Stack component only. In case Elasticsearch is not monitored, other Stack components will not be available on the Stack Monitoring Kibana page (check [View monitoring data in Kibana](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md)).






