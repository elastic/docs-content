---
navigation_title: Traffic filtering
applies_to:
  deployment: 
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: unavailable
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-deployment-configuration.html
---

# Traffic filtering

Traffic filtering allows you to limit how your deployments and clusters can be accessed. Add another layer of security to your installation and deployments by restricting inbound traffic to *only* the sources that you trust.

Depending on your deployment type you can use different mechanisms to restrict traffic, such as [IP filters](./ip-traffic-filtering.md), [private links](./private-link-traffic-filters.md) provided by cloud platforms, or [Kubernetes network policies](./k8s-network-policies.md).

::::{note}
This section covers traffic filtering at the deployment level. If you need the IP addresses used by Elastic Cloud to configure them in your network firewalls, refer to [](./elastic-cloud-static-ips.md).
::::

:::::{tab-set}
:group: deployment-type

::::{tab-item} {{ecloud}}
:sync: cloud

On {{ecloud}}, the following types of traffic filters are available for your {{ech}} deployments:

| **Traffic filter type** | **Status** | **Description** |
|------------|--------------|-------------|
| IP traffic filters | [Configurable](ip-traffic-filtering.md) | IP addresses and Classless Inter-Domain Routing (CIDR) masks |
| AWS VPCs over AWS PrivateLink | [Configurable](aws-privatelink-traffic-filters.md) | AWS PrivateLink filters. Can only be applied to {{ech}} deployments in AWS regions |
| Azure Virtual Networks (VNets) | [Configurable](azure-private-link-traffic-filters.md) | Azure Private Link filters. Can only be applied to {{ech}} deployments in Azure regions |
| GCP Private Service Connect | [Configurable](gcp-private-service-connect-traffic-filters.md) | GCP traffic filters. Can only be applied to {{ech}} deployments in GCP regions |
| Ingress and Egress static IPs | [Configurable](elastic-cloud-static-ips.md) | Enable fixed IP addresses for traffic to and from {{ecloud}} |
| Remote cluster connections | [Configurable](/deploy-manage/remote-clusters.md) | Secure cross-cluster operations |

**How does it work?**

By default, all your {{ecloud}} deployments are accessible over the public internet. They are not accessible over unknown PrivateLink connections. This only applies to external traffic. Internal traffic is managed by {{ecloud}}. For example, {{kib}} can connect to {{es}}, as well as internal services which manage the deployment. Other deployments can’t connect to deployments protected by traffic filters.

In {{ecloud}} you can define traffic filters from the **Features** > **Traffic filters** page, and apply them to your {{ech}} deployments individually from their **Settings** page.

Once you associate at least one traffic filter with a deployment, traffic that does not match any rules (for this deployment) is denied. 

:::{note} 
Traffic filters operate on the proxy. Requests rejected by the traffic filters are not forwarded to the deployment. The proxy responds to the client with `403 Forbidden`.
Domain-based filtering rules are not allowed for Cloud traffic filtering, because the original IP is hidden behind the proxy. Only IP-based filtering rules are allowed.
:::

Filtering rules are grouped into rule sets, which in turn are associated with one or more deployments to take effect. You can have a maximum of 1024 rule sets per organization and 128 rules in each rule set. Rule sets work as follows:

- You can assign multiple rule sets to a single deployment. The rule sets can be of different types. In case of multiple rule sets, traffic can match ANY of them. If none of the rule sets match the request is rejected with `403 Forbidden`.
- Traffic filter rule sets are bound to a single region. The rule sets can be assigned only to deployments in the same region. If you want to associate a rule set with deployments in multiple regions you have to create the same rule set in all the regions you want to apply it to.
- You can mark a rule set as *default*. It is automatically attached to all new deployments that you create in its region. You can detach default rule sets from deployments after they are created. Note that a *default* rule set is not automatically attached to existing deployments.
- Traffic filter rule sets when associated with a deployment will apply to all deployment endpoints, such as {{es}}, {{kib}}, APM Server, and others.
- Any traffic filter rule set assigned to a deployment overrides the default behavior of *allow all access over the public internet endpoint; deny all access over Private Link*. The implication is that if you make a mistake putting in the traffic source (for example, specified the wrong IP address) the deployment will be effectively locked down to any of your traffic. You can use the UI to adjust or remove the rule sets.


