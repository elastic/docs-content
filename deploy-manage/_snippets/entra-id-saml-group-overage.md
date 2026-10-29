### Symptoms

* Some users receive a `Forbidden` response or don't receive the expected roles after signing in with Microsoft Entra ID.
* Their SAML assertion contains `http://schemas.microsoft.com/claims/groups.link` instead of the group membership attribute used by your role mappings.

### Resolution

Microsoft Entra ID limits group claims in SAML assertions to 150 groups, including nested groups. When a user exceeds this limit, Entra ID omits the group list and sends a link to retrieve memberships through a Graph API instead. This is called a *group overage*. Role mappings that depend on the missing groups don't match.

Configure Entra ID to send only the groups needed for access to Elastic. The **Groups assigned to the application** option requires a Microsoft Entra ID license that supports assigning groups to applications. It includes only direct group memberships, so users who access Elastic through nested groups need direct membership in a group assigned to the application.

1. In Microsoft Entra ID, open **Enterprise applications** and select the application you configured for Elastic SAML SSO.
2. In **Users and groups**, assign the groups used by your Elastic role mappings. Confirm that affected users are direct members of these groups.
3. In **Single sign-on** → **Attributes & Claims**, edit the group claim and select **Groups assigned to the application**. Keep the claim name and source attribute required by your Elastic configuration, then save your changes.
4. Confirm that the groups returned for each user stay within the 150-group SAML limit. Assigning groups to the application reduces the group list but doesn't remove this limit.
5. Sign in again with an affected user. Confirm that the SAML assertion includes the expected group values and that the user receives the roles assigned by your Elastic role mappings.

For details about group assignment and other ways to limit group claims, refer to [Configure group claims for applications](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-fed-group-claims) and [Group overages](https://learn.microsoft.com/en-us/security/zero-trust/develop/configure-tokens-group-claims-app-roles#group-overages) in the Microsoft documentation.
