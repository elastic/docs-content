---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autoops-configuration.html
applies_to:
  deployment:
    eck: ga 3.3
products:
  - id: cloud-kubernetes
navigation_title: Configuration
---

# Configuration for AutoOps on {{eck}} [k8s-autoops-configuration]

AutoOps on ECK uses the `AutoOpsAgentPolicy` custom resource to connect your ECK-managed {{es}} clusters to AutoOps. ECK automatically handles the creation of API keys, Agent configuration, and deployment of the AutoOps Agent required to send metrics to AutoOps.

## AutoOps configuration [k8s-autoops-configuring-autoops]

Define an `AutoOpsAgentPolicy` resource to connect your {{es}} clusters to AutoOps:

```yaml
apiVersion: autoops.k8s.elastic.co/v1alpha1
kind: AutoOpsAgentPolicy
metadata:
  name: autoops-policy
spec:
  version: 9.2.1 <1>
  autoOpsRef:
    secretName: autoops-config
  resourceSelector:
    matchLabels:
      autoops: enabled
```
1. 9.2.1 is the minimum version allowed for the AutoOps Agent

The `AutoOpsAgentPolicy` resource requires:

* `spec.autoOpsRef.secretName`: A reference to a `Secret` containing connection details.
* `spec.resourceSelector`: A label selector to match multiple {{es}} clusters (see [Selecting {{es}} clusters](#k8s-autoops-selecting-clusters))

## Connecting to AutoOps [k8s-autoops-connecting-to-autoops]

To connect to AutoOps you must provide the following fields within a `Secret`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: autoops-config
type: Generic
stringData:
  autoops-token: "token-from-wizard"
  autoops-otel-url: "url-from-wizard"
  cloud-connected-mode-api-key: "key-from-wizard"
  cloud-connected-mode-api-url: "url-from-wizard"
```

Then reference this `Secret` in your `AutoOpsAgentPolicy`:

```yaml
apiVersion: autoops.k8s.elastic.co/v1alpha1
kind: AutoOpsAgentPolicy
metadata:
  name: autoops-policy
spec:
  version: 9.2.1
  autoOpsRef:
    secretName: autoops-config
  resourceSelector:
    matchLabels:
      autoops: enabled
```

:::{note}
The `autoops-token`, `autoops-otel-url` and `cloud-connected-mode-api-key` are required. You can obtain these from the ECK AutoOps installation wizard in {{ecloud}}.
:::

## Selecting {{es}} clusters [k8s-autoops-selecting-clusters]

You can connect {{es}} clusters using the `resourceSelector` with label matching:

```yaml
apiVersion: autoops.k8s.elastic.co/v1alpha1
kind: AutoOpsAgentPolicy
metadata:
  name: autoops-policy
spec:
  version: 9.2.1
  autoOpsRef:
    secretName: autoops-config
  resourceSelector:
    matchLabels:
      autoops: enabled
```

The `resourceSelector` uses standard {{k8s}} [label selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors) to match {{es}} clusters. All {{es}} clusters within the cluster that match the selector will be connected to AutoOps.

## Viewing AutoOps status

After creating an `AutoOpsAgentPolicy`, you can check its status:

```sh
kubectl get autoopsagentpolicy
```

```sh
NAMESPACE   NAME                        READY   PHASE   AGE
elastic     eck-autoops-config-policy   2       Ready   22h
```

To view detailed information:

```sh
kubectl describe autoopsagentpolicy eck-autoops-config-policy
```

The status shows:
1. A count of errors encountered when configuring the AutoOps Agent.
2. The Phase of the Policy.
3. A count of the number of resources selected by the resourceSelector.
4. A count of the number of resources that are ready, and shipping data to AutoOps.

## Removing the connection to AutoOps

To disconnect a set of clusters from AutoOps, delete the `AutoOpsAgentPolicy` resource:

```sh
kubectl delete autoopsagentpolicy eck-autoops-config-policy
```

ECK automatically removes the AutoOps Agents, and removes the previous-created {{es}} API keys.
