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

An organization is the umbrella for a group of {{ecloud}} resources, users, and account settings. Every organization has a unique identifier.

When you [sign up for {{ecloud}}](/deploy-manage/deploy/elastic-cloud/create-an-organization.md), you have the option to create a new organization. You also can be [added to an existing organization](/deploy-manage/users-roles/cloud-organization/manage-users.md).

The administrator of an organization is referred to as the organization owner, and belongs to the [Organization owner role](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_organization_level_roles). An organization can have more than one organization owner.

## Organization management tasks

As an organization owner, you can perform the following tasks to manage your Cloud organization:

* [Manage billing](/deploy-manage/cloud-organization/billing.md)
* Manage user access to your organization: 
  * [Add members to your organization](/deploy-manage/users-roles/cloud-organization/manage-users.md)
  * [Assign roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md)
  * [Create custom roles](/deploy-manage/users-roles/cloud-enterprise-orchestrator.md) ({{serverless-short}} only)
  * [Configure SAML single sign-on](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) to your organization
* [Manage API keys](/deploy-manage/api-keys.md) to use with the [{{ecloud}}](https://www.elastic.co/docs/api/doc/cloud), [{{ecloud}} Billing](https://www.elastic.co/docs/api/doc/cloud-billing/), and [{{serverless-full}}](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless) APIs
* Configure who receives [operational emails](/deploy-manage/cloud-organization/operational-emails.md) related to your organization
* Track the [status of {{ecloud}} services](/deploy-manage/cloud-organization/service-status.md)
% * [Delete](/deploy-manage/cloud-organization/delete-an-organization.md) an organization.

Several aspects of your organization can also be managed using tools provided by Elastic. For a list of tools, refer to [{{ecloud}} organization tools and APIs](/deploy-manage/cloud-organization/tools-and-apis.md).

::::{tip} 
To learn how to manage your {{ecloud}} account as a user, refer to [Manage your Cloud account](/cloud-account/index.md).
::::

## Managing multiple organizations

You can create or access multiple organizations from a single {{ecloud}} account. 

You might want to create multiple organizations for reasons such as the following:

* You want to separate management of your {{ecloud}} resources and settings for different use cases or teams.
* You want to create a [trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial) to evaluate additional {{ecloud}} features or solutions.

Each organization has its own set of resources, users, settings, and billing and licensing.

You need to be logged in to the organization you want to manage to make changes to its resources and settings. [Learn how to manage multiple organizations](/deploy-manage/cloud-organization/manage-multiple-organizations.md).