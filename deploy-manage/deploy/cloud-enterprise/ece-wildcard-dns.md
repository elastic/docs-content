---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-wildcard-dns.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Wildcard DNS record and certificates [ece-wildcard-dns]

::::{warning} 
Don't use `ip.es.io` for production systems. Set up your own domain name and DNS resolver for production. We do not guarantee uptime with `ip.es.io`.

`ip.es.io` is intended for use only by {{ece}} customers. We may, acting in our sole discretion, immediately terminate, suspend, or block any unauthorized users or uses without notice.  
::::

By default, {{ece}} uses the external `ip.es.io` service provided by Elastic to resolve virtual {{es}} cluster host names in compliance with RFC1918. The service works by resolving host names of the form `<ip>.ip.es.io` to `<ip>`. In the case of {{ece}}, each cluster is assigned a virtual host name of the form `<cluster id>.<proxy ip address>.ip.es.io:<port>`, such as `6dfc65aae62341e18a8b7692dcc97186.10.8.156.132.ip.es.io:9243`. 

The `ip.es.io` service simply resolves the virtual host name of the cluster to the proxy address which is specified during installation, `10.8.156.132` in our example, so that client requests are sent to the proxy. The proxy then extracts the cluster ID from the virtual host name of the cluster and uses its internal routing table to route the request to the right allocator.

## Considerations for production

The `ip.es.io` service is provided to help you evaluate {{ece}} without having to set up DNS records for your environment. You must set up a wildcard DNS record for your production system. You typically set up a wildcard DNS record that resolves to the proxy host or to a load balancer if you set up multiple proxies fronted by a load balancer. You can create both a wildcard DNS entry for your endpoints and a wildcard TLS/SSL certificate, so that you can create multiple clusters without the need for further DNS or TSL/SSL modifications. Simply configure your DNS to point to your load balancers and install your certificates on them, so that communication with the cluster is secure.

## Configuring wildcard DNS certificates

{{ece}} highly recommends using a wildcard DNS certificate, typically configured as a subdomain (for example, `*.ece.mycompany.com`), to automatically secure the unique endpoints generated for each deployment (for example, `[cluster-id].ece.mycompany.com`). For details on modifying the deployment domain name, see [Change endpoint URLs](change-endpoint-urls.md). The deployment domain name also determines the endpoint URLs displayed in the Cloud UI.

Additionally, if you use custom endpoint aliases, you must configure a wildcard DNS certificate for each application-specific subdomain, such as `*.es.mycompany.com` for {{es}} or `*.kb.mycompany.com` for {{kib}}. Refer to [Enable custom endpoint aliases](./enable-custom-endpoint-aliases.md) for more information. Platform administrators must enable this feature to allow deployment managers to create and modify aliases for their deployments.


### Wildcard DNS certificate vs static SAN certificates

In {{ece}}, each deployment generates multiple DNS entries, as every component within a deployment has its own cluster ID and fully qualified domain name (FQDN), and may also have an [alias](./enable-custom-endpoint-aliases.md). In environments with many deployments, especially when aliases are used, this can result in hundreds of unique FQDNs that must be covered by the certificate.

For this reason, using a wildcard DNS certificate for a subdomain, such as `*.ece.mycompany.com`, is recommended over a certificate with static SAN entries, as it offers a more scalable, efficient, and operationally safe solution:

* **Operational cost:** Because deployment FQDNs cannot be predicted in advance, a wildcard certificate provides optimal flexibility, allowing the proxy to present a valid certificate for any deployment URL. In contrast, a certificate with static SAN entries must be reissued whenever a new deployment is created, which increases the operational overhead.

* **Security:** We suggest configuring your wildcard DNS certificate for a subdomain, such as `*.ece.mycompany.com`. Doing so significantly reduces security risks associated with certificate misconfigurations. In contrast, if a certificate with static SAN entries does not include the new deployment’s cluster IDs, clients will encounter certificate name mismatch warnings, indicating a security misconfiguration.

* **Performance:** Wildcard certificates are generally more performant than certificates with a large number of SAN entries. They are smaller, which reduces TLS handshake time, and scale automatically with new deployments. In contrast, certificates with a large number of SAN entries can increase handshake latency and may affect client compatibility.


