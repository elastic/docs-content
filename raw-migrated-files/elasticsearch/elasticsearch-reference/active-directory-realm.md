# Active Directory user authentication [active-directory-realm]

You can configure {{stack}} {{security-features}} to communicate with Active Directory to authenticate users. See [Configuring an Active Directory realm](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#ad-realm-configuration).

The {{security-features}} use LDAP to communicate with Active Directory, so `active_directory` realms are similar to [`ldap` realms](../../../deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md). Like LDAP directories, Active Directory stores users and groups hierarchically. The directory’s hierarchy is built from containers such as the *organizational unit* (`ou`), *organization* (`o`), and *domain component* (`dc`).

The path to an entry is a *Distinguished Name* (DN) that uniquely identifies a user or group. User and group names typically have attributes such as a *common name* (`cn`) or *unique ID* (`uid`). A DN is specified as a string, for example `"cn=admin,dc=example,dc=com"` (white spaces are ignored).

The {{security-features}} supports only Active Directory security groups. You cannot map distribution groups to roles.

::::{note} 
When you use Active Directory for authentication, the username entered by the user is expected to match the `sAMAccountName` or `userPrincipalName`, not the common name.
::::


The Active Directory realm authenticates users using an LDAP bind request. After authenticating the user, the realm then searches to find the user’s entry in Active Directory. Once the user has been found, the Active Directory realm then retrieves the user’s group memberships from the `tokenGroups` attribute on the user’s entry in Active Directory.

## Configuring an Active Directory realm [ad-realm-configuration]

To integrate with Active Directory, you configure an `active_directory` realm and map Active Directory users and groups to roles in the role mapping file.

1. Add a realm configuration of type `active_directory` to `elasticsearch.yml` under the `xpack.security.authc.realms.active_directory` namespace. At a minimum, you must specify the Active Directory `domain_name` and `order`.

    See [Active Directory realm settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ad-settings) for all of the options you can set for an `active_directory` realm.

    ::::{note} 
    Binding to Active Directory fails if the domain name is not mapped in DNS. If DNS is not being provided by a Windows DNS server, add a mapping for the domain in the local `/etc/hosts` file.
    ::::


    For example, the following realm configuration configures {{es}} to connect to `ldaps://example.com:636` to authenticate users through Active Directory:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 0 <1>
                domain_name: ad.example.com
                url: ldaps://ad.example.com:636 <2>
    ```

    1. The realm order controls the order in which the configured realms are checked when authenticating a user.
    2. If you don’t specify the URL, it defaults to `ldap:<domain_name>:389`.


    ::::{important} 
    When you configure realms in `elasticsearch.yml`, only the realms you specify are used for authentication. If you also want to use the `native` or `file` realms, you must include them in the realm chain.
    ::::

2. If you are authenticating users across multiple domains in a forest, extra steps are required. There are a few minor differences in the configuration and the way that users authenticate.

    Set the `domain_name` setting to the forest root domain name.

    You must also set the `url` setting, since you must authenticate against the Global Catalog, which uses a different port and might not be running on every Domain Controller.

    For example, the following realm configuration configures {{es}} to connect to specific Domain Controllers on the Global Catalog port with the domain name set to the forest root:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 0
                domain_name: example.com <1>
                url: ldaps://dc1.ad.example.com:3269, ldaps://dc2.ad.example.com:3269 <2>
                load_balance:
                  type: "round_robin" <3>
    ```

    1. The `domain_name` is set to the name of the root domain in the forest.
    2. The `url` value used in this example has URLs for two different Domain Controllers, which are also Global Catalog servers. Port 3268 is the default port for unencrypted communication with the Global Catalog; port 3269 is the default port for SSL connections. The servers that are being connected to can be in any domain of the forest as long as they are also Global Catalog servers.
    3. A load balancing setting is provided to indicate the desired behavior when choosing the server to connect to.


    In this configuration, users will need to use either their full User Principal Name (UPN) or their Down-Level Logon Name. A UPN is typically a concatenation of the username with `@<DOMAIN_NAME` such as `johndoe@ad.example.com`. The Down-Level Logon Name is the NetBIOS domain name, followed by a `\` and the username, such as `AD\johndoe`. Use of Down-Level Logon Name requires a connection to the regular LDAP ports (389 or 636) in order to query the configuration container to retrieve the domain name from the NetBIOS name.

3. (Optional) Configure how {{es}} should interact with multiple Active Directory servers.

    The `load_balance.type` setting can be used at the realm level. Two modes of operation are supported: failover and load balancing. See [Active Directory realm settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ad-settings).

4. (Optional) To protect passwords, [encrypt communications between {{es}} and the Active Directory server](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#tls-active-directory).
5. Restart {{es}}.
6. (Optional) Configure a bind user.

    The Active Directory realm authenticates users using an LDAP bind request. By default, all of the LDAP operations are run by the user that {{es}} is authenticating. In some cases, regular users may not be able to access all of the necessary items within Active Directory and a *bind user* is needed. A bind user can be configured and is used to perform all operations other than the LDAP bind request, which is required to authenticate the credentials provided by the user.

    The use of a bind user enables the [run as feature](../../../deploy-manage/users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md) to be used with the Active Directory realm and the ability to maintain a set of pooled connections to Active Directory. These pooled connection reduce the number of resources that must be created and destroyed with every user authentication.

    The following example shows the configuration of a bind user through the user of the `bind_dn` and `secure_bind_password` settings:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 0
                domain_name: ad.example.com
                url: ldaps://ad.example.com:636
                bind_dn: es_svc_user@ad.example.com <1>
    ```

    1. This is the user that all Active Directory search requests are executed as. Without a bind user configured, all requests run as the user that is authenticating with {{es}}.


    The password for the `bind_dn` user should be configured by adding the appropriate `secure_bind_password` setting to the {{es}} keystore. For example, the following command adds the password for the example realm above:

    ```shell
    bin/elasticsearch-keystore add  \
    xpack.security.authc.realms.active_directory.my_ad.secure_bind_password
    ```

    When a bind user is configured, connection pooling is enabled by default. Connection pooling can be disabled using the `user_search.pool.enabled` setting.

7. Map Active Directory users and groups to roles.

    An integral part of a realm authentication process is to resolve the roles associated with the authenticated user. Roles define the privileges a user has in the cluster.

    Since with the `active_directory` realm the users are managed externally in the Active Directory server, the expectation is that their roles are managed there as well. In fact, Active Directory supports the notion of groups, which often represent user roles for different systems in the organization.

    The `active_directory` realm enables you to map Active Directory users to roles via their Active Directory groups or other metadata. This role mapping can be configured via the [role-mapping APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) or by using a file stored on each node. When a user authenticates against an Active Directory realm, the privileges for that user are the union of all privileges defined by the roles to which the user is mapped.

    Within a mapping definition, you specify groups using their distinguished names. For example, the following mapping configuration maps the Active Directory `admins` group to both the `monitoring` and `user` roles, maps the `users` group to the `user` role and maps the `John Doe` user to the `user` role.

    Configured via the role-mapping API:

    ```console
    PUT /_security/role_mapping/admins
    {
      "roles" : [ "monitoring" , "user" ],
      "rules" : { "field" : {
        "groups" : "cn=admins,dc=example,dc=com" <1>
      } },
      "enabled": true
    }
    ```

    1. The Active Directory distinguished name (DN) of the `admins` group.


    ```console
    PUT /_security/role_mapping/basic_users
    {
      "roles" : [ "user" ],
      "rules" : { "any": [
        { "field" : {
          "groups" : "cn=users,dc=example,dc=com" <1>
        } },
        { "field" : {
          "dn" : "cn=John Doe,cn=contractors,dc=example,dc=com" <2>
        } }
      ] },
      "enabled": true
    }
    ```

    1. The Active Directory distinguished name (DN) of the `users` group.
    2. The Active Directory distinguished name (DN) of the user `John Doe`.


    Or, alternatively, configured via the role-mapping file:

    ```yaml
    monitoring: <1>
      - "cn=admins,dc=example,dc=com" <2>
    user:
      - "cn=users,dc=example,dc=com" <3>
      - "cn=admins,dc=example,dc=com"
      - "cn=John Doe,cn=contractors,dc=example,dc=com" <4>
    ```

    1. The name of the role.
    2. The Active Directory distinguished name (DN) of the `admins` group.
    3. The Active Directory distinguished name (DN) of the `users` group.
    4. The Active Directory distinguished name (DN) of the user `John Doe`.


    For more information, see [Mapping users and groups to roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

8. (Optional) Configure the `metadata` setting in the Active Directory realm to include extra properties in the user’s metadata.

    By default, `ldap_dn` and `ldap_groups` are populated in the user’s metadata. For more information, see [User metadata in Active Directory realms](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#ad-user-metadata).



## User metadata in Active Directory realms [ad-user-metadata]

When a user is authenticated via an Active Directory realm, the following properties are populated in the user’s *metadata*:

|     |     |
| --- | --- |
| Field | Description |
| `ldap_dn` | The distinguished name of the user. |
| `ldap_groups` | The distinguished name of each of the groups that were                        resolved for the user (regardless of whether those                        groups were mapped to a role). |

This metadata is returned in the [authenticate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-authenticate) and can be used with [templated queries](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#templating-role-query) in roles.

Additional metadata can be extracted from the Active Directory server by configuring the `metadata` setting on the Active Directory realm.


## Load balancing and failover [ad-load-balancing]

The `load_balance.type` setting can be used at the realm level to configure how the {{security-features}} should interact with multiple Active Directory servers. Two modes of operation are supported: failover and load balancing.

See [Load balancing and failover](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#load-balancing).


## Encrypting communications between {{es}} and Active Directory [tls-active-directory]

To protect the user credentials that are sent for authentication, it’s highly recommended to encrypt communications between {{es}} and your Active Directory server. Connecting via SSL/TLS ensures that the identity of the Active Directory server is authenticated before {{es}} transmits the user credentials and the usernames and passwords are encrypted in transit.

Clients and nodes that connect via SSL/TLS to the Active Directory server need to have the Active Directory server’s certificate or the server’s root CA certificate installed in their keystore or truststore.

1. Create the realm configuration for the `xpack.security.authc.realms` namespace in the `elasticsearch.yml` file. See [Configuring an Active Directory realm](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#ad-realm-configuration).
2. Set the `url` attribute in the realm configuration to specify the LDAPS protocol and the secure port number. For example, `url: ldaps://ad.example.com:636`.
3. Configure each node to trust certificates signed by the certificate authority (CA) that signed your Active Directory server certificates.

    The following example demonstrates how to trust a CA certificate (`cacert.pem`), which is located within the configuration directory:

    ```shell
    xpack:
      security:
        authc:
          realms:
            active_directory:
              ad_realm:
                order: 0
                domain_name: ad.example.com
                url: ldaps://ad.example.com:636
                ssl:
                  certificate_authorities: [ "ES_PATH_CONF/cacert.pem" ]
    ```

    The CA cert must be a PEM encoded certificate.

    For more information about these settings, see [Active Directory realm settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ad-settings).

4. Restart {{es}}.

::::{note} 
By default, when you configure {{es}} to connect to Active Directory using SSL/TLS, it attempts to verify the hostname or IP address specified with the `url` attribute in the realm configuration with the values in the certificate. If the values in the certificate and realm configuration do not match, {{es}} does not allow a connection to the Active Directory server. This is done to protect against man-in-the-middle attacks. If necessary, you can disable this behavior by setting the `ssl.verification_mode` property to `certificate`.
::::



