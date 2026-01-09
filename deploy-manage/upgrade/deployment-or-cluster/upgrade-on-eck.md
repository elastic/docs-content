---
navigation_title: Upgrade on {{eck}}
applies_to:
  deployment:
    eck: ga
products:
  - id: kibana
  - id: cloud-kubernetes
  - id: elasticsearch
---
# Upgrade your deployment on {{eck}} (ECK)

The ECK orchestrator can safely perform upgrades to newer versions of the {{stack}}.

Before you start the upgrade, [plan your upgrade](/deploy-manage/upgrade/plan-upgrade.md), [take the upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md), and ensure your ECK version is [compatible](/deploy-manage/deploy/cloud-on-k8s.md#stack-compatibility) with the {{stack}} version you’re upgrading to. If it's incompatible, [upgrade your orchestrator](/deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) first.

## How ECK manages upgrades

ECK ensures that {{stack}} components are upgraded in the correct order. Upgrades to dependent resources are delayed until that dependency is upgraded. For example, the {{kib}} upgrade starts only when the associated {{es}} cluster has been upgraded.

Check out [Nodes orchestration](/deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md) for more information on how ECK manages upgrades and how to tune its behavior.

## Perform the upgrade

The upgrade procedure depends on whether you are deploying the {{stack}} components using resource manifests or the [`eck-stack` Helm chart](/deploy-manage/deploy/cloud-on-k8s/managing-deployments-using-helm-chart.md).

### Upgrade using resource manifests

1. In the resource spec file, modify the `version` field for the desired {{stack}} version.
2. Save your changes. The orchestrator will start the upgrade process automatically.

In this example, we’re upgrading {{es}} and {{kib}} to {{version.stack}}.

:::{important}
For production use, for {{stack}} version 8.16 and later, set the `vm.max_map_count` kernel setting to `1048576`; for {{stack}} version 8.15 and earlier, set `vm.max_map_count` to `262144`. Refer to [Virtual memory](/deploy-manage/deploy/cloud-on-k8s/virtual-memory.md) for more information.
:::

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
  namespace: production
spec:
  version: {{version.stack}}
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
          command: ['sh', '-c', 'sysctl -w vm.max_map_count=1048576']
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
          command: ['sh', '-c', 'sysctl -w vm.max_map_count=1048576']
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
  version: {{version.stack}}
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

### Upgrade using Helm charts

If you deploy your {{stack}} resources using our Helm chart, refer to [managing deployments using Helm chart](/deploy-manage/deploy/cloud-on-k8s/managing-deployments-using-helm-chart.md#k8s-upgrade-modify-helm) for details on how to perform upgrades with Helm.

## Next steps

Once you've successfully upgraded your deployment, you can [upgrade your ingest components](/deploy-manage/upgrade/ingest-components.md), such as {{ls}}, {{agents}}, or {{beats}}.
