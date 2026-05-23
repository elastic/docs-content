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

An [organization](/deploy-manage/cloud-organization.md) is the umbrella for all of your {{ecloud}} resources, users, and account settings. You can create or access multiple organizations from a single {{ecloud}} account. You might want to use multiple organizations for reasons such as the following:

* You want to separate management of your {{ecloud}} resources and settings for different use cases or teams.
* You want to create a [trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial) to evaluate additional {{ecloud}} features or solutions.

Although you can access multiple organizations from the same {{ecloud}} account, each organization is independent. Each organization has its own set of resources, users, settings, and billing and licensing. Because of this, you need to be logged in to the organization you want to manage to make changes to its resources and settings, or invite users to join it.

You can perform the following tasks to manage multiple organizations:

**Admin actions:**

* [Create a new organization](#create-a-new-organization)
* [Invite users to join additional organizations](#invite-users-to-join-additional-organizations)
* [View your users' organization memberships](#view-your-users-organization-memberships)

**User actions:**

* [Accept an invitation](#accept-an-invitation)
* [Log in with multiple organizations](#log-in-with-multiple-organizations)
* [View the organizations you have access to](#view-organizations)
* [Switch to a different organization](#switch-to-a-different-organization)
* [Leave an organization](#leave-an-organization)

## Technical preview limitations

The following limitations apply during the multi-organization tech preview:

* **Email notification links:** Organization-specific links in notification emails, such as billing or deployment health alerts, don't yet carry organization context. If you belong to multiple organizations, an email link might take you to the wrong organization. Switch to the appropriate organization before taking action.

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

## Invite users to join additional organizations

You must [send invitations](/deploy-manage/users-roles/cloud-organization/manage-users.md#ec-invite-users) from the organization you want users to join. You can't invite users to join multiple organizations at once.

If a user already has an {{ecloud}} account, then they don't need to sign up again. Instead, they can log in with their selected login method. 

If your organization uses [SAML SSO](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md), then you don't need to invite users to join the organization. Users are added to the organization automatically when they log in to your identity provider SSO URL.

Organizations can have different authentication requirements. For example, one organization might enforce SAML SSO, while another organization might not enforce any specific login method. If your organization enforces a specific login method, then the user will need to use that method to log in, and might be prompted to re-authenticate. 

## View your users' organization memberships

You can view the organizations that your users are members of from the **Members** tab of the **Organization** page. This page shows which organizations each member of your current organization belongs to.

To view the organizations:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From a deployment or project on the home page, select **Manage**.
3. From the lower navigation menu, select **Organization**.
4. Click the **Members** tab.
5. Click the name of the user you want to view the organizations for.

## Accept an invitation

When you're invited to join an organization, you receive an email with a link to accept the invitation. Invitations expire after 72 hours.

To accept an invitation:

1. Open the invitation email and click **Accept invitation**.
2. Log in if prompted. If you already have an active session in your browser, you don't need to log in again.
3. After accepting, you're switched to the new organization automatically. The new organization also appears in your [list of organizations](#view-organizations).

:::{note}
If the organization enforces a specific login method (such as SAML SSO), you're redirected to that login flow when accepting the invitation.
:::

To decline an invitation, you can ignore the email. The invitation expires automatically after 72 hours.

## Log in with multiple organizations

When you belong to multiple organizations, the login experience depends on whether your browser has information about the organization you most recently used:

* **Returning user (same browser):** You're automatically logged in to the organization you last used. You don't need to select an organization.
* **New browser or cleared data:** After logging in, you're presented with a list of your organizations to choose from. Select the organization you want to access.

If your last used organization enforces a specific login method (such as SAML SSO), you're directed to that login flow automatically.

If you log out, your browser remembers which organization you last used. The next time you log in, you're directed to the appropriate login page for that organization.

:::{include} _snippets/view-orgs.md
:::

:::{include} _snippets/switch-orgs.md
:::

## Leave an organization

You can leave an organization at any time, as long as you are a member of at least one other organization. If you are the only owner of an organization, you must transfer ownership before leaving.

You can leave only the organization you're currently signed in to. To leave a different organization, [switch to it](#switch-to-a-different-organization) first.

:::{warning}
Leaving an organization revokes your access to all of its resources, including deployments, projects, and settings. This action cannot be undone. To rejoin the organization, ask an organization owner to invite you again.
:::

To leave your current organization:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, click on the user menu and select **Profile**.
3. Click the **My organizations** tab.
4. Click **Leave current organization**.
5. In the confirmation dialog, click **Leave current organization** to confirm.