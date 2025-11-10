---
navigation_title: Deploy an {{es}} cluster
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-elasticsearch.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Deploy an {{es}} cluster [k8s-deploy-elasticsearch]

To deploy a simple [{{es}}](/solutions/search/get-started.md) cluster specification, with one {{es}} node:

```yaml subs=true
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 1
    config:
      node.store.allow_mmap: false
EOF
```

The operator automatically creates and manages Kubernetes resources to achieve the desired state of the {{es}} cluster. It may take up to a few minutes until all the resources are created and the cluster is ready for use.

::::{warning}
Setting `node.store.allow_mmap: false` has performance implications and should be tuned for production workloads as described in the [Virtual memory](virtual-memory.md) section.
::::


::::{note}
If your Kubernetes cluster does not have any Kubernetes nodes with at least 2GiB of free memory, the pod will be stuck in `Pending` state. Check [*Manage compute resources*](manage-compute-resources.md) for more information about resource requirements and how to configure them.
::::


::::{note}
The cluster that you deployed in this quickstart guide only allocates a persistent volume of 1GiB for storage using the default [storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) defined for the Kubernetes cluster. You will most likely want to have more control over this for production workloads. Refer to [Volume claim templates](volume-claim-templates.md) for more information.
::::


For a full description of each `CustomResourceDefinition` (CRD), refer to the [*API Reference*](cloud-on-k8s://reference/api-docs.md) or view the CRD files in the [project repository](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/crds). You can also retrieve information about a CRD from the cluster. For example, describe the {{es}} CRD specification with [`describe`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_describe/):

```sh
kubectl describe crd elasticsearch
```


## Monitor cluster health and creation progress [k8s-elasticsearch-monitor-cluster-health]

Get an overview of the current {{es}} clusters in the Kubernetes cluster with [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/), including health, version and number of nodes:

```sh
kubectl get elasticsearch
```

When you first create the Kubernetes cluster, there is no `HEALTH` status and the `PHASE` is empty. After the pod and service start-up, the `PHASE` turns into `Ready`, and `HEALTH` becomes `green`. The `HEALTH` status comes from {{es}}'s [cluster health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health).

```sh subs=true
NAME          HEALTH    NODES     VERSION   PHASE         AGE
quickstart              1         {{version.stack}}               1s
```

While the {{es}} pod is in the process of being started it will report `Pending` as checked with [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/):

```sh
kubectl get pods --selector='elasticsearch.k8s.elastic.co/cluster-name=quickstart'
```

Which will output similar to:

```sh
NAME                      READY   STATUS    RESTARTS   AGE
quickstart-es-default-0   0/1     Pending   0          9s
```

During and after start-up, up that pod’s [`logs`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/) can be accessed:

```sh
kubectl logs -f quickstart-es-default-0
```

Once the pod has finished coming up, our original [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/) request will now report:

```sh subs=true
NAME          HEALTH    NODES     VERSION   PHASE         AGE
quickstart    green     1         {{version.stack}}     Ready         1m
```


## Request {{es}} access [k8s_request_es_access]

A `ClusterIP` Service is automatically created for your cluster as checked with [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/):

```sh
kubectl get service quickstart-es-http
```

Which will output similar to:

```sh
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
quickstart-es-http   ClusterIP   10.15.251.145   <none>        9200/TCP   34m
```

In order to make requests to the [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md):

1. Get the credentials.

    By default, a user named `elastic` is created with the password stored inside a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/). This default user can be disabled if desired, refer to [Users and roles](../../users-roles/cluster-or-deployment-auth/native.md) for more information.

    ```sh
    PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')
    ```

2. Request the [{{es}} root API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-info). You can do so from inside the Kubernetes cluster or from your local workstation. For demonstration purposes, certificate verification is disabled using the `-k` curl flag; however, this is not recommended outside of testing purposes. Refer to [Setup your own certificate](/deploy-manage/security/k8s-https-settings.md#k8s-setting-up-your-own-certificate) for more information.

    * From inside the Kubernetes cluster:

        ```sh
        curl -u "elastic:$PASSWORD" -k "<ELASTICSEARCH_HOST_URL>:9200"
        ```

    * From your local workstation:

        1. Use the following command in a separate terminal:

            ```sh
            kubectl port-forward service/quickstart-es-http 9200
            ```

        2. Request `localhost`:

            ```sh
            curl -u "elastic:$PASSWORD" -k "https://localhost:9200"
            ```


## Next steps

This completes the quickstart of deploying an {{es}} cluster. We recommend continuing to:

* [Deploy a {{kib}} instance](kibana-instance-quickstart.md)
* For information about how to apply changes to your deployments, refer to [applying updates](./update-deployments.md).
* To explore other configuration options for your {{es}} cluster, see [](./elasticsearch-configuration.md) and [](./configure-deployments.md).
