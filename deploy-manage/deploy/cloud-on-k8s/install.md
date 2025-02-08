---
applies:
  eck: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-installing-eck.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-supported.html
---

# Install ECK [k8s-installing-eck]

% What needs to be done: Lift-and-shift

% Scope notes: Entry point, i think the current page is valid.

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-installing-eck.md

% TBD: supported versions here or in the intro??

% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-supported.md

Pending to add link to supported versions (in the intro) [](../cloud-on-k8s.md#k8s-supported)

## Installation overview

% TBD: I kind of hate this paragraph :) not because of the content, but because of the format...

Elastic Cloud on Kubernetes (ECK) is a [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) to orchestrate Elastic applications (Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash) on Kubernetes. It relies on a set of [Custom Resource Definitions (CRD)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) to declaratively define the way each application is deployed. CRDs are global resources shared by all users of the Kubernetes cluster, which requires [certain permissions](../../../deploy-manage/deploy/cloud-on-k8s/required-rbac-permissions.md#k8s-eck-permissions-installing-crds) to install them for initial use. The operator itself can be installed as a cluster-scoped application managing all namespaces or it can be restricted to a pre-defined set of namespaces. Multiple copies of the operator can be installed on a single Kubernetes cluster provided that the global CRDs are compatible with each instance and optional cluster-scoped extensions such as the [validating webhook](../../../deploy-manage/deploy/cloud-on-k8s/configure-validating-webhook.md) are disabled.

::::{warning}
Deleting CRDs will trigger deletion of all custom resources (Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash) in all namespaces of the cluster, regardless of whether they are managed by a single operator or multiple operators.
::::

## Installation methods

ECK offers multiple installation methods, including standard Kubernetes deployments and specialized procedures for environments such as OpenShift and GKE Autopilot. Choose the method that best suits your infrastructure:

* [Install ECK using the YAML manifests (quickstart)](./install-using-yaml-manifest-quickstart.md)
* [Install ECK using the Helm chart](./install-using-helm-chart.md)
* [](./deploy-eck-on-openshift.md)
* [](./deploy-eck-on-gke-autopilot.md)
* [](./deploy-fips-compatible-version-of-eck.md)
* [](./air-gapped-install.md)