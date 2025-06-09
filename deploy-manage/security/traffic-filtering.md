---
navigation_title: Network security
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-deployment-configuration.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-deployment-configuration.html
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
  serverless: ga
products:
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: elasticsearch
  - id: cloud-serverless
---

# Network security

Network security allows you to limit how your deployments and clusters can be accessed. Add another layer of security to your installation and deployments by restricting inbound traffic to only the sources that you trust.

## Network security methods

Depending on your deployment type you can use different mechanisms to restrict traffic.

::::{note}
This section covers network security at the deployment level. If you need the IP addresses used by {{ech}} to configure them in your network firewalls, refer to [](./elastic-cloud-static-ips.md).

You can also allow traffic to or from a [remote cluster](/deploy-manage/remote-clusters.md) for use with cross-cluster replication or search.
::::

| Filter type | Description | Applicable deployment types |
| --- | --- | --- |
| [IP filters](ip-traffic-filtering.md) | Filter traffic using IP addresses and Classless Inter-Domain Routing (CIDR) masks.<br><br>• [In {{serverless-short}} or ECH](/deploy-manage/security/ip-filtering-cloud.md)<br><br>• [In ECE](/deploy-manage/security/ip-filtering-ece.md)<br><br>• [In ECK or self-managed](/deploy-manage/security/ip-filtering-basic.md) | {{serverless-short}}, ECH, ECE, ECK, and self-managed clusters |
| [Private connections and VCPE filtering](/deploy-manage/security/private-link-traffic-filters.md) | Allow traffic between {{es}} and other resources hosted by the same cloud provider using private link services. Choose the relevant option for your region:<br><br>• AWS regions: [AWS PrivateLink](/deploy-manage/security/aws-privatelink-traffic-filters.md)<br><br>• Azure regions: [Azure Private Link](/deploy-manage/security/azure-private-link-traffic-filters.md)<br><br>• GCP regions: [GCP Private Service Connect](/deploy-manage/security/gcp-private-service-connect-traffic-filters.md) | {{ech}} only |
| [Kubernetes network policies](/deploy-manage/security/k8s-network-policies.md) | Isolate pods by restricting incoming and outgoing network connections to a trusted set of sources and destinations. | {{eck}} only |

:::{include} _snippets/eck-traffic-filtering.md
:::

## How security rules and policies work

By default, in {{serverless-full}}, {{ech}}, and {{ece}}, all your deployments are accessible over the public internet. After you associate at least one IP filtering rule with an {{ece}} deployment, or one network security policy with an {{ecloud}} deployment or project, traffic that does not match any rules or policies for the deployment or project is denied.

For details about how these rules and policies interact with your deployment or project, other rules or policies, and the internet, refer to the topic for your deployment type:

* [](network-security-policies.md)
* [](ece-filter-rules.md)

:::{note}
For details about how IP filters and Kubernetes network policies impact your network, refer to the guide for the feature: 

* [](/deploy-manage/security/ip-filtering-basic.md)
* [](/deploy-manage/security/k8s-network-policies.md) 
:::