When the remote cluster server is enabled, ECK automatically creates a Kubernetes service named `<cluster-name>-es-remote-cluster` that exposes the server internally on port `9443`.

To allow clusters running outside your Kubernetes environment to connect to this {{es}} cluster, you must expose this service externally. The way to expose this service depends on your ECK version.

:::::{applies-switch}

::::{applies-item} eck: ga 3.3
You can customize how the remote cluster service is exposed by overriding its service specification directly under `spec.remoteClusterServer.service` in the {{es}} resource. By default, this service listens on port 9443.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: <cluster-name>
  namespace: <namespace>
spec:
  version: 9.2.1
  remoteClusterServer:
    enabled: true
    service:
      spec:
        type: LoadBalancer <1>
  nodeSets:
    - name: default
      count: 3
      ...
      ...
```
1. On cloud providers that support external load balancers, setting the type to `LoadBalancer` provisions a load balancer for your service. Alternatively, expose the service `<cluster-name>-es-remote-cluster` through one of the Kubernetes Ingress controllers that support TCP services.
::::

::::{applies-item} eck: ga 3.0

In ECK 3.2 and earlier, you can't customize the service that ECK generates for the remote cluster interface, but you can create your own `LoadBalancer` service, `Ingress` object, or use another method available in your environment.

For example, for a cluster named `quickstart`, the following command creates a separate `LoadBalancer` service named `quickstart-es-remote-cluster-lb`, pointing to the ECK-managed service `quickstart-es-remote-cluster`:

```sh
kubectl expose service quickstart-es-remote-cluster \
  --name=quickstart-es-remote-cluster-lb \
  --type=LoadBalancer \ <1>
  --port=9443 --target-port=9443
```
1. On cloud providers that support external load balancers, setting the type to `LoadBalancer` provisions a load balancer for your service. Alternatively, expose the service `<cluster-name>-es-remote-cluster` through one of the Kubernetes Ingress controllers that support TCP services.

::::
:::::

:::{warning}
If you change the service’s `port` to expose a different port externally, set `targetPort` explicitly to `9443`, which is the default remote cluster server listening port. Otherwise, Kubernetes uses the same value for both fields, resulting in failed connections.
:::

