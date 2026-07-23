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

# SAML authentication [saml-realm]

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

To enable SSO, register the {{stack}} as a known SP within your IdP, and configure {{es}} and {{kib}} to trust and communicate with your IdP. When SAML is enabled in {{kib}}, unauthenticated users are redirected to the IdP login page by default.
 
The {{stack}} implements SAML SSO with the SAML 2.0 Web Browser SSO profile. Because the flow is browser-based, the SAML realm is not suitable for standard REST clients. If you configure SAML for {{kib}}, also add a realm for API access, such as the [native realm](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md).

SAML also supports [Single Logout](#saml-logout), which ends both the {{kib}} session and the IdP session when a user logs out.

## Before you begin [saml-prerequisites]

Setting up SAML requires coordination with your Identity Provider (IdP). You'll collect some information from it, and register the {{stack}} as a Service Provider (SP) within it.

### IdP requirements [saml-guide-idp]

The {{stack}} supports the SAML 2.0 Web Browser SSO and Single Logout profiles, and can integrate with any IdP that supports at least the Web Browser SSO profile. It has been tested with [Microsoft Active Directory Federation Services (ADFS)](https://www.elastic.co/blog/how-to-configure-elasticsearch-saml-authentication-with-adfs), [Microsoft Entra ID](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-entra.md), and [Okta](https://www.elastic.co/blog/how-to-set-up-okta-saml-login-kibana-elastic-cloud).

To configure {{es}}, you will need a standard XML-formatted SAML *metadata* document from your IdP, which defines its capabilities and features. You should be able to download or generate it from your IdP's administration interface. You can pass it to {{es}} as a URL (preferred, so {{es}} reloads it automatically when it changes) or as a local file. For more information, refer to [Create a SAML realm in {{es}}](#saml-create-realm).

Most IdPs will provide an appropriate metadata file with all the features that the {{stack}} requires. Verify that your IdP's metadata includes the following:

* An `<EntityDescriptor>` with an `entityID` that you will configure as `idp.entity_id` in the {{es}} realm
* An `<IDPSSODescriptor>` that supports the SAML 2.0 protocol (`urn:oasis:names:tc:SAML:2.0:protocol`)
* At least one `<KeyDescriptor>` configured for signing (with `use="signing"`, or `use` left unspecified)
* A `<SingleSignOnService>` with binding of HTTP-Redirect (`urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect`)
* If you want [Single Logout](#saml-logout): a `<SingleLogoutService>` with binding of HTTP-Redirect

All messages from the IdP must be signed. For `<Response>` messages, the signature can be on the response itself or on individual assertions. For `<LogoutRequest>` messages, the signature must be provided as a URL parameter, as required by the `HTTP-Redirect` binding.

### Prerequisites for self-managed clusters

If you're using a self-managed cluster:

* Enable TLS for the {{es}} HTTP interface. SAML requires HTTPS. For more information, see [Encrypt HTTP client communications for {{es}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-http-communication). If you started {{es}} [with security enabled](/deploy-manage/security/self-setup.md), TLS is already enabled.
* The {{es}} token service must be enabled. It is automatically enabled when TLS is configured on the HTTP interface. You can also enable it explicitly in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):
  ```yaml
  xpack.security.authc.token.enabled: true
  ```

:::{note}
{{ech}}, {{ece}}, and {{eck}} enable HTTPS and the token service by default.
:::

## Configuration steps

:::::{stepper}

::::{step} Configure your identity provider
:anchor: saml-configure-idp

Register the {{stack}} as a SAML service provider in your IdP. The exact steps vary by provider, but you generally need to:

1. Create a new SAML application or service provider entry in your IdP.
2. Set the **Assertion Consumer Service (ACS) URL** to your {{kib}} base URL followed by `/api/security/saml/callback` (for example, `https://kibana.example.com/api/security/saml/callback`).
3. Set the **entity ID** to a URI that uniquely identifies this {{kib}} instance as a Service Provider. We recommend using the {{kib}} base URL (for example, `https://kibana.example.com`).
4. Set the **logout URL** to your {{kib}} base URL followed by `/logout` if your IdP supports Single Logout (for example, `https://kibana.example.com/logout`).
5. Identify the user attributes your IdP can include in SAML assertions. Consult your IdP documentation or local admin. This varies between providers. These attribute URIs will be used to configure the attribute mapping in the {{es}} realm.
6. Note the **IdP metadata URL** or download the metadata file. You will need this for the {{es}} configuration.

:::{tip}
If your IdP supports SP metadata import, you can generate an SP metadata file after [configuring the {{es}} realm](#saml-create-realm) and import it into your IdP to register the {{stack}} as a Service Provider automatically. Refer to [Generate SP metadata](#saml-sp-metadata).
:::

:::{note}
If your IdP requires signed outgoing SAML messages (authentication requests or logout requests), you will also need to provide your {{es}} signing certificate to the IdP at this stage. Refer to [Signing and encryption](#saml-enc-sign) for how to generate certificates and configure signing in {{es}}.
:::
::::

::::{step} Create a SAML realm in {{es}}
:anchor: saml-create-realm

Add a SAML realm to your [{{es}} configuration](/deploy-manage/stack-settings.md#configure-stack-settings) and restart the cluster for the changes to take effect.

The realm ties together three pieces: your IdP's identity and metadata, the {{stack}}'s service provider endpoints, and the attribute mapping that tells {{es}} how to identify users from the IdP's assertions.

```yaml
xpack.security.authc.realms.saml.saml1:
  order: 2  # <1>
  idp.metadata.path: "https://idp.example.com/metadata"
  idp.entity_id: "https://idp.example.com/"
  sp.entity_id: "https://kibana.example.com"
  sp.acs: "https://kibana.example.com/api/security/saml/callback"
  sp.logout: "https://kibana.example.com/logout"
  attributes.principal: "urn:oid:0.9.2342.19200300.100.1.1"
  attributes.groups: "urn:oid:1.3.6.1.4.1.5923.1.5.1."
```

1. Controls realm priority. Assign SSO realms higher order values than password-based realms (native, LDAP). If you're using {{eck}}, set `order` to a value greater than the file realm (default `-100`) and native realm (default `-99`).

Configure each setting as described below. For the full list of available settings, refer to [SAML realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings).

`idp.metadata.path`
:   The path or URL to the SAML metadata file for your Identity Provider. A URL is recommended so {{es}} reloads it automatically when it changes.

    :::{tip}
    If you want to pass a file path, then review the following:
    * File path settings are resolved relative to the {{es}} config directory. {{es}} will automatically monitor this file for changes and will reload the configuration whenever it is updated.
    * If you're using {{ech}} or {{ece}}, then you must upload the file before it can be referenced. For {{ech}}, upload the file [as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md). For {{ece}}, follow the equivalent [ECE procedure](/deploy-manage/deploy/cloud-enterprise/add-custom-bundles-plugins.md).
    * If you're using {{eck}}, then install the file as [custom configuration files](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).
    :::

`idp.entity_id`
:   The identifier (SAML EntityID) that your IdP uses. Must match the `entityID` attribute in the IdP metadata exactly. The comparison is case-sensitive.

`sp.entity_id`
:   A unique identifier for your {{kib}} instance, expressed as a URI. Must match exactly the entity ID you [configure in your IdP](#saml-configure-idp). The comparison is case-sensitive. We recommend using the {{kib}} base URL.

`sp.acs`
:   The URL of the Assertion Consumer Service within {{kib}} that receives authentication responses from your IdP, using the HTTP-POST binding. For example, `https://kibana.example.com/api/security/saml/callback`. This URL must be reachable from users' browsers — it does not need to be directly accessible by {{es}} or the IdP. If {{kib}} is behind a reverse proxy, use the public-facing URL.

`sp.logout`
:   The URL of the Single Logout service within {{kib}} that receives logout messages from your IdP. For example, `https://kibana.example.com/logout`. Required for [SAML Single Logout](#saml-logout). If not configured, {{es}} refuses all `<LogoutRequest>` messages from the IdP.

`attributes.principal` (required)
:   The SAML attribute that {{es}} uses as the username (`principal`). Replace with the URI your IdP uses. Attribute URIs vary between providers. If your IdP uses `NameID`, use `nameid` here. See [Attribute mapping](#saml-attributes-mapping).

`attributes.groups` (recommended)
:   The SAML attribute that maps to group memberships. Replace with the URI your IdP uses. Recommended if you want to assign roles based on IdP group memberships. See [Attribute mapping](#saml-attributes-mapping).

:::{note}
If your IdP requires signed requests or uses encrypted assertions, refer to [Signing and encryption](#saml-enc-sign).
:::

:::{note}
If your IdP supports Authentication Context restrictions (for example, to require MFA), you can configure `req_authn_context_class_ref` in the realm. Refer to [Request specific authentication methods](#req-authn-context).
:::

#### Attribute mapping [saml-attributes-mapping]

When a user authenticates through SAML, the IdP sends an assertion containing *attributes* (pieces of information about the user such as their username, email address, or group memberships). The `attributes.*` realm settings tell {{es}} which SAML attribute URI to use for each {{es}} user property.

:::{warning}
The attribute URIs must exactly match what your IdP sends in the assertion. A mismatch silently breaks authentication: the login might appear to succeed but the user's principal or group memberships will be missing or incorrect. Verify the exact URIs with your IdP administrator or by inspecting a captured SAML assertion.
:::

The most important mappings are `attributes.principal` and `attributes.groups`: `attributes.principal` is required and determines the username {{es}} assigns to the authenticated user, and `attributes.groups` is recommended if you want to assign roles based on IdP group memberships.

For a complete reference of mappable user properties, special attribute names, and advanced patterns, refer to [Map SAML attributes to {{es}} user properties](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-attribute-mapping.md).

::::

::::{step} Configure {{kib}} for SAML authentication
:anchor: saml-configure-kibana

Add the SAML [authentication provider](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md) to your [{{kib}} configuration](/deploy-manage/stack-settings.md#configure-stack-settings) and restart {{kib}} for the changes to take effect.

```yaml
xpack.security.authc.providers:
  saml.saml1:
    order: 0
    realm: "saml1"  # <1>
```

1. Must match the SAML realm name defined in your {{es}} configuration.

With this configuration, {{kib}} redirects all unauthenticated users to your IdP for login.

:::{note}
If you run multiple {{kib}} instances connected to the same cluster or deployment (for example, behind a load balancer), apply this SAML provider configuration to every instance. If each instance is accessed through a different URL, each needs its own SAML realm. Refer to [Multiple {{kib}} instances and URLs](#_operating_multiple_kib_instances).
:::

#### Allow both SAML and basic authentication [saml-kibana-basic]

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

::::{step} Configure role mappings
:anchor: saml-role-mapping

SAML authentication identifies users to the {{stack}}, but does not automatically grant them any access. You must map SAML users to {{es}} roles before they can do anything.

Role mappings connect SAML user identities to {{es}} roles, but the roles themselves must exist first. You can use built-in roles such as `superuser` or `kibana_admin` for initial testing. For production, create [custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) with appropriate access to your data and [{{kib}} features](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-feature-privileges).

You can create role mappings in the **Role Mappings** page in {{kib}} or with the [role mapping API]({{es-apis}}operation/operation-security-put-role-mapping). For the general concepts, UI workflow, and rule syntax, refer to [Map external users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md). The examples below show common SAML patterns.

:::{note}
[Role mapping files](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file) cannot be used for SAML users.
:::

#### Grant access by realm

This is an example of a simple role mapping that grants the `example_role` role to any user who authenticates against the `saml1` realm:

```console
PUT /_security/role_mapping/saml-all-users
{
  "roles": [ "example_role" ], <1>
  "enabled": true,
  "rules": {
    "field": { "realm.name": "saml1" }
  }
}
```

1. Replace `example_role` with the role you want to assign.

#### Grant access by group

The user fields available in role mapping rules are derived from the SAML attributes configured in the realm:

* `username`: The `principal` attribute
* `dn`: The `dn` attribute
* `groups`: The `groups` attribute
* `metadata`: See [User metadata](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-attribute-mapping.md#saml-user-metadata)

If your IdP provides group memberships, [configure `attributes.groups` in the {{es}} realm](#saml-create-realm) and then use it in a role mapping rule.

This example grants the `finance_data` role to users in the `finance-team` group authenticating through `saml1` realm:

```console
PUT /_security/role_mapping/saml-finance
{
  "roles": [ "finance_data" ],
  "enabled": true,
  "rules": { "all": [
    { "field": { "realm.name": "saml1" } },
    { "field": { "groups": "finance-team" } } <1>
  ] }
}
```

1. The `groups` field supports wildcards (`*`). Refer to the [role mapping API]({{es-apis}}operation/operation-security-put-role-mapping) for the full rule syntax.

#### Delegate authorization to another realm

If your users also exist in a repository that can be directly accessed by {{es}} (such as an LDAP directory), you can use [authorization realms](/deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md#authorization_realms) instead of role mappings:

1. Configure `attributes.principal` in your SAML realm to identify the user for the lookup.
2. Create a realm that can look up users from your repository (for example, an `ldap` realm).
3. Set `authorization_realms` in your SAML realm to the name of the realm from step 2.
::::

::::{step} Test SAML authentication
:anchor: saml-test

After applying all changes, open {{kib}} in a browser. You should be redirected to your IdP's login page. After authenticating, you should be returned to {{kib}} as a logged-in user.

To verify the user's identity and roles, use the [authenticate API]({{es-apis}}operation/operation-security-authenticate):

```console
GET /_security/_authenticate
```

The response shows the authenticated username, assigned roles, and SAML metadata. If roles are missing or incorrect, review your role mapping rules, the realm configuration, and the SAML attributes your IdP is sending.

:::{tip}
If SAML is not yet working and you cannot access {{kib}}, make sure you have configured a basic authentication provider as described in [Allow both SAML and basic authentication](#saml-kibana-basic).
:::

If something does not work as expected, refer to the [SAML troubleshooting documentation](../../../troubleshoot/elasticsearch/security/trb-security-saml.md) for common issues and their resolutions, including how to enable debug logging to diagnose authentication failures.
::::

:::::

## Advanced configuration

The following sections cover optional features and specific SAML behaviors that go beyond the standard configuration steps. They address particular aspects of the protocol, such as logout coordination, message signing, or authentication constraints, that you might need depending on your IdP's capabilities and your organization's security requirements.

### Signing and encryption [saml-enc-sign]

Depending on your IdP, you might need to sign outgoing SAML messages (authentication or logout requests), decrypt encrypted assertions, or both. {{es}} supports both cases using X.509 certificates configured in the SAML realm.

For a complete example including certificate generation and configuration for PEM, PKCS#12, and JKS formats, refer to [Configure SAML signing and encryption](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-signing-encryption.md).

For available settings, refer to [SAML realm signing settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-signing-settings) and [SAML realm encryption settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-encryption-settings).

### SAML Single Logout [saml-logout]

The SAML protocol supports Single Logout (SLO), which ends both the {{kib}} session and the IdP session when a user logs out. Support for SLO varies between identity providers. Consult your IdP's documentation to determine what Logout services it offers.

By default, {{es}} uses SAML SLO when all of the following are true:
* Your IdP metadata includes a `<SingleLogoutService>` with HTTP-Redirect binding
* Your IdP releases a `NameID` in the SAML assertion
* You have configured `sp.logout`
* The setting `idp.use_single_logout` is not `false`

The `sp.logout` setting specifies a URL in {{kib}} to which the IdP can send both `<LogoutRequest>` and `<LogoutResponse>` messages using the HTTP-Redirect binding. {{es}} sends both message types to the IdP's `<SingleLogoutService>` as appropriate. When {{es}} receives a `<LogoutRequest>`, it performs a global signout that invalidates all {{es}} security tokens associated with that SAML session.

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
Some IdPs require logout requests to be signed. Check your IdP's documentation and configure [signing certificates](#saml-enc-sign) if needed.
::::

### Request specific authentication methods [req-authn-context]

It is sometimes necessary for a SAML SP to impose specific restrictions on the authentication that takes place at the IdP. The restrictions might relate to the authentication method used — such as password, client certificates, or MFA — the user identification method during registration, and other details. {{es}} implements [SAML 2.0 Authentication Context](https://docs.oasis-open.org/security/saml/v2.0/saml-authn-context-2.0-os.pdf) for this purpose.

The SAML SP sends a set of Authentication Context Class Reference values in the Authentication Request, describing the restrictions to impose on the IdP. The IdP attempts to satisfy those restrictions and indicates the result in its Authentication Response. If the IdP cannot grant the requested restrictions, authentication fails.

Configure the class reference values using `req_authn_context_class_ref` in your SAML realm. For example:

```yaml
xpack.security.authc.realms.saml.saml1:
  req_authn_context_class_ref:
    - "http://schemas.microsoft.com/claims/multipleauthn"  # <1>
```

1. This example uses the Entra ID URI for MFA. The exact URI values depend on your IdP. Some standard SAML 2.0 values such as `urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport` are widely supported, but IdP-specific URIs are common. Consult your IdP's documentation.

{{es}} supports only the `exact` comparison method. The Authentication Response must include one of the specified values; otherwise, authentication fails. For more details, refer to [`req_authn_context_class_ref`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings).

### Generate SP metadata [saml-sp-metadata]

The SP metadata is an XML document that describes your {{stack}} as a SAML Service Provider. It contains your entity ID, ACS URL, logout URL, and any signing or encryption certificates configured in the realm. Some Identity Providers can import this file to configure the integration automatically, instead of requiring you to enter each value individually when [registering the {{stack}} in your IdP](#saml-configure-idp).

Once you have [configured a SAML realm in {{es}}](#saml-create-realm), you can generate its SP metadata file using the [SAML service provider metadata API]({{es-apis}}operation/operation-security-saml-service-provider-metadata) or the [`bin/elasticsearch-saml-metadata` command](elasticsearch://reference/elasticsearch/command-line-tools/saml-metadata.md).

#### Using the SAML service provider metadata API

You can generate the SAML metadata by issuing the API request to {{es}} and store it as an XML file using tools like `jq`. For example, the following command generates the metadata for the SAML realm `saml1` and saves it to a `metadata.xml` file:

```console
curl -u user_name:password -X GET https://elasticsearch.example.com:9200/_security/saml/metadata/saml1 -H 'Content-Type: application/json' | jq -r '.[]' > metadata.xml  # <1>
```

1. Replace `elasticsearch.example.com:9200` with your actual {{es}} endpoint.

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

### Multiple {{kib}} instances and URLs [_operating_multiple_kib_instances]
```yaml {applies_to}
  deployment:
    self: ga
    eck: ga
```

Use this configuration when each {{kib}} instance is reached through a different URL. If multiple instances serve the same URL (for example, behind a load balancer), use a single SAML realm and apply the same provider settings to every instance, as shown in [Configure {{kib}} for SAML authentication](#saml-configure-kibana).

When instances use different URLs and authenticate against the same {{es}} cluster, each instance requires its own SAML realm. Each realm must have its own unique Entity ID (`sp.entity_id`) and Assertion Consumer Service URL (`sp.acs`), but they can all use the same Identity Provider. In {{kib}}, configure each instance's SAML provider to point to its corresponding realm.

The following is an example of having 3 different {{kib}} instances, 2 of which use the same internal IdP, and another which uses a different IdP.

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

It is possible to have one or more {{kib}} instances that use SAML, while other instances use basic authentication against another realm type (for example, [Native](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md) or [LDAP](/deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md)).

### SAML without {{kib}} [saml-no-kibana]

If you're building a custom web application that needs to authenticate users against {{es}} using SAML (without {{kib}}), you can use the SAML REST APIs to implement the full authentication flow directly. This is relevant when you have a custom portal, a microservice-based architecture, or any scenario where the browser-based SSO flow must be handled by your own application code rather than by {{kib}}.

The application acts as an authentication proxy: it drives the SP-initiated or IdP-initiated SSO flow, exchanges the SAML response for an {{es}} access token and refresh token, and uses that token as a `Bearer` credential for subsequent requests.

For the complete implementation guide (including service account setup, SP-initiated and IdP-initiated flows, and logout handling), refer to [SAML without {{kib}}](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-without-kibana.md).
