---
navigation_title: SAML attribute mapping
description: Understand how SAML attributes map to Elasticsearch user properties and metadata, and how to configure attribute mappings in your SAML realm.
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Map SAML attributes to {{es}} user properties [saml-attributes-mapping]

This page is a detailed reference for SAML attribute mapping. For the complete SAML SSO configuration, refer to [SAML authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md).

When a user connects to {{kib}} through your Identity Provider, the Identity Provider supplies a SAML assertion about the user. The assertion contains an *Authentication Statement* indicating that the user has successfully authenticated to the IdP and one or more *Attribute Statements* that include *Attributes* for the user.

These attributes might include information like:

* The user's username
* The user's email address
* The user's groups or roles

Attributes in SAML are [usually](#saml-attribute-mapping-nameid) named using a URI such as `urn:oid:0.9.2342.19200300.100.1.1` or `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn`, and have one or more values associated with them.

These attribute identifiers vary between IdPs, and most IdPs offer ways to customize the URIs and their associated values.

{{es}} does not require specific attribute URIs, but the values configured in the SAML realm must exactly match the identifiers sent by the IdP.

{{es}} uses these attributes to infer information about the user who has logged in, and they can be used for [role mapping](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-role-mapping).

## How attributes appear in user metadata [saml-user-metadata]

By default, users who authenticate through SAML have some additional metadata fields.

* `saml_nameid` is set to the value of the `NameID` element in the SAML authentication response
* `saml_nameid_format` is set to the full URI of the NameID's `format` attribute
* Every SAML Attribute that is provided in the authentication response, regardless of whether it is mapped to an {{es}} user property, is added as the metadata field `saml(name)` where "name" is the full URI name of the attribute. For example, `saml(urn:oid:0.9.2342.19200300.100.1.3)`.
* For every SAML attribute that has a *friendlyName*, it is also added as the metadata field `saml_friendlyName` where "name" is the friendly name of the attribute. For example, `saml_mail`.

This behavior can be disabled by adding `populate_user_metadata: false` as a setting in the SAML realm.

## Map attributes

For SAML attributes to be useful in {{es}}, {{es}} and the IdP need to have a common value for the names of the attributes. This is done manually, by configuring the IdP and the SAML realm to use the same URI name for each logical user attribute.

The recommended steps for configuring these SAML attributes are as follows:

1. Consult your IdP to see what user attributes it can provide. This varies greatly between providers, but you should be able to obtain a list from the documentation, or from your local admin.
2. Review the list of [user properties](#saml-es-user-properties) that {{es}} supports, and decide which of them are useful to you, and can be provided by your IdP. At a *minimum*, you must configure a mapping for the required `principal` user property.
3. Configure your IdP to "release" those attributes to your {{kib}} SAML service provider. This process varies by provider: some will provide a user interface for this, while others might require that you edit configuration files.

   Because {{es}} does not require that any specific URIs are used, you can use any URIs as recommended by the IdP or your local administrator.
4. Configure the SAML realm in {{es}} to associate the [{{es}} user properties](#saml-es-user-properties) to the URIs that you configured in your IdP. Refer to [Create a SAML realm](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-create-realm) for a sample configuration with `principal` and `groups`.

## Special attribute names [saml-attribute-mapping-nameid]

In general, {{es}} expects that the configured value for an attribute is a URI, such as `urn:oid:0.9.2342.19200300.100.1.1`. However, there are some additional names that can be used:

`nameid`
:   This uses the SAML `NameID` value (all leading and trailing whitespace removed) instead of a SAML attribute. SAML `NameID` elements are an optional, but frequently provided, field within a SAML Assertion that the IdP can use to identify the Subject of that Assertion. Sometimes the `NameID` will relate to the user's login identifier (username) within the IdP, but often they will be internally generated identifiers that have no obvious meaning outside of the IdP.

`nameid:persistent`
:   This uses the SAML `NameID` value (all leading and trailing whitespace removed), but only if the NameID format is `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`. A SAML `NameID` element has an optional `Format` attribute that indicates the semantics of the provided name. It is common for IdPs to be configured with "transient" NameIDs that present a new identifier for each session. Because it is rarely useful to use a transient NameID as part of an attribute mapping, the `nameid:persistent` attribute name can be used as a safety mechanism that will cause an error if you attempt to map from a `NameID` that does not have a persistent value.

:::{note}
Identity Providers can be either statically configured to release a `NameID` with a specific format, or they can be configured to try to conform with the requirements of the SP. The SP declares its requirements as part of the Authentication Request, using an element which is called the `NameIDPolicy`. If this is needed, you can set the [`nameid_format`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings) setting in the SAML realm to request that the IdP releases a `NameID` with a specific format.
:::

*friendlyName*
:   A SAML attribute can have a *friendlyName* in addition to its URI based name. For example, the attribute with a name of `urn:oid:0.9.2342.19200300.100.1.1` might also have a friendlyName of `uid`. You can use these friendly names within an attribute mapping, but it is recommended that you use the URI based names, as friendlyNames are neither standardized nor mandatory.

The following example configures a realm to use a persistent NameID for the principal, and the attribute with the friendlyName `roles` for the user's groups.

```yaml
xpack.security.authc.realms.saml.saml1:
  order: 2
  idp.metadata.path: saml/idp-metadata.xml
  idp.entity_id: "https://sso.example.com/"
  sp.entity_id:  "https://kibana.example.com/"
  sp.acs: "https://kibana.example.com/api/security/saml/callback"
  attributes.principal: "nameid:persistent"
  attributes.groups: "roles"
  nameid_format: "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent"
```

## Mappable {{es}} user properties [saml-es-user-properties]

The {{es}} SAML realm can be configured to map SAML `attributes` to the following properties on the authenticated user:

`principal`
:   *(Required)* This is the *username* that will be applied to a user that authenticates against this realm. The `principal` appears in places such as the {{es}} audit logs.

`groups`
:   *(Recommended)* If you want to use your IdP's concept of groups or roles as the basis for a user's {{es}} privileges, you should map them with this attribute. The `groups` are passed directly to your [role mapping rules](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-role-mapping).

    :::{note}
    Some IdPs are configured to send the `groups` list as a single value, comma-separated string. To map this SAML attribute to the `attributes.groups` setting in the {{es}} realm, you can configure a string delimiter using the `attribute_delimiters.groups` setting.<br><br>For example, splitting the SAML attribute value `engineering,elasticsearch-admins,employees` on a delimiter value of `,` will result in `engineering`, `elasticsearch-admins`, and `employees` as the list of groups for the user.
    :::

`name`
:   *(Optional)* The user's full name. It will be used in {{kib}}'s profile page to display user details.

`mail`
:   *(Optional)* The user's email address. It will be used in {{kib}}'s profile page to display user details.

`dn`
:   *(Optional)* The user's X.500 *Distinguished Name*.

For the full list of `attributes.*` and related settings, including type and configuration details, refer to [SAML realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings).

## Extract partial values from SAML attributes [saml-attribute-patterns]

An IdP's attribute might contain more information than you want to use within {{es}}. A common example of this is one where the IdP works exclusively with email addresses, but you want the user's `principal` to use the `local-name` part of the email address. For example, if user's email address is `james.wong@staff.example.com`, then you might want their principal to be `james.wong`.

You can extract a partial value from an attribute using the `attribute_patterns` setting in the {{es}} realm, as demonstrated in the realm configuration below:

```yaml
xpack.security.authc.realms.saml.saml1:
  order: 2
  idp.metadata.path: saml/idp-metadata.xml
  idp.entity_id: "https://sso.example.com/"
  sp.entity_id:  "https://kibana.example.com/"
  sp.acs: "https://kibana.example.com/api/security/saml/callback"
  attributes.principal: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
  attribute_patterns.principal: "^([^@]+)@staff\\.example\\.com$"
```

In this example, the user's `principal` is mapped from an email attribute, but a regular expression is applied to the value before it is assigned to the user. If the regular expression matches, then the result of the first group is used as the effective value. If the regular expression does not match, then the attribute mapping fails.

Using this expression, the email address must belong to the `staff.example.com` domain, and then the local-part (anything before the `@`) is used as the principal. Any users who try to log in using a different email domain will fail because the regular expression will not match against their email address, so their principal attribute — which is mandatory — will not be populated.

::::{important}
Small mistakes in these regular expressions can have significant security consequences. For example, if we accidentally left off the trailing `$` from the preceding example, then we would match any email address where the domain starts with `staff.example.com`, and this would accept an email address such as `admin@staff.example.com.attacker.net`. It is important that you make sure your regular expressions are as precise as possible so that you don't open an avenue for user impersonation attacks.
::::
