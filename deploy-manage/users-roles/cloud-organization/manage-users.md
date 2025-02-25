---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-invite-users.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-organization.html
  - https://www.elastic.co/guide/en/cloud/current/ec-api-organizations.html
applies_to:
  deployment:
      serverless: all
      ess: all
---

# Manage users

$$$general-assign-user-roles$$$

You can invite users to join your organization to allow them to interact with all or specific instances, projects and settings. After they're invited, you can manage the users in your organization.

Alternatively, [configure {{ecloud}} SAML SSO](../../../deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) to enable your organization members to join the {{ecloud}} organization automatically.

::::{note}
Users can only belong to one organization at a time. If a user that you want to invite already belongs to a different organization, that user first needs to leave their current organization, or to use a different email address. Check [Join an organization from an existing {{ecloud}} account](/cloud-account/join-or-leave-an-organization.md).
::::

:::{tip}
If you're using {{ech}}, then you can also manage users and control access [at the deployment level](/deploy-manage/users-roles/cluster-or-deployment-auth.md).
:::

## Invite your team [ec-invite-users]

To invite users to your organization:

1. Go to the user icon on the header bar and select **Organization**.
2. On the **Members** page, click **Invite members**.
3. Enter the email addresses of the users you want to invite in the textbox.

    To add multiple members, enter the member email addresses, separated by a space.

4. If desired, assign roles to the users so that they automatically get the appropriate permissions when they accept the invitation and sign in to {{ecloud}}.

   If you're assigning roles for {{serverless-full}} projects, then you can grant access to all projects of the same type with a unique role, or select individual roles for specific projects. For more details about roles, refer to [](/deploy-manage/users-roles/cloud-organization/user-roles.md).

5. Click **Send invites**.

    Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation before it expires. If the invite has expired, an admin can resend the invitation.

## Manage existing users

On the **Members** tab of the **Organization** page, you can view the list of current members, including status and role.

In the **Actions** column, click the three dots to edit a member’s role, or revoke an invite, or remove a member from your organization.

## Manage users through the {{ecloud}} API [ec-api-organizations]

You can also manage members of your organization using the [{{ecloud}} API](https://www.elastic.co/docs/api/doc/cloud/).

:::{dropdown} Get information about your organization

Get information about your {{ecloud}} organization.

```sh
curl -XGET \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations"
```
:::

:::{dropdown} Invite members to your organization

Invite members to your {{ecloud}} organization.

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/invitations" \
-d '
{
  "emails": [
    "test@test.com" <1>
  ]
}'
```

1. One or more email addresses to invite to the organization
:::

:::{dropdown} View pending invitations to your organization

View pending invitations to your {{ecloud}} organization.

```sh
curl -XGET \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/invitations"
```

:::{dropdown} View members in your organization

View members in your {{ecloud}} organization.

```sh
curl -XGET \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/members"
```
:::

:::{dropdown} Remove members from your organization

Remove members from your {{ecloud}} organization.

```sh
curl -XDELETE \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/members/$USER_IDS"
```

`USER_IDS`  One or more comma-delimited user ids to remove from the organization
:::