---
navigation_title: Install
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-installing-eck.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Install ECK [k8s-installing-eck]

{{eck}} (ECK) is a [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) that helps you deploy and manage Elastic applications on Kubernetes, including {{eck_resources_list}}.

ECK relies on a set of [Custom Resource Definitions (CRDs)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) to define how applications are deployed. CRDs are global resources, shared across the entire Kubernetes cluster, so installing them requires [specific permissions](../../../deploy-manage/deploy/cloud-on-k8s/required-rbac-permissions.md#k8s-eck-permissions-installing-crds).

ECK can be installed in two modes, depending on the namespaces the operator is allowed to manage:
1. **Cluster-wide installation**: Allows the operator to orchestrate applications in all namespaces of the Kubernetes cluster. This is the default installation method.
2. **Namespace-restricted installation**: Limited to specific, pre-defined namespaces. Use the `namespaces` [configuration flag](./configure-eck.md) to limit the namespaces in which the operator is allowed to work.

::::{note}
You can install multiple instances of ECK in the same Kubernetes cluster, but only if the CRDs are compatible across all operator instances (e.g., by ensuring they run the same version). If running multiple instances, you must also disable cluster-wide features like the [validating webhook](../../../deploy-manage/deploy/cloud-on-k8s/configure-validating-webhook.md).
::::

::::{warning}
Deleting CRDs will trigger deletion of all custom resources ({{eck_resources_list}}) in all namespaces of the cluster, regardless of whether they are managed by a single operator or multiple operators.
::::

For a list of supported Kubernetes versions refer to [](../cloud-on-k8s.md#k8s-supported)

## Installation methods

ECK supports multiple installation methods. Choose the one that best fits your infrastructure:

* [Install ECK using YAML manifests](./install-using-yaml-manifest-quickstart.md)
* [Install ECK using a Helm chart](./install-using-helm-chart.md)
* [](./deploy-eck-on-openshift.md)
* [](./deploy-eck-on-gke-autopilot.md)
* [Deploy ECK on Google Distributed Hosted Cloud](./eck-gdch.md)
* [](./deploy-fips-compatible-version-of-eck.md)

For air-gapped environments, refer to [](./air-gapped-install.md) to understand the requirements and installation considerations.

Refer to [Required RBAC permissions](required-rbac-permissions.md) for a complete list of the permissions needed by the operator.

::::{note}
To upgrade ECK, refer to [](../../upgrade/orchestrator/upgrade-cloud-on-k8s.md).
::::