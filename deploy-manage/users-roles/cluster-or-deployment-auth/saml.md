---
navigation_title: SAML
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/saml-realm.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-sign-outgoing-saml-message.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece_sign_outgoing_saml_message.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece_optional_settings.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-clusters-SAML.html
  - https://www.elastic.co/guide/en/cloud/current/ec-securing-clusters-SAML.html
  - https://www.elastic.co/guide/en/cloud/current/ec-sign-outgoing-saml-message.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-securing-clusters-SAML.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echsign-outgoing-saml-message.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-saml-authentication.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/saml-guide-stack.html
applies_to:
  stack: all
products:
  - id: elasticsearch
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-kubernetes
---

# SAML single sign-on [saml-realm]

% eedugon note: compare with original, add extra links if needed (advanced, etc.. perhaps)

The {{stack}} supports SAML single sign-on (SSO) into {{kib}}, using {{es}} as a backend service. This guide helps you configure SAML SSO so that users can log in to {{kib}} using your organization's identity provider (IdP).

For a detailed walk-through of how to implement SAML authentication for {{kib}} with Microsoft Entra ID as an identity provider, refer to [Set up SAML with Microsoft Entra ID](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-entra.md).

Because this feature is designed with {{kib}} in mind, most sections of this guide assume {{kib}} is used. To learn how a custom web application could use the SAML REST APIs to authenticate users to {{es}} without {{kib}}, refer to [SAML without {{kib}}](#saml-no-kibana).

::::{note}
{{stack}} SSO is a [subscription feature](https://www.elastic.co/subscriptions).
::::

::::{tip}
This page describes implementing SAML SSO at the deployment or cluster level, for the purposes of authenticating with a {{kib}} instance.

Depending on your deployment type, you can also configure SSO for the following use cases:

* If you're using {{ech}} or {{serverless-full}}, then you can configure SAML SSO [at the organization level](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md). SAML SSO configured at this level can be used to control access to both the {{ecloud}} Console and to specific {{ech}} deployments and {{serverless-full}} projects. [Learn more about deployment-level vs. organization-level SSO](/deploy-manage/users-roles/cloud-organization.md#organization-deployment-sso).
* If you're using {{ece}}, then you can configure SAML [at the installation level](/deploy-manage/users-roles/cloud-enterprise-orchestrator/saml.md), and then configure [SSO](/deploy-manage/users-roles/cloud-enterprise-orchestrator/configure-sso-for-deployments.md) for deployments.
::::

## How it works [saml-how-it-works]

In SAML terminology, your identity system is the *Identity Provider* (IdP): it authenticates users and issues SAML assertions about them. The {{stack}} acts as a *Service Provider* (SP): {{kib}} initiates and coordinates the SSO flow, and {{es}} validates the SAML assertions and issues session tokens.

To enable SSO, register the {{stack}} as a known SP within your IdP, and configure {{es}} and {{kib}} to trust and communicate with your IdP. When SAML is enabled in {{kib}}, unauthenticated users are redirected to the IdP login page by default. Refer to [Configure {{kib}}](#saml-configure-kibana) for details.
 
The {{stack}} implements SAML SSO with the SAML 2.0 Web Browser SSO profile. Because the flow is browser-based, the SAML realm is not suitable for standard REST clients. If you configure SAML for {{kib}}, also add a realm for API access, such as the [native realm](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md).

SAML also supports [Single Logout](#saml-logout), which ends both the {{kib}} session and the IdP session when a user logs out.

## Before you begin [saml-prerequisites]

Setting up SAML requires coordination with your Identity Provider (IdP). You'll collect some information from it, and register the {{stack}} as a Service Provider (SP) within it.

### IdP requirements [saml-guide-idp]

The {{stack}} supports the SAML 2.0 Web Browser SSO and Single Logout profiles, and can integrate with any IdP that supports at least the Web Browser SSO profile. It has been tested with [Microsoft Active Directory Federation Services (ADFS)](https://www.elastic.co/blog/how-to-configure-elasticsearch-saml-authentication-with-adfs), [Microsoft Entra ID](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-entra.md), and [Okta](https://www.elastic.co/blog/how-to-set-up-okta-saml-login-kibana-elastic-cloud).

To configure {{es}}, you will need a standard XML-formatted SAML *metadata* document from your IdP, which defines its capabilities and features. You should be able to download or generate it from your IdP's administration interface.

Most IdPs will provide an appropriate metadata file with all the features that the {{stack}} requires. The minimum requirements that the {{stack}} has for the IdP's metadata are:

* An `<EntityDescriptor>` with an `entityID` that you will configure as `idp.entity_id` in {{es}}
* An `<IDPSSODescriptor>` that supports the SAML 2.0 protocol (`urn:oasis:names:tc:SAML:2.0:protocol`)
* At least one `<KeyDescriptor>` configured for signing (with `use="signing"`, or `use` left unspecified)
* A `<SingleSignOnService>` with binding of HTTP-Redirect (`urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect`)
* If you want Single Logout: a `<SingleLogoutService>` with binding of HTTP-Redirect

All messages from the IdP must be signed. For `<Response>` messages, the signature can be on the response itself or on individual assertions. For `<LogoutRequest>` messages, the signature must be provided as a URL parameter, as required by the `HTTP-Redirect` binding.

### Information to gather [saml-info-collect]

Collect the following from your IdP before you begin:

| What you need | Where to find it |
|---|---|
| **IdP metadata URL or file** | Your IdP's admin interface. A URL is preferred so {{es}} can reload it automatically when it changes. |
| **IdP entity ID** | An identifier assigned to your IdP, most commonly expressed as a URI. Your admin interface might display it directly, or you can find it in the metadata XML as the `entityID` attribute on the `EntityDescriptor` element. |

### Prerequisites for self-managed clusters

If you're using a self-managed cluster:

* Enable TLS for the {{es}} HTTP interface. SAML requires HTTPS. For more information, see [Encrypt HTTP client communications for {{es}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-http-communication). If you started {{es}} [with security enabled](/deploy-manage/deploy/self-managed/installing-elasticsearch.md), TLS is already enabled.
* The {{es}} token service must be enabled. It is automatically enabled when TLS is configured on the HTTP interface. You can also enable it explicitly in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):
  ```yaml
  xpack.security.authc.token.enabled: true
  ```

{{ech}}, {{ece}}, and {{eck}} have TLS and the token service enabled by default.

## Configuration steps

:::::{stepper}

::::{step} Configure your identity provider
:anchor: saml-configure-idp

Register the {{stack}} as a SAML service provider in your IdP. The exact steps vary by provider, but you generally need to:

1. Create a new SAML application or service provider entry in your IdP.
2. Set the **Assertion Consumer Service (ACS) URL** to `{kibana-url}/api/security/saml/callback`.
3. Set the **entity ID** to a URI that uniquely identifies this {{kib}} instance as a Service Provider. We recommend using the {{kib}} base URL (for example, `https://kibana.example.com`).
4. Set the **logout URL** to `{kibana-url}/logout` if your IdP supports Single Logout.
5. Identify the user attributes your IdP can include in SAML assertions — consult your IdP documentation or local admin. This varies between providers. These attribute URIs will be used to configure the attribute mapping in {{es}}.
6. Note the **IdP metadata URL** or download the metadata file — you will need this for the {{es}} configuration.

:::{tip}
If your IdP supports SP metadata import, you can generate an SP metadata file after [configuring the {{es}} realm](#saml-create-realm) and use it to populate or verify these values in your IdP. Refer to [Generate SP metadata](#saml-sp-metadata) for more details.
:::

:::{note}
If your IdP requires signed outgoing SAML messages (authentication requests or logout requests), you will also need to provide your {{es}} signing certificate to the IdP at this stage. Refer to [Signing and encryption](#saml-enc-sign) for how to generate certificates and configure signing in {{es}}.
:::
::::

::::{step} Create a SAML realm in {{es}}
:anchor: saml-create-realm

% eedugon note: compare a bit more with original, links to bundles, check common-settings dropdown and do final refinement and decision

Add a SAML realm to your [{{es}} configuration](/deploy-manage/stack-settings.md).

This realm has a few mandatory settings and a number of optional settings. The available settings are described in detail in [Security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md):

* [SAML realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings)
* [SAML realm signing settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-signing-settings)
* [SAML realm encryption settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-encryption-settings)
* [SAML realm SSL settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-ssl-settings)

```yaml
xpack.security.authc.realms.saml.saml1:
  order: 2
  idp.metadata.path: "https://idp.example.com/metadata"  # <1>
  idp.entity_id: "https://idp.example.com/"              # <2>
  sp.entity_id: "https://kibana.example.com"             # <3>
  sp.acs: "https://kibana.example.com/api/security/saml/callback"  # <4>
  sp.logout: "https://kibana.example.com/logout"         # <5>
  attributes.principal: "urn:oid:0.9.2342.19200300.100.1.1"  # <6>
  attributes.groups: "urn:oid:1.3.6.1.4.1.5923.1.5.1."      # <7>
```

1. URL or file path to the IdP's SAML metadata. A URL is recommended — {{es}} monitors it for changes and reloads automatically. If using a file path, it is resolved relative to the {{es}} config directory. For {{ech}} and {{ece}}, [upload the file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) first. For {{eck}}, install it as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md).
2. The entity ID your IdP uses. Must match the `entityID` attribute in the IdP metadata.
3. A unique identifier for this {{kib}} instance, expressed as a URI. Must match the entity ID you set in your IdP in [Step 1](#saml-configure-idp). We recommend using the {{kib}} base URL.
4. The ACS URL where the IdP sends authentication responses. Must be reachable from users' browsers.
5. The URL where the IdP sends logout messages. Required for [SAML Single Logout](#saml-logout). If not configured, {{es}} refuses all `<LogoutRequest>` messages from the IdP.
6. The SAML attribute that {{es}} uses as the username (`principal`). Replace with the URI your IdP uses. See [Map SAML attributes](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-attribute-mapping.md).
7. The SAML attribute that maps to group memberships. Replace with the URI your IdP uses. Optional but recommended for role-based access control.

:::{note}
The `order` setting controls realm priority. Assign SSO realms (SAML, OpenID Connect) higher order values than password-based realms (native, LDAP). If you're using {{eck}}, set `order` to a value greater than the file realm (default `-100`) and native realm (default `-99`), which ECK relies on for its own operation.
:::

For the full list of available settings, refer to [SAML realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings).

#### Map SAML attributes [saml-attributes-mapping]

The values for `attributes.principal` and `attributes.groups` must exactly match the attribute identifiers your IdP sends. {{es}} does not require specific URIs. For options such as mapping from the SAML `NameID` or extracting part of an attribute value, refer to [Map SAML attributes](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-attribute-mapping.md).

If your IdP requires signed requests or uses encrypted assertions, refer to [Signing and encryption](#saml-enc-sign).
::::

::::{step} Configure role mappings
:anchor: saml-role-mapping

SAML authentication identifies users to the {{stack}}, but does not automatically grant them any access. You must map SAML users to {{es}} roles before they can do anything.

You can configure role mappings using:
* The **Role Mappings** page in {{kib}}
* The [role mapping API]({{es-apis}}operation/operation-security-put-role-mapping)
* [Authorization realms](/deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md#authorization_realms) (if your users exist in an LDAP directory or similar)

:::{note}
[Role mapping files](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file) cannot be used for SAML users.
:::

**Grant access by realm**

This mapping grants the `example_role` role to all users who authenticate via the `saml1` realm:

```console
PUT /_security/role_mapping/saml-all-users
{
  "roles": [ "example_role" ],
  "enabled": true,
  "rules": {
    "field": { "realm.name": "saml1" }
  }
}
```

**Grant access by group**

If your IdP provides group memberships, you can map specific groups to roles. This mapping grants the `finance_data` role to users in the `finance-team` group authenticating via `saml1`:

```console
PUT /_security/role_mapping/saml-finance
{
  "roles": [ "finance_data" ],
  "enabled": true,
  "rules": { "all": [
    { "field": { "realm.name": "saml1" } },
    { "field": { "groups": "finance-team" } }
  ] }
}
```

The `groups` field supports wildcards (`*`). Refer to the [role mapping API]({{es-apis}}operation/operation-security-put-role-mapping) for the full rule syntax.

**Delegate authorization to another realm**

If your users also exist in an LDAP directory or similar repository that {{es}} can directly access, you can use [authorization realms](/deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md#authorization_realms) instead of role mappings:

1. Configure `attributes.principal` in your SAML realm to identify the user for the lookup.
2. Create a realm that can look up users from your repository (for example, an `ldap` realm).
3. Set `authorization_realms` in your SAML realm to the name of the realm from step 2.
::::

::::{step} Configure {{kib}}
:anchor: saml-configure-kibana

Add the SAML authentication provider to your {{kib}} configuration.

If you're using a self-managed cluster, configure {{kib}} to connect to {{es}} over HTTPS. You may also need to configure `elasticsearch.ssl.certificateAuthorities` to trust the certificates {{es}} uses.

```yaml
xpack.security.authc.providers:
  saml.saml1:
    order: 0
    realm: "saml1"  # <1>
```

1. Must match the SAML realm name defined in your {{es}} configuration.

With this configuration, {{kib}} redirects all unauthenticated users to your IdP for login.

**Allow both SAML and username/password login**

To let some users (for example, local administrators) log in with a username and password, enable a basic provider alongside SAML:

```yaml
xpack.security.authc.providers:
  saml.saml1:
    order: 0
    realm: "saml1"
    description: "Log in with SSO"
  basic.basic1:
    order: 1
```

Users will see a login selector and can choose their preferred method. Users who log in with basic authentication must have credentials in a configured {{es}} realm (such as native or LDAP).

You can also adjust [session timeout settings](/deploy-manage/security/kibana-session-management.md) (`xpack.security.session.idleTimeout` and `xpack.security.session.lifespan`) to match your security requirements.
::::

:::::

## Troubleshooting [saml-troubleshooting]

If you encounter issues, refer to the [SAML troubleshooting documentation](../../../troubleshoot/elasticsearch/security/trb-security-saml.md).

## Advanced configuration

The following sections cover optional features and specific SAML behaviors that go beyond the standard configuration steps. They address particular aspects of the protocol — such as logout coordination, message signing, or authentication constraints — that you may need depending on your IdP's capabilities and your organization's security requirements.

### SAML Single Logout [saml-logout]

The SAML protocol supports Single Logout (SLO), which ends both the {{kib}} session and the IdP session when a user logs out. Support for SLO varies between identity providers — consult your IdP's documentation to determine what Logout services it offers.

By default, {{es}} uses SAML SLO when all of the following are true:
* Your IdP metadata includes a `<SingleLogoutService>` with HTTP-Redirect binding
* Your IdP releases a `NameID` in the SAML assertion
* You have configured `sp.logout`
* The setting `idp.use_single_logout` is not `false`

**IdP SLO service requirements**

The `<SingleLogoutService>` in your IdP's metadata must support the `urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect` binding. {{es}} sends both `<LogoutRequest>` and `<LogoutResponse>` messages to this service.

**The `sp.logout` setting**

`sp.logout` specifies a URL in {{kib}} to which the IdP can send both `<LogoutRequest>` and `<LogoutResponse>` messages using the HTTP-Redirect binding. When {{es}} receives a `<LogoutRequest>`, it performs a global signout that invalidates all {{es}} security tokens associated with that SAML session.

If you don't configure `sp.logout`, {{es}} will refuse all `<LogoutRequest>` messages from the IdP.

**When SLO is not available**

If your IdP does not support Single Logout, or you choose not to use it, {{kib}} performs a local logout only: the {{es}} session token is invalidated, but the IdP session remains active. Users are still considered logged in to the IdP and will be automatically reauthenticated if they navigate back to the {{kib}} landing page without entering credentials.

The possible solutions to this problem are:

* Ask your IdP administrator or vendor to provide a Single Logout service.
* If your IdP does provide a Single Logout service, make sure it is included in the IdP metadata file and do *not* set `idp.use_single_logout` to `false`.
* Advise your users to close their browser after logging out of {{kib}}.
* Enable `force_authn: true` in your SAML realm. This forces fresh authentication at the IdP on every login, preventing session reuse even without SLO. It defaults to `false` because it adds friction to the user experience, but it is an effective protection against users piggybacking on existing IdP sessions.

To disable SLO even when your IdP advertises support for it, set `idp.use_single_logout: false` in the realm configuration.

::::{note}
Some IdPs require logout requests to be signed. Check your IdP's documentation and configure [signing credentials](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-signing-settings) if needed.
::::

### Signing and encryption [saml-enc-sign]

Some IdPs require SAML logout requests or authentication requests to be signed. Others, like Microsoft Entra ID, accept unsigned requests. Some IdPs also encrypt their SAML assertions.

You can configure {{es}} to:
* Sign outgoing SAML messages (all message types, or only specific ones such as `AuthnRequest` or `LogoutRequest`)
* Decrypt incoming encrypted assertions

{{es}} supports PEM, PKCS#12, and JKS certificate formats. For a step-by-step guide including certificate generation (using `openssl` or `elasticsearch-certutil`) and full configuration examples, refer to [Configure SAML signing and encryption](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-signing-encryption.md).

For the full list of available settings, refer to:
* [SAML realm signing settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-signing-settings)
* [SAML realm encryption settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-encryption-settings)

### Request specific authentication methods [req-authn-context]

It is sometimes necessary for a SAML SP to impose specific restrictions on the authentication that takes place at the IdP, in order to assess the level of confidence it can place in the corresponding authentication response. The restrictions might relate to the authentication method (password, client certificates, etc.), the user identification method during registration, and other details. {{es}} implements [SAML 2.0 Authentication Context](https://docs.oasis-open.org/security/saml/v2.0/saml-authn-context-2.0-os.pdf) for this purpose.

The SAML SP sends a set of Authentication Context Class Reference values in the Authentication Request, describing the restrictions to impose on the IdP. The IdP attempts to satisfy those restrictions and indicates the result in its Authentication Response. If the IdP cannot grant the requested restrictions, authentication fails.

Configure the class reference values using `req_authn_context_class_ref` in your SAML realm. Refer to [SAML realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings).

{{es}} supports only the `exact` comparison method. The Authentication Response must include one of the specified values; otherwise, authentication fails.

### Generate SP metadata [saml-sp-metadata]

Some Identity Providers support importing a metadata file from the Service Provider. This will automatically configure many of the integration options between the IdP and the SP.

Once you have [configured a SAML realm in {{es}}](#saml-create-realm), you can generate its SP metadata file using the [SAML service provider metadata API]({{es-apis}}operation/operation-security-saml-service-provider-metadata) or the [`bin/elasticsearch-saml-metadata` command](elasticsearch://reference/elasticsearch/command-line-tools/saml-metadata.md).

#### Using the SAML service provider metadata API

You can generate the SAML metadata by issuing the API request to {{es}} and store it as an XML file using tools like `jq`. For example, the following command generates the metadata for the SAML realm `saml1` and saves it to a `metadata.xml` file:

```console
curl -u user_name:password  -X GET http://localhost:9200/_security/saml/metadata/saml1 -H 'Content-Type: application/json' | jq -r '.[]' > metadata.xml
```

#### Using the `elasticsearch-saml-metadata` command

```{applies_to}
deployment:
  self:
  eck:
```

You can generate the SAML metadata by running the [`bin/elasticsearch-saml-metadata` command](elasticsearch://reference/elasticsearch/command-line-tools/saml-metadata.md).

::::{applies-switch}
:::{applies-item} self:
```sh
bin/elasticsearch-saml-metadata --realm saml1
```
:::
:::{applies-item} eck:
To generate the Service Provider metadata using the `elasticsearch-saml-metadata` command in {{eck}}, you need to run the command using `kubectl`, and then copy the generated metadata file to your local machine. For example:

```sh
# Create metadata
kubectl exec -it elasticsearch-sample-es-default-0 -- sh -c "/usr/share/elasticsearch/bin/elasticsearch-saml-metadata --realm saml1"

# Copy metadata file
kubectl cp elasticsearch-sample-es-default-0:/usr/share/elasticsearch/saml-elasticsearch-metadata.xml saml-elasticsearch-metadata.xml
```
:::
::::

### Multiple {{kib}} instances [_operating_multiple_kib_instances]

If multiple {{kib}} instances authenticate against the same {{es}} cluster, each instance requires its own SAML realm with a unique `sp.entity_id` and `sp.acs`. {{es}} routes each authentication request to the correct realm by matching the `sp.acs` value.

The following example shows three {{kib}} instances: two share an internal IdP, and one uses a different IdP.

```yaml
xpack.security.authc.realms.saml.saml_finance:
  order: 2
  idp.metadata.path: saml/idp-metadata.xml
  idp.entity_id: "<sso-example-url>"
  sp.entity_id: "<kibana-finance-example-url>"
  sp.acs: "<kibana-finance-example-url>/api/security/saml/callback"
  sp.logout: "<kibana-finance-example-url>/logout"
  attributes.principal: "urn:oid:0.9.2342.19200300.100.1.1"
  attributes.groups: "urn:oid:1.3.6.1.4.1.5923.1.5.1."
xpack.security.authc.realms.saml.saml_sales:
  order: 3
  idp.metadata.path: saml/idp-metadata.xml
  idp.entity_id: "<sso-example-url>"
  sp.entity_id: "<kibana-sales-example-url>"
  sp.acs: "<kibana-sales-example-url>/api/security/saml/callback"
  sp.logout: "<kibana-sales-example-url>/logout"
  attributes.principal: "urn:oid:0.9.2342.19200300.100.1.1"
  attributes.groups: "urn:oid:1.3.6.1.4.1.5923.1.5.1."
xpack.security.authc.realms.saml.saml_eng:
  order: 4
  idp.metadata.path: saml/idp-external.xml
  idp.entity_id: "<engineering-sso-example-url>"
  sp.entity_id: "<kibana-engineering-example-url>"
  sp.acs: "<kibana-engineering-example-url>/api/security/saml/callback"
  sp.logout: "<kibana-engineering-example-url>/logout"
  attributes.principal: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn"
```

### SAML without {{kib}} [saml-no-kibana]

If you're building a custom web application that needs to authenticate users against {{es}} using SAML — without {{kib}} — you can use the SAML REST APIs to implement the full authentication flow directly. This is relevant when you have a custom portal, a microservice-based architecture, or any scenario where the browser-based SSO flow must be handled by your own application code rather than by {{kib}}.

The application acts as an authentication proxy: it drives the SP-initiated or IdP-initiated SSO flow, exchanges the SAML response for an {{es}} access token and refresh token, and uses that token as a `Bearer` credential for subsequent requests.

For the complete implementation guide — including service account setup, SP-initiated and IdP-initiated flows, and logout handling — refer to [SAML without {{kib}}](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-without-kibana.md).
