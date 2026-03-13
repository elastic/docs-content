---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-advanced-node-scheduling.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Advanced {{es}} node scheduling [k8s-advanced-node-scheduling]

{{eck}} (ECK) offers full control over {{es}} cluster nodes scheduling by combining {{es}} configuration with Kubernetes scheduling options:

* [Define {{es}} nodes roles](#k8s-define-elasticsearch-nodes-roles)
* [Pod affinity and anti-affinity](#k8s-affinity-options)
* [Topology spread constraints and availability zone awareness](#k8s-availability-zone-awareness)
  * [Zone awareness using the `zoneAwareness` field](#k8s-zone-awareness) {applies_to}`eck: ga 3.4`
  * [Manual zone awareness configuration](#k8s-zone-awareness-manual)
* [Hot-warm topologies](#k8s-hot-warm-topologies)

You can combine these features to deploy a production-grade {{es}} cluster.

## Define {{es}} nodes roles [k8s-define-elasticsearch-nodes-roles]

You can configure {{es}} nodes with [one or multiple roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md).

::::{tip}
You can use [YAML anchors](https://yaml.org/spec/1.2/spec.html#id2765878) to declare the configuration change once and reuse it across all the node sets.
::::


This allows you to describe an {{es}} cluster with 3 dedicated master nodes, for example:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  # 3 dedicated master nodes
  - name: master
    count: 3
    config:
      node.roles: ["master"]
  # 3 ingest-data nodes
  - name: ingest-data
    count: 3
    config:
      node.roles: ["data", "ingest"]
```


## Affinity options [k8s-affinity-options]

You can set up various [affinity and anti-affinity options](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) through the `podTemplate` section of the {{es}} resource specification.

### A single {{es}} node per Kubernetes host (default) [k8s_a_single_elasticsearch_node_per_kubernetes_host_default]

To avoid scheduling several {{es}} nodes from the same cluster on the same host, use a `podAntiAffinity` rule based on the hostname and the cluster name label:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        affinity:
          podAntiAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    elasticsearch.k8s.elastic.co/cluster-name: quickstart
                topologyKey: kubernetes.io/hostname
```

This is ECK default behavior if you don’t specify any `affinity` option. To explicitly disable the default behavior, set an empty affinity object:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        affinity: {}
```

The default affinity is using `preferredDuringSchedulingIgnoredDuringExecution`, which acts as best effort and won’t prevent an {{es}} node from being scheduled on a host if there are no other hosts available. Scheduling a 4-nodes {{es}} cluster on a 3-host Kubernetes cluster would then successfully schedule 2 {{es}} nodes on the same host. To enforce a strict single node per host, specify `requiredDuringSchedulingIgnoredDuringExecution` instead:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  elasticsearch.k8s.elastic.co/cluster-name: quickstart
              topologyKey: kubernetes.io/hostname
```


### Local Persistent Volume constraints [k8s_local_persistent_volume_constraints]

By default, volumes can be bound to a Pod before the Pod gets scheduled to a particular Kubernetes node. This can be a problem if the PersistentVolume can only be accessed from a particular host or set of hosts. Local persistent volumes are a good example: they are accessible from a single host. If the Pod gets scheduled to a different host based on any affinity or anti-affinity rule, the volume may not be available.

To solve this problem, you can [set the Volume Binding Mode](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode) of the `StorageClass` you are using. Make sure `volumeBindingMode: WaitForFirstConsumer` is set, [especially if you are using local persistent volumes](https://kubernetes.io/docs/concepts/storage/volumes/#local).

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```


### Node affinity [k8s_node_affinity]

To restrict the scheduling to a particular set of Kubernetes nodes based on labels, use a [NodeSelector](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector). The following example schedules {{es}} Pods on Kubernetes nodes tagged with both labels `diskType: ssd` and `environment: production`.

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        nodeSelector:
          diskType: ssd
          environment: production
```

You can achieve the same (and more) with [node affinity](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#node-affinity-beta-feature):

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: environment
                  operator: In
                  values:
                  - e2e
                  - production
            preferredDuringSchedulingIgnoredDuringExecution:
              - weight: 1
                preference:
                  matchExpressions:
                  - key: diskType
                    operator: In
                    values:
                    - ssd
```

This example restricts {{es}} nodes so they are only scheduled on Kubernetes hosts tagged with `environment: e2e` or `environment: production`. It favors nodes tagged with `diskType: ssd`.



## Topology spread constraints and availability zone awareness [k8s-availability-zone-awareness]

Distributing {{es}} nodes and shard replicas across failure domains (typically cloud availability zones) is a fundamental requirement for production clusters. ECK provides built-in zone awareness support and also allows manual configuration for advanced use cases.

### Zone awareness using the `zoneAwareness` field [k8s-zone-awareness]

{applies_to}`eck: ga 3.4`

The `zoneAwareness` field on NodeSets is the recommended way to set up availability zone awareness. Instead of manually configuring topology spread constraints, downward node labels, environment variables, and {{es}} allocation awareness settings yourself, you add a single `zoneAwareness` field and ECK handles the rest.

When `zoneAwareness` is set on a NodeSet, the operator automatically:

* Injects a `TopologySpreadConstraint` with `maxSkew: 1` and `whenUnsatisfiable: DoNotSchedule` to evenly spread pods across zones.
* Exposes the Kubernetes node's zone as a `ZONE` environment variable inside each pod using [downward node labels](#k8s-availability-zone-awareness-downward-api).
* Sets `node.attr.zone` and `cluster.routing.allocation.awareness.attributes: k8s_node_name,zone` in the {{es}} configuration.
* Injects a required node affinity rule ensuring that the topology key label exists on the node, so pods are only placed on nodes that carry the label.
* When `zones` are specified, additionally restricts pod placement to those specific zones.

#### Minimal zone awareness

To spread pods across all available zones using defaults:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 6
    zoneAwareness: {}
```

#### Zone awareness with explicit zones

To restrict pods to specific availability zones:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: hot
    count: 6
    config:
      node.roles: ["data_hot"]
    zoneAwareness:
      zones:
        - us-east1-a
        - us-east1-b
        - us-east1-c
```

#### Zone awareness with custom topology key

By default, `zoneAwareness` uses the `topology.kubernetes.io/zone` node label. To use a different label:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 6
    zoneAwareness:
      topologyKey: my.custom/zone-label
```

#### Customizing spread behavior

To customize `maxSkew`, `whenUnsatisfiable`, or other topology spread constraint fields, provide a `topologySpreadConstraint` for the same `topologyKey` in the `podTemplate`. The operator preserves user-provided constraints and does not inject its own default for that key:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 6
    zoneAwareness:
      topologyKey: topology.kubernetes.io/zone
    podTemplate:
      spec:
        topologySpreadConstraints:
        - topologyKey: topology.kubernetes.io/zone
          maxSkew: 3
          whenUnsatisfiable: ScheduleAnyway
```

#### Mixed NodeSets with and without zone awareness

Enable `zoneAwareness` on **all** NodeSets in a cluster for the best results. If some NodeSets are accidentally left without `zoneAwareness`, the operator applies safeguards to keep the cluster consistent:

* All NodeSets in the cluster still receive the `ZONE` environment variable and {{es}} zone configuration (`node.attr.zone`, `cluster.routing.allocation.awareness.attributes`) so that shard allocation awareness works cluster-wide.
* Non-zoneAware NodeSets receive a required node affinity ensuring that the topology key exists for nodes that carry the topology label, but they do not receive topology spread constraints and may not be evenly distributed across zones.

::::{important}
Adding `zoneAwareness` to any NodeSet triggers a one-time rolling restart of **all** NodeSets in the cluster, because zone-related {{es}} configuration and environment variables are applied cluster-wide. To avoid unnecessary restarts, enable `zoneAwareness` on every NodeSet at the same time.
::::

#### Validation rules

* All zone-aware NodeSets in a cluster must use the same `topologyKey`.
* When using the default topology key (`topology.kubernetes.io/zone`), the operator allows it automatically if the `--exposed-node-labels` flag is unset or empty. If `--exposed-node-labels` is explicitly set to a non-empty value, the default topology key must also be included in the allowed list. Custom topology keys must always be allowed by the operator’s `--exposed-node-labels` configuration.
* The `zones` list, when specified, must contain at least one entry and no duplicates.

### Manual zone awareness configuration [k8s-zone-awareness-manual]

For ECK versions before 3.4.0, or for advanced use cases not covered by the `zoneAwareness` field, you can manually configure availability zone awareness. The following section describes how to manually configure availability zone awareness.

#### Exposing Kubernetes node topology labels in Pods [k8s-availability-zone-awareness-downward-api]

:::{note}
Starting with Kubernetes 1.35 and later, the `PodTopologyLabelsAdmission` feature is enabled by default. As a result, the labels `topology.kubernetes.io/region` and `topology.kubernetes.io/zone` from the node are automatically propagated as labels on Pods. This means that you can skip using the `eck.k8s.elastic.co/downward-node-labels` annotation and avoid making additional configuration changes to expose these topology labels in your Pods. In this situation, you can skip the first two steps described below. Additionally, in this scenario, node labels appear as Pod labels rather than annotations.
:::

1. First, ensure that the operator’s flag `exposed-node-labels` contains the list of the Kubernetes node labels that should be exposed in the {{es}} Pods. If you are using the provided installation manifest, or the Helm chart, then this flag is already preset with two wildcard patterns for well-known node labels that describe Kubernetes cluster topology, like `topology.kubernetes.io/.*` and `failure-domain.beta.kubernetes.io/.*`.
2. On the {{es}} resources set the `eck.k8s.elastic.co/downward-node-labels` annotations with the list of the Kubernetes node labels that should be copied as Pod annotations.
3. Use the [Kubernetes downward API](https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/) in the `podTemplate` to make those annotations available as environment variables in {{es}} Pods.

Refer to the next section or to the [{{es}} sample resource in the ECK source repository](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/samples/elasticsearch/elasticsearch.yaml) for a complete example.


#### Using node topology labels, Kubernetes topology spread constraints, and {{es}} shard allocation awareness [k8s-availability-zone-awareness-example]

The following example demonstrates how to use the `topology.kubernetes.io/zone` node labels to spread a NodeSet across the availability zones of a Kubernetes cluster.

By default ECK creates a `k8s_node_name` attribute with the name of the Kubernetes node running the Pod, and configures {{es}} to use this attribute. This ensures that {{es}} allocates primary and replica shards to Pods running on different Kubernetes nodes and never to Pods that are scheduled onto the same Kubernetes node. To preserve this behavior while making {{es}} aware of the availability zone, include the `k8s_node_name` attribute in the comma-separated `cluster.routing.allocation.awareness.attributes` list.

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  annotations:
    eck.k8s.elastic.co/downward-node-labels: "topology.kubernetes.io/zone"
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    config:
      node.attr.zone: ${ZONE}
      cluster.routing.allocation.awareness.attributes: k8s_node_name,zone
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          env:
          - name: ZONE
            valueFrom:
              fieldRef:
                fieldPath: metadata.annotations['topology.kubernetes.io/zone']
        topologySpreadConstraints:
          - maxSkew: 1
            topologyKey: topology.kubernetes.io/zone
            whenUnsatisfiable: DoNotSchedule
            labelSelector:
              matchLabels:
                elasticsearch.k8s.elastic.co/cluster-name: quickstart
                elasticsearch.k8s.elastic.co/statefulset-name: quickstart-es-default
```

This example relies on:

* Kubernetes nodes in each zone being labeled accordingly. `topology.kubernetes.io/zone` [is standard](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#interlude-built-in-node-labels), but any label can be used.
* [Pod topology spread constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/) to spread the Pods across availability zones in the Kubernetes cluster.
* {{es}} configured to [allocate shards based on node attributes](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md). Here we specified `node.attr.zone`, but any attribute name can be used. `node.attr.rack_id` is another common example.



## Hot-warm topologies [k8s-hot-warm-topologies]

By combining [{{es}} shard allocation awareness](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md) with [Kubernetes node affinity](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#node-affinity-beta-feature), you can set up an {{es}} cluster with hot-warm topology:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  # hot nodes, with high CPU and fast IO
  - name: hot
    count: 3
    config:
      node.roles: ["data_hot", "ingest", "master"]
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          resources:
            limits:
              memory: 16Gi
              cpu: 4
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: beta.kubernetes.io/instance-type
                  operator: In
                  values:
                  - highio
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 1Ti
        storageClassName: local-storage
  # warm nodes, with high storage
  - name: warm
    count: 3
    config:
      node.roles: ["data_warm"]
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          resources:
            limits:
              memory: 16Gi
              cpu: 2
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: beta.kubernetes.io/instance-type
                  operator: In
                  values:
                  - highstorage
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 10Ti
        storageClassName: local-storage
```

In this example, we configure two groups of {{es}} nodes:

* The first group has the `data` attribute set to `hot`. It is intended to run on hosts with high CPU resources and fast IO (SSD). Pods can only be scheduled on Kubernetes nodes labeled with `beta.kubernetes.io/instance-type: highio` (to adapt to the labels of your Kubernetes nodes).
* The second group has the `data` attribute set to `warm`. It is intended to run on hosts with larger but maybe slower storage. Pods can only be scheduled on nodes labeled with `beta.kubernetes.io/instance-type: highstorage`.

::::{note}
This example uses [Local Persistent Volumes](https://kubernetes.io/docs/concepts/storage/volumes/#local) for both groups, but can be adapted to use high-performance volumes for `hot` {{es}} nodes and high-storage volumes for `warm` {{es}} nodes.
::::

Finally, set up [Index Lifecycle Management](/manage-data/lifecycle/index-lifecycle-management.md) policies on your indices, [optimizing for hot-warm architectures](https://www.elastic.co/blog/implementing-hot-warm-cold-in-elasticsearch-with-index-lifecycle-management).


