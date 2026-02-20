---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-organizations.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
---

# Manage your Cloud organization [ec-organizations]

When you [sign up for {{ecloud}}](/deploy-manage/deploy/elastic-cloud/create-an-organization.md), you create an organization. This organization is the umbrella for all of your {{ecloud}} resources, users, and account settings. Every organization has a unique identifier. 

You can perform the following tasks to manage your Cloud organization:

* [Manage billing](/deploy-manage/cloud-organization/billing.md)
* Manage user access to your organization: 
  * [Add members to your organization](/deploy-manage/users-roles/cloud-organization/manage-users.md)
  * [Assign roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md)
  * [Create custom roles](/deploy-manage/users-roles/cloud-enterprise-orchestrator.md) ({{serverless-short}} only)
  * [Configure SAML single sign-on](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) to your organization
* [Manage API keys](/deploy-manage/api-keys.md) to use with the [{{ecloud}}](https://www.elastic.co/docs/api/doc/cloud), [{{ecloud}} Billing](https://www.elastic.co/docs/api/doc/cloud-billing/), and [{{serverless-full}}](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless) APIs. For {{serverless-full}} projects, you can also create {{ecloud}} API keys that grant access to project-level {{es}} and {{kib}} APIs.
* Configure who receives [operational emails](/deploy-manage/cloud-organization/operational-emails.md) related to your organization
* Track the [status of {{ecloud}} services](/deploy-manage/cloud-organization/service-status.md).

Several aspects of your organization can also be managed using tools provided by Elastic. For a list of tools, refer to [{{ecloud}} organization tools and APIs](/deploy-manage/cloud-organization/tools-and-apis.md).

::::{tip} 
To learn how to manage your {{ecloud}} account as a user, refer to [Manage your Cloud account](/cloud-account/index.md).
::::
