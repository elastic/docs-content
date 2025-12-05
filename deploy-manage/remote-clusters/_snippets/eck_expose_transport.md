<!--
This snippet is in use in the following locations:
- eck-remote-clusters-from-external.md
- ec-enable-ccs-for-eck.md
- ece-enable-ccs-for-eck.md
-->
Expose the transport service (defaults to port `9300`) of your ECK cluster to allow external {{es}} clusters to connect:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: <remote-cluster-name>
spec:
  transport:
    service:
      spec:
        type: LoadBalancer <1>
```

1. On cloud providers which support external load balancers, setting the type field to `LoadBalancer` provisions a load balancer for your service. Alternatively, expose the service `<cluster-name>-es-transport` through one of the Kubernetes Ingress controllers that support TCP services.
