---
navigation_title: Pause orchestration
applies_to:
  deployment:
    eck: ga 3.5
products:
  - id: cloud-kubernetes
description: Learn how to temporarily pause ECK spec-driven orchestration during maintenance windows.
---

# Pause orchestration on ECK [k8s-pause-orchestration]

During maintenance windows, such as draining {{k8s}} nodes or applying infrastructure changes, you can temporarily prevent ECK from applying spec changes to your Elastic resources. The `eck.k8s.elastic.co/pause-orchestration` annotation lets you freeze spec-driven orchestration on any ECK-managed resource while keeping essential housekeeping running.

## Paused vs. fully unmanaged [k8s-pause-vs-unmanaged]

ECK provides two annotations that affect reconciliation behavior:

| Annotation | Availability | Effect |
|---|---|---|
| `eck.k8s.elastic.co/pause-orchestration: "true"` | {applies_to}`eck: ga 3.5+` | Pauses spec-driven changes only. Housekeeping continues. |
| `eck.k8s.elastic.co/managed: "false"` | {applies_to}`eck: deprecated 3.5+` | Stops all reconciliation entirely. Deprecated in favor of `pause-orchestration`. |

The key difference is that `pause-orchestration` keeps certificate rotation, service reconciliation, user and secret management, and health monitoring running. This avoids cluster degradation during extended maintenance windows.

## Supported resources [k8s-pause-orchestration-resources]

The annotation is supported on all ECK-managed resource types: {{es}}, {{kib}}, {{apm-server}}, Enterprise Search, {{hosted-ems}}, {{ls}}, {{agent}}, {{beats}}, and AutoOps Agent Policy.

## How to pause orchestration [k8s-pause-orchestration-usage]

Set the annotation to `"true"` on any ECK resource:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
  annotations:
    eck.k8s.elastic.co/pause-orchestration: "true"
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
```

The same annotation works on any other resource type. Only the exact string values `"true"` and `"false"` are accepted — the webhook rejects any other value (for example `"True"`, `"1"`, or an empty string).

## What continues and what pauses [k8s-pause-orchestration-behaviour]

| Operation | Behavior when paused |
|---|---|
| Certificate rotation (HTTP and transport) | Continues |
| Service reconciliation | Continues |
| User and role reconciliation | Continues |
| Health monitoring and status updates | Continues |
| Keystore reconciliation | Continues |
| Pod disruption budget reconciliation | Continues |
| StatefulSet or Deployment spec updates | Paused |
| Rolling upgrades | Paused |
| Scale up and scale down | Paused |
| Volume expansion | Paused |

## Observability [k8s-pause-orchestration-observability]

When orchestration is paused, ECK sets an `OrchestrationPaused` condition on the resource status. If spec changes are pending at the time of the pause, ECK also emits a {{k8s}} warning event indicating that changes will be applied once the annotation is removed.

```sh
kubectl get elasticsearch quickstart -o jsonpath='{.status.conditions}' | jq .
```

On resume (annotation removed or set to `"false"`), ECK clears the condition and immediately applies any pending spec changes through the normal reconciliation path.