::::

::::{tab-item} ECE/ECK
:sync: ece-eck

**Available features**

| **Traffic filter type** | **Status** | **Description** |
|------------|--------------|-------------|
| IP traffic filters | [Configurable](ip-traffic-filtering.md) | IP addresses and Classless Inter-Domain Routing (CIDR) masks |
| AWS VPCs over AWS PrivateLink | N/A | X |
| Azure Virtual Networks (VNets) | N/A | X |
| GCP Private Service Connect | N/A | X |
| Ingress and Egress static IPs | N/A | X |
| Remote cluster connections | [Configurable](/deploy-manage/remote-clusters.md) | Secure cross-cluster operations |

**Before you begin**

On {{ece}}, make sure your [load balancer](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md) handles the `X-Forwarded-For` header appropriately for HTTP requests to prevent IP address spoofing. Make sure the proxy protocol v2 is enabled for HTTP and transport protocols (9243 and 9343).

**How does it work?**

By default, all your deployments are accessible over the public internet, assuming that your orchestrator's proxies are accessible. This only applies to external traffic. Internal traffic is managed by the orchestrator. For example, {{kib}} can connect to {{es}}, as well as internal services which manage the deployment. Other deployments can’t connect to deployments protected by traffic filters.

You can define traffic filters from the **Platform** > **Security** page, and apply them to your {{ech}} deployments individually from their **Settings** page.

Once you associate at least one traffic filter with a deployment, traffic that does not match any rules (for this deployment) is denied. 

:::{note} 
Traffic filters operate on the proxy. Requests rejected by the traffic filters are not forwarded to the deployment. The proxy responds to the client with `403 Forbidden`.
Domain-based filtering rules are not allowed for Cloud traffic filtering, because the original IP is hidden behind the proxy. Only IP-based filtering rules are allowed.
:::

Filtering rules are grouped into rule sets, which in turn are associated with one or more deployments to take effect. You can have a maximum of 512 rule sets per organization and 128 rules in each rule set. Rule sets work as follows:

- You can assign multiple rule sets to a single deployment. The rule sets can be of different types. In case of multiple rule sets, traffic can match ANY of them. If none of the rule sets match the request is rejected with `403 Forbidden`.
- Traffic filter rule sets are bound to a single region. The rule sets can be assigned only to deployments in the same region. If you want to associate a rule set with deployments in multiple regions you have to create the same rule set in all the regions you want to apply it to.
- You can mark a rule set as *default*. It is automatically attached to all new deployments that you create in its region. You can detach default rule sets from deployments after they are created. Note that a *default* rule set is not automatically attached to existing deployments.
- Traffic filter rule sets when associated with a deployment will apply to all deployment endpoints, such as {{es}}, {{kib}}, APM Server, and others.
- Any traffic filter rule set assigned to a deployment overrides the default behavior of *allow all access over the public internet endpoint; deny all access over Private Link*. The implication is that if you make a mistake putting in the traffic source (for example, specified the wrong IP address) the deployment will be effectively locked down to any of your traffic. You can use the UI to adjust or remove the rule sets.

::::

:::{tab-item} Self-managed
:sync: self-managed

| **Traffic filter type** | **Status** | **Description** |
|------------|--------------|-------------|
| IP traffic filters | [Configurable](ip-traffic-filtering.md) | IP addresses and Classless Inter-Domain Routing (CIDR) masks |
| AWS VPCs over AWS PrivateLink | N/A | X |
| Azure Virtual Networks (VNets) | N/A | X |
| GCP Private Service Connect | N/A | X |
| Ingress and Egress static IPs | N/A | X |
| Remote cluster connections | N/A | X |

:::

:::::