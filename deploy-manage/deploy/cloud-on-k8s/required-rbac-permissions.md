---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-eck-permissions.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Required RBAC permissions [k8s-eck-permissions]

Installing and running ECK, as well as using ECK-managed resources, requires the following Kubernetes [permissions](https://kubernetes.io/docs/reference/access-authn-authz/rbac):

* [Installing CRDs](#k8s-eck-permissions-installing-crds)
* [Installing the ECK operator](#k8s-eck-permissions-installing-operator)
* [Running ECK operator](#k8s-eck-permissions-running)
* [Using ECK-managed resources](#k8s-eck-permissions-using)


## Installing CRDs [k8s-eck-permissions-installing-crds]

This permission is required to install CRDs. CRDs ([CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)) are the only non-namespaced resources required to be installed.

| Name | API group | Optional? | Usage |
| --- | --- | --- | --- |
| `CustomResourceDefinition` | `apiextensions.k8s.io` | no | Extend Kubernetes APIs with {{stack}} application resources. |


## Installing the ECK operator [k8s-eck-permissions-installing-operator]

These permissions are required to install the ECK operator in a Kubernetes cluster.

| Name | API group | Optional? | Usage |
| --- | --- | --- | --- |
| `StatefulSet or Deployment` | `apps` | no | The ECK operator can be either deployed as a StatefulSet or as a Deployment. |
| `ServiceAccount` | `core` | no | Service account that the operator Pods run as. |
| `Role or ClusterRole` | `rbac.authorization.k8s.io` | no | Role bound to the operators Service account. Depending on the installation type (global/restricted) either a global (ClusterRole) or a namespaced (Role) resource is needed. |
| `RoleBinding or ClusterRoleBinding` | `rbac.authorization.k8s.io` | no | Binding between the operators role and the operators service account. Depending on the installation type (global/restricted), either global (ClusterRoleBinding) or namespaced (RoleBinding) resource is needed. |
| `ConfigMap` | `core` | yes | Configuration parameters of the Operator. They can be specified directly in the StatefulSet (or Deployment) resource instead. |
| `Namespace` | `core` | yes | Namespace where the operator will run. It can be a pre-existing namespace as well. |
| `ValidatingWebhookConfiguration` | `admissionregistration.k8s.io` | yes | Validating webhook installation. It provides fast feedback for the user directly as a APIServer response. A subset of these validations is also run by the operator itself, but the results are only available through operator logs and Kubernetes events. Check [docs](/deploy-manage/deploy/cloud-on-k8s/configure-validating-webhook.md) for more. |
| `Secret` | `core` | yes | Secret containing the validating webhook’s endpoint CA certificate. |
| `Service` | `core` | yes | Service for validating webhook endpoint. |

And all permissions that [Running ECK operator](#k8s-eck-permissions-running) section specifies.


## Running ECK operator [k8s-eck-permissions-running]

These permissions are needed by the Service Account that ECK operator runs as.

| Name | API group | Optional? | Usage |
| --- | --- | --- | --- |
| `Pod` |  | no | Assuring expected Pods presence during {{es}} reconciliation, safely deleting Pods during configuration changes and validating `podTemplate` by dry-run creation of Pods. |
| `Endpoint` |  | no | Checking availability of service endpoints. |
| `Event` |  | no | Emitting events concerning reconciliation progress and issues. |
| `PersistentVolumeClaim` |  | no | Expanding existing volumes. Check [docs](volume-claim-templates.md#k8s-volume-claim-templates-update) to learn more. |
| `Secret` |  | no | Reading/writing configuration, passwords, certificates, and so on. |
| `Service` |  | no | Creating Services fronting {{stack}} applications. |
| `ConfigMap` |  | no | Reading/writing configuration. |
| `StatefulSet` | `apps` | no | Deploying {{es}} |
| `Deployment` | `apps` | no | Deploying {{kib}}, APM Server, EnterpriseSearch, Maps, Beats or Elastic Agent. |
| `DaemonSet` | `apps` | no | Deploying Beats or Elastic Agent. |
| `PodDisruptionBudget` | `policy` | no | Ensuring update safety for {{es}}. Check [docs](/deploy-manage/deploy/cloud-on-k8s/pod-disruption-budget.md) to learn more. |
| `StorageClass` | `storage.k8s.io` | yes | Validating storage expansion support. Check [docs](volume-claim-templates.md#k8s-volume-claim-templates-update) to learn more. |
| `coreauthorization.k8s.io` | `SubjectAccessReview` | yes | Controlling access between referenced resources. Check [docs](/deploy-manage/deploy/cloud-on-k8s/restrict-cross-namespace-resource-associations.md) to learn more. |
| {applies_to}`eck: ga 3.3.1+` `Namespace` |  | yes | The AutoOps functionality uses an optional `namespaceSelector` to match namespaces by label. It requires listing and filtering namespace resources across the cluster to determine which {{es}} instances must be configured.

And all permissions that the [Using ECK-managed resources](#k8s-eck-permissions-using) chapter specifies.


## Using ECK-managed resources [k8s-eck-permissions-using]

These permissions are needed to manage each {{stack}} application. For example, to create, update and delete {{es}} clusters the permissions for the respective verbs must be held by the user that performs the operation.

| Name | API group | Optional? |
| --- | --- | --- |
| `Elasticsearch`<br>`Elasticsearch/status`<br>`Elasticsearch/finalizers` | `elasticsearch.k8s.elastic.co` | no |
| `Kibana`<br>`Kibana/status`<br>`Kibana/finalizers` | `kibana.k8s.elastic.co` | no |
| `APMServer`<br>`APMServer/status`<br>`APMServer/finalizers` | `apm.k8s.elastic.co` | no |
| `EnterpriseSearch`<br>`EnterpriseSearch/status`<br>`EnterpriseSearch/finalizers` | `enterprisesearch.k8s.elastic.co` | no |
| `Beat`<br>`Beat/status`<br>`Beat/finalizers` | `beat.k8s.elastic.co` | no |
| `Agent`<br>`Agent/status`<br>`Agent/finalizers` | `agent.k8s.elastic.co` | no |
| `ElasticMapsServer`<br>`ElasticMapsServer/status`<br>`ElasticMapsServer/finalizers` | `maps.k8s.elastic.co` | no |
| `Logstash`<br>`Logstash/status`<br>`Logstash/finalizers` | `logstashes.k8s.elastic.co` | no |

