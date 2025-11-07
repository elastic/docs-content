When the remote cluster server is enabled, ECK automatically creates a Kubernetes service named `<cluster-name>-es-remote-cluster` that exposes the server internally on port `9443`:

```sh
quickstart-es-remote-cluster       ClusterIP      None             <none>         9443/TCP            4h13m
```

To allow other clusters running outside your Kubernetes environment to connect, you must expose this service externally. As of ECK {{version.eck}}, you cannot customize the service that ECK generates for the remote cluster interface, but you can create your own `LoadBalancer` service, `Ingress` object, or use another method available in your environment.

For example, the following command creates a service named `quickstart-es-remote-cluster-lb`, similar to the managed `quickstart-es-remote-cluster` but of type `LoadBalancer`.

```sh
kubectl expose service quickstart-es-remote-cluster \
  --name=quickstart-es-remote-cluster-lb \
  --type=LoadBalancer \ <1>
  --port=9443 --target-port=9443
```

1. On cloud providers which support external load balancers, setting the type to LoadBalancer provisions a load balancer for your service. Alternatively, expose the service `<cluster-name>-es-remote-cluster` through one of the Kubernetes Ingress controllers that support TCP services.


:::{admonition} About exposing the service and TLS certificates
When exposing the remote cluster service, determine which TLS certificate will be presented to clients and whether a certificate authority (CA) is required to establish trust. This depends on how traffic to port `9443` is routed in your environment and which component terminates the TLS connection:

* **{{es}} TLS termination**

  If the connection reaches the {{es}} Pods without intermediate TLS termination, the {{es}} nodes present their transport certificates managed by ECK. The local cluster must therefore trust these certificates by including the ECK-managed transport CA, which you can retrieve in the next section.

  This setup is typical when using standard `LoadBalancer` services provided by most cloud providers.

* **External TLS termination**

  If the connection to port `9443` of your {{es}} cluster is handled by an external load balancer, Ingress controller, or another proxy that performs SSL termination with its own certificates, use the CA associated with that component if it's signed by a private CA.
  
  If the external TLS termination uses a publicly trusted certificate, no additional CA is needed.
:::

