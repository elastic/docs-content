---
navigation_title: YAML manifests
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-install-yaml-manifests.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-eck.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Install ECK using the YAML manifests [k8s-install-yaml-manifests]

In this guide, you'll learn how to deploy ECK using Elastic-provided YAML manifests. This method is the quickest way to get started with ECK if you have full administrative access to the Kubernetes cluster.

To learn about other installation methods, refer to [](/deploy-manage/deploy/cloud-on-k8s/install.md).

During the installation, the following components are installed or updated:

* `CustomResourceDefinition` objects for all supported resource types ({{eck_resources_list}}).
* `Namespace` named `elastic-system` to hold all operator resources.
* `ServiceAccount`, `ClusterRole` and `ClusterRoleBinding` to allow the operator to manage resources throughout the cluster.
* `ValidatingWebhookConfiguration` to validate Elastic custom resources on admission.
* `StatefulSet`, `ConfigMap`, `Secret` and `Service` in `elastic-system` namespace to run the operator application.

## Prerequisites and considerations

Before you begin, review the following prerequisites and recommendations:

* You're running a Kubernetes cluster using a [supported platform](/deploy-manage/deploy/cloud-on-k8s.md#k8s-supported).

* If you are using GKE, make sure your user has `cluster-admin` permissions. For more information, check [Prerequisites for using Kubernetes RBAC on GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/role-based-access-control#iam-rolebinding-bootstrap).

* If you are using Amazon EKS, make sure the Kubernetes control plane is allowed to communicate with the Kubernetes nodes on port 443. This is required for communication with the validating webhook. For more information, check [Recommended inbound traffic](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html).


##  Installation procedure

To deploy the ECK operator:

1. Install Elastic's [custom resource definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) with [`create`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/):

    ```sh subs=true
    kubectl create -f https://download.elastic.co/downloads/eck/{{version.eck}}/crds.yaml
    ```

    You'll see output similar to the following as resources are created:

    ```sh
    customresourcedefinition.apiextensions.k8s.io/agents.agent.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/apmservers.apm.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/beats.beat.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/elasticmapsservers.maps.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/elasticsearches.elasticsearch.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/kibanas.kibana.k8s.elastic.co created
    customresourcedefinition.apiextensions.k8s.io/logstashes.logstash.k8s.elastic.co created
    ```

2. Using [`kubectl apply`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/), install the operator with its RBAC rules:

    ```sh subs=true
    kubectl apply -f https://download.elastic.co/downloads/eck/{{version.eck}}/operator.yaml
    ```

    ::::{note}
    The ECK operator runs by default in the `elastic-system` namespace. While this namespace is used for the operator itself, it is recommended that you deploy your application workloads in a separate, dedicated namespace instead of `elastic-system` or `default`. You will need to consider this when setting up your applications.
    ::::

3. Using [`kubectl logs`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs), monitor the operator’s setup by watching the logs:

    ```sh
    kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
    ```

4. Use [`kubectl get pods`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/) to check the operator status, passing in the namespace using the `-n` flag:

    ```sh
    kubectl get -n elastic-system pods
    ```

    When the operator is ready to use, it will report as `Running`

    ```
    $ kubectl get -n elastic-system pods
    NAME                 READY   STATUS    RESTARTS   AGE
    elastic-operator-0   1/1     Running   0          1m
    ```


## Next steps

* To continue the quickstart, go to [](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md)
* For more configuration options, refer to [](/deploy-manage/deploy/cloud-on-k8s/configure.md).
