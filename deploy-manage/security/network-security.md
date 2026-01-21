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

Network security allows you to control how your deployments and clusters can be accessed. Add another layer of security to your installation and deployments by restricting traffic to only the sources that you trust.

Elastic also offers other network security features, such as TLS encryption. For an overview of the available security features, refer to [](/deploy-manage/security.md).

:::{note}
The network security feature was formerly referred to as traffic filtering.

Network security policies were formerly referred to as traffic filter rules.
:::

## Network security methods

Depending on your deployment type you can use different mechanisms to control access.

::::{note}
This section covers network security at the deployment level. If you need the IP addresses used by {{ech}} to configure them in your network firewalls, refer to [](./elastic-cloud-static-ips.md).

You can also allow traffic to or from a [remote cluster](/deploy-manage/remote-clusters.md) for use with cross-cluster replication or search.
::::

| Filter type | Description | Applicable deployment types |
| --- | --- | --- |
| [IP filters](ip-filtering.md) | Filter traffic from the public internet by allowlisting specific IP addresses and Classless Inter-Domain Routing (CIDR) masks.<br><br>• [In {{serverless-short}} or ECH](/deploy-manage/security/ip-filtering-cloud.md)<br><br>• [In ECE](/deploy-manage/security/ip-filtering-ece.md)<br><br>• [In ECK or self-managed](/deploy-manage/security/ip-filtering-basic.md) | {{serverless-short}}, ECH, ECE, ECK, and self-managed clusters |
| [Remote cluster filters](./remote-cluster-filtering.md) | Filter incoming remote cluster traffic by validating the client certificate against its `organization_id` and `cluster_id`.<br><br>Only applicable with the API key–based authentication model.<br><br>Not supported for ECE → ECH traffic. | ECH and ECE, limited to [these use cases](/deploy-manage/remote-clusters.md#use-cases-network-security) |
| [Private connectivity and VPC filtering](/deploy-manage/security/private-connectivity.md) | Establish private connections between {{es}} and other resources hosted by the same cloud provider using private link services, and further secure these connections using VPC filtering. Choose the relevant option for your region:<br><br>• AWS regions: [AWS PrivateLink](/deploy-manage/security/private-connectivity-aws.md)<br><br>• Azure regions: [Azure Private Link](/deploy-manage/security/private-connectivity-azure.md)<br><br>• GCP regions: [GCP Private Service Connect](/deploy-manage/security/private-connectivity-gcp.md) | {{ech}} only |
| [Kubernetes network policies](/deploy-manage/security/k8s-network-policies.md) | Isolate pods by restricting incoming and outgoing network connections to a trusted set of sources and destinations. | {{eck}} only |

:::{include} _snippets/eck-traffic-filtering.md
:::

## How network security works
```{applies_to}
deployment:
  ece: all
  ess: all
serverless: all
```

By default, in {{serverless-full}}, {{ech}}, and {{ece}}, all external traffic is allowed. After you apply a network security mechanism, such as an IP filtering rule in an {{ece}} deployment or a network security policy in an {{ecloud}} deployment or project, only traffic that matches the configured rules or policies is allowed; all other traffic is denied.

For details about how these policies and rules interact with your deployment or project, other policies or rules, and the internet, refer to the topic for your deployment type:

* [](network-security-policies.md)
* [](ece-filter-rules.md)

:::{note}
For details about how basic IP filters and Kubernetes network policies impact your cluster, refer to the guide for the feature: 

* [](/deploy-manage/security/ip-filtering-basic.md)
* [](/deploy-manage/security/k8s-network-policies.md) 
:::