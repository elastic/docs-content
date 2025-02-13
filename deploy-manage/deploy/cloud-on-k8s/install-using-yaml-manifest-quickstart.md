---
navigation_title: YAML manifests
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-install-yaml-manifests.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-eck.html
applies:
  eck: all
---

# Install ECK using the YAML manifests [k8s-install-yaml-manifests]

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/357

% Scope notes: Work with the quickstart and the small "yaml manifest installation" doc to create a single doc.

% Use migrated content from existing pages that map to this page:

% removed both
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-install-yaml-manifests.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-deploy-eck.md

In this guide, you'll learn how to deploy ECK using Elastic-provided YAML manifests. This method is the quickest way to get started with ECK if you have full administrative access to the Kubernetes cluster. 

To learn about other installation methods, refer to [](/deploy-manage/deploy/cloud-on-k8s/install.md).

During the installation, the following components are installed or updated:

* `CustomResourceDefinition` objects for all supported resource types (Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash).
* `Namespace` named `elastic-system` to hold all operator resources.
* `ServiceAccount`, `ClusterRole` and `ClusterRoleBinding` to allow the operator to manage resources throughout the cluster.
* `ValidatingWebhookConfiguration` to validate Elastic custom resources on admission.
* `StatefulSet`, `ConfigMap`, `Secret` and `Service` in `elastic-system` namespace to run the operator application.

## Prerequisites and considerations

Before you begin, review the following prerequisites and recommendations:

* You're running a Kubernetes cluster using a [supported platform](/deploy-manage/deploy/cloud-on-k8s.md#k8s-supported).

* If you are using GKE, make sure your user has `cluster-admin` permissions. For more information, check [Prerequisites for using Kubernetes RBAC on GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/role-based-access-control#iam-rolebinding-bootstrap).

* If you are using Amazon EKS, make sure the Kubernetes control plane is allowed to communicate with the Kubernetes nodes on port 443. This is required for communication with the validating webhook. For more information, check [Recommended inbound traffic](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html).

* Refer to [*Install ECK*](../../../deploy-manage/deploy/cloud-on-k8s/install.md) for more information on installation options.

* Check the [upgrade notes](../../../deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) if you are attempting to upgrade an existing ECK deployment.

##  Installation procedure

To deploy the ECK operator:

1. Install [custom resource definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) with [`create`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/):

    ```sh
    kubectl create -f https://download.elastic.co/downloads/eck/{{eck_version}}/crds.yaml
    ```

    This will output similar to the following upon Elastic resources' creation:

    ```sh
    customresourcedefinition.apiextensions.k8s.io/agents.agent.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/apmservers.apm.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/beats.beat.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/elasticmapsservers.maps.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/elasticsearches.elasticsearch.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/enterprisesearches.enterprisesearch.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/kibanas.kibana.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/logstashes.logstash.k8s.elastic.co created
    ```

2. Install the operator with its RBAC rules with [`apply`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/):

    ```sh
    kubectl apply -f https://download.elastic.co/downloads/eck/{{eck_version}}/operator.yaml
    ```

    ::::{note}
    The ECK operator runs by default in the `elastic-system` namespace. It is recommended that you choose a dedicated namespace for your workloads (such as Elasticsearch and Kibana), rather than using the `elastic-system` or the `default` namespace.
    ::::

3. Monitor the operator’s setup from its logs through [`logs`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/):

    ```sh
    kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
    ```

4. Once ready, the operator will report as `Running` as shown with [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/), replacing default `elastic-system` with applicable installation namespace as needed: *

```
$ kubectl get -n elastic-system pods
NAME                 READY   STATUS    RESTARTS   AGE
elastic-operator-0   1/1     Running   0          1m
```

This completes the quickstart of the ECK operator. We recommend continuing to [Deploying an {{es}} cluster](../../../deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md); but for more configuration options as needed, navigate to [Operating ECK](../../../deploy-manage/deploy/cloud-on-k8s/configure.md).
