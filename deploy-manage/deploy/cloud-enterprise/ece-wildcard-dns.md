---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-wildcard-dns.html
---

# Wildcard DNS record [ece-wildcard-dns]

::::{warning} 
We do not recommend using `ip.es.io` for production systems. Please set up your own domain name and DNS resolver for production. We do not guarantee uptime with `ip.es.io`.
::::

By default, Elastic Cloud Enterprise uses the external `ip.es.io` service provided by Elastic to resolve virtual Elasticsearch cluster host names in compliance with RFC1918. The service works by resolving host names of the form `<ip>.ip.es.io` to `<ip>`. In the case of Elastic Cloud Enterprise, each cluster is assigned a virtual host name of the form `<cluster id>.<proxy ip address>.ip.es.io:<port>`, such as `6dfc65aae62341e18a8b7692dcc97186.10.8.156.132.ip.es.io:9243`. The `ip.es.io` service simply resolves the virtual host name of the cluster to the proxy address which is specified during installation, `10.8.156.132` in our example, so that client requests are sent to the proxy. The proxy then extracts the cluster ID from the virtual host name of the cluster and uses its internal routing table to route the request to the right allocator.

The `ip.es.io` service is provided to help you evaluate Elastic Cloud Enterprise without having to set up DNS records for your environment. You must set up a wildcard DNS record for your production system. You typically set up a wildcard DNS record that resolves to the proxy host or to a load balancer if you set up multiple proxies fronted by a load balancer. You can create both a wildcard DNS entry for your endpoints and a wildcard TLS/SSL certificate, so that you can create multiple clusters without the need for further DNS or TSL/SSL modifications. Simply configure your DNS to point to your load balancers and install your certificates on them, so that communication with the cluster is secure.

A wildcard certificate is enabled based on the deployment domain name. For more information on modifying the deployment domain name, check [Configure endpoints](change-endpoint-urls.md). The deployment domain name also determines the endpoint URLs that are displayed in the Cloud UI.

