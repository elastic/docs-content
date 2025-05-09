---
applies_to:
  deployment:
    ess: ga
---

# Private link traffic filters

In {{ech}}, you can allow traffic between {{es}} and other resources hosted by the same cloud provider using private link services. 

Choose the relevant option for your cloud service provider:

| Cloud service provider | Service |
| --- | --- |
| AWS | [AWS PrivateLink](/deploy-manage/security/aws-privatelink-traffic-filters.md) |
| Azure | [Azure Private Link](/deploy-manage/security/azure-private-link-traffic-filters.md) |
| GCP | [GCP Private Service Connect](/deploy-manage/security/gcp-private-service-connect-traffic-filters.md) |

After you set up your private link, you can [claim ownership of your filter link ID](/deploy-manage/security/claim-traffic-filter-link-id-ownership-through-api.md) to prevent other organizations from using it in a traffic filter ruleset.

:::{tip}
{{ech}} also supports [IP traffic filters](/deploy-manage/security/ip-filtering-cloud.md).
:::
