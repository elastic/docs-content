---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-marketplaces.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Subscribe from a marketplace [ec-marketplaces]

You can subscribe to {{ecloud}} from a cloud marketplace instead of paying Elastic directly. Marketplace subscriptions offer the following benefits:

- **Consolidated billing.** Your {{ecloud}} charges appear on your existing cloud provider bill alongside your other services.
- **Spend commitment.** Your {{ecloud}} usage counts toward your committed spend with your cloud provider. If you subscribe directly to Elastic (with a credit card or an Elastic contract), your {{ecloud}} spend does not count toward any cloud provider commitment.
- **Simplified procurement.** No need to set up a separate billing relationship with Elastic.

Trial availability and duration can vary depending on the marketplace.

## Marketplace options

* [{{aws}} Marketplace](aws-marketplace.md)
* [Microsoft Marketplace](azure-native-isv-service.md)
* [{{gcp}} Marketplace](google-cloud-platform-marketplace.md)
* [Heroku](heroku.md) ({{ech}} only - no organization functionality)

::::{tip}
You can also purchase {{ecloud}} through a reseller on any of these marketplaces. Contact your reseller to learn more.
::::

## How marketplaces, organizations, and accounts work together [ec-marketplace-org-relationship]

When you subscribe to {{ecloud}} through a marketplace, a relationship is established between your marketplace account and an {{ecloud}} [organization](/deploy-manage/cloud-organization.md).

- **One marketplace subscription maps to one {{ecloud}} organization.** Billing for all deployments and projects within that organization flows through the linked marketplace subscription. The specifics vary by marketplace:
    - **{{aws}}**: One subscription for each {{aws}} billing account. Customers with multiple {{aws}} accounts (for example, production and development) can have separate subscriptions, each linked to its own {{ecloud}} organization.
    - **{{gcp}}**: One {{ecloud}} organization for each {{gcp}} billing account.
    - **Azure**: Organization creation is tied to Elastic resource creation in the Azure portal, so customers who create multiple resources can accumulate multiple organizations.
- **Each organization can only be linked to a single billing source**: either a marketplace subscription or direct credit card billing.
- **A single {{ecloud}} account can belong to [multiple organizations](/deploy-manage/cloud-organization/manage-multiple-organizations.md).** When you subscribe through a marketplace, you can either create a new organization or link the subscription to an existing one. If your account is organization owner for multiple organizations, you choose which organization to associate with the marketplace subscription.
- **Your {{ecloud}} account uses a single email address across all your organizations.** If you already have an {{ecloud}} account, you can sign in with your existing credentials during the marketplace sign-up process. If you don't have an account, one is created using your marketplace email.

If you already have an {{ecloud}} trial and want to start paying through a marketplace, you can [upgrade your trial to a marketplace subscription](marketplace-trial-upgrade.md) without losing your existing deployments, projects, or data.

## Multi-cloud strategy [ec-marketplace-multi-cloud]

Because a single {{ecloud}} account can belong to multiple organizations, and each organization can be linked to a different marketplace, you can subscribe to multiple marketplaces to support a multi-cloud strategy. For example, you might have:

- An {{aws}} Marketplace subscription for an organization running production workloads on {{aws}}
- A {{gcp}} Marketplace subscription for a separate organization running analytics workloads on {{gcp}}

Each subscription counts toward the respective cloud provider's spend commitment, letting you maximize the benefits of each marketplace independently.
