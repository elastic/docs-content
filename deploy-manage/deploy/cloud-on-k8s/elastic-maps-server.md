---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-maps.html
---

# Elastic Maps Server [k8s-maps]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


If you cannot connect to Elastic Maps Service from the Kibana server or browser clients, and you are running ECK with an Enterprise license, you can opt to host the service on your Kubernetes cluster. Check also the [Elastic Maps Server documentation.](https://www.elastic.co/guide/en/kibana/current/maps-connect-to-ems.html#elastic-maps-server)

The following sections describe how to customize an Elastic Maps Server deployment to suit your requirements.

* [Deploy Elastic Maps Server](deploy-elastic-maps-server.md)
* [Map data](map-data.md)

    * [Basemap Download](map-data.md#k8s-maps-basemap-download)
    * [Pod Configuration](map-data.md#k8s-maps-pod-configuration)

* [Advanced configuration](advanced-configuration-maps-server.md)

    * [Elastic Maps Server configuration](advanced-configuration-maps-server.md#k8s-maps-configuration)
    * [Scale out an Elastic Maps Server deployment](advanced-configuration-maps-server.md#k8s-maps-scaling)

* [HTTP Configuration](http-configuration.md)

    * [Load balancer settings and TLS SANs](http-configuration.md#k8s-maps-http-publish)
    * [Provide your own certificate](http-configuration.md#k8s-maps-http-custom-tls)
    * [Disable TLS](http-configuration.md#k8s-maps-http-disable-tls)
    * [Ingress and Kibana configuration](http-configuration.md#k8s-maps-ingress)






