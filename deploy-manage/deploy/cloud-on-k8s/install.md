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

## Hardened ECK container image [k8s-installing-eck-container-image]

Elastic has partnered with [Chainguard](https://www.chainguard.dev/) to provide hardened container images based on [Wolfi](https://wolfi.dev), a minimal, security-focused Linux distribution designed for containerized environments. These images significantly reduce the CVE footprint of Elastic containers by including only the application and its necessary runtime dependencies. For background on this initiative, refer to the blog post [Reducing CVEs in Elastic container images](https://www.elastic.co/blog/reducing-cves-in-elastic-container-images).

ECK operator images are hardened in different ways depending on the variant:

* The **standard** operator image has been hardened and built on Wolfi since ECK 2.15. No additional configuration is required — pulling the standard operator image from `docker.elastic.co` already provides a hardened, Wolfi-based container.
* The **UBI** operator image is hardened following Red Hat's Universal Base Image (UBI) requirements.
* The **FIPS** operator image is hardened following Federal Information Processing Standard (FIPS) Publication 140-2 requirements. Refer to [Deploy a FIPS-compatible version of ECK](./deploy-fips-compatible-version-of-eck.md) for details.

::::{note}
Only operator images distributed through `docker.elastic.co`, as well as the official [Red Hat Certified Operator](https://catalog.redhat.com/software/operators/detail/5f32f067651c4c0bcecf1bfe) images published on `catalog.redhat.com`, are officially supported by Elastic. Third-party hardened image sources, such as Docker Hardened Images (DHI) on Docker Hub, are not maintained by Elastic and fall outside the scope of Elastic support.
::::
