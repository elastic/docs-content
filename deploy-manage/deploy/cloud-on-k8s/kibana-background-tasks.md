---
navigation_title: Background task isolation
applies_to:
  deployment:
    eck: ga 3.6
products:
  - id: cloud-kubernetes
description: Run Kibana background tasks such as alerting rules and reporting in a dedicated pool of pods managed by ECK, separate from the pods that serve the UI.
---

# {{kib}} background task isolation on ECK [k8s-kibana-background-tasks]

{{kib}} runs alerting, actions and reporting as persistent [background tasks](/deploy-manage/distributed-architecture/kibana-tasks-management.md). By default, every instance serves user requests and runs background tasks, so a heavy task workload competes with user traffic for CPU and memory. {{kib}} can [dedicate instances to one of these jobs](/deploy-manage/distributed-architecture/kibana-tasks-management.md#task-manager-dedicated-task-nodes) through the `node.roles` setting.

ECK can manage this split for you. When you set `spec.backgroundTasks` on a {{kib}} resource, ECK runs two pools of pods:

* The **primary pool** serves UI and API requests with `node.roles: ["ui"]`. It is the only pool behind the {{kib}} HTTP Service.
* The **background tasks pool** runs task manager work only, with `node.roles: ["background_tasks"]`.

Without `spec.backgroundTasks`, ECK runs a single pool with all roles.

## Requirements [k8s-kibana-background-tasks-requirements]

* {{kib}} 8.16.0 or later.
* A valid Enterprise license or Enterprise trial license. Refer to [Manage your license in ECK](../../license/manage-your-license-in-eck.md).


## Enable background task isolation [k8s-kibana-background-tasks-enable]

Add `spec.backgroundTasks` to the {{kib}} resource. The following example runs two UI instances and two background task instances:

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: {{version.stack}}
  count: 2 <1>
  elasticsearchRef:
    name: elasticsearch-sample
  backgroundTasks:
    count: 2 <2>
```

1. Number of instances in the primary pool.
2. Number of instances in the background tasks pool.

An empty `backgroundTasks: {}` section is enough to enable the additional pool. The section accepts the following fields:

| Field | Description |
| --- | --- |
| `count` | Number of instances in the background tasks pool. When omitted, ECK does not manage the replica count of the background tasks Deployment, so a [Horizontal Pod Autoscaler](#k8s-kibana-background-tasks-scaling) can own it. |
| `config` | {{kib}} settings for the background tasks pool only, merged on top of `spec.config`. Do not set `node.roles` here, ECK manages it. |
| `resources` | CPU and memory for the `kibana` container of the background tasks pool. Overrides the resources of that container in `spec.podTemplate` and `spec.backgroundTasks.podTemplate`. |
| `podTemplate` | A [Pod Template](https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates) overlay for the background tasks pods, applied as a [strategic merge](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/#use-a-strategic-merge-patch-to-update-a-deployment) on top of `spec.podTemplate`. |

The background tasks pool is a second {{kib}} deployment, so each of its pods needs the same resources as a primary pod. When you don't set `resources`, each background tasks pod is allocated 2Gi of memory with no CPU constraint, matching the primary pool defaults. Make sure your Kubernetes cluster has capacity for the additional pods.

All other fields of the {{kib}} spec, such as `spec.config`, `spec.podTemplate`, `spec.secureSettings`, `spec.elasticsearchRef` and `spec.http`, apply to both pools.

If you set `server.basePath` or `server.rewriteBasePath` in `spec.backgroundTasks.config`, the values must match the primary pool, because both pools share the same HTTP Service.

When you enable background task isolation, ECK restarts your existing pods, restricting them to the `ui` role, and creates a new Deployment for background tasks in the same operation. Background task execution pauses briefly until the first background tasks pod is ready.

To reverse the change, remove `spec.backgroundTasks` and ECK cleans up the extra Deployment automatically.

### Example

The following example keeps the primary pool on frontend nodes and gives the background tasks pool more memory and its own task manager settings:

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: {{version.stack}}
  count: 2
  elasticsearchRef:
    name: elasticsearch-sample
  podTemplate:
    spec:
      nodeSelector:
        type: frontend <1>
  backgroundTasks:
    count: 2
    config:
      xpack.task_manager.poll_interval: 5000 <2>
    resources:
      requests:
        memory: 2Gi
        cpu: 1
      limits:
        memory: 4Gi
        cpu: 2
    podTemplate:
      spec:
        nodeSelector:
          type: workers <3>
```

1. Applies to both pools.
2. Applies to the background tasks pool only.
3. Overrides the node selector inherited from `spec.podTemplate` for the background tasks pods only.

## Check the status [k8s-kibana-background-tasks-status]

Check the status of your pools with `kubectl get kibana`. The top-level `count`, `availableNodes`, and `health` fields aggregate the status for both pools. The `status.pools` section breaks this information down for each pool.

```yaml
status:
  associationStatus: Established
  availableNodes: 4
  count: 4
  elasticsearchAssociationStatus: Established
  health: green
  observedGeneration: 1
  pools:
    backgroundTasks:
      availableNodes: 2
      count: 2
      health: green
      selector: common.k8s.elastic.co/type=kibana,kibana.k8s.elastic.co/name=kibana-sample,kibana.k8s.elastic.co/role=background_tasks
      version: 9.5.2
    primary:
      availableNodes: 2
      count: 2
      health: green
      selector: common.k8s.elastic.co/type=kibana,kibana.k8s.elastic.co/name=kibana-sample,kibana.k8s.elastic.co/role=primary
      version: 9.5.2
  selector: common.k8s.elastic.co/type=kibana,kibana.k8s.elastic.co/name=kibana-sample
  version: 9.5.2
```

`status.pools.backgroundTasks` is only present when `spec.backgroundTasks` is set.

The aggregated health reflects the state of both pools:

* `green`: All pools are healthy.
* `yellow`: The primary pool is serving requests, but a pool is not green, for example while the background tasks pods are starting.
* `red`: The primary pool is not available.

To list the pods of one pool, use the `kibana.k8s.elastic.co/role` label, which has the value `primary` or `background_tasks`:

```sh
kubectl get pods -l kibana.k8s.elastic.co/name=kibana-sample,kibana.k8s.elastic.co/role=background_tasks
```

::::{important}
Requests sent through the HTTP Service, including the task manager health API, are served by the primary pool and do not reflect task execution state. Refer to [Retrieve health data when {{kib}} uses separate task nodes](/troubleshoot/kibana/task-manager.md#task-manager-health-multi-node).
::::

## Scale the pools [k8s-kibana-background-tasks-scaling]

`spec.count` sets the size of the primary pool, and `spec.backgroundTasks.count` sets the size of the background tasks pool.

A [Horizontal Pod Autoscaler](/deploy-manage/autoscaling/autoscaling-in-eck.md#k8s-stateless-autoscaling) that targets the {{kib}} resource through its `scale` subresource scales the primary pool only. To autoscale the background tasks pool, omit `spec.backgroundTasks.count` and target the background tasks Deployment directly. ECK then keeps whatever replica count the autoscaler sets:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: kibana-sample-bg
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kibana-sample-kb-bg <1>
  minReplicas: 1
  maxReplicas: 4
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

1. The background tasks Deployment of the {{kib}} named `kibana-sample`. ECK names it `<kibana-name>-kb-bg`.

Refer to the [{{kib}} task manager scaling guide](/deploy-manage/production-guidance/kibana-task-manager-scaling-considerations.md) to size the background tasks pool.
