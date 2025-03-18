---
navigation_title: "Upgrade on {{eck}}"
---

# Upgrade your deployment on {{eck}} (ECK)

The ECK orchestrator can safely perform upgrades to newer versions of the {{stack}}. 

Once you are prepared to upgrade, ensure the ECK version is [compatible](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-supported.html) with the {{stack}} version you’re upgrading to. If it's incompatible, [upgrade your orchestrator](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md). 

% Note: Add a link once confirmed where prepare to upgrade will reside in TOC. 

## Perform the upgrade 

1. In the resource spec file, modify the `version` field for the desired {{stack}} version. 
2. Save your changes. The orchestrator will start the upgrade process automatically. 

In this example, we’re modifying the version to `9.0.0`. 

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
  namespace: production
spec:
  version: 9.0.0
  monitoring:
    metrics:
      elasticsearchRefs:
        - name: monitoring-cluster
          namespace: observability
    logs:
      elasticsearchRefs:
        - name: monitoring-cluster
          namespace: observability
  http:
    service:
      spec:
        type: LoadBalancer
  nodeSets:
  - name: master
    count: 3
    config:
      node.roles: ["master"]
      xpack.ml.enabled: true
      node.store.allow_mmap: false
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 20Gi
        storageClassName: standard
    podTemplate:
      metadata:
        labels:
          key: sample
      spec:
        initContainers:
        - name: sysctl
          securityContext:
            privileged: true
          command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
        containers:
        - name: elasticsearch
          resources:
            requests:
              memory: 2Gi
              cpu: 0.5
            limits:
              memory: 2Gi
              cpu: 1
  - name: data
    count: 3
    config:
      node.roles: ["data", "ingest", "ml", "transform"]
      node.store.allow_mmap: false
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 20Gi
        storageClassName: standard
    podTemplate:
      metadata:
        labels:
          key: sample
      spec:
        initContainers:
        - name: sysctl
          securityContext:
            privileged: true
          command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
        containers:
        - name: elasticsearch
          resources:
            requests:
              memory: 2Gi
              cpu: 0.5
            limits:
              memory: 2Gi
              cpu: 1
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
  namespace: production
spec:
  version: 9.0.0
  monitoring:
    metrics:
      elasticsearchRefs:
        - name: monitoring-cluster
          namespace: observability
    logs:
      elasticsearchRefs:
        - name: monitoring-cluster
          namespace: observability
  http:
    service:
      spec:
        type: LoadBalancer
  count: 1
  elasticsearchRef:
    name: elasticsearch-sample
```

ECK will ensure that {{stack}} components are upgraded in the correct order. Upgrades to dependent resources are delayed until that dependency is upgraded. For example, the {{kib}} upgrade will start only when the associated {{es}} cluster has been upgraded.

Check out [Nodes orchestration](/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md) for more information on how ECK manages upgrades and how to tune its behavior.

## Next steps

Once you've successfully upgraded your deployment, [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md), such as {{ls}}, {{agents}}, or {{beats}}. 
