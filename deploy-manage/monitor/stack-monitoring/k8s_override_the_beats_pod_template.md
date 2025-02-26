---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_override_the_beats_pod_template.html
applies_to:
  deployment:
    eck: all
---

# Override the Beats Pod Template [k8s_override_the_beats_pod_template]

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

