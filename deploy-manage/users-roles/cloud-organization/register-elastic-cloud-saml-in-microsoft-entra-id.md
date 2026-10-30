---
navigation_title: Microsoft Entra ID
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-saml-sso-entra.html
applies_to:
  deployment:
    ech: all
  serverless: all
products:
  - id: cloud-hosted
---

# Register {{ecloud}} SAML in Microsoft Entra ID [ec-saml-sso-entra]

To [configure {{ecloud}} SAML SSO](configure-saml-authentication.md) with Microsoft Entra ID (formerly Azure AD) as the identity provider (IdP), perform the following steps.


## Create a new Entra ID Enterprise application [ec_create_a_new_entra_id_enterprise_application]

In Microsoft Entra ID, create a new Entra ID Enterprise application.

1. From the Microsoft Entra Gallery, create a non-gallery application.
2. Provide a name and basic information about the application.
3. In the **Single sign-on** section, select **SAML** as the single sign-on method.
4. In the basic SAML configuration, enter placeholder values for the entity ID and the reply or assertion consumer service (ACS) URL.
5. In the **Attributes & Claims** section, configure claims:

    1. Configure a claim named `email` to send the email address of your users. This attribute is required in the SAML response.
    2. Optional: Configure a `firstName` and `lastName` claim to set the {{ecloud}} user’s name during SSO.
    3. Optional: If you plan to use [role mappings](configure-saml-authentication.md#role-mappings) to automate role assignments, add a group claim. In **Advanced options**, customize the group claim name to `groups`.

6. Optional: If you use group-based role mappings and your Microsoft Entra ID license supports assigning groups to applications, restrict the group claim to groups assigned to the application. This helps keep the groups sent for each user within the 150-group SAML limit.

    1. In **Attributes & Claims**, edit the group claim and select **Groups assigned to the application**. Keep the custom claim name set to `groups`, then save the claim.
    2. In **Users and groups**, assign the groups you plan to use in your Cloud role mappings. Users must be direct members of these groups: this option doesn't include nested group memberships.

    If a user's group list exceeds this limit, Entra ID omits the group claim and group-based role mappings don't match. For details about this problem, refer to [Resolve missing group claims](#cloud-entra-saml-missing-group-claims).

7. Collect information about the application from the Entra ID screen.

    1. Get the **Login URL** for the SSO URL, which is the URL where users will be redirected at login.
    2. Get the **Microsoft Entra Identifier** for use as the issuer.
    3. From the **SAML Certificates** section, download the Base64 signing certificate.



## Register with {{ecloud}} [ec_register_with_ecloud_2]

[Register the IdP with {{ecloud}}](configure-saml-authentication.md#ec-saml-sso-register-idp).

1. From the navigation menu, select **Organization** → [**SSO**](https://cloud.elastic.co/account/idp).
2. In the **User authentication** section, click **Configure SSO**.
3. Fill the following fields:

    1. **Identity Provider Entity ID**: Enter the **Microsoft Entra Identifier** that you collected in the previous step.
    2. **Identity Provider SSO URL**: Enter the **Login URL** that you collected in the previous step. Users will be redirected to this URL when they attempt to log in.
    3. **Public x509 certificate**: Paste the contents of the downloaded Base64 signing certificate.
    4. **Login identifier prefix**: A customizable piece of the {{ecloud}} SSO URL that your organization members can use to authenticate. This could be the name of your business. You can use lowercase alphanumeric characters and hyphens in this value, and you can change it later.

4. Click **Update configuration**.

If successful, the API will return additional details that will need to be provided to the IdP.


## Update the Entra ID Enterprise application [ec_update_the_entra_id_enterprise_application]

Update the **Basic SAML Configuration** section of the Entra ID Enterprise application to use the values returned in the **User authentication** page.

1. Set the entity ID to the **Service provider Entity ID** value.
2. Set the reply or ACS URL to the **Service provider ACS URL** value.
3. Set the sign on URL to the **SSO Login URL** value.
4. Optional: Fill in other details using information from the metadata file available at the **metadata URL**.

When these steps are complete, you should be able to test SSO as described in [Configure {{ecloud}} SAML SSO](configure-saml-authentication.md).

## Resolve missing group claims [cloud-entra-saml-missing-group-claims]

Use this procedure if users can't access your {{ecloud}} organization, {{ech}} deployments, or {{serverless-short}} projects because their SAML group role mappings don't match.

:::{include} /deploy-manage/_snippets/entra-id-saml-group-overage.md
:::

For {{ecloud}} organization SSO, keep the custom group claim name set to `groups`, as described in [Create a new Entra ID Enterprise application](#ec_create_a_new_entra_id_enterprise_application).

{{ecloud}} organization SSO doesn't resolve memberships from the `groups.link` attribute. The Microsoft Graph Authz plugin for {{es}} applies to cluster or deployment-level SAML and can't resolve group overages for organization SSO, including access to {{ech}} deployments and {{serverless-short}} projects through that SSO configuration.
