---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Manage connected cluster users
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Manage connected cluster users for AutoOps

Learn how to invite users to your {{ecloud}} organization and give them access to AutoOps on your connected ECE, ECK, or self-managed clusters.

## Invite users

:::{note}
:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::
:::

To invite users to your organization and give them access to your cluster:

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
1. From the navigation menu, select **Organization**. 
1. On the **Members** page, click **Invite members**.
1. Enter the email address of the user you want to invite.
    
    To add multiple users, enter their email addresses separated by a space.
1. In the **Assign roles** section, enable **Connected cluster access**. 
1. Set roles for the users on all or selected clusters so that they have the appropriate permissions when they accept the invitation and sign in to {{ecloud}}. 

    Learn more about roles and their levels of access to AutoOps in [{{ecloud}} roles for AutoOps](#assign-roles).
1. Click **Send invites**.
    
    Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation before it expires. If an invitation expires, an admin can resend it.

You can also [manage existing users](/deploy-manage/users-roles/cloud-organization/manage-users.md#manage-existing-users) and [manage users through the {{ecloud}} API](/deploy-manage/users-roles/cloud-organization/manage-users.md#ec-api-organizations).

## {{ecloud}} roles for AutoOps [assign-roles]

The following {{ecloud}} roles determine the level of access to AutoOps features and data:

| Role | Allowed actions in AutoOps |
| --- | --- |
| **Organization owner** | View events and metrics reports <br> Add or edit customizations and notification preferences <br> Connect and disconnect clusters |
| **Connected cluster access** | **Viewer**: <br> View events and metrics reports <br><br>  **Admin** for all connected clusters: <br> View events and metrics reports <br> Add or edit customizations and notification preferences <br> Connect and disconnect clusters <br><br>  **Admin** for selected clusters: <br> View events and metrics reports <br> Connect clusters |
