---
navigation_title: In ECK
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autoscaling.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stateless-autoscaling.html
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
---
# Autoscaling in {{eck}}

Configure autoscaling for {{es}} deployments in {{eck}}. Learn how to enable autoscaling, define policies, manage resource limits, and monitor scaling. Includes details on autoscaling stateless applications like {{kib}}, APM Server, and Elastic Maps Server.

## Deployments autoscaling on ECK [k8s-autoscaling]

::::{note}
{{es}} autoscaling requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::


ECK can leverage the [autoscaling API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-autoscaling) introduced in {{es}} 7.11 to adjust automatically the number of Pods and the allocated resources in a tier. Currently, autoscaling is supported for {{es}} [data tiers](/manage-data/lifecycle/data-tiers.md) and machine learning nodes.

### Supported Resources for Autoscaling per Elasticsearch Tier

| Tiers | Storage | Memory | CPU |
| --- | ---| --- | --- |
| Data Nodes (except Frozen) | Yes | Calculated proportionally to the required amount of storage | Calculated proportionally to the required amount of memory
| Frozen Nodes | Yes | Yes | Calculated proportionally to the required amount of memory
| Machine Learning | No | Yes | Calculated proportionally to the required amount of memory


### Enable autoscaling [k8s-enable]

To enable autoscaling on an {{es}} cluster, you need to define one or more autoscaling policies. Each autoscaling policy applies to one or more NodeSets which share the same set of roles specified in the `node.roles` setting in the {{es}} configuration.


#### Define autoscaling policies [k8s-autoscaling-policies]

Autoscaling policies can be defined in an `ElasticsearchAutoscaler` resource. Each autoscaling policy must have the following fields:

* `name` is a unique name used to identify the autoscaling policy.
* `roles` contains a set of node roles, unique across all the autoscaling policies, used to identify the NodeSets to which this policy applies. At least one NodeSet with the exact same set of roles must exist in the {{es}} resource specification.
* `resources` helps define the minimum and maximum compute resources usage:

    * `nodeCount` defines the minimum and maximum nodes allowed in the tier.
    * `cpu` and `memory` enforce minimum and maximum compute resources usage for the {{es}} container.
    * `storage` enforces minimum and maximum storage request per PersistentVolumeClaim.


If there is no recommendation from the Autoscaling API for a given resource, and if this resource is not set in the policy, then the resource is not managed by the operator and existing requirements in the NodeSets remain unchanged.

```yaml
apiVersion: autoscaling.k8s.elastic.co/v1alpha1
kind: ElasticsearchAutoscaler
metadata:
  name: autoscaling-sample
spec:
  ## The name of the Elasticsearch cluster to be scaled automatically.
  elasticsearchRef:
    name: elasticsearch-sample
  ## The autoscaling policies.
  policies:
    - name: data-ingest
      roles: ["data", "ingest" , "transform"]
      resources:
        nodeCount:
          min: 3
          max: 8
        cpu:
          min: 2
          max: 8
        memory:
          min: 2Gi
          max: 16Gi
        storage:
          min: 64Gi
          max: 512Gi
    - name: ml
      roles:
        - ml
      resources:
        nodeCount:
          min: 1
          max: 9
        cpu:
          min: 1
          max: 4
        memory:
          min: 2Gi
          max: 8Gi
        storage:
          min: 1Gi
          max: 1Gi
```

::::{warning}
A node role should not be referenced in more than one autoscaling policy.
::::


In the case of storage the following restrictions apply:

* Scaling the storage size automatically requires the `ExpandInUsePersistentVolumes` feature to be enabled. It also requires a storage class that supports [volume expansion](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/).
* Only one persistent volume claim per {{es}} node is supported when autoscaling is enabled.
* Volume size cannot be scaled down.
* Scaling up (vertically) is only supported if the available capacity in a PersistentVolume matches the capacity claimed in the PersistentVolumeClaim. Refer to the next section for more information.


#### Scale Up and Scale Out [k8s-autoscaling-algorithm]

In order to adapt the resources to the workload, the operator first attempts to scale up the resources (cpu, memory, and storage) allocated to each node in the NodeSets. The operator always ensures that the requested resources are within the limits specified in the autoscaling policy. If each individual node has reached the limits specified in the autoscaling policy, but more resources are required to handle the load, then the operator adds some nodes to the NodeSets. Nodes are added up to the `max` value specified in the `nodeCount` of the policy.

::::{warning}
Scaling up (vertically) is only supported if the actual storage capacity of the persistent volumes matches the capacity claimed. If the physical capacity of a PersistentVolume may be greater than the capacity claimed in the PersistentVolumeClaim, it is advised to set the same value for the `min` and the `max` setting of each resource. It is however still possible to let the operator scale out the NodeSets automatically, as in the following example:
::::


```yaml
apiVersion: autoscaling.k8s.elastic.co/v1alpha1
kind: ElasticsearchAutoscaler
metadata:
  name: autoscaling-sample
spec:
  elasticsearchRef:
    name: elasticsearch-sample
  policies:
    - name: data-ingest
      roles: ["data", "ingest" , "transform"]
      resources:
        nodeCount:
          min: 3
          max: 9
        cpu:
          min: 4
          max: 4
        memory:
          min: 16Gi
          max: 16Gi
        storage:
          min: 512Gi
          max: 512Gi
```


#### Set the limits [k8s-autoscaling-resources]

The value set for memory and CPU limits are computed by applying a ratio to the calculated resource request. The default ratio between the request and the limit for both CPU and memory is 1. This means that request and limit have the same value. You can change the default ratio between the request and the limit for both the CPU and memory ranges by using the `requestsToLimitsRatio` field.

