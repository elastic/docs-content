---
applies_to:
  deployment:
    ess: ga
  serverless: ga
navigation_title: "Add private connections"
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Private connections

In {{ech}} and {{serverless-full}}, you can allow traffic between {{es}} and other virtual private cloud (VCP) endpoints hosted by the same cloud provider  by setting up a private connection using that provider's private link service. You can also optionally further filter that cloud provider's traffic using VCP filters. 

Choose the relevant option for your cloud service provider:

| Cloud service provider | Service |
| --- | --- |
| AWS | [AWS PrivateLink](/deploy-manage/security/aws-privatelink-traffic-filters.md) |
| Azure | [Azure Private Link](/deploy-manage/security/azure-private-link-traffic-filters.md) |
| GCP | [GCP Private Service Connect](/deploy-manage/security/gcp-private-service-connect-traffic-filters.md) |

After you set up your private connection, you can [claim ownership of your filter link ID](/deploy-manage/security/claim-traffic-filter-link-id-ownership-through-api.md) to prevent other organizations from using it.

:::{tip}
{{ech}} and {{serverless-full}} also support [IP filters](/deploy-manage/security/ip-filtering-cloud.md). You can apply both IP filters and private connections to a single {{ecloud}} resource.
:::
