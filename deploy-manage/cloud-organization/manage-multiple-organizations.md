---
applies_to:
  deployment:
    ess: preview
  serverless: preview
products:
  - id: cloud-hosted
  - id: cloud-serverless
navigation_title: Manage multiple organizations
---

# Manage multiple {{ecloud}} organizations

You can create or access multiple organizations from a single {{ecloud}} account. You might want to use multiple organizations for reasons such as the following:

* You want to separate management of your {{ecloud}} resources and settings for different use cases or teams.
* You want to create a [trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial) to evaluate additional {{ecloud}} features or solutions.

Although you can access multiple organizations from the same {{ecloud}} account, each organization is independent. Each organization has its own set of resources, users, settings, and billing and licensing. Because of this, you need to be logged in to the organization you want to manage to make changes to its resources and settings, or invite users to join it.

You can perform the following tasks to manage multiple organizations:

* [Create a new organization](#create-a-new-organization)
* [View the organizations you have access to](#view-organizations)
* [Switch to a different organization](#switch-to-a-different-organization)
* [Invite users to join additional organizations](#invite-users-to-join-additional-organizations)
* [View your users' organization memberships](#view-your-users-organization-memberships)
% * [Delete an organization](#delete-an-organization)

## Create a new organization

You can create a new organization at any time. Each organization starts with its own [14-day trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).

To create a new organization:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, click on the user menu and select **Profile**.
3. Click the **My organizations** tab.
4. From the **Organizations** page, click {icon}`plus_in_circle` **Create organization**.
5. Enter an optional name for your organization, and then click **Create organization**.

After you create the organization, you can switch to it by clicking the organization name in the **Organizations** list.

:::{tip}
You can also create a new organization by clicking on your current organization name and selecting {icon}`plus_in_circle`  **Create**.
:::

:::{include} _snippets/view-orgs.md
:::


:::{include} _snippets/switch-orgs.md
:::

% ## Delete an organization

% Can it be done? Do we want to document this?

% tech preview content below - this would probably be split off onto other pages at GA time

## Invite users to join additional organizations

Because users are managed at the organization level, you must [invite users](/deploy-manage/users-roles/cloud-organization/manage-users.md#ec-invite-users) from within the organization that you want them to join. You can't invite users to join multiple organizations at once.

If a user already has an {{ecloud}} account, then they don't need to sign up again. Instead, they can log in with their selected login method. 

If your organization uses [SAML SSO](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md), then you don't need to invite users to join the organization. Users are added to the organization automatically when they log in to your identity provider SSO URL.

Organizations can have different authentication requirements. For example, one organization might enforce SAML SSO, while another organization might enforce email-based authentication. If your organization enforces a specific login method, then the user will need to use that method to log in, and might be prompted to re-authenticate. 

## View your users' organization memberships

You can view the organizations that your users are members of from the **Members** tab of the **Organization** page. This page shows which organizations each member of your current organization belongs to.

To view the organizations:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From a deployment or project on the home page, select **Manage**.
3. From the lower navigation menu, select **Organization**.
4. Click the **Members** tab.
5. Click the name of the user you want to view the organizations for.