For example, you can set a CPU limit to twice the value of the request, as follows:

```yaml
apiVersion: autoscaling.k8s.elastic.co/v1alpha1
kind: ElasticsearchAutoscaler
metadata:
  name: autoscaling-sample
spec:
  elasticsearchRef:
    name: elasticsearch-sample
  policies:
    - name: data-ingest
      roles: ["data", "ingest" , "transform"]
      resources:
        nodeCount:
          min: 2
          max: 5
        cpu:
          min: 1
          max: 2
          requestsToLimitsRatio: 2
        memory:
          min: 2Gi
          max: 6Gi
        storage:
          min: 512Gi
          max: 512Gi
```

You can find [a complete example in the ECK GitHub repository](https://github.com/elastic/cloud-on-k8s/blob/{{version.eck | M.M}}/config/recipes/autoscaling/elasticsearch.yaml) which will also show you how to fine-tune the [autoscaling deciders](/deploy-manage/autoscaling/autoscaling-deciders.md).


#### Change the polling interval [k8s-autoscaling-polling-interval]

The {{es}} autoscaling capacity endpoint is polled every minute by the operator. This interval duration can be controlled using the `pollingPeriod` field in the autoscaling specification:

```yaml
apiVersion: autoscaling.k8s.elastic.co/v1alpha1
kind: ElasticsearchAutoscaler
metadata:
  name: autoscaling-sample
spec:
  pollingPeriod: "42s"
  elasticsearchRef:
    name: elasticsearch-sample
  policies:
    - name: data-ingest
      roles: ["data", "ingest" , "transform"]
      resources:
        nodeCount:
          min: 2
          max: 5
        cpu:
          min: 1
          max: 2
        memory:
          min: 2Gi
          max: 6Gi
        storage:
          min: 512Gi
          max: 512Gi
```


### Monitoring [k8s-monitoring]


#### Autoscaling status [k8s-autoscaling-status]

In addition to the logs generated by the operator, an autoscaling status is maintained in the `ElasticsearchAutoscaler` resource. This status holds several `Conditions` to summarize the health and the status of the autoscaling mechanism. For example, dedicated `Conditions` may report if the controller cannot connect to the {{es}} cluster, or if a resource limit has been reached:

```sh
kubectl get elasticsearchautoscaler autoscaling-sample \
    -o jsonpath='{ .status.conditions }' | jq
```

```json subs=true
[
 {
   "lastTransitionTime": "2022-09-09T08:07:10Z",
   "message": "Limit reached for policies data-ingest",
   "status": "True",
   "type": "Limited"
 },
  {
   "lastTransitionTime": "2022-09-09T07:55:08Z",
   "status": "True",
   "type": "Active"
 },
 {
   "lastTransitionTime": "2022-09-09T08:07:10Z",
   "status": "True",
   "type": "Healthy"
 },
 {
   "lastTransitionTime": "2022-09-09T07:56:22Z",
   "message": "{{es}} is available",
   "status": "True",
   "type": "Online"
 }
]
```


#### Expected resources [k8s-autoscaling-expected-resources]

The autoscaler status also contains a `policies` section which describes the expected resources for each NodeSet managed by an autoscaling policy.

```sh
kubectl get elasticsearchautoscaler.autoscaling.k8s.elastic.co/autoscaling-sample \
    -o jsonpath='{ .status.policies }' | jq
```

```json
[
  {
    "lastModificationTime": "2022-10-05T05:47:13Z",
    "name": "data-ingest",
    "nodeSets": [
      {
        "name": "nodeset-1",
        "nodeCount": 2
      }
    ],
    "resources": {
      "limits": {
        "cpu": "1",
        "memory": "2Gi"
      },
      "requests": {
        "cpu": "500m",
        "memory": "2Gi",
        "storage": "1Gi"
      }
    }
  }
]
```


#### Events [k8s-events]

Important events are also reported through Kubernetes events, for example when the maximum autoscaling size limit is reached:

```sh
> kubectl get events

40m  Warning  HorizontalScalingLimitReached  elasticsearch/sample   Can't provide total required storage 32588740338, max number of nodes is 5, requires 6 nodes
```


### Disable autoscaling [k8s-disable]

You can disable autoscaling at any time by deleting the `ElasticsearchAutoscaler` resource. For machine learning the following settings are not automatically reset:

* `xpack.ml.max_ml_node_size`
* `xpack.ml.max_lazy_ml_nodes`
* `xpack.ml.use_auto_machine_memory_percent`

You should adjust those settings manually to match the size of your deployment when you disable autoscaling.

## Autoscaling stateless applications on ECK [k8s-stateless-autoscaling]

::::{note}
This section only applies to stateless applications. Check [{{es}} autoscaling](#k8s-autoscaling) for more details about automatically scaling {{es}}.
::::


The [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale) can be used to automatically scale the deployments of the following resources:

* Kibana
* APM Server
* Elastic Maps Server

These resources expose the `scale` subresource which can be used by the Horizontal Pod Autoscaler controller to automatically adjust the number of replicas according to the CPU load or any other custom or external metric. This example shows how to create an `HorizontalPodAutoscaler` resource to adjust the replicas of a {{kib}} deployment according to the CPU load:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  nodeSets:
    - name: default
      count: 1
      config:
        node.store.allow_mmap: false

apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: kb
spec:
  scaleTargetRef:
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    name: kibana-sample
  minReplicas: 1
  maxReplicas: 4
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```
