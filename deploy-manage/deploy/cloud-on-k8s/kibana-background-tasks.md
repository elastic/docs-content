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

{{kib}} runs alerting, actions and reporting as persistent [background tasks](/deploy-manage/distributed-architecture/kibana-tasks-management.md). By default every instance serves user requests and runs background tasks, so a heavy task workload competes with user traffic for CPU and memory. {{kib}} can dedicate instances to one of these jobs through the `node.roles` setting. Refer to [Dedicated background task nodes](/deploy-manage/distributed-architecture/kibana-tasks-management.md#task-manager-dedicated-task-nodes).

ECK manages this split for you. When you set `spec.backgroundTasks` on a {{kib}} resource, ECK runs two pools of pods:

* The **primary pool** serves UI and API requests with `node.roles: ["ui"]`.
* The **background tasks pool** runs task manager work only, with `node.roles: ["background_tasks"]`.

Without `spec.backgroundTasks`, ECK runs a single pool with all roles, as before.

::::{note}
{{kib}} background task isolation requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses. Refer to [License checks](#k8s-kibana-background-tasks-license) for the behavior without a license.
::::

## Requirements [k8s-kibana-background-tasks-requirements]

* ECK 3.6 or later.
* {{kib}} 8.16.0 or later. Background tasks pods do not serve `/login`, so ECK probes their readiness through the unauthenticated `/api/status` endpoint introduced in 8.16.0.
* A valid Enterprise license or Enterprise trial license.

## Enable background task isolation [k8s-kibana-background-tasks-enable]

Add `spec.backgroundTasks` to the {{kib}} resource. The following example runs one UI instance and two background task instances:

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

An empty `backgroundTasks: {}` section is enough to enable the split. The section accepts the following fields:

| Field | Description |
| --- | --- |
| `count` | Number of instances in the background tasks pool. When omitted, ECK does not manage the replica count of the background tasks Deployment, so a [Horizontal Pod Autoscaler](#k8s-kibana-background-tasks-scaling) can own it. |
| `config` | {{kib}} settings for the background tasks pool only, merged on top of `spec.config`. Do not set `node.roles` here, ECK manages it. |
| `resources` | CPU and memory for the `kibana` container of the background tasks pool. Overrides the resources of that container in `spec.podTemplate` and `spec.backgroundTasks.podTemplate`. |
| `podTemplate` | A [Pod Template](https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates) overlay for the background tasks pods, applied as a strategic merge on top of `spec.podTemplate`. |

All other fields of the {{kib}} spec, such as `spec.config`, `spec.podTemplate`, `spec.secureSettings`, `spec.elasticsearchRef` and `spec.http`, apply to both pools.

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
        containers:
        - name: kibana
          env:
          - name: NODE_OPTIONS
            value: "--max-old-space-size=3072"
```

1. Applies to both pools.
2. Applies to the background tasks pool only.
3. Overrides the node selector inherited from `spec.podTemplate` for the background tasks pods only.

## What ECK creates [k8s-kibana-background-tasks-resources]

For a {{kib}} named `kibana-sample` with `spec.backgroundTasks` set, ECK manages:

| Resource | Name | Purpose |
| --- | --- | --- |
| Deployment | `kibana-sample-kb` | The primary pool, `node.roles: ["ui"]`. |
| Deployment | `kibana-sample-kb-bg` | The background tasks pool, `node.roles: ["background_tasks"]`. |
| Secret | `kibana-sample-kb-config` | The rendered `kibana.yml` shared by both pools. |
| Secret | `kibana-sample-kb-bg-config` | The rendered `kibana.yml` of the background tasks pool. Only created when `spec.backgroundTasks.config` is set. |
| Service | `kibana-sample-kb-http` | The HTTP Service. It only routes traffic to the primary pool. |

ECK sets the node roles through the `NODE_ROLES` environment variable of the `kibana` container, not in `kibana.yml`. Every pod carries the `kibana.k8s.elastic.co/role` label with the value `primary` or `background_tasks`, and the label is part of the Deployment and Service selectors. A {{kib}} without `spec.backgroundTasks` has the `primary` label too. Use the label to select the pods of one pool:

```sh
kubectl get pods -l kibana.k8s.elastic.co/name=kibana-sample,kibana.k8s.elastic.co/role=background_tasks
```

::::{important}
Requests sent through the HTTP Service, including the task manager health API, are served by the primary pool and do not reflect task execution state. Refer to [Retrieve health data when {{kib}} uses separate task nodes](/troubleshoot/kibana/task-manager.md#task-manager-health-multi-node).
::::

## Check the status [k8s-kibana-background-tasks-status]

The {{kib}} status reports each pool under `status.pools`. The top-level `count`, `availableNodes` and `health` aggregate both pools and are what `kubectl get kibana` shows:

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

`status.pools.backgroundTasks` is only present when `spec.backgroundTasks` is set. The aggregated health is `green` when all pools are green, `yellow` when the primary pool serves requests but a pool is not green, for example while the background tasks pods are starting, and `red` when the primary pool is not available.

## Scale the pools [k8s-kibana-background-tasks-scaling]

`spec.count` sets the size of the primary pool and `spec.backgroundTasks.count` the size of the background tasks pool.

A [Horizontal Pod Autoscaler](/deploy-manage/autoscaling/autoscaling-in-eck.md#k8s-stateless-autoscaling) that targets the {{kib}} resource through its `scale` subresource scales the **primary pool only**. To autoscale the background tasks pool, omit `spec.backgroundTasks.count` and target the background tasks Deployment directly. ECK then keeps whatever replica count the autoscaler sets:

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

1. The background tasks Deployment of the {{kib}} named `kibana-sample`.

Refer to the [{{kib}} task manager scaling guide](/deploy-manage/production-guidance/kibana-task-manager-scaling-considerations.md) to size the background tasks pool.

## Validation rules [k8s-kibana-background-tasks-validation]

When `spec.backgroundTasks` is set, the [validating webhook](configure-validating-webhook.md) rejects a {{kib}} resource if:

* `spec.version` is lower than 8.16.0.
* `node.roles` is set in `spec.config` or `spec.backgroundTasks.config`, or the `NODE_ROLES` environment variable is set on the `kibana` container of either pod template. ECK owns the node roles of both pools.
* The two pools resolve to different base paths. The base path comes from `server.basePath` and `server.rewriteBasePath`, or from the `SERVER_BASEPATH` and `SERVER_REWRITEBASEPATH` environment variables. Both pools share the same HTTP Service, so `spec.backgroundTasks` can repeat the primary values but must not change them.

The operator runs the same checks when the webhook is turned off and reports failures as events on the {{kib}} resource.

## Rollouts to expect [k8s-kibana-background-tasks-rollouts]

**Upgrading ECK.** The first reconciliation by ECK 3.6 or later adds the role label to the pod template of every existing {{kib}}, with or without `spec.backgroundTasks`. Each {{kib}} goes through one rolling update. Selectors are not changed by the upgrade itself.

**Turning isolation on.** ECK rolls the primary pods to the `ui` role and creates the background tasks Deployment in the same reconciliation. The two rollouts are not ordered, so background task execution pauses until the first background tasks pod is ready. No task is lost: the task manager picks up pending work as soon as a pod with the role is running.

Turning isolation on or off also adds or removes the role label in the immutable Deployment selector. ECK migrates the primary Deployment without downtime: it rolls the pods until all carry the label, lets the old ReplicaSets be pruned, then deletes the Deployment with orphan propagation and recreates it with the new selector so it adopts the running pods. The Service selector follows the Deployment selector, so no endpoint is dropped. The migration is deferred while [orchestration is paused](k8s-pause-orchestration.md).

**Turning isolation off.** Remove `spec.backgroundTasks`. ECK rolls the primary pods back to all roles and deletes the background tasks Deployment and its configuration Secret.

**Version upgrades.** [Version upgrades cause {{kib}} downtime](k8s-kibana-advanced-configuration.md#k8s-kibana-configuration) on ECK. With two pools, ECK scales both Deployments to zero before starting the new version, so no two versions run at the same time. The background tasks replica count is saved in the `kibana.k8s.elastic.co/prev-replicas` annotation of the Deployment and restored afterwards, including a count set by a Horizontal Pod Autoscaler.

## License checks [k8s-kibana-background-tasks-license]

ECK checks the Enterprise license in the validating webhook, which rejects a request with a message you see immediately, and in the operator, which logs and adds a Kubernetes event to the {{kib}} resource. The operator check does not depend on the webhook, which [can be turned off](configure-validating-webhook.md#k8s-disable-webhook). Both decide whether the feature is already active by looking for the background tasks Deployment.

With a valid Enterprise license nothing changes. Without one the background tasks cannot be enabled. A {{kib}} that already runs background tasks keeps running them after the license expires, with warning events until you install a license or remove `spec.backgroundTasks`. A {{kib}} cannot be split without a license.

::::{warning}
If the background tasks Deployment is deleted by hand while no valid Enterprise license is installed, the operator treats the feature as new and stops reconciling that {{kib}} until you install a license or remove `spec.backgroundTasks`.
::::
