:::{admonition} For organizations with many group memberships
If you configure [`claims.groups`](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-user-properties) to read the list of Azure AD groups from the ID token, be aware that users who belong to many groups may exceed Azure AD’s token size limit. In that case, the `groups` claim will be omitted.

To avoid this, enable the **Groups assigned to the application** option in Azure Entra (**App registrations > Token configuration > Edit groups claim**). This setting limits the `groups` claim to only those assigned to the application.

**Alternative:** If you can’t restrict groups to app-assigned ones, use the [Microsoft Graph Authz plugin for Elasticsearch](https://www.elastic.co/docs/reference/elasticsearch/plugins/ms-graph-authz). It looks up group memberships through Microsoft Graph during authorization, so it continues to work even when the `groups` claim is omitted due to overage.

Refer to [Group overages](https://learn.microsoft.com/en-us/security/zero-trust/develop/configure-tokens-group-claims-app-roles#group-overages) for more information.
:::