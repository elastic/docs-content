---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-invite-users.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-organization.html
applies_to:
  serverless: all
  deployment:
    ess: all
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Join or leave an organization

Organizations in {{ecloud}} group user accounts, projects and deployments under a common billing and access structure. If you have been invited to an organization, you can accept the invitation and become a member. You can also leave an organization at any time, as long as you don’t have active projects or deployments associated with your account.

This guide explains how to join or leave an organization, including steps for handling projects and deployments when switching organizations.

## Accept an invitation [ec-accept-invitation]

Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation. If they do not join within that period, an administrator of the organization will have to send a new invitation. Refer to [manage users](/deploy-manage/users-roles/cloud-organization/manage-users.md) for more information.

## Leave an organization [ec-leave-organization]

On the **Members** tab of the **Organization** page, click the three dots corresponding to your email address and select **Leave organization**.

If you’re the only user in the organization, you can only leave if you deleted all your deployments and projects, and you don’t have pending bills.

## Join an organization from an existing {{ecloud}} account [ec-join-invitation]

If you already belong to an organization, and you want to join a new one you will need to leave your existing organization and follow this steps:

1. Make sure you do not have active projects or deployments before you leave your current organization.
2. Delete your projects or deployments and clear any bills.
3. Leave your current organization.
4. Ask the administrator to invite you to the organization you want to join.
5. Accept the invitation that you will get by email.

Alternatively, for Elastic Cloud Hosted deployments, there's a possibility to migrate your deployments to the new organization through back up and restore operations. In such case:

1. [Back up your deployments to any private repository](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md) so that you can restore them to your new organization.
2. Leave your current organization.
3. Ask the administrator to invite you to the organization you want to join.
4. Accept the invitation that you will get by email.
5. Configure the private repository in your new organization and restore the backup you took in step 1.
