---
navigation_title: "Configure {{ecloud}} SAML SSO"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-saml-sso.html
---



# Configure SAML authentication [ec-saml-sso]


You can centrally control access to your {{ecloud}} organization by setting up SAML single sign-on (SSO) with a SAML 2.0 identity provider (IdP).

When users log in to {{ecloud}} for the first time using SSO, they’re automatically added to your organization and their accounts are automatically provisioned.

You can also enhance security by enforcing SSO authentication for members of your organization, and centrally manage role assignments by mapping IdP groups to {{ecloud}} roles.


## Should I use organization-level or deployment-level SSO? [ec_should_i_use_organization_level_or_deployment_level_sso_2]

You can also integrate third-party authentication directly [at the deployment level](../cluster-or-deployment-auth.md). The option that you choose depends on your requirements:

| Consideration | Organization-level | Deployment-level |
| --- | --- | --- |
| **Management experience** | Manage authentication and role mapping centrally for all deployments in the organization | Configure SSO for each deployment individually |
| **Authentication protocols** | SAML only | Multiple protocols, including LDAP, OIDC, and SAML |
| **Role mapping** | [Organization-level roles and instance access roles](user-roles.md), Serverless project [custom roles](https://docs.elastic.co/serverless/custom-roles.html) | [Built-in](../cluster-or-deployment-auth/built-in-roles.md) and [custom](../cluster-or-deployment-auth/defining-roles.md) stack-level roles |
| **User experience** | Users interact with Cloud | Users interact with the deployment directly |

If you want to avoid exposing users to the {{ecloud}} UI, or have users who only interact with some deployments, then you might prefer users to interact with your deployment directly.

In some circumstances, you might want to use both organization-level and deployment-level SSO. For example, if you have a data analyst who interacts only with data in specific deployments, then you might want to configure deployment-level SSO for them. If you manage multiple tenants in a single organization, then you might want to configure organization-level SSO to administer deployments, and deployment-level SSO for the users who are using each deployment.


## Prerequisites [ec_prerequisites_4]

* This functionality requires an [Enterprise subscription](https://www.elastic.co/subscriptions/cloud).
* You must have a SAML 2.0 compatible identity provider.


## Risks and considerations [ec_risks_and_considerations]

Before you configure SAML SSO, familiarize yourself with the following risks and considerations:

* Actions taken on the IdP are not automatically reflected in {{ecloud}}. For example, if you remove a user from your IdP, they are not removed from the {{ecloud}} organization and their active sessions are not invalidated.

    To immediately revoke a user’s active sessions, an organization owner must [remove the user from the {{ecloud}} organization](https://cloud.elastic.co/account/members) or remove their assigned roles.

* If you enforce SSO authentication, you can be locked out of {{ecloud}} if your IdP is unavailable or misconfigured. You might need to work with Elastic Support to regain access to your account. To avoid being locked out, you should maintain and store an [{{ecloud}} API key](../../api-keys/elastic-cloud-api-keys.md#ec-api-keys) with organization owner level privileges so that an administrator can disable enforcement in an emergency.
* If you do not enforce SSO authentication, users can still log in without authenticating with your IdP. You need to manage these users in Elastic Cloud.
* Cloud passwords are invalidated each time a user logs in using SSO. If a user needs sign in with their email and password again, they need to [change their password](../../../cloud-account/change-your-password.md).
* Role mappings only take effect when your organization’s members authenticate using SSO. If SSO authentication is not enforced, users might have roles that are inconsistent with the role mapping when they log in using other methods.
* Roles manually assigned using the {{ecloud}} UI are overwritten by the role mapping when the user logs in using SSO.


## Claim a domain [ec-saml-sso-claim-domain]

Before you can register and use your IdP with {{ecloud}}, you must claim one or more domains. Only users that have email addresses that match claimed domains can authenticate with your IdP.

If the members of your {{ecloud}} organization have email addresses from multiple domains, you can claim multiple domains.

You must have authority to modify your domain’s DNS records and be a member of the **Organization owner** role in {{ecloud}} to complete this step.

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **Domains** section, click **Add domain**.
3. In the **Domain name** field, enter the domain that you want to claim and then click **Generate verification code**.
4. In the DNS provider settings for your domain, add a new TXT record with the name `_elastic_domain_challenge` and the verification code as the value.
5. Verify that your DNS provider settings are correct by running a `dig` command in a Linux terminal. For example, for the domain `example.com`:

    ```sh
    dig _elastic_domain_challenge.example.com TXT
    ...
    ;; ANSWER SECTION:
    _elastic_domain_challenge.example.com. 60 IN	TXT "1234rvic48untuh8uckoroaelpz7iid4uk5b8g0m2e4q57b07kak66r7xetoge8zn"
    ...
    ```

6. In the {{ecloud}} UI, click **Verify and add domain**.

::::{note}
It might take some time for the DNS records to be updated and propagated in the network. If verification isn’t successful, wait a while and try again.
::::



## Register a SAML IdP [ec-saml-sso-register-idp]

After you have claimed one or more domains, you can register your IdP with {{ecloud}}. The steps vary by IdP; for more specific details, refer to [Register {{ecloud}} SAML in Microsoft Entra ID](register-elastic-cloud-saml-in-microsoft-entra-id.md) and [Register {{ecloud}} SAML in Okta](register-elastic-cloud-saml-in-okta.md).


### Create a new SAML 2 application [ec_create_a_new_saml_2_application]

Create a new SAML 2 application in your IdP.

1. Use placeholder values for the assertion consumer service (ACS) and SP entity ID/audience. Those values will be provided by {{ecloud}} in a later step.
2. Configure your application to send an `email` attribute statement with the email address of your organization members. The email should match the domain that you claimed.
3. Optionally configure the application to send `firstName` and `lastName` attribute statements, which will be used to set the respective fields of the user’s {{ecloud}} account.
4. If you’re planning to use role mappings, configure the application to send a `groups` attribute statement with the groups that you want to map to roles in {{ecloud}}.
5. Note the SAML issuer and the SSO URL, which is the URL of the IdP where users will be redirected at login.
6. Download the public certificate of the SAML 2 application.


### Register the IdP with {{ecloud}} [ec_register_the_idp_with_ecloud]

Add the information that you collected to {{ecloud}}.

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **User authentication** section, click **Configure SSO**.
3. Fill the following fields:

    1. **Identity Provider Entity ID**: The SAML issuer that you collected in the previous step. This is unique identifier of your identity provider that allows Elastic Cloud to verify the source of SAML assertions.
    2. **Identity Provider SSO URL**: The SSO URL that you collected in the previous step. This should be the HTTP-POST SAML binding of your identity provider. Users will be redirected to this URL when they attempt to log in.
    3. **Public x509 certificate**: The public certificate of the SAML 2 application that you downloaded in the previous step. This is the certificate that SAML responses will be signed with by your IdP. The certificate must be in PEM format.
    4. **Login identifier prefix**: A customizable piece of the {{ecloud}} SSO URL that your organization members can use to authenticate. This could be the name of your business. You can use lowercase alphanumeric characters and hyphens in this value, and you can change it later.

4. Click **Update configuration**.

::::{tip}
The **Only allow login through my identity provider** option is disabled by default. You must verify your SSO configuration by logging in using SSO to enable this option.
::::


If your configuration is valid, the following details of the service provider (SP) will be displayed:

* **SSO Login URL**: The URL that your organization members can use to log in to your organization using your IdP.

    If your IdP supports an application bookmark or tile, this is the URL that should be used. {{ecloud}} does not support IdP-initiated SSO.

* **Service provider Entity ID**: The unique identifier that allows your IDP to recognize and validate requests from {{ecloud}}.
* **Service provider ACS URL**: The {{ecloud}} URL that receives SAML assertions from your IdP.
* **Metadata URL**: The link to an XML metadata file that contains the Elastic service provider metadata. If your IdP accepts metadata files, then you can use this file to configure your IdP.


### Update the SAML 2 application in your IdP [ec_update_the_saml_2_application_in_your_idp]

Using the details returned in the previous step, update the assertion consumer service (ACS), SP entity ID/audience, and SSO login URL values in your SAML 2 application.

::::{tip}
Additional details that you might want to use in your IdP configuration, such as the request signing certificate, are available in the downloadable metadata file.
::::



## Test SSO [ec_test_sso]

After you register the IdP in {{ecloud}} and configure your IdP, you can test authentication. To begin SSO, open the identity provider SSO URL in an incognito browsing session. If everything is configured correctly, you should be redirected to your IdP for authentication and then redirected back to {{ecloud}} signed in.

Users who are not a member of the {{ecloud}} organization can authenticate with your IdP to automatically create an {{ecloud}} account provided that their email matches the claimed domain.


## Enforce SSO [enforce-sso]

After SSO is configured successfully, you might want to enforce SSO authentication for members of your organization. This enforcement requires members to authenticate with SSO through the organization’s SAML IdP and prevents them from logging in by any other methods. It ensures that users who have been off-boarded in your IdP can no longer authenticate to {{ecloud}}, and also ensures users have the appropriate role mappings applied at each login.

::::{warning}
If you turn on enforcement, you will be unable to access {{ecloud}} if your IdP is unavailable or misconfigured or there is an {{ecloud}} incident. It is recommended that you maintain and store an {{ecloud}} API key with organization owner level privileges so that an administrator can disable enforcement in an emergency. Refer to [Create an API key](../../api-keys/elastic-cloud-api-keys.md#ec-api-keys). You can also open a support issue if you lose access to your {{ecloud}} account.

::::



### Enable enforcement [ec_enable_enforcement]

To protect your account from being accidentally locked out when this option is enabled, we validate that you are authenticated SSO with the latest applied configuration before enabling enforcement.

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **User authentication** section, click **Edit**.
3. Toggle the **Only allow login through my identity provider** option on to enable enforcement.


### Disable enforcement [ec_disable_enforcement]

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **User authentication** section, click **Edit**.
3. Toggle the **Only allow login through my identity provider** option off to disable enforcement.

If you are unable to access the UI for any reason, use the following API call to disable enforcement. The API key that you use must have organization owner level privileges to disable enforcement.

```sh
curl -XPUT \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/organizations/$ORGANIZATION_ID" \
-d '
{
  "enforce_authentication_method": null
}
'
```


## Role mappings [role-mappings]

To automate [role](user-roles.md) assignments to your {{ecloud}} organization’s members, you can use role mappings. Role mappings map groups returned by your IdP in the `groups` SAML attribute to one or more {{ecloud}} roles. The mapping will be evaluated and the applicable roles will be assigned each time your organization’s members log into {{ecloud}} using SSO.

::::{note}
If [SSO enforcement](#enforce-sso) is not enabled, user roles might not be consistent with your role mapping and additional manual role assignment might be needed. Roles manually assigned using the {{ecloud}} UI are overwritten by the role mapping when the user logs in using SSO.
::::


::::{note}
If the `groups` attribute is not included in the SAML response, the user will keep whatever groups they were last assigned by the IdP. If you want to remove all groups for a user as part of an offboarding process, instead unassign the user from the {{ecloud}} application.
::::


To configure role mappings:

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **Role mappings** section, click **Create role mapping**.
3. Add a name for the role mapping. The name helps to identify the role mapping to other members, and must be unique.
4. Click to configure the roles that you want to assign to users who meet the mapping rules, click **Add roles** and then select the roles. For more information, refer to [*User roles and privileges*](user-roles.md).
5. In the **Mapping rules** section, add rules for the role mapping:

    1. Select **All are true** or **Any are true** to define how the rules are evaluated.
    2. Add group name or names that the member must have in their SAML assertion to be assigned the role.

        Use the wildcard character `*` to specify group name patterns. Wildcards will match 0 or more characters.



## Disable SSO [ec_disable_sso]

If SSO enforcement is enabled, then you must disable SSO enforcement before you disable SSO.

1. Open your organization’s [**Security**](https://cloud.elastic.co/account/idp) tab.
2. In the **User authentication** section, click **Edit**.
3. Click **Disable SAML SSO**.


## Troubleshoot SSO [ec_troubleshoot_sso]


### SSO screen is not redirecting to my IdP [ec_sso_screen_is_not_redirecting_to_my_idp]

Double check the `saml_idp.sso_url` provided during IdP registration. This should be the HTTP-POST binding URL to your IdP’s SAML application. {{ecloud}} will redirect to this URL during sign in.


### Failure to redirect back to {{ecloud}} after IdP log in, or redirected to `/access-denied` [ec_failure_to_redirect_back_to_ecloud_after_idp_log_in_or_redirected_to_access_denied]

There could be a variety of issues that might result in sign in failure. Try tracing the SAML request and response with a SAML tracer. You should see a `SAMLRequest` field when redirecting to your IdP, and a `SAMLResponse` field when redirecting to the Cloud ACS.

If there was an error in your IdP, there may be a non-success `Status` field which should describe the error that occurred.

If the SAML response was successful, double-check the components of the SAML response:

* The `Destination` and `Recipient` should match the `acs` provided by the {{ecloud}} IdP registration API.
* An `AttributeStatement` named `email` should be sent with the email matching a domain claimed by your {{ecloud}} organization. If the domain of the email doesn’t match a claimed domain, the authentication flow will not complete.
* The `AudienceRestriction` `Audience` should match the `sp_entity_id` provided by the {{ecloud}} IdP registration API.
* The `Issuer` should match the value provided to the {{ecloud}} IdP registration API.
* The signature of the SAML response should be verifiable by the certificate provided during IdP configuration in Cloud.
