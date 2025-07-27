---
applies_to:
  deployment:
    self:
navigation_title: Manage users
---

# Manage users

Learn how to invite users to your connected clusters and assign roles to new and existing users.

## Invite users

:::{note}
:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::
:::

To invite users to your organization and give them access to your self-managed cluster:

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, select a cluster.
3. From the lower navigation menu, select **Organization**. 
4. On the **Members** page, click **Invite members**.
5. Enter the email address of the user you want to invite in the textbox. \
To add multiple users, enter their email addresses separated by a space.
6. In the **Assign roles** section, switch on **Connected cluster access**. 
7. Set roles for the user(s) on all or selected self-managed clusters so that they have the appropriate permissions when they accept the invitation and sign in to {{ecloud}}. Learn more about roles and their levels of access to AutoOps in [Assign roles](#assign-roles).
8. Click **Send invites**. \
Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation before it expires. If the invite has expired, an admin can resend the invitation.

You can also [manage existing users](/deploy-manage/users-roles/cloud-organization/manage-users.md#manage-existing-users) and [manage users through the {{ecloud}} API](/deploy-manage/users-roles/cloud-organization/manage-users.md#ec-api-organizations).

## Assign roles

Assign the following roles to new or existing users based on levels of access to AutoOps: 

| Role | Allowed actions in AutoOps |
| --- | --- |
| **Organization owner** | - View events and metrics reports <br> - Add or edit customizations and notification preferences <br> - Connect and disconnect clusters |
| **Connected cluster access** | **Viewer** <br> - View events and metrics reports <br><br>  **Admin** for all connected clusters <br> - View events and metrics reports <br> - Add or edit customizations and notification preferences <br> - Connect and disconnect clusters <br><br>  **Admin** for selected clusters <br> - View events and metrics reports <br> - Add or edit customizations and notification preferences <br> - Connect clusters |
