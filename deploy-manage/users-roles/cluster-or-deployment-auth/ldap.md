---
navigation_title: LDAP
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ldap-realm.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-clusters-ldap.html
applies_to:
  deployment:
    self:
    ece:
    eck:
products:
  - id: elasticsearch
  - id: cloud-enterprise
---

# LDAP user authentication [ldap-realm]

:::{{warning}}
This type of user authentication cannot be configured on {{ech}} deployments.
:::

You can configure the {{stack}} {{security-features}} to communicate with a Lightweight Directory Access Protocol (LDAP) server to authenticate users. See [Configuring an LDAP realm](../../../deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md#ldap-realm-configuration).

To integrate with LDAP, you configure an `ldap` realm and map LDAP groups to user roles.

:::{{tip}}
This topic describes implementing LDAP at the cluster or deployment level, for the purposes of authenticating with {{es}} and {{kib}}.

You can also configure an {{ece}} installation to use an LDAP server to authenticate users. [Learn more](/deploy-manage/users-roles/cloud-enterprise-orchestrator/ldap.md).
:::

## How it works

LDAP stores users and groups hierarchically, similar to the way folders are grouped in a file system. An LDAP directory’s hierarchy is built from containers such as the *organizational unit* (`ou`), *organization* (`o`), and *domain component* (`dc`).

The path to an entry is a *Distinguished Name* (DN) that uniquely identifies a user or group. User and group names typically have attributes such as a *common name* (`cn`) or *unique ID* (`uid`). A DN is specified as a string, for example  `"cn=admin,dc=example,dc=com"` (white spaces are ignored).

The `ldap` realm supports two modes of operation, a user search mode and a mode with specific templates for user DNs.

::::{important}
When you configure realms in [`elasticsearch.yml`](/deploy-manage/stack-settings.md), only the realms you specify are used for authentication. If you also want to use the `native` or `file` realms, you must include them in the realm chain.
::::

## Step 1: Add a new realm configuration [ldap-realm-configuration]

The `ldap` realm supports two modes of operation, a user search mode and a mode with specific templates for user DNs:

* **LDAP user search**: The most common mode of operation. In this mode, a specific user with permission to search the LDAP directory is used to search for the DN of the authenticating user based on the provided username and an LDAP attribute. Once found, the user is authenticated by attempting to bind to the LDAP server using the found DN and the provided password.

* **DN templates**:  If your LDAP environment uses a few specific standard naming conditions for users, you can use user DN templates to configure the realm. The advantage of this method is that a search does not have to be performed to find the user DN. However, multiple bind operations might be needed to find the correct user DN.


### Set up LDAP user search mode

To configure an `ldap` realm with user search:

1. Add a realm configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) under the `xpack.security.authc.realms.ldap` namespace.

   At a minimum, you must specify the `url` and `order` of the LDAP server, and set `user_search.base_dn` to the container DN where the users are searched for. See [LDAP realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings) for all of the options you can set for an `ldap` realm.

    For example, the following snippet shows an LDAP realm configured with a user search:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            ldap:
              ldap1:
                order: 2 <1>
                url: "ldap://ldap.example.com:389" <2>
                bind_dn: "cn=ldapuser, ou=users, o=services, dc=example, dc=com" <3>
                user_search:
                  base_dn: "ou=users, o=services, dc=example, dc=com" <4>
                  filter: "(cn=\{0})" <5>
                group_search:
                  base_dn: "ou=groups, o=services, dc=example, dc=com" <6>
    ```

    1. The order in which the LDAP realm will be consulted during an authentication attempt.
    2. The LDAP URL pointing to the LDAP server that should handle authentication.
    3. The DN of the bind user.
    4. The base DN under which your users are located in LDAP.
    5. Optionally specify an additional LDAP filter used to search the directory in attempts to match an entry with the username provided by the user. Defaults to `(uid={{0}})`. `{{0}}` is substituted with the username provided by the user for authentication.
    6. The base DN under which groups are located in LDAP.

    ::::{warning}
    In {{ece}}, you must apply the user settings to each [deployment template](/deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md).
    ::::

2. Configure the password for the `bind_dn` user by adding the `xpack.security.authc.realms.ldap.<ldap1>.secure_bind_password` setting [to the {{es}} keystore](/deploy-manage/security/secure-settings.md).

  :::{warning}
  In {{ech}} and {{ece}}, after you configure `secure_bind_password`, any attempt to restart the deployment will fail until you complete the rest of the configuration steps. If you want to rollback the Active Directory realm configurations, you need to remove the `xpack.security.authc.realms.ldap.<ldap1>.secure_bind_password` that was just added.
  :::

1. (Optional) Configure how the {{security-features}} interact with multiple LDAP servers.

    The `load_balance.type` setting can be used at the realm level. The {{es}} {{security-features}} support both failover and load balancing modes of operation. See [LDAP realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings).

2. (Optional) To protect passwords, [encrypt communications between {{es}} and the LDAP server](../../../deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md#tls-ldap).

    * **For self-managed clusters and {{eck}} deployments**, clients and nodes that connect using SSL/TLS to the Active Directory server need to have the Active Directory server’s certificate or the server’s root CA certificate installed in their keystore or trust store.

    * **For {{ece}} and {{ech}} deployments**, if your Domain Controller is configured to use LDAP over TLS and it uses a self-signed certificate or a certificate that is signed by your organization’s CA, you need to enable the deployment to trust this certificate.
3. Restart {{es}}.

### Set up LDAP with user DN templates

To configure an `ldap` realm with user DN templates:

1. Add a realm configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) in the `xpack.security.authc.realms.ldap` namespace. At a minimum, you must specify the `url` and `order` of the LDAP server, and specify at least one template with the `user_dn_templates` option. See [LDAP realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings) for all of the options you can set for an `ldap` realm.

    For example, the following snippet shows an LDAP realm configured with user DN templates:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            ldap:
              ldap1:
                order: 2 <1>
                url: "ldap://ldap.example.com:389" <2>
                user_dn_templates: <3>
                  - "uid={0}, ou=users, o=engineering, dc=example, dc=com"
                  - "uid={0}, ou=users, o=marketing, dc=example, dc=com"
                group_search:
                  base_dn: ou=groups, o=services, dc=example, dc=com" <4>
    ```

    1. The order in which the LDAP realm will be consulted during an authentication attempt.
    2. The LDAP URL pointing to the LDAP server that should handle authentication.
    3. The templates that should be tried for constructing the user DN and authenticating to LDAP. If a user attempts to authenticate with username `user1` and password `password1`, authentication will be attempted with the DN `uid=user1, ou=users, o=engineering, dc=example, dc=com` and if not successful, also with `uid=user1, ou=users, o=marketing, dc=example, dc=com` and the given password. If authentication with one of the constructed DNs is successful, all subsequent LDAP operations are run with this user.
    4. The base DN under which groups are located in LDAP.

    The `bind_dn` setting is not used in template mode. All LDAP operations run as the authenticating user.

    ::::{warning}
    In {{ece}}, you must apply the user settings to each [deployment template](../../../deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md).
    ::::

