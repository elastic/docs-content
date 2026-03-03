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

Organizations in {{ecloud}} group user accounts, projects and deployments under a common billing and access structure. If you have been invited to an organization, you can accept the invitation and become a member. You can join multiple organizations, or [create a new organization](/deploy-manage/cloud-organization/manage-multiple-organizations.md#create-a-new-organization).

You can also leave an organization at any time, as long as you don’t have active projects or deployments associated with your account.

This guide explains how to join or leave an organization. To learn how to view organizations you have access to and switch between them, refer to [](switch-organizations.md).

## Accept an invitation [ec-accept-invitation]

Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation. If they do not join within that period, an administrator of the organization will have to send a new invitation. Refer to [manage users](/deploy-manage/users-roles/cloud-organization/manage-users.md) for more information.

If you're a member of more than one organization, then after you accept an invitation, the new organization appears in your list of organizations. You can switch to the new organization by clicking the organization name in the list. Refer to [Switch between organizations](/cloud-account/switch-organizations.md) for more information.

## Leave an organization [ec-leave-organization]

On the **Members** tab of the **Organization** page, click the three dots corresponding to your email address and select **Leave organization**.

If you’re the only user in the organization, you can only leave if you deleted all your deployments and projects, and you don’t have pending bills.
