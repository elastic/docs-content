---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-invite-users.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-organization.html
---

# Join or leave an organization

## Accept an invitation [ec-accept-invitation]

Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation. If they do not join within that period, an administrator of the organization will have to send a new invitation. Refer to [manage users](/deploy-manage/users-roles/cloud-organization/manage-users.md) for more information.

## Leave an organization [ec-leave-organization]

On the **Members** tab of the **Organization** page, click the three dots corresponding to your email address and select **Leave organization**.

If you’re the only user in the organization, you can only leave if you deleted all your deployments and projects, and you don’t have pending bills.

## Join an organization from an existing {{ecloud}} account [ec-join-invitation]

You already belong to an organization. If you want to join a new one and bring your deployments over, follow these steps:

1. Back up your deployments to any private repository so that you can restore them to your new organization.
2. Leave your current organization.
3. Ask the administrator to invite you to the organization you want to join.
4. Accept the invitation that you will get by email.
5. Restore the backup you took in step 1.

If you want to join a new one, but leave your deployments, follow these steps:

1. Make sure you do not have active deployments before you leave your current organization.
2. Delete your deployments and clear any bills.
3. Leave your current organization.
4. Ask the administrator to invite you to the organization you want to join.
5. Accept the invitation that you will get by email.