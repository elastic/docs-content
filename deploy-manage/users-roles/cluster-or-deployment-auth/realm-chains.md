---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/realm-chains.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Realm chains [realm-chains]

[Realms](authentication-realms.md) live within a *realm chain*. It is essentially a prioritized list of configured realms typically of various types. Realms are consulted in ascending order: the realm with the lowest `order` value is consulted first.

You must make sure each configured realm has a distinct `order` setting. In the event that two or more realms have the same `order`, the node will fail to start.

During the authentication process, {{es}} consults and tries to authenticate the request one realm at a time. Once one of the realms successfully authenticates the request, the authentication is considered to be successful. The authenticated user is associated with the request, which then proceeds to the authorization phase. If a realm can't authenticate the request, the next realm in the chain is consulted. If none of the realms in the chain can authenticate the request, the authentication is considered to be unsuccessful and an authentication error is returned (as HTTP status code `401`).

::::{note}
Some systems, such as Active Directory, have a temporary lock-out period after several successive failed login attempts. If the same username exists in multiple realms, unintentional account lockouts are possible. For more information, see [Users are frequently locked out of Active Directory](/troubleshoot/elasticsearch/security/trouble-shoot-active-directory.md).
::::

## Configure a realm chain

The default realm chain contains the `file` and `native` realms. To explicitly configure a realm chain, specify the chain in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file.

If your realm chain does not contain `file` or `native` realm or does not disable them explicitly, `file` and `native` realms will be added automatically to the beginning of the realm chain in that order. To opt out from this automatic behavior, you can explicitly configure the `file` and `native` realms with the `order` and `enabled` settings.

Each realm has a unique name that identifies it. Each type of realm dictates its own set of required and optional settings. There are also settings that are common to all realms. To explore these settings, refer to [Realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#realm-settings).

The following snippet configures a realm chain that enables the `file` realm, two LDAP realms, and an Active Directory realm, and disables the `native` realm.

```yaml
xpack.security.authc.realms:
  file.file1:
      order: 0

  ldap.ldap1:
      order: 1
      enabled: false
      url: 'url_to_ldap1'
      ...

  ldap.ldap2:
      order: 2
      url: 'url_to_ldap2'
      ...

  active_directory.ad1:
      order: 3
      url: 'url_to_ad'

  native.native1:
      enabled: false
```

## Delegating authorization to another realm [authorization_realms]

Some realms have the ability to perform authentication internally, but delegate the lookup and assignment of roles (authorization) to another realm.

For example, you might want to use a PKI realm to authenticate your users with TLS client certificates, then look up that user in an LDAP realm and use their LDAP group assignments to determine their roles in {{es}}.

Any realm that supports retrieving users without needing their credentials can be used as an authorization realm. Refer to [Looking up users without authentication](looking-up-users-without-authentication.md) to learn which realms can be used as authorization realms.

For realms that support this feature, it can be enabled by configuring the `authorization_realms` setting on the authenticating realm. Check the list of [supported settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#realm-settings) for each realm to see if they support the `authorization_realms` setting.

If delegated authorization is enabled for a realm, it authenticates the user in its standard manner, including relevant caching, then looks for that user in the configured list of authorization realms. It tries each realm in the order they are specified in the `authorization_realms` setting. The user is retrieved by principal - the user must have identical usernames in the authentication and authorization realms. If the user can't be found in any of the authorization realms, then authentication fails.

See [Configuring authorization delegation](authorization-delegation.md) for more details.

::::{note}
Delegated authorization requires that you have a [subscription](https://www.elastic.co/subscriptions) that includes custom authentication and authorization realms.
::::



