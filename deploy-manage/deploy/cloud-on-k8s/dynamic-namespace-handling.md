---
navigation_title: Dynamic namespace handling
applies_to:
  deployment:
    eck: ga 3.5
products:
  - id: cloud-kubernetes
description: Use a label selector to dynamically control which namespaces the ECK operator manages, without restarting the operator.
---

# Dynamic namespace handling [k8s-dynamic-namespace-handling]

By default, the ECK operator manages either all namespaces in the cluster or a static list of namespaces defined through the [`namespaces` configuration option](configure-eck.md). Dynamic namespace handling replaces the static list with a [Kubernetes label selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors): the operator evaluates the selector against each namespace's labels at runtime to determine which namespaces it manages.

When a namespace gains labels that match the selector, the operator starts managing the Elastic resources in it. This is called namespace **on-boarding**. When a namespace stops matching the selector, it is **off-boarded** and the operator stops managing its resources. The operator monitors namespace label changes live and adjusts on the fly, no operator restart is required in either direction.

::::{note}
Dynamic namespace handling requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::

## How it works [k8s-dynamic-namespace-handling-how-it-works]

With a namespace selector configured, the operator watches all namespaces cluster-wide and filters the events it receives by matching each namespace's current labels against the selector:

* Events from resources in non-matching namespaces are ignored, and the operator does not reconcile those resources.
* The operator also watches `Namespace` objects themselves. When a namespace flips in or out of the selector's scope, the operator immediately enumerates the Elastic resources in that namespace and starts or stops managing them.
* The [validating webhook](configure-validating-webhook.md) applies the same filtering: resources in namespaces that do not match the selector are not validated (admission requests for them are silently accepted rather than blocked).
* The namespace in which the operator itself runs is always considered managed, regardless of its labels.

### On-boarding [k8s-dynamic-namespace-handling-onboarding]

To on-board a namespace, apply the labels that match the configured selector. For example, with a selector matching `eck-managed: "true"`:

```sh
kubectl label namespace my-namespace eck-managed=true
```

The operator picks up any existing Elastic resources in the namespace and starts reconciling them immediately.

### Off-boarding [k8s-dynamic-namespace-handling-offboarding]

To off-board a namespace, remove or change the labels so that the namespace no longer matches the selector:

```sh
kubectl label namespace my-namespace eck-managed-
```

::::{important}
Off-boarding a namespace does not delete or modify the Elastic resources deployed in it. Existing {{es}} clusters, {{kib}} instances, and other Elastic applications keep running as they are, but the operator stops monitoring and operating them: changes to their manifests are no longer reconciled, and features driven by the operator, such as certificate rotation, stop being applied. If the namespace is on-boarded again later, the operator resumes managing those resources.
::::

## Enable dynamic namespace handling [k8s-dynamic-namespace-handling-enable]

The namespace selector supports the standard Kubernetes `matchLabels` and `matchExpressions` semantics, and is subject to the following constraints:

* It is mutually exclusive with the static list of managed namespaces (`namespaces` in the operator configuration, `managedNamespaces` in the Helm chart).
* It requires the operator to run with cluster-wide permissions, because the operator must watch namespaces and Elastic resources across the whole cluster. It is therefore not compatible with the [restricted installation mode](install-using-helm-chart.md#k8s-install-helm-restricted) of the Helm chart.
* An empty selector (`{}`) disables dynamic namespace handling, and the operator manages all namespaces.

### Using the Helm chart

If you installed ECK through the [Helm chart](install-using-helm-chart.md), set the `managedNamespaceSelector` value. Note that this is a top-level chart value, not part of the `config` section:

```yaml
managedNamespaceSelector:
  matchLabels:
    eck-managed: "true"
```

Or using `matchExpressions`:

```yaml
managedNamespaceSelector:
  matchExpressions:
    - key: environment
      operator: In
      values: [production, staging]
```

Instead of a values file, you can also set the selector directly on the command line when installing or upgrading the release:

```sh
helm upgrade elastic-operator elastic/eck-operator -n elastic-system \
  --reuse-values \
  --set-string 'managedNamespaceSelector.matchLabels.eck-managed=true'
```

Note the use of `--set-string`, which prevents Helm from interpreting the label value `true` as a boolean, namespace label values are always strings. If the label key contains dots, escape them with `\.` (for example, `managedNamespaceSelector.matchLabels.kubernetes\.io/metadata\.name`).

::::{important}
When `managedNamespaceSelector` is set, the chart requires `createClusterScopedResources` to be `true` (the default), and fails to install if `managedNamespaces` is set at the same time.
::::

### Using the YAML manifests

If you installed ECK using the [YAML manifests](install-using-yaml-manifest-quickstart.md), add the `namespace-selector` option to the `eck.yaml` key of the `elastic-operator` ConfigMap, as described in [](configure-eck.md):

```yaml
namespace-selector:
  matchLabels:
    eck-managed: "true"
```

::::{note}
Because the value of `namespace-selector` is an object rather than a scalar, it can only be set through the operator configuration file. It cannot be passed as a command-line flag or as an environment variable.
::::

## License handling [k8s-dynamic-namespace-handling-license]

Dynamic namespace handling is an Enterprise feature. While no valid Enterprise license is present, the operator skips the reconciliation of Elastic resources entirely, emits a Kubernetes event indicating that Enterprise features are turned off, and retries every 5 minutes. As soon as a valid [Enterprise license or trial license](../../license/manage-your-license-in-eck.md) is installed, reconciliation resumes automatically.

::::{warning}
When the Enterprise license expires, ECK normally reverts the managed {{es}} clusters to a Basic license. With dynamic namespace handling enabled, reconciliation stops entirely instead: the `status` of ECK-managed resources becomes stale, and the clusters keep their now-expired Enterprise or Platinum license. In this state, {{es}} blocks the `_cluster/health`, `_cluster/stats`, and `_stats` APIs with a `403` security exception, while data operations (read and write) continue to work.

To recover, install a valid [Enterprise license](../../license/manage-your-license-in-eck.md) (or Enterprise Trial License), or remove the namespace selector so that the operator reverts the clusters to Basic.
::::

Create the license secret in the operator's namespace, as described in [Manage your license in ECK](../../license/manage-your-license-in-eck.md). This is particularly important with dynamic namespace handling: the operator's namespace is always in scope regardless of its labels, so a license stored there can never be off-boarded together with a managed namespace.
