---
navigation_title: Okta
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-saml-sso-okta.html
applies_to:
  deployment:
    ess: all
  serverless: all
products:
  - id: cloud-hosted
---

# Register {{ecloud}} SAML in Okta [ec-saml-sso-okta]

To [configure {{ecloud}} SAML SSO](configure-saml-authentication.md) with Okta as the identity provider (IdP), perform the following steps.


## Create a new SAML 2.0 application [ec_create_a_new_saml_2_0_application]

Follow these steps to create a new SAML application for {{ecloud}} in Okta.

1. In Okta, create a new app integration. select SAML 2.0 as the sign-in method.
2. Add a name for the application.
3. In the app visibility section, select the **Do not display appliation icon** options. {{ecloud}} does not support IdP-initiated login.

    If you want to create an Okta tile for {{ecloud}}, then set one up using [the Bookmark App integration](https://help.okta.com/en-us/content/topics/apps/apps_bookmark_app.htm) after you have configured SAML SSO.

4. In the SAML settings, fill in the details for your new application. Enter placeholder SAML settings such as `http://example.com/sso` and `http://example.com/sp` for the single sign-on URL and audience URI.
5. Add attribute statements for your organization members' email addresses. These addresses should match the domains that you claimed using [Claim a domain](configure-saml-authentication.md#ec-saml-sso-claim-domain). Optionally add first and last names, which will be used to set the respective fields of the user’s {{ecloud}} account.
6. Optional: If you plan to use [role mappings](configure-saml-authentication.md#role-mappings) to automate role assignments, add a group attribute statement named `groups` and filter the groups as desired.
7. Save the application.
8. Collect information about the application from the Okta **Sign on** tab.

    1. Get the SAML issuer and the SSO URL, which is the URL of the IdP where users will be redirected at login.
    2. Download the signing certificate of the SAML 2 application.



## Register with {{ecloud}} [ec_register_with_ecloud]

[Register the IdP with {{ecloud}}](configure-saml-authentication.md#ec-saml-sso-register-idp).

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **User authentication** section, click **Configure SSO**.
3. Fill the following fields:

    1. **Identity Provider Entity ID**: Enter the SAML issuer that you collected in the previous step.
    2. **Identity Provider SSO URL**: Enter the SSO URL that you collected in the previous step. Users will be redirected to this URL when they attempt to log in.
    3. **Public x509 certificate**: Paste the contents of the downloaded signing certificate.
    4. **Login identifier prefix**: A customizable piece of the {{ecloud}} SSO URL that your organization members can use to authenticate. This could be the name of your business. You can use lowercase alphanumeric characters and hyphens in this value, and you can change it later.

4. Click **Update configuration**.

If successful, the API will return additional details that will need to be provided to the IdP.


## Update the application in Okta [ec_update_the_application_in_okta]

Update your SAML 2 application in Okta to use the values returned in the **User authentication** page.

1. Set the single sign-on URL to the **SSO Login URL**.
2. Set the audience URI (SP entity ID) to the **Service provider Entity ID**.
3. Optional: Fill in other details using information from the metadata file available at the **metadata URL**.

When these steps are complete, you should be able to test SSO as described in [Configure {{ecloud}} SAML SSO](configure-saml-authentication.md).

Optionally, if you want to create an Okta tile for {{ecloud}}, then you can set one up using [the Bookmark App integration](https://help.okta.com/en-us/content/topics/apps/apps_bookmark_app.htm) at this stage.
