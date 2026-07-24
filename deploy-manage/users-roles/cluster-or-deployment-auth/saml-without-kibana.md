---
navigation_title: SAML without Kibana
description: Implement SAML authentication for a custom web application using the Elasticsearch SAML REST APIs, without Kibana.
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# SAML without {{kib}} [saml-no-kibana]

The SAML realm in {{es}} is designed to allow users to authenticate to {{kib}} and as such, most of the [SAML SSO guide](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md) makes the assumption that {{kib}} is used. This page describes how a custom web application could use the relevant SAML REST APIs in order to authenticate users to {{es}} with SAML.

::::{note}
This page assumes that you are familiar with the SAML 2.0 standard and more specifically with the SAML 2.0 Web Browser Single Sign On profile.
::::

Single sign-on realms such as OpenID Connect and SAML make use of the Token Service in {{es}} and in principle exchange a SAML or OpenID Connect Authentication response for an {{es}} access token and a refresh token. The access token is used as credentials for subsequent calls to {{es}}. The refresh token enables the user to get new {{es}} access tokens after the current one expires.

## SAML realm [saml-no-kibana-realm]

You must create a SAML realm and configure it accordingly in {{es}}. See [Create a SAML realm](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-create-realm).

## Service account user for accessing the APIs [saml-no-kibana-user]

The realm is designed with the assumption that there needs to be a privileged entity acting as an authentication proxy. In this case, the custom web application is the authentication proxy handling the authentication of end users (more correctly, "delegating" the authentication to the SAML Identity Provider). The SAML related APIs require authentication and the necessary authorization level for the authenticated user. For this reason, you must create a Service Account user and assign it a role that gives it the `manage_saml` cluster privilege. The use of the `manage_token` cluster privilege will be necessary after the authentication takes place, so that the service account user can maintain access in order to refresh access tokens on behalf of the authenticated users or to subsequently log them out.

```console
POST /_security/role/saml-service-role
{
  "cluster" : ["manage_saml", "manage_token"]
}
```

```console
POST /_security/user/saml-service-user
{
  "password" : "<somePasswordHere>",
  "roles"    : ["saml-service-role"]
}
```

## Handling the SP-initiated authentication flow [saml-no-kibana-sp-init-sso]

On a high level, the custom web application would need to perform the following steps in order to authenticate a user with SAML against {{es}}:

1. Make an HTTP POST request to `_security/saml/prepare`, authenticating as the `saml-service-user` user. Use either the name of the SAML realm in the {{es}} configuration or the value for the Assertion Consumer Service URL in the request body. See the [SAML prepare authentication API]({{es-apis}}operation/operation-security-saml-prepare-authentication) for more details.

    ```console
    POST /_security/saml/prepare
    {
      "realm" : "saml1"
    }
    ```

2. Handle the response from `/_security/saml/prepare`. The response from {{es}} will contain 3 parameters: `redirect`, `realm` and `id`. The custom web application would need to store the value for `id` in the user's session (client side in a cookie or server side if session information is persisted this way). It must also redirect the user's browser to the URL that was returned in the `redirect` parameter. The `id` value should not be disregarded as it is used as a nonce in SAML in order to mitigate against replay attacks.

3. Handle a subsequent response from the SAML IdP. After the user is successfully authenticated with the Identity Provider they will be redirected back to the Assertion Consumer Service URL. This `sp.acs` needs to be defined as a URL which the custom web application handles. When it receives this HTTP POST request, the custom web application must parse it and make an HTTP POST request itself to the `_security/saml/authenticate` API. It must authenticate as the `saml-service-user` user and pass the Base64 encoded SAML Response that was sent as the body of the request. It must also pass the value for `id` that it had saved in the user's session previously.

    See [SAML authenticate API]({{es-apis}}operation/operation-security-saml-authenticate) for more details.

    ```console
    POST /_security/saml/authenticate
    {
      "content" : "PHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMD.....",
      "ids" : ["4fee3b046395c4e751011e97f8900b5273d56685"]
    }
    ```

    {{es}} will validate this and if all is correct will respond with an access token that can be used as a `Bearer` token for subsequent requests. It also supplies a refresh token that can be later used to refresh the given access token as described in the [get token API]({{es-apis}}operation/operation-security-get-token).

