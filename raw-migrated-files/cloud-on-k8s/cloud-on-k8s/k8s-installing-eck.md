# Install ECK [k8s-installing-eck]

Elastic Cloud on Kubernetes (ECK) is a [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) to orchestrate Elastic applications (Elasticsearch, Kibana, APM Server, Beats, Elastic Agent, Elastic Maps Server, and Logstash) on Kubernetes. It relies on a set of [Custom Resource Definitions (CRD)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/#customresourcedefinitions) to declaratively define the way each application is deployed. CRDs are global resources shared by all users of the Kubernetes cluster, which requires [certain permissions](../../../deploy-manage/deploy/cloud-on-k8s/required-rbac-permissions.md#k8s-eck-permissions-installing-crds) to install them for initial use. The operator itself can be installed as a cluster-scoped application managing all namespaces or it can be restricted to a pre-defined set of namespaces. Multiple copies of the operator can be installed on a single Kubernetes cluster provided that the global CRDs are compatible with each instance and optional cluster-scoped extensions such as the [validating webhook](../../../deploy-manage/deploy/cloud-on-k8s/configure-validating-webhook.md) are disabled.

::::{warning}
Deleting CRDs will trigger deletion of all custom resources (Elasticsearch, Kibana, APM Server, Beats, Elastic Agent, Elastic Maps Server, and Logstash) in all namespaces of the cluster, regardless of whether they are managed by a single operator or multiple operators.
::::


* [Install ECK using the YAML manifests](../../../deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md)
* [Install ECK using the Helm chart](../../../deploy-manage/deploy/cloud-on-k8s/install-using-helm-chart.md)
