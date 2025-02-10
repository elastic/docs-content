---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_audit_logging.html
applies:
  eck: all
---

# Audit logging [k8s_audit_logging]

Audit logs are collected and shipped to the monitoring cluster referenced in the `monitoring.logs` section when audit logging is enabled (it is disabled by default).

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
spec:
  monitoring:
    metrics:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
    logs:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
  nodeSets:
  - name: default
    config:
      # https://www.elastic.co/guide/en/elasticsearch/reference/current/enable-audit-logging.html
      xpack.security.audit.enabled: true
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
spec:
  monitoring:
    metrics:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
    logs:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
  config:
    # https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html
    xpack.security.audit.enabled: true
```