2. (Optional) Configure how the {{security-features}} interact with multiple LDAP servers.

    The `load_balance.type` setting can be used at the realm level. The {{es}} {{security-features}} support both failover and load balancing modes of operation. See [LDAP realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings).

3. (Optional) To protect passwords, [encrypt communications between {{es}} and the LDAP server](../../../deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md#tls-ldap).

    * **For self-managed clusters and {{eck}} deployments**, clients and nodes that connect using SSL/TLS to the Active Directory server need to have the Active Directory server’s certificate or the server’s root CA certificate installed in their keystore or trust store.

    * **For {{ece}} and {{ech}} deployments**, if your Domain Controller is configured to use LDAP over TLS and it uses a self-signed certificate or a certificate that is signed by your organization’s CA, you need to enable the deployment to trust this certificate.
4. Restart {{es}}.

## Step 2: Map LDAP groups to roles [mapping-roles-ldap]

An integral part of a realm authentication process is to resolve the roles associated with the authenticated user. Roles define the privileges a user has in the cluster.

Because users are managed externally in the LDAP server, the expectation is that their roles are managed there as well. LDAP groups often represent user roles for different systems in the organization.

The `active_directory` realm enables you to map Active Directory users to roles using their Active Directory groups or other metadata.

You can map LDAP groups to roles in the following ways:

* Using the role mappings page in {{kib}}.
* Using the [role mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping).
* Using a role mapping file.

For more information, see [Mapping users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

::::{note}
The LDAP realm supports [authorization realms](../../../deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md#authorization_realms) as an alternative to role mapping.
::::

### Example: using the role mapping API

```console
POST /_security/role_mapping/ldap-superuser <1>
{
  "enabled": true,
  "roles": [ "superuser" ], <2>
  "rules": {
    "all" : [
      { "field": { "realm.name": "ldap1" } },<3>
      { "field": { "groups": "cn=administrators, ou=groups, o=services, dc=example, dc=com" } }<4>
    ]
  },
  "metadata": { "version": 1 }
}
```

1. The name of the role mapping.
2. The name of the role we want to assign, in this case `superuser`.
3. The name of our LDAP realm.
4. The DN of the LDAP group whose members should get the `superuser` role in the deployment.


### Example: Using a role mapping file

:::{tip}
If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced. If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret). If you're using a self-managed cluster, then the file must be present on each node.
:::

```yaml
monitoring: <1>
  - "cn=admins,dc=example,dc=com" <2>S
user:
  - "cn=users,dc=example,dc=com" <3>
  - "cn=admins,dc=example,dc=com"
```

1. The name of the mapped role.
2. The LDAP distinguished name (DN) of the `admins` group.
3. The LDAP distinguished name (DN) of the `users` group.

Referencing the file in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 2
            url: "ldaps://ldap.example.com:636"
            bind_dn: "cn=ldapuser, ou=users, o=services, dc=example, dc=com"
            user_search:
              base_dn: "ou=users, o=services, dc=example, dc=com"
            group_search:
              base_dn: ou=groups, o=services, dc=example, dc=com"
            ssl:
              verification_mode: certificate
              certificate_authorities: ["/app/config/cacerts/ca.crt"]
            files:
              role_mapping: "/app/config/mappings/role-mappings.yml"
```

## User metadata in LDAP realms [ldap-user-metadata]

When a user is authenticated via an LDAP realm, the following properties are populated in the user’s metadata:

| Field | Description |
| --- | --- |
| `ldap_dn` | The distinguished name of the user. |
| `ldap_groups` | The distinguished name of each of the groups that were                        resolved for the user (regardless of whether those                        groups were mapped to a role). |

This metadata is returned in the [authenticate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-authenticate), and can be used with [templated queries](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#templating-role-query) in roles.

Additional fields can be included in the user's metadata by configuring the `metadata` setting on the LDAP realm. This metadata is available for use with the [role mapping API](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-api) or in [templated role queries](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#templating-role-query).

The example below includes the user’s common name (`cn`) as an additional field in their metadata.

```yaml
xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 0
            metadata: cn
```


## Load balancing and failover [ldap-load-balancing]

The `load_balance.type` setting can be used at the realm level to configure how the {{security-features}} should interact with multiple LDAP servers. The {{security-features}} support both failover and load balancing modes of operation.

See [Load balancing and failover](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#load-balancing).


## Encrypting communications between {{es}} and LDAP [tls-ldap]

To protect the user credentials that are sent for authentication in an LDAP realm, it’s highly recommended to encrypt communications between {{es}} and your LDAP server. Connecting using SSL/TLS ensures that the identity of the LDAP server is authenticated before {{es}} transmits the user credentials and the contents of the connection are encrypted. Clients and nodes that connect using TLS to the LDAP server need to have the LDAP server’s certificate or the server’s root CA certificate installed in their keystore or trust store.

If you're using {{ech}} or {{ece}}, then you must [upload your certificate as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.

If you're using {{eck}}, then install the certificate as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

:::{tip}

If you're using {{ece}} or {{ech}}, then these steps are required only if TLS is enabled and the Active Directory controller is using self-signed certificates.
:::

::::{admonition} Certificate formats
The following example uses a PEM encoded certificate. If your CA certificate is available as a `JKS` or `PKCS#12` keystore, you can reference it in the user settings. For example:

```yaml
xpack.security.authc.realms.ldap.ldap1.ssl.truststore.path:
"/app/config/truststore/ca.p12"
```

If the keystore is also password protected (which isn’t typical for keystores that only contain CA certificates), you can also provide the password for the keystore by adding `xpack.security.authc.realms.active_directory.ldap.ldap1.truststore.password: password` in the user settings.
::::

The following example demonstrates how to trust a CA certificate (`cacert.pem`), which is located within the configuration directory.

```shell
xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 0
            url: "ldaps://ldap.example.com:636"
            ssl:
              certificate_authorities: [ "cacert.pem" ]
```

You can also specify the individual server certificates rather than the CA certificate, but this is only recommended if you have a single LDAP server or the certificates are self-signed

For more information about these settings, see [LDAP realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings).

::::{note}
By default, when you configure {{es}} to connect to an LDAP server using SSL/TLS, it attempts to verify the hostname or IP address specified with the `url` attribute in the realm configuration with the values in the certificate. If the values in the certificate and realm configuration do not match, {{es}} does not allow a connection to the LDAP server. This is done to protect against man-in-the-middle attacks. If necessary, you can disable this behavior by setting the `ssl.verification_mode` property to `certificate`.
::::

### Using {{kib}} with LDAP [ldap-realm-kibana]

The LDAP security realm uses the {{kib}}-provided [basic authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#basic-authentication) login form. Basic authentication is enabled by default.

You can also use LDAP with [token authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#token-authentication) in {{kib}}.
