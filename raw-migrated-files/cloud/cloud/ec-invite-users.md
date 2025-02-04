---
navigation_title: "Invite members to your organization"
---

# Invite members to your {{ecloud}} organization [ec-invite-users]


By inviting users to join your organization, you can allow them to interact with all or specific instances and settings. To do that, some predefined roles are available for you to assign to your organization’s members.

To invite a new member, go to your avatar in the upper right corner, choose **Organization** and click **Invite members**. You can add multiple members by entering their email addresses separated by a space. You can also assign roles to the users when you invite them, so that they automatically get the appropriate permissions when they accept the invitation and sign in to {{ecloud}}.

::::{note}
Users can only belong to one organization at a time. If a user that you want to invite already belongs to a different organization, that user first needs to leave their current organization, or to use a different email address. Check [Join an organization from an existing {{ecloud}} account](../../../deploy-manage/users-roles/cloud-organization/manage-users.md#ec-join-invitation).
::::


Alternatively, [configure {{ecloud}} SAML SSO](../../../deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) to enable your organization members to join the {{ecloud}} organization automatically. [preview]

On the **Members** tab of the **Organization** page, you can view the list of current members, their status, and their roles.

:::{image} ../../../images/cloud-ec-org-members-tab.png
:alt: Members tab
:::

To edit a member’s roles, in the **Actions** column click the three dots and select **Edit role**.


## Accept an invitation [ec-accept-invitation]

Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation. If they do not join within that period, you will have to send a new invitation.


## Join an organization from an existing {{ecloud}} account [ec-join-invitation]

You already belong to an organization. If you want to join a new one and bring your deployments over, follow these steps:

1. Backup your deployments to any private repository so that you can restore them to your new organization.
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


## Leave an organization [ec-leave-organization]

On the **Members** tab of the **Organization** page, click the three dots corresponding to your email address and select **Leave organization**.

If you’re the only user in the organization, you can only leave if you deleted all your deployments and projects, and you don’t have pending bills.

