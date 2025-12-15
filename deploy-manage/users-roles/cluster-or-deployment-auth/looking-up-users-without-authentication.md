---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/user-lookup.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Looking up users without authentication [user-lookup]

{{es}} [realms](authentication-realms.md) exist primarily to support [user authentication](user-authentication.md). Some realms authenticate users with a password (such as the [`native`](native.md) and [`ldap`](ldap.md) realms), and other realms use more complex authentication protocols (such as the [`saml`](saml.md) and [`oidc`](openid-connect.md) realms). In each case, the *primary* purpose of the realm is to establish the identity of the user who has made a request to the {{es}} API.

However, some {{es}} features need to *look up* a user without using their credentials.

* The [`run_as`](submitting-requests-on-behalf-of-other-users.md) feature executes requests on behalf of another user. An authenticated user with `run_as` privileges can perform requests on behalf of another unauthenticated user.
* The [delegated authorization](realm-chains.md#authorization_realms) feature links two realms together so that a user who authenticates against one realm can have the roles and metadata associated with a user from a different realm.

In each of these cases, a user must first authenticate to one realm and then {{es}} will query the second realm to find another user. The authenticated user credentials are used to authenticate in the first realm only, The user in the second realm is retrieved by username, without needing credentials.

When {{es}} resolves a user using their credentials (as performed in the first realm), it is known as *user authentication*.

When {{es}} resolves a user using the username only (as performed in the second realm), it is known as *user lookup*.

See the [run_as](submitting-requests-on-behalf-of-other-users.md) and [delegated authorization](realm-chains.md#authorization_realms) documentation to learn more about these features, including which realms and authentication methods support `run_as` or delegated authorization. In both cases, only the following realms can be used for the user lookup:

* The reserved, [`native`](native.md) and [`file`](file-based.md) realms always support user lookup.
* The [`ldap`](ldap.md) realm supports user lookup when the realm is configured in [*user search* mode](ldap.md#ldap-realm-configuration). User lookup is not support when the realm is configured with `user_dn_templates`.
* User lookup support in the [`active_directory`](active-directory.md) realm requires that the realm be configured with a [`bind_dn`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ad-settings) and a bind password.

The `pki`, `saml`, `oidc`, `kerberos` and `jwt` realms do not support user lookup.

::::{note}
If you want to use a realm only for user lookup and prevent users from authenticating against that realm, you can [configure the realm](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-realm-settings) and set `authentication.enabled` to `false`
::::


The user lookup feature is an internal capability that is used to implement the `run_as` and delegated authorization features - there are no APIs for user lookup. If you want to test your user lookup configuration, then you can do this with `run_as`. Use the [Authenticate](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-authenticate) API, authenticate as a `superuser` (e.g. the builtin `elastic` user) and specify the [`es-security-runas-user` request header](submitting-requests-on-behalf-of-other-users.md).

::::{note}
The [Get users](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-user) API and [User profiles](user-profiles.md) feature are alternative ways to retrieve information about a {{stack}} user. Those APIs are not related to the user lookup feature.
::::


