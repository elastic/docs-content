---
navigation_title: With Microsoft Entra ID
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-securing-clusters-saml-azure.html
applies_to:
  deployment:
    self:
    ess:
    ece:
    eck:
products:
  - id: cloud-hosted
---
# Set up SAML with Microsoft Entra ID [ec-securing-clusters-saml-azure]

This guide provides a walk-through of how to configure Microsoft Entra ID, formerly known as Azure Active Directory, as an identity provider for SAML single sign-on (SSO) authentication, used for accessing {{kib}} in {{ech}}.

For more information about SAML configuration, refer to:

* [Secure your clusters with SAML](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md)
* [Single Sign-On SAML protocol](https://docs.microsoft.com/en-us/azure/active-directory/develop/single-sign-on-saml-protocol)


## Configure SAML with Microsoft Entra ID to access {{kib}} [ec-securing-clusters-saml-azure-kibana]

Follow these steps to configure SAML with Microsoft Entra ID as an identity provider to access {{kib}}.

1. Configure the Entra Identity Provider:

    1. Log in to the [Azure Portal](https://portal.azure.com/) and navigate to **Entra** (formerly Azure Active Directory).
    2. Click **Enterprise applications** and then **New application** to register a new application.
    3. Click **Create your own application**, provide a name, and select the **Integrate any other application you don’t find in the gallery** option.

        :::{image} /deploy-manage/images/cloud-ec-saml-azuread-create-app.png
        :alt: The Azure Create your own application flyout
        :::

    4. Navigate to the new application, click **Users and groups**, and add all necessary users and groups. Only the users and groups that you add here will have SSO access to the {{stack}}.

        :::{image} /deploy-manage/images/cloud-ec-saml-azuread-users-and-groups.png
        :alt: The Entra User and groups page
        :::

    5. Navigate to **Single sign-on** and edit the basic SAML configuration, adding the following information:

        * `Identifier (Entity ID)` - a string that uniquely identifies a SAML service provider. We recommend using your {{kib}} URL, but you can use any identifier.

            For example, `https://saml-azure.kb.northeurope.azure.elastic-cloud.com:443`.

        * `Reply URL` - This is the {{kib}} URL with `/api/security/saml/callback` appended.

            For example, `https://saml-azure.kb.northeurope.azure.elastic-cloud.com:443/api/security/saml/callback`.

        * `Logout URL` - This is the {{kib}} URL with `/logout` appended.

            For example, `https://saml-azure.kb.northeurope.azure.elastic-cloud.com:443/logout`.

            :::{image} /deploy-manage/images/cloud-ec-saml-azuread-kibana-config.png
            :alt: The Entra SAML configuration page with {{kib}} settings
            :::

    6. Navigate to **SAML-based Single sign-on**, open the **User Attributes & Claims** configuration, and update the fields to suit your needs. These settings control what information from  will be made available to the {{stack}} during SSO. This information can be used to identify a user in the {{stack}} and/or to assign different roles to users in the {{stack}}. We suggest that you configure a proper value for the `Unique User Identifier (Name ID)` claim that identifies the user uniquely and is not prone to changes.

        :::{image} /deploy-manage/images/cloud-ec-saml-azuread-user-attributes.png
        :alt: The Entra ID User Attributes & Claims page
        :::

    7. From the SAML configuration page, make a note of the `App Federation Metadata URL`.

2. Configure {{es}} and {{kib}} for SAML:

    1. [Update your {{es}} user settings](/deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

        ```sh
        xpack.security.authc.realms.saml.kibana-realm:
          order: 2
          attributes.principal: nameid
          attributes.groups: "http://schemas.microsoft.com/ws/2008/06/identity/claims/groups"
          idp.metadata.path: "https://login.microsoftonline.com/<Tenant ID>/federationmetadata/2007-06/federationmetadata.xml?appid=<Application_ID>"
          idp.entity_id: "https://sts.windows.net/<Tenant_ID>/"
          sp.entity_id: "<Kibana_Endpoint_URL>"
          sp.acs: "<Kibana_Endpoint_URL>/api/security/saml/callback"
          sp.logout: "<Kibana_Endpoint_URL>/logout"
        ```

        Where:

        * `<Application_ID>` is your Application ID, available in the application details in Azure.
        * `<Tenant_ID>` is your Tenant ID, available in the tenant overview page in Azure.
        * `<Kibana_Endpoint_URL>` is your {{kib}} endpoint, available from the {{ech}} console. Ensure this is the same value that you set for `Identifier (Entity ID)` in the earlier Microsoft Entra ID configuration step.

        * For `idp.metadata.path`, we’ve shown the format to construct the URL. This value should be identical to the `App Federation Metadata URL` setting that you made a note of in the previous step.

        :::{admonition} For organizations with many group memberships
        If you configure [`attributes.groups`](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-es-user-properties) to read the list of Azure AD groups from the SAML assertion, be aware that users who belong to many groups may exceed Azure AD’s size limit for SAML tokens. In that case, the `groups` attribute will be omitted.

        To avoid this, enable the **Groups assigned to the application** option in Azure Entra (**Enterprise applications > Single sign-on > Attributes & Claims > Edit**). This setting limits the `groups` attribute in the SAML assertion to only those groups assigned to the application.

        **Alternative:** If you can’t restrict groups to app-assigned ones, use the [Microsoft Graph Authz plugin for Elasticsearch](elasticsearch://reference/elasticsearch-plugins/ms-graph-authz.md). It looks up group memberships through Microsoft Graph during authorization, so it continues to work even when the `groups` attribute is omitted due to overage.

        Refer to [Group overages](https://learn.microsoft.com/en-us/security/zero-trust/develop/configure-tokens-group-claims-app-roles#group-overages) in the Microsoft Security documentation for more information.
        :::

        If you're using {{ece}} or {{ech}}, and you're using machine learning or a deployment with hot-warm architecture, you must include this configuration in the user settings section for each node type.

    2. Next, configure {{kib}} to enable SAML authentication:
        1. [Update your {{kib}} user settings](/deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

            ```yaml
            xpack.security.authc.providers:
              saml.kibana-realm:
                order: 0
                realm: kibana-realm
                description: "Log in with Microsoft Entra ID"
            ```

            The configuration values used in the example above are:

            `xpack.security.authc.providers`
            :   Add `saml` provider to instruct {{kib}} to use SAML SSO as the authentication method.

            `xpack.security.authc.providers.saml.<provider-name>.realm`
            :   Set this to the name of the SAML realm that you have used in your [{{es}} realm configuration](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-create-realm). For this example, use the realm name that you configured in the previous step: `kibana-realm`.

        2. Create a role mapping.

            The following role mapping for SAML SSO restricts access to a specific user `(email)` based on the `attributes.principal` email address. This prevents other users on the same domain from having access to your deployment. You can remove the rule or adjust it at your convenience.

            ```json
            POST /_security/role_mapping/SAML_kibana
            {
                "enabled": true,
                "roles": [ "superuser" ],
                "rules" : {
                  "all" : [
                    {
                      "field" : {
                        "realm.name" : "kibana-realm"
                      }
                    },
                    {
                      "field" : {
                        "username" : [
                          "<firstname.lastname>"
                        ]
                      }
                    }
                  ]
                },
                "metadata": { "version": 1 }
            }
            ```

            For more information, refer to [Configure role mapping](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-role-mapping) in the {{es}} SAML documentation.


You should now have successfully configured SSO access to {{kib}} with Microsoft Entra ID as the identity provider.
