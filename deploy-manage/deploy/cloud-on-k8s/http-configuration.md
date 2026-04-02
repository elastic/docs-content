---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-maps-http-configuration.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Elastic Maps HTTP configuration [k8s-maps-http-configuration]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


## Load balancer settings and TLS SANs [k8s-maps-http-publish]

By default a `ClusterIP` [service](https://kubernetes.io/docs/concepts/services-networking/service/) is created and associated with the Elastic Maps Server deployment. If you want to expose maps externally with a [load balancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), it is recommended to include a custom DNS name or IP in the self-generated certificate.

Refer to [Reserve static IP and custom domain](/deploy-manage/security/k8s-https-settings.md#k8s-static-ip-custom-domain) for more details.


## Provide your own certificate [k8s-maps-http-custom-tls]

If you want to use your own certificate, the required configuration is identical to {{es}}. Check [Custom HTTP certificate](/deploy-manage/security/k8s-https-settings.md#k8s-setting-up-your-own-certificate).


## Disable TLS [k8s-maps-http-disable-tls]

You can disable the generation of the self-signed certificate and hence disable TLS. Check [Disable TLS](/deploy-manage/security/k8s-https-settings.md#k8s-disable-tls).

### Ingress and {{kib}} configuration [k8s-maps-ingress]

To use Elastic Maps Server from your {{kib}} instances, you need to configure {{kib}} to fetch maps from your Elastic Maps Server instance by using the [`map.emsUrl`](/explore-analyze/visualize/maps/maps-connect-to-ems.md#elastic-maps-server-kibana) configuration key. The value of this setting needs to be the URL where the Elastic Maps Server instance is reachable from your browser. The certificates presented by Elastic Maps Server need to be trusted by the browser, and the URL must have the same origin as the URL where your {{kib}} is hosted to avoid cross origin resource issues. Check the [recipe section](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/) for an example on how to set this up using an Ingress resource.

:::{admonition} Support scope for Ingress Controllers
[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) is a standard Kubernetes concept. While ECK-managed workloads can be publicly exposed using ingress resources, and we provide [example configurations](/deploy-manage/deploy/cloud-on-k8s/recipes.md), setting up an Ingress controller requires in-house Kubernetes expertise.

If ingress configuration is challenging or unsupported in your environment, consider using standard `LoadBalancer` services as a simpler alternative.
:::


