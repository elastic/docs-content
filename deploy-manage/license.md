---
applies_to:
  deployment:
    ece:
    ess:
    eck:
    self:
  serverless:
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
---

# Licenses and subscriptions

Your Elastic license or subscription determines which features are available and what level of support you receive. The same concept applies to every deployment type, but its effects differ:

* **{{ecloud}}**: One subscription applies to your whole organization. What it controls depends on the deployment type:
  * **{{ech}} deployments**: The subscription determines which features your deployments can use and the support level you receive. 
  * **{{serverless-short}} projects**: The subscription determines the support level only. Project features are controlled by each project's [feature tier and add-ons](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons). 
  
  To learn how to change your subscription level, see [Manage your subscription](/deploy-manage/cloud-organization/billing/manage-subscription.md).
* **{{ece}}**: One license at the orchestrator level applies to all deployments. See [](/deploy-manage/license/manage-your-license-in-ece.md).
* **{{eck}}**: One license at the operator level applies to all {{stack}} components it manages. See [](/deploy-manage/license/manage-your-license-in-eck.md).
* **Self-managed cluster**: One license applies to a single cluster. See [](/deploy-manage/license/manage-your-license-in-self-managed-cluster.md).

:::{note}
A paid {{ecloud}} subscription is not required for Cloud Connect. Each cluster's local license determines eligibility for connected services and certain {{ecloud}} features.
:::

## Subscription details

For more details about what is included in each subscription level or, for {{serverless-short}} projects, each feature tier, refer to the following resources:

* For ECE, ECK, and self-managed clusters, refer to [Elastic self-managed subscriptions]({{subscriptions}})

* For {{ecloud}}, refer to the following resources:
  * [{{ecloud}} managed service features]({{subscriptions}}/cloud): Includes feature availability for {{ech}} deployments, and support levels for both {{ech}} deployments and {{serverless-short}} projects.
  * [{{ecloud}} pricing](https://www.elastic.co/pricing)
  * {{serverless-full}} pricing:
    * [{{es-serverless}} projects](https://www.elastic.co/pricing/serverless-search)
    * [{{obs-serverless}} projects](https://www.elastic.co/pricing/serverless-observability)
    * [{{sec-serverless}} projects](https://www.elastic.co/pricing/serverless-security)
  * [{{serverless-short}} project feature overview](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons)
    * [](/solutions/security/security-serverless-feature-tiers.md)
    * [](/solutions/observability/observability-serverless-feature-tiers.md)

    There are no additional project features or add-ons for {{es-serverless}} projects. 
