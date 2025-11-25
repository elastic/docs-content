---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-accessing-elastic-services.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-request-elasticsearch-endpoint.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-services.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Accessing services [k8s-accessing-elastic-services]

To provide access to {{es}}, {{kib}}, and other {{stack}} applications when applicable, ECK relies on [Kubernetes services](https://kubernetes.io/docs/concepts/services-networking/service/).

All {{stack}} resources deployed by the ECK operator are secured by default. The operator sets up basic authentication and TLS to encrypt network traffic to, from, and within your {{es}} cluster.

This section explains how to access and customize the Kubernetes services and secrets created by ECK, covering topics such as:

* [Retrieving the `elastic` user password for basic authentication](#k8s-authentication)
* [Managing Kubernetes services](#k8s-kubernetes-service)
* [Obtaining the CA certificate and accessing the endpoint](#k8s-request-elasticsearch-endpoint)

For advanced use cases related to exposing and accessing orchestrated applications, see:

* [](/deploy-manage/security/secure-cluster-communications.md): Configuration options for the HTTP SSL certificates, including integration with certificate management systems such as [cert-manager](https://cert-manager.io/).
* [](./service-meshes.md): Connect ECK and your managed deployments to service mesh implementations such as [Istio](https://istio.io) and [Linkerd](https://linkerd.io).
* [](./requests-routing-to-elasticsearch-nodes.md): Create custom services to expose different node types.
* [Use Ingress to expose {{es}} or {{kib}}](./managing-deployments-using-helm-chart.md#k8s-eck-stack-ingress): Helm based installation also facilitates the creation of Ingress resources.

## Retrieve the `elastic` user password [k8s-authentication]

To access Elastic resources, the operator manages a default user named `elastic` with the `superuser` role. Its password is stored in a `Secret` named `<name>-elastic-user`.

Run the following command to obtain the password of the `elastic` user:

```sh
> kubectl get secret hulk-es-elastic-user -o go-template='{{.data.elastic | base64decode }}'
42xyz42citsale42xyz42
```

::::{note}
Beware of copying this Secret as-is into a different namespace. Check [Common Problems: Owner References](../../../troubleshoot/deployments/cloud-on-k8s/common-problems.md#k8s-common-problems-owner-refs) for more information.
::::

For more information about handling built-in users on ECK deployments, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).

## Managing Kubernetes services [k8s-kubernetes-service]

You can access Elastic resources by using native Kubernetes services that are not reachable from the public Internet by default.

For each resource, the operator manages a Kubernetes service named `<name>-[es|kb|apm|ent|agent]-http`, which is of type `ClusterIP` by default. `ClusterIP` exposes the service on a cluster-internal IP and makes the service only reachable within the cluster.

```sh
> kubectl get svc

NAME                TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)          AGE
hulk-apm-http       ClusterIP      10.19.212.105   <none>           8200/TCP   1m
hulk-es-http        ClusterIP      10.19.252.160   <none>           9200/TCP   1m
hulk-kb-http        ClusterIP      10.19.247.151   <none>           5601/TCP   1m
```

### Allow public access [k8s-allow-public-access]

You can expose services in [different ways](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) by specifying an `http.service.spec.type` in the `spec` of the resource manifest. On cloud providers which support external load balancers, you can set the `type` field to `LoadBalancer` to provision a load balancer for the `Service`, and populate the column `EXTERNAL-IP` after a short delay. Depending on the cloud provider, it may incur costs.

By default, the {{es}} service created by ECK is configured to route traffic to all {{es}} nodes in the cluster. Depending on your cluster configuration, you may want more control over the set of nodes that handle different types of traffic (query, ingest, and so on). Refer to [](./requests-routing-to-elasticsearch-nodes.md) for more information.

::::{warning}
When you change the `clusterIP` setting of the service, ECK will delete and re-create the service as `clusterIP` is an immutable field. Depending on your client implementation, this might result in a short disruption until the service DNS entries refresh to point to the new endpoints.

If you change the service’s `port`, set `targetPort` to the container’s default port. Otherwise Kubernetes uses the same value for both fields, resulting in failed connections. For reference, default ports are `9200` for the {{es}} HTTP interface, and `5601` for {{kib}}.
::::

```yaml subs=true
apiVersion: <kind>.k8s.elastic.co/v1
kind: <Kind>
metadata:
  name: hulk
spec:
  version: {{version.stack}}
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

## Access the endpoint [k8s-request-elasticsearch-endpoint]

You can access the {{es}} endpoint within or outside the Kubernetes cluster.

**Within the Kubernetes cluster**

1. Retrieve the CA certificate.
2. Retrieve the password of the `elastic` user.
3. Use the service name to access the endpoint.

```sh
NAME=hulk

kubectl get secret "$NAME-es-http-certs-public" -o go-template='{{index .data "tls.crt" | base64decode }}' > tls.crt
PW=$(kubectl get secret "$NAME-es-elastic-user" -o go-template='{{.data.elastic | base64decode }}')

curl --cacert tls.crt -u elastic:$PW https://$NAME-es-http:9200/
```

::::{tip}
You can also use the examples in this section to access {{kib}} instead of {{es}} by adapting the secret and service names.
::::

**Outside the Kubernetes cluster**

1. Retrieve the CA certificate.
2. Retrieve the password of the `elastic` user.
3. Retrieve the IP of the `LoadBalancer` service.

```sh
NAME=hulk

kubectl get secret "$NAME-es-http-certs-public" -o go-template='{{index .data "tls.crt" | base64decode }}' > tls.crt
IP=$(kubectl get svc "$NAME-es-http" -o jsonpath='{.status.loadBalancer.ingress[].ip}')
PW=$(kubectl get secret "$NAME-es-elastic-user" -o go-template='{{.data.elastic | base64decode }}')

curl --cacert tls.crt -u elastic:$PW https://$IP:9200/
```



