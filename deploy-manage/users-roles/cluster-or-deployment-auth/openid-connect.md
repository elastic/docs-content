---
navigation_title: OpenID Connect
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/oidc-realm.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/oidc-guide.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-secure-clusters-oidc.html
  - https://www.elastic.co/guide/en/cloud/current/ec-secure-clusters-oidc.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-secure-clusters-oidc.html
applies_to:
  deployment:
    self:
    ess:
    ece:
    eck:
products:
  - id: elasticsearch
  - id: cloud-enterprise
  - id: cloud-hosted
---

# OpenID Connect authentication [oidc-realm]

The OpenID Connect realm enables {{es}} to serve as an OpenID Connect Relying Party (RP) and provides single sign-on (SSO) support in {{kib}}.

It is specifically designed to support authentication using an interactive web browser, so it does not operate as a standard authentication realm. Instead, there are {{kib}} and {{es}} {{security-features}} that work together to enable interactive OpenID Connect sessions.

This means that the OpenID Connect realm is not suitable for use by standard REST clients. If you configure an OpenID Connect realm for use in {{kib}}, you should also configure another realm, such as the [native realm](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md), in your authentication chain.

Because this feature is designed with {{kib}} in mind, most sections of this guide assume {{kib}} is used. To learn how a custom web application could use the OpenID Connect REST APIs to authenticate the users to {{es}} with OpenID Connect, refer to [OpenID Connect without {{kib}}](#oidc-without-kibana).

For a detailed description of how to implement OpenID Connect with various OpenID Connect Providers (OPs), refer to [Set up OpenID Connect with Azure, Google, or Okta](/deploy-manage/users-roles/cluster-or-deployment-auth/oidc-examples.md).

::::{note}
OpenID Connect realm support in {{kib}} is designed with the expectation that it will be the primary authentication method for the users of that {{kib}} instance. The [Configuring {{kib}}](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-configure-kibana) section describes what this entails and how you can set it up to support other realms if necessary.
::::

## The OpenID Connect Provider [oidc-guide-op]

The OpenID Connect Provider (OP) is the entity in OpenID Connect that is responsible for authenticating the user and for granting the necessary tokens with the authentication and user information to be consumed by the Relying Parties.

In order for the {{stack}} to be able to use your OpenID Connect Provider for authentication, a trust relationship needs to be established between the OP and the RP. In the OpenID Connect Provider, this means registering the RP as a client. OpenID Connect defines a dynamic client registration protocol but this is usually geared towards real-time client registration and not the trust establishment process for cross security domain single sign on. All OPs will also allow for the manual registration of an RP as a client, via a user interface or (less often) via the consumption of a metadata document.

The process for registering the {{stack}} RP will be different from OP to OP, so you should follow your provider's documentation. The information for the RP that you commonly need to provide for registration are the following:

* `Relying Party Name`: An arbitrary identifier for the relying party. There are no constraints on this value, either from the specification or the {{stack}} implementation.
* `Redirect URI`: The URI where the OP will redirect the user’s browser after authentication, sometimes referred to as a `Callback URI`. The appropriate value for this will depend on your setup, and whether or not {{kib}} sits behind a proxy or load balancer.

  It will typically be `${kibana-url}/api/security/oidc/callback` (for the authorization code flow) or `${kibana-url}/api/security/oidc/implicit` (for the implicit flow) where *${kibana-url}* is the base URL for your {{kib}} instance.

  If you're using {{ech}}, then set this value to `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`.

At the end of the registration process, the OP will assign a Client Identifier and a Client Secret for the RP ({{stack}}) to use. Note these two values as they will be used in the {{es}} configuration.


## Prerequisites [oidc-elasticsearch-authentication]

Before you set up an OpenID Connect realm, you must have an OpenID Connect Provider where the {{stack}} Relying Party will be registered.

If you're using a self-managed cluster, then perform the following additional steps:

* Enable TLS for HTTP.

    If your {{es}} cluster is operating in production mode, you must configure the HTTP interface to use SSL/TLS before you can enable OIDC authentication. For more information, see [Encrypt HTTP client communications for {{es}}](../../../deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-http-communication).

    If you started {{es}} [with security enabled](/deploy-manage/deploy/self-managed/installing-elasticsearch.md), then TLS is already enabled for HTTP.

    {{ech}}, {{ece}}, and {{eck}} have TLS enabled by default.

* Enable the token service.

    The {{es}} OIDC implementation makes use of the {{es}} token service. If you configure TLS on the HTTP interface, this service is automatically enabled. It can be explicitly configured by adding the following setting in your [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file:

    ```yaml
    xpack.security.authc.token.enabled: true
    ```

    {{ech}}, {{ece}}, and {{eck}} have TLS enabled by default.

## Create an OpenID Connect realm [oidc-create-realm]

OpenID Connect based authentication is enabled by configuring the appropriate realm within the authentication chain for {{es}}.

This realm has a few mandatory settings, and a number of optional settings. The available settings are described in detail in [OpenID Connect realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-oidc-settings). This guide will explore the most common settings.

1. Create an OpenID Connect (the realm type is `oidc`) realm in your [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file similar to what is shown below.

    If you're using {{ece}} or {{ech}}, and you're using machine learning or a deployment with hot-warm architecture, you must include this configuration in the user settings section for each node type.

    ::::{note}
    The values used below are meant to be an example and are not intended to apply to every use case. The details below the configuration snippet provide insights and suggestions to help you pick the proper values, depending on your OP configuration.
    ::::

    ```yaml
    xpack.security.authc.realms.oidc.oidc1:
      order: 2
      rp.client_id: "the_client_id"
      rp.response_type: code
      rp.redirect_uri: "<kibana-example-url>:5601/api/security/oidc/callback"
      op.issuer: "<op-example-url>"
      op.authorization_endpoint: "<op-example-url>/oauth2/v1/authorize"
      op.token_endpoint: "<op-example-url>/oauth2/v1/token"
      op.jwkset_path: oidc/jwkset.json
      op.userinfo_endpoint: "<op-example-url>/oauth2/v1/userinfo"
      op.endsession_endpoint: "<op-example-url>/oauth2/v1/logout"
      rp.post_logout_redirect_uri: "<kibana-example-url>:5601/security/logged_out"
      claims.principal: sub
      claims.groups: "<example-url>/claims/groups"
    ```

    ::::{dropdown} Common settings

    xpack.security.authc.realms.oidc.<oidc1>
    :   The OpenID Connect realm name. The realm name can only contain alphanumeric characters, underscores, and hyphens.

    order
    :   The order of the OpenID Connect realm in your authentication chain. Allowed values are between `2` and 100. Set to `2` unless you plan on configuring multiple SSO realms for this cluster.

    rp.client_id
    :   The Client Identifier that was assigned to the {{stack}} RP by the OP upon registration. The value is usually an opaque, arbitrary string.

    rp.response_type
    :   An identifier that controls which OpenID Connect authentication flow this RP supports and also which flow this RP requests the OP should follow. Supported values are:

        * `code`: The Authorization Code flow. If your OP supports the Authorization Code flow, you should select this instead of the Implicit Flow.
        * `id_token token`: The Implicit flow, where {{es}} also requests an oAuth2 access token from the OP that can be used for followup requests (`UserInfo`). Select this option if the OP offers a `UserInfo` endpoint in its configuration, or if you know that the claims that you need to use for role mapping aren't available in the ID Token.
        * `id_token`: The Implicit flow, without an oAuth2 token request. Select this option if all necessary claims will be contained in the ID Token, or if the OP doesn’t offer a UserInfo endpoint.


    rp.redirect_uri
    :   The redirect URI where the OP will redirect the browser after authentication. This needs to be *exactly* the same as the one [configured with the OP upon registration](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-guide-op) and will typically be `${kibana-url}/api/security/oidc/callback` where *${kibana-url}* is the base URL for your {{kib}} instance.

    op.issuer
    :   A verifiable Identifier for your OpenID Connect Provider. An Issuer Identifier is usually a case sensitive URL. The value for this setting should be provided by your OpenID Connect Provider.

    op.authorization_endpoint
    :   The URL for the Authorization Endpoint in the OP. This is where the user’s browser will be redirected to start the authentication process. The value for this setting should be provided by your OpenID Connect Provider.

    op.token_endpoint
    :   The URL for the Token Endpoint in the OpenID Connect Provider. This is the endpoint where {{es}} will send a request to exchange the code for an ID Token. This setting is optional when you use the implicit flow. The value for this setting should be provided by your OpenID Connect Provider.

    op.jwkset_path
    :   The path to a file or a URL containing a JSON Web Key Set with the key material that the OpenID Connect Provider uses for signing tokens and claims responses. Your OpenID Connect Provider should provide you with this file or a URL where it is available.

        If your OpenID Connect Provider doesn’t publish its JWKS at an https URL, or if you want to use a local copy, you can upload the JWKS as a file.

        :::{tip}
        * In self-managed clusters, the specified path is resolved relative to the {{es}} config directory. {{es}} will automatically monitor this file for changes and will reload the configuration whenever it is updated.
        * If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.
        * If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).
        :::

    op.userinfo_endpoint
    :   (Optional) The URL for the UserInfo Endpoint in the OpenID Connect Provider. This is the endpoint of the OP that can be queried to get further user information, if required. The value for this setting should be provided by your OpenID Connect Provider.

    op.endsession_endpoint
    :   (Optional) The URL to the End Session Endpoint in the OpenID Connect Provider. This is the endpoint where the user’s browser will be redirected after local logout, if the realm is configured for RP-initiated single logout and the OP supports it. The value for this setting should be provided by your OpenID Connect Provider.

    rp.post_logout_redirect_uri
    :   (Optional) The Redirect URL where the OpenID Connect Provider should redirect the user after a successful single logout (assuming `op.endsession_endpoint` above is also set). This should be set to a value that will not trigger a new OpenID Connect Authentication, such as `${kibana-url}/security/logged_out`  or `${kibana-url}/login?msg=LOGGED_OUT` where *${kibana-url}* is the base URL for your {{kib}} instance.

    claims.principal
    :   See [Claims mapping](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-claims-mappings).

    claims.groups
    :   See [Claims mapping](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-claims-mappings).

   ::::

1. Set the `Client Secret` that was assigned to the RP during registration in the OP.  To set the client secret, add the `xpack.security.authc.realms.oidc.<oidc1>.rp.client_secret` setting [to the {{es}} keystore](/deploy-manage/security/secure-settings.md).

:::{warning}
In {{ech}} and {{ece}}, after you configure Client Secret, any attempt to restart the deployment will fail until you complete the rest of the configuration steps. If you want to roll back the OpenID Connect realm configurations, you need to remove the `xpack.security.authc.realms.oidc.oidc1.rp.client_secret` that was just added.
:::

::::{note}
According to the OpenID Connect specification, the OP should also make their configuration available at a well known URL, which is the concatenation of their `Issuer` value with the `.well-known/openid-configuration` string. For example: `<example-op-url>/.well-known/openid-configuration`.

That document should contain all the necessary information to configure the OpenID Connect realm in {{es}}.
::::

## Map claims [oidc-claims-mappings]

When authenticating to {{kib}} using OpenID Connect, the OP will provide information about the user in the form of **OpenID Connect Claims**. These claims can be included either in the ID Token, or be retrieved from the UserInfo endpoint of the OP.

An **OpenID Connect Claim** is a piece of information asserted by the OP for the authenticated user, and consists of a name/value pair that contains information about the user.

**OpenID Connect Scopes** are identifiers that are used to request access to specific lists of claims. The standard defines a set of scope identifiers that can be requested.

* **Mandatory scopes**: `openid`

* **Commonly used scopes**:
  * `profile`: Requests access to the `name`,`family_name`,`given_name`,`middle_name`,`nickname`, `preferred_username`,`profile`,`picture`,`website`,`gender`,`birthdate`,`zoneinfo`,`locale`, and `updated_at` claims.
  * `email`: Requests access to the `email` and `email_verified` claims.

The RP requests specific scopes during the authentication request. If the OP Privacy Policy allows it and the authenticating user consents to it, the related claims are returned to the RP (either in the ID Token or as a UserInfo response).

The list of the supported claims will vary depending on the OP you are using, but [standard claims](https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims) are usually supported.

### How claims appear in user metadata [oidc-user-metadata]

By default, users who authenticate through OpenID Connect have additional metadata fields. These fields include every OpenID claim that is provided in the authentication response, regardless of whether it is mapped to an {{es}} user property.

For example, in the metadata field `oidc(claim_name)`, "claim_name" is the name of the claim as it was contained in the ID Token or in the User Info response. Note that these will include all the [ID Token claims](https://openid.net/specs/openid-connect-core-1_0.html#IDToken) that pertain to the authentication event, rather than the user themselves.

This behavior can be disabled by adding `populate_user_metadata: false` as a setting in the OIDC realm.


### Map claims to user properties [oidc-claim-to-property]

The goal of claims mapping is to configure {{es}} in such a way as to be able to map the values of specified returned claims to one of the [user properties](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-user-properties) that are supported by {{es}}. These user properties are then utilized to identify the user in the {{kib}} UI or the audit logs, and can also be used to create [role mapping](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-role-mappings) rules.

To configure claims mapping:

1. Using your OP configuration, identify the claims that it might support.

   The list provided in the OP’s metadata or in the configuration page of the OP is a list of potentially supported claims. However, for privacy reasons it might not be a complete one, or not all supported claims will be available for all authenticated users.
2. Review the list of [user properties](#oidc-user-properties) that {{es}} supports, and decide which of them are useful to you, and can be provided by your OP in the form of claims. At a minimum, the `principal` user property is required.
3. Configure your OP to "release" those claims to your {{stack}} Relying Party. This process greatly varies by provider. You can use a static configuration while others will support that the RP requests the scopes that correspond to the claims to be "released" on authentication time. See [`rp.requested_scopes`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-oidc-settings) for details about how to configure the scopes to request. To ensure interoperability and minimize the errors, you should only request scopes that the OP supports, and that you intend to map to {{es}} user properties.

    :::{note}
    You can only map claims with values that are strings, numbers, Boolean values, or an array consisting of strings, numbers, and Boolean values.
    :::

4. Configure the OpenID Connect realm in {{es}} to associate the [{{es}} user properties](#oidc-user-properties) to the name of the claims that your OP will release.

   The [sample configuration](#oidc-create-realm) configures the `principal` and `groups` user properties as follows:

   * `claims.principal: sub`: Instructs {{es}} to look for the OpenID Connect claim named `sub` in the ID Token that the OP issued for the user (or in the UserInfo response) and assign the value of this claim to the `principal` user property.

      `sub` is a commonly used claim for the principal property as it is an identifier of the user in the OP and it is also a required claim of the ID Token. This means that `sub` is available in most OPs. However, the OP may provide another claim that is a better fit for your needs.
   * `claims.groups: "<example-url>/claims/groups"`: Instructs {{es}} to look for the claim with the name `<example-url>/claims/groups`, either in the ID Token or in the UserInfo response, and map the value(s) of it to the user property `groups` in {{es}}.

      There is no standard claim in the specification that is used for expressing roles or group memberships of the authenticated user in the OP, so the name of the claim that should be mapped here will vary between providers. Consult your OP documentation for more details.

      :::{tip}
      In this example, the value is a URI, treated as a string and not a URL pointing to a location that will be retrieved.
      :::



### Mappable {{es}} user properties [oidc-user-properties]

The {{es}} OpenID Connect realm can be configured to map OpenID Connect claims to the following properties on the authenticated user:

principal
:   *(Required)* This is the username that will be applied to a user that authenticates against this realm. The `principal` appears in places such as the {{es}} audit logs.

::::{note}
If the principal property fails to be mapped from a claim, the authentication fails.
::::


groups
:   *(Recommended)* If you want to use your OP’s concept of groups or roles as the basis for a user’s {{es}} privileges, you should map them with this property. The `groups` are passed directly to your [role mapping rules](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-role-mappings).

name
:   *(Optional)* The user’s full name. It will be used in {{kib}}'s profile page to display user details. Use the payload key of your ID token that fits best here.

mail
:   *(Optional)* The user’s email address. It will be used in {{kib}}'s profile page to display user details. Use the payload key of your ID token that fits best here.

dn
:   *(Optional)* The user’s X.500 Distinguished Name.


### Extract partial values from OpenID Connect claims [_extracting_partial_values_from_openid_connect_claims]

There are some occasions where the value of a claim contains more information than you want to use within {{es}}. A common example of this is one where the OP works exclusively with email addresses, but you want the user’s `principal` to use the `local-name` part of the email address. For example if their email address was `james.wong@staff.example.com`, then you might want their principal to be `james.wong`.

This can be achieved using the `claim_patterns` setting in the {{es}} realm, as demonstrated in the realm configuration below:

```yaml
xpack.security.authc.realms.oidc.oidc1:
  order: 2
  rp.client_id: "the_client_id"
  rp.response_type: code
  rp.redirect_uri: "<kibana-example-url>:5601/api/security/oidc/callback"
  op.authorization_endpoint: "<op-example-url>/oauth2/v1/authorize"
  op.token_endpoint: "<op-example-url>/oauth2/v1/token"
  op.userinfo_endpoint: "<op-example-url>/oauth2/v1/userinfo"
  op.endsession_endpoint: "<op-example-url>/oauth2/v1/logout"
  op.issuer: "<op-example-url>"
  op.jwkset_path: oidc/jwkset.json
  claims.principal: email_verified
  claim_patterns.principal: "^([^@]+)@staff\\.example\\.com$"
```

In this case, the user’s `principal` is mapped from the `email_verified` claim, but a regular expression is applied to the value before it is assigned to the user. If the regular expression matches, then the result of the first group is used as the effective value. If the regular expression does not match then the claim mapping fails.

In this example, the email address must belong to the `staff.example.com` domain, and then the local-part (anything before the `@`) is used as the principal. Any users who try to login using a different email domain will fail because the regular expression will not match against their email address, and thus their principal user property - which is mandatory - will not be populated.

::::{important}
Small mistakes in these regular expressions can have significant security consequences. For example, if we accidentally left off the trailing `$` from the example above, then we would match any email address where the domain starts with `staff.example.com`, and this would accept an email address such as `admin@staff.example.com.attacker.net`. It is important that you make sure your regular expressions are as precise as possible so that you don't open an avenue for user impersonation attacks.
::::


## Configure third party initiated single sign-on [third-party-login]

The Open ID Connect realm in {{es}} supports 3rd party initiated login as described in the [specification](https://openid.net/specs/openid-connect-core-1_0.html#ThirdPartyInitiatedLogin).

This allows the OP, or a third party other than the RP, to initiate the authentication process while requesting the OP to be used for the authentication. The {{stack}} RP should already be configured for this OP for this process to succeed.


## Configure RP-initiated logout [oidc-logout]

The OpenID Connect realm in {{es}} supports RP-initiated logout functionality as described in the [specification](https://openid.net/specs/openid-connect-rpinitiated-1_0.html)

In this process, the OpenID Connect RP (the {{stack}} in this case) will redirect the user’s browser to predefined URL of the OP after successfully completing a local logout. The OP can then logout the user also, depending on the configuration, and should finally redirect the user back to the RP.

RP-initiated logout is controlled by two settings:

* `op.endsession_endpoint`: The URL in the OP that the browser will be redirected to.
* `rp.post_logout_redirect_uri` The URL to redirect the user back to after the OP logs them out.

When configuring `rp.post_logout_redirect_uri`, do not point to a URL that will trigger re-authentication of the user. For instance, when using OpenID Connect to support single sign-on to {{kib}}, this could be set to either `${kibana-url}/security/logged_out`, which will show a user-friendly message to the user, or `${kibana-url}/login?msg=LOGGED_OUT` which will take the user to the login selector in {{kib}}.


## Configure SSL [oidc-ssl-config]

OpenID Connect depends on TLS to provide security properties such as encryption in transit and endpoint authentication. The RP is required to establish back-channel communication with the OP in order to exchange the code for an ID Token during the Authorization code grant flow and in order to get additional user information from the `UserInfo` endpoint. If you configure `op.jwks_path` as a URL, {{es}} will need to get the OP’s signing keys from the file hosted there. As such, it is important that {{es}} can validate and trust the server certificate that the OP uses for TLS. Because the system trust store is used for the client context of outgoing https connections, if your OP is using a certificate from a trusted CA, no additional configuration is needed.

However, if the issuer of your OP’s certificate is not trusted by the JVM on which {{es}} is running (e.g it uses an organization CA), then you must configure {{es}} to trust that CA.

If you're using {{ech}} or {{ece}}, then you must [upload your certificate as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.

If you're using {{eck}}, then install the certificate as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

The following example demonstrates how to trust a CA certificate (`/oidc/company-ca.pem`), which is located within the configuration directory.

```yaml
xpack.security.authc.realms.oidc.oidc1:
  order: 1
  ...
  ssl.certificate_authorities: ["/oidc/company-ca.pem"]
```

## Map OIDC users to roles [oidc-role-mappings]

When a user authenticates using OpenID Connect, they are identified to the {{stack}}, but this does not automatically grant them access to perform any actions or access any data.

Your OpenID Connect users can't do anything until they are assigned roles. You can map roles This can be done through either the [add role mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping) or with [authorization realms](/deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md#authorization_realms).

You can map LDAP groups to roles in the following ways:

* Using the role mappings page in {{kib}}.
* Using the [role mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping).
* By delegating authorization to another realm.

For more information, see [Mapping users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

::::{note}
You can't use [role mapping files](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file) to grant roles to users authenticating using OpenID Connect.
::::

### Example: using the role mapping API

If you want all your users authenticating with OpenID Connect to get access to {{kib}}, issue the following request to {{es}}:

```sh
POST /_security/role_mapping/CLOUD_OIDC_TO_KIBANA_ADMIN <1>
{
    "enabled": true,
    "roles": [ "kibana_admin" ], <2>
    "rules": { <3>
        "field": { "realm.name": "oidc-realm-name" } <4>
    },
    "metadata": { "version": 1 }
}
```

1. The name of the new role mapping.
2. The role mapped to the users.
3. The fields to match against.
4. The name of the OpenID Connect realm. This needs to be the same value as the one used in the cluster configuration.

### Example: Role mapping API, using OpenID Claim information

The user properties that are mapped via the realm configuration are used to process role mapping rules, and these rules determine which roles a user is granted.

The user fields that are provided to the role mapping are derived from the OpenID Connect claims as follows:

* `username`: The `principal` user property
* `dn`: The `dn` user property
* `groups`: The `groups` user property
* `metadata`: See [User metadata](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-user-metadata)


If your OP has the ability to provide groups or roles to RPs using an OpenID Claim, then you should map this claim to the `claims.groups` setting in the {{es}} realm (see [Mapping claims to user properties](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-claim-to-property)), and then make use of it in a role mapping.

For example:

This mapping grants the {{es}} `finance_data` role, to any users who authenticate via the `oidc1` realm with the `finance-team` group membership.

```console
PUT /_security/role_mapping/oidc-finance
{
  "roles": [ "finance_data" ],
  "enabled": true,
  "rules": { "all": [
        { "field": { "realm.name": "oidc1" } },
        { "field": { "groups": "finance-team" } }
  ] }
}
```

### Delegating OIDC authorization to another realm

If your users also exist in a repository that can be directly accessed by {{es}}, such as an LDAP directory, then you can use [authorization realms](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-delegation.md) instead of role mappings.

In this case, you perform the following steps:

1. In your OpenID Connect realm, assign a claim to act as the lookup userid, by configuring the `claims.principal` setting.
2. Create a new realm that can look up users from your local repository (e.g. an `ldap` realm).
3. In your OpenID Connect realm, set `authorization_realms` to the name of the realm you created in step 2.

## Configure {{kib}} [oidc-configure-kibana]

OpenID Connect authentication in {{kib}} requires additional settings in addition to the standard {{kib}} security configuration.

If you're using a self-managed cluster, then, because OIDC requires {{es}} nodes to use TLS on the HTTP interface, you must configure {{kib}} to use a `https` URL to connect to {{es}}, and you may need to configure `elasticsearch.ssl.certificateAuthorities` to trust the certificates that {{es}} has been configured to use.

OpenID Connect authentication in {{kib}} is subject to the following timeout settings in [`kibana.yml`](/deploy-manage/stack-settings.md):

* [`xpack.security.session.idleTimeout`](/deploy-manage/security/kibana-session-management.md#session-idle-timeout)
* [`xpack.security.session.lifespan`](/deploy-manage/security/kibana-session-management.md#session-lifespan)

You may want to adjust these timeouts based on your security requirements.

### Add the OIDC provider to {{kib}}

::::{tip}
You can configure multiple authentication providers in {{kib}} and let users choose the provider they want to use. For more information, check [the {{kib}} authentication documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md).
::::

The three additional settings that are required for OpenID Connect support are shown below:

```yaml
xpack.security.authc.providers:
  oidc.oidc1:
    order: 0
    realm: "oidc1"
```

The configuration values used in the example above are:

`xpack.security.authc.providers`
:   Add an `oidc` provider to instruct {{kib}} to use OpenID Connect single sign-on as the authentication method. This instructs {{kib}} to attempt to initiate an SSO flow every time a user attempts to access a URL in {{kib}}, if the user is not already authenticated.

`xpack.security.authc.providers.oidc.<provider-name>.realm`
:   The name of the OpenID Connect realm in {{es}} that should handle authentication for this {{kib}} instance.

### Supporting OIDC and basic authentication in {{kib}}

If you also want to allow users to log in with a username and password, you must enable the `basic` authentication provider too. This will allow users that haven’t already authenticated with OpenID Connect to log in using the {{kib}} login form:

```yaml
xpack.security.authc.providers:
  oidc.oidc1:
    order: 0
    realm: "oidc1"
    description: "Log in with my OpenID Connect" <1>
  basic.basic1:
    order: 1
```

1. This arbitrary string defines how OpenID Connect login is titled in the Login Selector UI that is shown when you enable multiple authentication providers in {{kib}}. If you have a {{kib}} instance, you can also configure the optional icon and hint settings for any authentication provider.


## OpenID Connect without {{kib}} [oidc-without-kibana]

The OpenID Connect realm is designed to allow users to authenticate to {{kib}}. As a result, most sections of this guide assume {{kib}} is used. This section describes how a custom web application could use the relevant OpenID Connect REST APIs to authenticate the users to {{es}} with OpenID Connect.

::::{note}
The OpenID Connect protocol enables authentication for interactive users via a web browser. Users must be able to open a login URL in their browser and enter credentials when prompted.
{{es}} does not support using OpenID Connect to authenticate non-interactive users such as service principals or automated processes. If you wish to authenticate a service, the [JWT](jwt.md) realm may be a suitable alternative.
The JWT realm is able to authenticate tokens that are produced by OpenID Connect providers.
::::

Single sign-on realms such as OpenID Connect and SAML make use of the Token Service in {{es}} and in principle exchange a SAML or OpenID Connect Authentication response for an {{es}} access token and a refresh token. The access token is used as credentials for subsequent calls to {{es}}. The refresh token enables the user to get new {{es}} access tokens after the current one expires.

::::{note}
The {{es}} Token Service can be seen as a minimal oAuth2 authorization server and the access token and refresh token mentioned above are tokens that pertain *only* to this authorization server. They are generated and consumed *only* by {{es}} and are in no way related to the tokens ( access token and ID Token ) that the OpenID Connect Provider issues.
::::


### Register the RP with an OpenID Connect Provider [_register_the_rp_with_an_openid_connect_provider]

The Relying Party ({{es}} and the custom web app) will need to be registered as client with the OpenID Connect Provider. Note that when registering the `Redirect URI`, it needs to be a URL in the custom web app.


### OpenID Connect Realm [_openid_connect_realm]

An OpenID Connect realm needs to be created and configured accordingly in {{es}}. See [Configure {{es}} for OpenID Connect authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-elasticsearch-authentication)


### Service Account user for accessing the APIs [_service_account_user_for_accessing_the_apis]

The realm is designed with the assumption that there needs to be a privileged entity acting as an authentication proxy. In this case, the custom web application is the authentication proxy handling the authentication of end users ( more correctly, "delegating" the authentication to the OpenID Connect Provider ). The OpenID Connect APIs require authentication and the necessary authorization level for the authenticated user. For this reason, a Service Account user needs to be created and assigned a role that gives them the `manage_oidc` cluster privilege. The use of the `manage_token` cluster privilege will be necessary after the authentication takes place, so that the user can maintain access or be subsequently logged out.

```console
POST /_security/role/facilitator-role
{
  "cluster" : ["manage_oidc", "manage_token"]
}
```

```console
POST /_security/user/facilitator
{
  "password" : "<somePasswordHere>",
  "roles"    : [ "facilitator-role"]
}
```


### Handling the authentication flow [_handling_the_authentication_flow]

On a high level, the custom web application would need to perform the following steps in order to authenticate a user with OpenID Connect:

1. Make an HTTP POST request to `_security/oidc/prepare`, authenticating as the `facilitator` user, using the name of the OpenID Connect realm in the {{es}} configuration in the request body. For more details, see [OpenID Connect prepare authentication](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-oidc-prepare-authentication).

    ```console
    POST /_security/oidc/prepare
    {
      "realm" : "oidc1"
    }
    ```

2. Handle the response to `/_security/oidc/prepare`. The response from {{es}} will contain 3 parameters: `redirect`, `state`, `nonce`. The custom web application would need to store the values for `state` and `nonce` in the user’s session (client side in a cookie or server side if session information is persisted this way) and redirect the user’s browser to the URL that will be contained in the `redirect` value.
3. Handle a subsequent response from the OP. After the user is successfully authenticated with the OpenID Connect Provider, they will be redirected back to the callback/redirect URI. Upon receiving this HTTP GET request, the custom web app will need to make an HTTP POST request to `_security/oidc/authenticate`, again - authenticating as the `facilitator` user - passing the URL where the user’s browser was redirected to, as a parameter, along with the values for `nonce` and `state` it had saved in the user’s session previously. If more than one OpenID Connect realms are configured, the custom web app can specify the name of the realm to be used for handling this, but this parameter is optional. For more details, see [OpenID Connect authenticate](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-oidc-authenticate).

    ```console
    POST /_security/oidc/authenticate
    {
      "redirect_uri" : "https://oidc-kibana.elastic.co:5603/api/security/oidc/callback?code=jtI3Ntt8v3_XvcLzCFGq&state=4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I",
      "state" : "4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I",
      "nonce" : "WaBPH0KqPVdG5HHdSxPRjfoZbXMCicm5v1OiAj0DUFM",
      "realm" : "oidc1"
    }
    ```

    {{es}} will validate this and if all is correct will respond with an access token that can be used as a `Bearer` token for subsequent requests and a refresh token that can be later used to refresh the given access token as described in [Get token](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-token).

4. At some point, if necessary, the custom web application can log the user out by using the [OIDC logout API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-oidc-logout) passing the access token and refresh token as parameters. For example:

    ```console
    POST /_security/oidc/logout
    {
      "token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==",
      "refresh_token": "vLBPvmAB6KvwvJZr27cS"
    }
    ```

    If the realm is configured accordingly, this may result in a response with a `redirect` parameter indicating where the user needs to be redirected in the OP in order to complete the logout process.