4. The response to calling `/_security/saml/authenticate` will contain only the username of the authenticated user. If you need to get the values for the SAML Attributes that were contained in the SAML Response for that user, you can call the Authenticate API `/_security/_authenticate/` using the access token as a `Bearer` token and the SAML attribute values will be contained in the response as part of the [user metadata](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-attribute-mapping.md#saml-user-metadata).

## Handling the IdP-initiated authentication flow [saml-no-kibana-idp-init-sso]

{{es}} can also handle the IdP-initiated Single Sign On flow of the SAML 2 Web Browser SSO profile. In this case the authentication starts with an unsolicited authentication response from the SAML Identity Provider. The difference with the [SP-initiated SSO](#saml-no-kibana-sp-init-sso) is that the web application needs to handle requests to the `sp.acs` that will not come as responses to previous redirections. As such, it will not have a session for the user already, and it will not have any stored values for the `id` parameter. The request to the `_security/saml/authenticate` API will look like the one below in this case:

```console
POST /_security/saml/authenticate
{
  "content" : "PHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMD.....",
  "ids" : []
}
```

## Handling the logout flow [saml-no-kibana-slo]

1. At some point, if necessary, the custom web application can log the user out by using the [SAML logout API]({{es-apis}}operation/operation-security-saml-logout) and passing the access token and refresh token as parameters. For example:

    ```console
    POST /_security/saml/logout
    {
      "token" : "46ToAxZVaXVVZTVKOVF5YU04ZFJVUDVSZlV3",
      "refresh_token": "mJdXLtmvTUSpoLwMvdBt_w"
    }
    ```

    If the SAML realm is configured accordingly and the IdP supports it (see [SAML Single Logout](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-logout)), this request will trigger a SAML SP-initiated Single Logout. In this case, the response will include a `redirect` parameter indicating where the user needs to be redirected at the IdP in order to complete the logout.

2. Alternatively, the IdP might initiate the Single Logout flow at some point. In order to handle this, the Logout URL (`sp.logout`) needs to be handled by the custom web app. The query part of the URL that the user will be redirected to will contain a SAML Logout request and this query part needs to be relayed to {{es}} using the [SAML invalidate API]({{es-apis}}operation/operation-security-saml-invalidate):

    ```console
    POST /_security/saml/invalidate
    {
      "query" : "SAMLRequest=nZFda4MwFIb%2FiuS%2BmviRpqFaClKQdbvo2g12M2KMraCJ9cRR9utnW4Wyi13sMie873MeznJ1aWrnS3VQGR0j4mLkKC1NUeljjA77zYyhVbIE0dR%2By7fmaHq7U%2BdegXWGpAZ%2B%2F4pR32luBFTAtWgUcCv56%2Fp5y30X87Yz1khTIycdgpUW9kY7WdsC9zxoXTvMvWuVV98YyMnSGH2SYE5pwALBIr9QKiwDGpW0oGVUznGeMyJZKFkQ4jBf5HnhUymjIhzCAL3KNFihbYx8TBYzzGaY7EnIyZwHzCWMfiDnbRIftkSjJr%2BFu0e9v%2B0EgOquRiiZjKpiVFp6j50T4WXoyNJ%2FEWC9fdqc1t%2F1%2B2F3aUpjzhPiXpqMz1%2FHSn4A&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=MsAYz2NFdovMG2mXf6TSpu5vlQQyEJAg%2B4KCwBqJTmrb3yGXKUtIgvjqf88eCAK32v3eN8vupjPC8LglYmke1ZnjK0%2FKxzkvSjTVA7mMQe2AQdKbkyC038zzRq%2FYHcjFDE%2Bz0qISwSHZY2NyLePmwU7SexEXnIz37jKC6NMEhus%3D",
      "realm" : "saml1"
    }
    ```

    The custom web application will then need to also handle the response, which will include a `redirect` parameter with a URL in the IdP that contains the SAML Logout response. The application should redirect the user there to complete the logout.

For SP-initiated Single Logout, the IdP may send back a logout response which can be verified by {{es}} using the [SAML complete logout API]({{es-apis}}operation/operation-security-saml-complete-logout).
