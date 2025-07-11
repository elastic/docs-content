---
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Private connectivity

Private connectivity is a secure way for your {{ecloud}} deployments and projects to communicate with other cloud provider services over your cloud provider's private network. You can create a virtual private connection (VPC) using your provider's private link service, and then manage it in {{ecloud}} using a private connection policy. You can also optionally filter traffic to your deployments by creating ingress filters for your VPC in {{ecloud}}.

:::{tip}
Private connection policies are a type of [network security policy](/deploy-manage/security/network-security-policies.md).
:::

Choose the relevant option for your cloud service provider:

| Cloud service provider | Service |
| --- | --- |
| AWS | [AWS PrivateLink](/deploy-manage/security/private-connectivity-aws.md) |
| Azure | [Azure Private Link](/deploy-manage/security/private-connectivity-azure.md) |
| GCP | [GCP Private Service Connect](/deploy-manage/security/private-connectivity-gcp.md) |

After you set up your private connection, you can [claim ownership of your private connection ID](/deploy-manage/security/claim-private-connection-api.md) to prevent other organizations from using it.

To learn how private connection policies work, how they affect your deployment, and how they interact with [IP filter policies](ip-filtering-cloud.md), refer to [](/deploy-manage/security/network-security-policies.md).

:::{tip}
{{ech}} and {{serverless-full}} also support [IP filters](/deploy-manage/security/ip-filtering-cloud.md). You can apply both IP filters and private connections to a single {{ecloud}} resource.
:::

:::{note}
Private connection policies were formerly referred to as PrivateLink traffic filters.
:::