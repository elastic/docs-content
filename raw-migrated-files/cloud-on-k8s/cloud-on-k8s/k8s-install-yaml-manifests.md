# Install ECK using the YAML manifests [k8s-install-yaml-manifests]

This method is the quickest way to get started with ECK if you have full administrative access to the Kubernetes cluster. The [Quickstart](../../../deploy-manage/deploy/cloud-on-k8s/deploy-an-orchestrator.md) document describes how to proceed with this method. When you run the `kubectl` command listed in [*Deploy ECK in your Kubernetes cluster*](../../../deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md), the following components are installed or updated:

* `CustomResourceDefinition` objects for all supported resource types (Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash).
* `Namespace` named `elastic-system` to hold all operator resources.
* `ServiceAccount`, `ClusterRole` and `ClusterRoleBinding` to allow the operator to manage resources throughout the cluster.
* `ValidatingWebhookConfiguration` to validate Elastic custom resources on admission.
* `StatefulSet`, `ConfigMap`, `Secret` and `Service` in `elastic-system` namespace to run the operator application.

