---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-authorization-delegation.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Authorization delegation [configuring-authorization-delegation]

In some cases, after the user has been authenticated by a realm, we may want to delegate user lookup and assignment of roles to another realm. Any realm that supports [user lookup](looking-up-users-without-authentication.md) (without needing the user’s credentials) can be used as an authorization realm.

For example, a user that is authenticated by the Kerberos or PKI realm can be looked up in the LDAP realm. The LDAP realm takes on responsibility for searching the user in LDAP and determining the role. In this case, the LDAP realm acts as an *authorization realm*.

## LDAP realm as an authorization realm [_ldap_realm_as_an_authorization_realm]

The following is an example configuration for the LDAP realm that can be used as an *authorization realm*. This LDAP realm is configured in user search mode with a specified filter.

For more information on configuring LDAP realms see [LDAP user authentication](ldap.md).

```yaml
xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 0
            authentication.enabled: true <1>
            user_search:
              base_dn: "dc=example,dc=org"
              filter: "(cn={0})"
            group_search:
              base_dn: "dc=example,dc=org"
            files:
              role_mapping: "ES_PATH_CONF/role_mapping.yml"
            unmapped_groups_as_roles: false
```

1. Here, we explicitly allow the LDAP realm to be used for authentication (that is, users can authenticate using their LDAP username and password). If we wanted this LDAP realm to be used for authorization only, then we would set this to `false`.

## Kerberos realm configured to delegate authorization [_kerberos_realm_configured_to_delegate_authorization]

The following is an example configuration where the Kerberos realm authenticates a user and then delegates authorization to the LDAP realm. The Kerberos realm authenticates the user and extracts user principal name (usually of format `user@REALM`). 

In this example, we enable the `remove_realm_name` setting to remove the `@REALM` part from the user principal name to get the username. This username is used to do a user lookup by the configured authorization realms (in this case the LDAP realm).

For more information on Kerberos realm see [Kerberos authentication](kerberos.md).

```yaml
xpack:
  security:
    authc:
      realms:
        kerberos:
          kerb1:
            order: 1
            keytab.path: "ES_PATH_CONF/es.keytab"
            remove_realm_name: true
            authorization_realms: ldap1
```


## PKI realm configured to delegate authorization [_pki_realm_configured_to_delegate_authorization]

is an example configuration where the PKI realm authenticates a user and then delegates authorization to the LDAP realm.

In this example, the username is the common name (CN) extracted from the DN of the client certificate. The LDAP realm uses this username to lookup user and assign the role.

For more information on PKI realms see [PKI user authentication](pki.md).

```yaml
xpack:
  security:
    authc:
      realms:
        pki:
          pki1:
            order: 2
            authorization_realms: ldap1
```
