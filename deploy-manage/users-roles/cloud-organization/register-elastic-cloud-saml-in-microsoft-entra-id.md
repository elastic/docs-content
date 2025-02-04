---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-saml-sso-entra.html
---

# Register Elastic Cloud SAML in Microsoft Entra ID [ec-saml-sso-entra]

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
    3. Optional: If you plan to use [role mappings](configure-saml-authentication.md#role-mappings) to automate role assignments, add a group claim and customize which groups are sent. Make sure that you customize the name of the group claim under the **Advanced options** section to set the groups claim attribute name `groups`.

6. Collect information about the application from the Entra ID screen.

    1. Get the **Login URL** for the SSO URL, which is the URL where users will be redirected at login.
    2. Get the **Microsoft Entra Identifier** for use as the issuer.
    3. From the **SAML Certificates** section, download the Base64 signing certificate.



## Register with {{ecloud}} [ec_register_with_ecloud_2]

[Register the IdP with {{ecloud}}](configure-saml-authentication.md#ec-saml-sso-register-idp).

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **User authentication** section, click **Configure SSO**.
3. Fill the following fields:

    1. **Identity Provider Entity ID**: Enter the **Microsoft Entra Identifier** that you collected in the previous step.
    2. **Identity Provider SSO URL**: Enter the **Login URL** that you collected in the previous step. Users will be redirected to this URL when they attempt to log in.
    3. **Public x509 certificate**: Paste the contents of the downloaded signing certificate.
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
