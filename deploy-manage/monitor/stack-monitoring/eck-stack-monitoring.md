---
navigation_title: Enable on ECK
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-monitoring.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_how_it_works.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_when_to_use_it.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_override_the_beats_pod_template.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_connect_to_an_external_monitoring_elasticsearch_cluster.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Enable stack monitoring on ECK deployments [k8s-stack-monitoring]

You can enable [Stack Monitoring](/deploy-manage/monitor.md) on {{es}}, {{kib}}, Beats and Logstash to collect and ship their metrics and logs to a monitoring cluster. Although self-monitoring is possible, it is advised to use a [separate monitoring cluster](/deploy-manage/monitor/stack-monitoring.md).

## How stack monitoring works in ECK

In the background, Metricbeat and Filebeat are deployed as sidecar containers in the same Pod as {{es}} and {{kib}}.

Metricbeat is used to collect monitoring metrics, and Filebeat to monitor the {{es}} log files and collect log events.

The two Beats are configured to ship data directly to the monitoring cluster(s) using HTTPS and dedicated Elastic users managed by ECK.

## When to use it

This feature is a good solution if you need to monitor your Elastic applications in restricted Kubernetes environments where you cannot grant the following advanced permissions:

* To Metricbeat, to allow querying the k8s API
* To Filebeat, to deploy a privileged DaemonSet

However, for maximum efficiency and minimizing resource consumption, or advanced use cases that require specific Beats configurations, you can deploy a standalone Metricbeat deployment and a Filebeat DaemonSet. Refer to [Beats configuration examples](/deploy-manage/deploy/cloud-on-k8s/configuration-examples-beats.md) for more information.

## Enable stack monitoring

To enable stack monitoring, reference the monitoring {{es}} cluster in the `spec.monitoring` section of their specification. 

The monitoring cluster must be managed by ECK in the same Kubernetes cluster as the monitored one. To learn how to connect an external monitoring cluster, refer to [Connect to an external monitoring {{es}} cluster](#k8s_connect_to_an_external_monitoring_elasticsearch_cluster).

The following example shows how {{stack}} components can be configured to send their monitoring data to a separate {{es}} cluster in the same Kubernetes cluster. 

You can also do the following: 
* Configure an {{es}} cluster to monitor itself. This is not recommended for production deployments.
* Send metrics and logs to two different {{es}} monitoring clusters.
* Enable stack monitoring on a single {{stack}} component only. If {{es}} is not monitored, other {{stack}} components will not be available on the [Stack Monitoring](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md) {{kib}} page.

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
2. The use of `namespace` is optional if the monitoring {{es}} cluster and the monitored {{stack}} resource are running in the same namespace.

::::{note}
If stack monitoring is configured for a Beat, but the corresponding {{es}} cluster is not monitored, the {{kib}} stack monitoring page will not show the Beats data.
::::

::::{note}
If Logs stack monitoring is configured for a Beat, and custom container arguments (`podTemplate.spec.containers[].args`) include `-e`, which enables logging to stderr and disables log file output, this argument will be removed from the Pod to allow the Filebeat sidecar to consume the Beat’s log files.
::::

## Connect to an external monitoring {{es}} cluster [k8s_connect_to_an_external_monitoring_elasticsearch_cluster]

If you want to connect to a monitoring {{es}} cluster not managed by ECK, you can reference a Secret instead of an {{es}} cluster in the `monitoring` section through the `secretName` attribute.

The next example sends cluster metrics to a remote monitoring cluster not managed by ECK, whereas cluster logs are sent to a remote cluster handled by ECK:

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
2. The `namespace` and `serviceName` attributes can only be used in conjunction with `name`, not with `secretName`, and only to reference clusters managed by the same ECK instance.

The referenced Secret must contain the following connection information:

* `url`: The URL to reach the {{es}} cluster
* `username`: The username of the user to be authenticated to the {{es}} cluster
* `password`: The password of the user to be authenticated to the {{es}} cluster
* `ca.crt`: The contents of the CA certificate in PEM format to secure communication to the {{es}} cluster (optional)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: monitoring-metrics-es-ref
stringData:
  url: <ELASTIC_CLOUD_URL>:9243
  username: monitoring-user
  password: <password>
```

The user referenced in the Secret must have been created beforehand.

## Override the Beats Pod template

You can customize the Filebeat and Metricbeat containers through the Pod template. Your configuration is merged with the values of the default Pod template that ECK uses.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
spec:
  monitoring:
    metrics:
      elasticsearchRef:
        name: monitoring
        namespace: observability
    logs:
      elasticsearchRef:
        name: monitoring
        namespace: observability
  nodeSets:
  - name: default
    podTemplate:
      spec:
        containers:
        - name: metricbeat
          env:
          - foo: bar
        - name: filebeat
          env:
          - foo: bar
```
