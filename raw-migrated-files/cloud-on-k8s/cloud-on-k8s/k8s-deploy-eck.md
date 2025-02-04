# Deploy ECK in your Kubernetes cluster [k8s-deploy-eck]

Things to consider before you start:

* For this quickstart guide, your Kubernetes cluster is assumed to be already up and running. Before you proceed with the ECK installation, make sure you check the [supported versions](../../../deploy-manage/deploy/cloud-on-k8s.md).
* If you are using GKE, make sure your user has `cluster-admin` permissions. For more information, check [Prerequisites for using Kubernetes RBAC on GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/role-based-access-control#iam-rolebinding-bootstrap).
* If you are using Amazon EKS, make sure the Kubernetes control plane is allowed to communicate with the Kubernetes nodes on port 443. This is required for communication with the Validating Webhook. For more information, check [Recommended inbound traffic](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.md).
* Refer to [*Install ECK*](../../../deploy-manage/deploy/cloud-on-k8s/install.md) for more information on installation options.
* Check the [upgrade notes](../../../deploy-manage/upgrade/orchestrator/upgrade-cloud-on-k8s.md) if you are attempting to upgrade an existing ECK deployment.

To deploy the ECK operator:

1. Install [custom resource definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) with [`create`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/):

    ```sh
    kubectl create -f https://download.elastic.co/downloads/eck/2.16.1/crds.yaml
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
    kubectl apply -f https://download.elastic.co/downloads/eck/2.16.1/operator.yaml
    ```

    ::::{note} 
    The ECK operator runs by default in the `elastic-system` namespace. It is recommended that you choose a dedicated namespace for your workloads, rather than using the `elastic-system` or the `default` namespace.
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

