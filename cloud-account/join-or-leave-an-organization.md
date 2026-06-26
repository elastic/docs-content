---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-invite-users.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-organization.html
applies_to:
  serverless: ga
  deployment:
    ess: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Join or leave an organization

Organizations in {{ecloud}} group user accounts, projects, and deployments under a common billing and access structure. If you have been invited to an organization, you can accept the invitation and become a member. You can join multiple organizations, or [create a new organization](/deploy-manage/cloud-organization/manage-multiple-organizations.md#create-a-new-organization).

You can also leave an organization, with some restrictions. Refer to [Leave an organization](#ec-leave-organization) for details.

This guide explains how to join or leave an organization. To learn how to view organizations you have access to and switch between them, refer to [](switch-organizations.md).

:::{tip}
If you're an organization owner or admin, refer to [](/deploy-manage/cloud-organization/manage-multiple-organizations.md) to learn how to manage multiple organizations.
:::

## Accept an invitation [ec-accept-invitation]

When you're invited to join an organization, you receive an email with a link to accept the invitation. Invitations expire after 72 hours. If you don't accept within that period, an administrator of the organization needs to send a new invitation. Refer to [manage users](/deploy-manage/users-roles/cloud-organization/manage-users.md) for more information.

To accept an invitation:

1. Open the invitation email and click **Accept invitation**.
2. Log in if prompted. If you already have an active session in your browser, you don't need to log in again.
3. After accepting, you're switched to the new organization automatically. The new organization also appears in your [list of organizations](/cloud-account/switch-organizations.md).

:::{note}
If the organization enforces a specific login method, such as SAML SSO, you're redirected to that login flow when accepting the invitation.
:::

To decline an invitation, you can ignore the email. The invitation expires automatically after 72 hours.

## Leave an organization [ec-leave-organization]

You can leave an organization at any time. If you are the only owner of an organization, you must transfer ownership before leaving.

You can leave only the organization you're currently signed in to. To leave a different organization, [switch to it](/cloud-account/switch-organizations.md) first.

:::{warning}
Leaving an organization revokes your access to all of its resources, including deployments, projects, and settings. This action cannot be undone. To rejoin the organization, ask an organization owner to invite you again.
:::

To leave your current organization:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, click on the user menu and select **Profile**.
3. Click the **My organizations** tab.
4. Click **Leave current organization**.
5. In the confirmation dialog, click **Leave current organization** to confirm.
