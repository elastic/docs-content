# Services [k8s-services]

You can access Elastic resources by using native Kubernetes services that are not reachable from the public Internet by default.

## Manage Kubernetes services [k8s-kubernetes-service]

For each resource, the operator manages a Kubernetes service named `<name>-[es|kb|apm|ent|agent]-http`, which is of type `ClusterIP` by default. `ClusterIP` exposes the service on a cluster-internal IP and makes the service only reachable from the cluster.

```sh
> kubectl get svc

NAME                TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)          AGE
hulk-apm-http       ClusterIP      10.19.212.105   <none>           8200/TCP   1m
hulk-es-http        ClusterIP      10.19.252.160   <none>           9200/TCP   1m
hulk-kb-http        ClusterIP      10.19.247.151   <none>           5601/TCP   1m
```


## Allow public access [k8s-allow-public-access]

You can expose services in [different ways](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) by specifying an `http.service.spec.type` in the `spec` of the resource manifest. On cloud providers which support external load balancers, you can set the `type` field to `LoadBalancer` to provision a load balancer for the `Service`, and populate the column `EXTERNAL-IP` after a short delay. Depending on the cloud provider, it may incur costs.

By default, the Elasticsearch service created by ECK is configured to route traffic to all Elasticsearch nodes in the cluster. Depending on your cluster configuration, you may want more control over the set of nodes that handle different types of traffic (query, ingest, and so on). Check [*Traffic Splitting*](../../../deploy-manage/deploy/cloud-on-k8s/requests-routing-to-elasticsearch-nodes.md) for more information.

::::{warning}
When you change the `clusterIP` setting of the service, ECK will delete and re-create the service as `clusterIP` is an immutable field. Depending on your client implementation, this might result in a short disruption until the service DNS entries refresh to point to the new endpoints.
::::


```yaml
apiVersion: <kind>.k8s.elastic.co/v1
kind: <Kind>
metadata:
  name: hulk
spec:
  version: 8.16.1
  http:
    service:
      spec:
        type: LoadBalancer
```

```sh
> kubectl get svc

NAME                TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)          AGE
hulk-apm-http       LoadBalancer   10.19.212.105   35.176.227.106   8200:31000/TCP   1m
hulk-es-http        LoadBalancer   10.19.252.160   35.198.131.115   9200:31320/TCP   1m
hulk-kb-http        LoadBalancer   10.19.247.151   35.242.197.228   5601:31380/TCP   1m
```
