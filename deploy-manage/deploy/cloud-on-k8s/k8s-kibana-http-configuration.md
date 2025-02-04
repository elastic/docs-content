---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-http-configuration.html
---

# HTTP configuration [k8s-kibana-http-configuration]

## Load balancer settings and TLS SANs [k8s-kibana-http-publish]

By default a `ClusterIP` [Service](https://kubernetes.io/docs/concepts/services-networking/service/) is created and associated with the {{kib}} deployment. If you want to expose {{kib}} externally with a [load balancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), it is recommended to include a custom DNS name or IP in the self-generated certificate.

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: "elasticsearch-sample"
  http:
    service:
      spec:
        type: LoadBalancer # default is ClusterIP
    tls:
      selfSignedCertificate:
        subjectAltNames:
        - ip: 1.2.3.4
        - dns: kibana.example.com
```


## Provide your own certificate [k8s-kibana-http-custom-tls]

If you want to use your own certificate, the required configuration is identical to {{es}}. Check [Custom HTTP certificate](../../security/secure-http-communications.md).


## Disable TLS [k8s-kibana-http-disable-tls]

You can disable the generation of the self-signed certificate and hence [disable TLS](https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html). This is not recommended outside of testing clusters.

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: "elasticsearch-sample"
  http:
    tls:
      selfSignedCertificate:
        disabled: true
```


