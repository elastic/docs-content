---
navigation_title: With Microsoft Entra ID
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-securing-clusters-saml-azure.html
applies_to:
  stack: all
products:
  - id: elasticsearch
  - id: kibana
---
# Set up SAML with Microsoft Entra ID [ec-securing-clusters-saml-azure]

This guide provides a walk-through of how to configure Microsoft Entra ID, formerly known as Azure Active Directory, as an identity provider for SAML single sign-on (SSO) authentication, used for accessing {{kib}}.

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

    6. Navigate to **SAML-based Single sign-on**, open the **User Attributes & Claims** configuration, and update the fields to suit your needs. These settings control what information from Microsoft Entra ID will be made available to the {{stack}} during SSO. This information can be used to identify a user in the {{stack}} and/or to assign different roles to users in the {{stack}}. We suggest that you configure a proper value for the `Unique User Identifier (Name ID)` claim that identifies the user uniquely and is not prone to changes.

        :::{image} /deploy-manage/images/cloud-ec-saml-azuread-user-attributes.png
        :alt: The Entra ID User Attributes & Claims page
        :::

    7. Optional: If you use group-based role mappings and your Microsoft Entra ID license supports assigning groups to applications, restrict the group claim to groups assigned to the application. This helps keep the groups sent for each user within the 150-group SAML limit.

        1. In **User Attributes & Claims**, click **Add a group claim**, or edit the existing group claim.
        2. Select **Groups assigned to the application**. Keep the default group claim name, `http://schemas.microsoft.com/ws/2008/06/identity/claims/groups`, to match `attributes.groups` in the {{es}} configuration, then save the claim.
        3. In **Users and groups**, assign the groups you plan to use in your Elastic role mappings. Users must be direct members of these groups: this option doesn't include nested group memberships.

        If a user's group list exceeds this limit, Entra ID omits the group claim and group-based role mappings don't match. For details about this problem, refer to [Resolve missing group claims](#entra-saml-missing-group-claims).

    8. From the SAML configuration page, make a note of the `App Federation Metadata URL`.

2. Configure {{es}} and {{kib}} for SAML:

    1. [Update your {{es}} settings](/deploy-manage/stack-settings.md) with the following configuration:

        ```yaml
        xpack.security.authc.realms.saml.kibana-realm:
          order: 2
          attributes.principal: nameid
          attributes.groups: "http://schemas.microsoft.com/ws/2008/06/identity/claims/groups" <1>
          idp.metadata.path: "https://login.microsoftonline.com/<Tenant ID>/federationmetadata/2007-06/federationmetadata.xml?appid=<Application_ID>"
          idp.entity_id: "https://sts.windows.net/<Tenant_ID>/"
          sp.entity_id: "<Kibana_Endpoint_URL>"
          sp.acs: "<Kibana_Endpoint_URL>/api/security/saml/callback"
          sp.logout: "<Kibana_Endpoint_URL>/logout"
        ```

        1. Entra ID omits this attribute when a user's groups exceed the 150-group SAML limit. For workarounds, refer to [Resolve missing group claims](#entra-saml-missing-group-claims).

        Where:

        * `<Application_ID>` is your Application ID, available in the application details in Azure.
        * `<Tenant_ID>` is your Tenant ID, available in the tenant overview page in Azure.
        * `<Kibana_Endpoint_URL>` is the base URL for your {{kib}} instance. Ensure this is the same value that you set for `Identifier (Entity ID)` in the earlier Microsoft Entra ID configuration step.

        * For `idp.metadata.path`, we’ve shown the format to construct the URL. This value should be identical to the `App Federation Metadata URL` setting that you made a note of in the previous step.

    2. Next, configure {{kib}} to enable SAML authentication:
        1. [Update your {{kib}} settings](/deploy-manage/stack-settings.md) with the following configuration:

            ```yaml
            xpack.security.authc.providers:
              saml.kibana-realm:
                order: 0
                realm: kibana-realm
                description: "Log in with Microsoft Entra ID"
            ```

            The configuration values used in the previous example are:

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

## Resolve missing group claims [entra-saml-missing-group-claims]

Use this procedure if users can't access {{kib}} or don't receive the expected roles because Entra ID omits their group memberships from the SAML assertion.

:::{include} /deploy-manage/_snippets/entra-id-saml-group-overage.md
:::

For the configuration in this guide, the group claim name must match [`attributes.groups`](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-attribute-mapping.md#saml-es-user-properties): `http://schemas.microsoft.com/ws/2008/06/identity/claims/groups`.

### Alternative: Retrieve groups with Microsoft Graph
```{applies_to}
stack: ga 9.1+
```

If you can't restrict the groups in the SAML assertion, configure the [Microsoft Graph Authz plugin](elasticsearch://reference/elasticsearch-plugins/ms-graph-authz.md) to retrieve group memberships from Microsoft Entra ID. Install the plugin and [configure your SAML realm to delegate authorization](elasticsearch://reference/elasticsearch-plugins/ms-graph-authz-configure-elasticsearch.md) to the Microsoft Graph realm.

For example, after configuring a Microsoft Graph realm named `microsoft_graph1`, add this setting to the `kibana-realm` SAML configuration from this guide:

```yaml
xpack.security.authc.realms.saml.kibana-realm.authorization_realms: microsoft_graph1
```

The plugin applies to SAML configured in {{es}}, including deployment-level SAML on {{ech}}. It doesn't apply to [{{ecloud}} organization SSO](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md).
