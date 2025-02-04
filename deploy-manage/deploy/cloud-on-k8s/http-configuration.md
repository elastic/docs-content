---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-maps-http-configuration.html
---

# HTTP configuration [k8s-maps-http-configuration]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


## Load balancer settings and TLS SANs [k8s-maps-http-publish]

By default a `ClusterIP` [service](https://kubernetes.io/docs/concepts/services-networking/service/) is created and associated with the Elastic Maps Server deployment. If you want to expose maps externally with a [load balancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), it is recommended to include a custom DNS name or IP in the self-generated certificate.

Refer to [Reserve static IP and custom domain](tls-certificates.md#k8s-static-ip-custom-domain) for more details.


## Provide your own certificate [k8s-maps-http-custom-tls]

If you want to use your own certificate, the required configuration is identical to Elasticsearch. Check [Custom HTTP certificate](../../security/secure-http-communications.md).


## Disable TLS [k8s-maps-http-disable-tls]

You can disable the generation of the self-signed certificate and hence disable TLS. Check [Disable TLS](tls-certificates.md#k8s-disable-tls).

### Ingress and Kibana configuration [k8s-maps-ingress]

To use Elastic Maps Server from your Kibana instances, you need to configure Kibana to fetch maps from your Elastic Maps Server instance by using the [`map.emsUrl`](https://www.elastic.co/guide/en/kibana/current/maps-connect-to-ems.html#elastic-maps-server-kibana) configuration key. The value of this setting needs to be the URL where the Elastic Maps Server instance is reachable from your browser. The certificates presented by Elastic Maps Server need to be trusted by the browser, and the URL must have the same origin as the URL where your Kibana is hosted to avoid cross origin resource issues. Check the [recipe section](https://github.com/elastic/cloud-on-k8s/tree/2.16/config/recipes/) for an example on how to set this up using an Ingress resource.



