---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-invite-users.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-organization.html
  - https://www.elastic.co/guide/en/cloud/current/ec-api-organizations.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Manage users

$$$general-assign-user-roles$$$

You can invite users to join your organization to allow them to interact with all or specific {{ecloud}} resources and settings. After they're invited, you can manage the users in your organization.

Alternatively, [configure {{ecloud}} SAML SSO](../../../deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md) to enable your organization members to join the {{ecloud}} organization automatically.

::::{note}
Users can only belong to one organization at a time. If a user that you want to invite already belongs to a different organization, that user first needs to leave their current organization, or to use a different email address. Check [Join an organization from an existing {{ecloud}} account](/cloud-account/join-or-leave-an-organization.md).
::::

:::{tip}
If you're using {{ech}}, then you can also manage users and control access [at the deployment level](/deploy-manage/users-roles/cluster-or-deployment-auth.md).
:::

## Invite your team [ec-invite-users]

To invite users to your organization:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From a deployment or project on the home page, select **Manage**.
3. From the lower navigation menu, select **Organization**.
4. On the **Members** page, click **Invite members**.
5. Enter the email addresses of the users you want to invite in the textbox.

    To add multiple members, enter the member email addresses, separated by a space.

5. If desired, assign roles to the users so that they automatically get the appropriate permissions when they accept the invitation and sign in to {{ecloud}}.

   If you're assigning roles for {{serverless-full}} projects, then you can grant access to all projects of the same type with a unique role, or select individual roles for specific projects. For more details about roles, refer to [](/deploy-manage/users-roles/cloud-organization/user-roles.md).

6. Click **Send invites**.

    Invitations to join an organization are sent by email. Invited users have 72 hours to accept the invitation before it expires. If the invite has expired, an admin can resend the invitation.

## Manage existing users

On the **Members** tab of the **Organization** page, you can view the list of current members, including status and role.

In the **Actions** column, click the three dots to edit a member’s role, or revoke an invite, or remove a member from your organization.

## Manage users through the {{ecloud}} API [ec-api-organizations]

You can also manage members of your organization using the [{{ecloud}} API]({{cloud-apis}}).

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

When creating an invitation, you can define the user's roles and specify the resources they will have access to in the API request body:

```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/invitations" \
-d '
{
  "emails": [
    "test@test.com"
  ],
  "role_assignments": {
    "deployment": [
      {
        "role_id": "deployment-admin",
        "organization_id": "ORG_ID_PLACEHOLDER",
        "all": true
      }
    ],
    "project": {
      "elasticsearch": [
        {
          "role_id": "elasticsearch-viewer", <1>
          "organization_id": "ORG_ID_PLACEHOLDER",
          "all": false,
          "project_ids": [
            "ES_PROJECT_ID_PLACEHOLDER"
          ],
          "application_roles": [
            "logs_viewer"
          ] <2>
        }
      ],
      "observability": [
        {
          "role_id": "observability-editor",
          "organization_id": "ORG_ID_PLACEHOLDER",
          "all": false,
          "project_ids": [
            "OBS_PROJECT_ID_PLACEHOLDER"
          ],
          "application_roles": [
          ] <3>
        }
      ]
    }
  }
}'
```
1. When granting a custom serverless role, you need to grant the relevant `viewer` role ID for the project type.
2. [Custom roles](/deploy-manage/users-roles/serverless-custom-roles.md) for the user in this {{serverless-short}} project. 
3. Pass an empty `application_roles` array to only grant the user Cloud Console access to the relevant resources. [Learn more about access options](/deploy-manage/users-roles/cloud-organization/user-roles.md#access).
:::

:::{dropdown} View pending invitations to your organization

View pending invitations to your {{ecloud}} organization.

```sh
curl -XGET \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID/invitations"
```
:::

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