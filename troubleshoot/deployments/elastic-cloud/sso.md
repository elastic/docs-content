---
navigation_title: SAML single sign-on (SSO)
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-saml-sso.html
applies_to:
  deployment:
    ess: all
  serverless: all
products:
  - id: cloud-hosted
---

# Troubleshoot {{ecloud}} SSO [ec_troubleshoot_sso]


## SSO screen is not redirecting to my IdP [ec_sso_screen_is_not_redirecting_to_my_idp]

Double check the `saml_idp.sso_url` provided during IdP registration. This should be the HTTP-POST binding URL to your IdP’s SAML application. {{ecloud}} will redirect to this URL during sign in.


## Failure to redirect back to {{ecloud}} after IdP log in, or redirected to `/access-denied` [ec_failure_to_redirect_back_to_ecloud_after_idp_log_in_or_redirected_to_access_denied]

There could be a variety of issues that might result in sign in failure. Try tracing the SAML request and response with a SAML tracer. You should see a `SAMLRequest` field when redirecting to your IdP, and a `SAMLResponse` field when redirecting to the Cloud ACS.

If there was an error in your IdP, there may be a non-success `Status` field which should describe the error that occurred.

If the SAML response was successful, double-check the components of the SAML response:

* The `Destination` and `Recipient` should match the `acs` provided by the {{ecloud}} IdP registration API.
* An `AttributeStatement` named `email` should be sent with the email matching a domain claimed by your {{ecloud}} organization. If the domain of the email doesn’t match a claimed domain, the authentication flow will not complete.
* The `AudienceRestriction` `Audience` should match the `sp_entity_id` provided by the {{ecloud}} IdP registration API.
* The `Issuer` should match the value provided to the {{ecloud}} IdP registration API.
* The signature of the SAML response should be verifiable by the certificate provided during IdP configuration in Cloud.
