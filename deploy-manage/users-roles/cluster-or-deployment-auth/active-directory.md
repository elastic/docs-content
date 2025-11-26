---
navigation_title: Active Directory
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/active-directory-realm.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-clusters-ad.html
applies_to:
  deployment:
    self:
    ece:
    eck:
products:
  - id: elasticsearch
  - id: cloud-enterprise
---

# Active Directory user authentication [active-directory-realm]

:::{{warning}}
This type of user authentication cannot be configured on {{ech}} deployments.
:::


You can configure {{stack}} {{security-features}} to communicate with Active Directory to authenticate users.

:::{{tip}}
This topic describes implementing Active Directory at the cluster or deployment level, for the purposes of authenticating with {{es}} and {{kib}}.

You can also configure an {{ece}} installation to use an Active Directory to authenticate users. [Learn more](/deploy-manage/users-roles/cloud-enterprise-orchestrator/active-directory.md).
:::

## How it works

The {{security-features}} use LDAP to communicate with Active Directory, so `active_directory` realms are similar to [`ldap` realms](/deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md). Like LDAP directories, Active Directory stores users and groups hierarchically. The directory’s hierarchy is built from containers such as the *organizational unit* (`ou`), *organization* (`o`), and *domain component* (`dc`).

The path to an entry is a *Distinguished Name* (DN) that uniquely identifies a user or group. User and group names typically have attributes such as a *common name* (`cn`) or *unique ID* (`uid`). A DN is specified as a string, for example `"cn=admin,dc=example,dc=com"` (white spaces are ignored).

The {{security-features}} supports only Active Directory security groups. You can't map distribution groups to roles.

::::{note}
When you use Active Directory for authentication, the username entered by the user is expected to match the `sAMAccountName` or `userPrincipalName`, not the common name.
::::

The Active Directory realm authenticates users using an LDAP bind request. After authenticating the user, the realm then searches to find the user’s entry in Active Directory. After the user has been found, the Active Directory realm then retrieves the user’s group memberships from the `tokenGroups` attribute on the user’s entry in Active Directory.

To integrate with Active Directory, you configure an `active_directory` realm and map Active Directory groups to user roles in {{es}}.

:::{tip}
If your Active Directory domain supports authentication with user-provided credentials, then you don't need to configure a `bind_dn`. [Learn more](#ece-ad-configuration-with-bind-user).
:::

## Step 1: Add a new realm configuration [ad-realm-configuration]

1. Add a realm configuration of type `active_directory` to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) under the `xpack.security.authc.realms.active_directory` namespace. At a minimum, you must specify the Active Directory `domain_name` and `order`.

    See [Active Directory realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ad-settings) for all of the options you can set for an `active_directory` realm.

    :::{note}
    Binding to Active Directory fails if the domain name is not mapped in DNS.

    In a self-managed cluster, if DNS is not being provided by a Windows DNS server, you can add a mapping for the domain in the local `/etc/hosts` file.
    :::

  ::::{tab-set}

  :::{tab-item} Single domain
  The following realm configuration configures {{es}} to connect to `ldaps://example.com:636` to authenticate users through Active Directory:

  ```yaml
  xpack:
    security:
      authc:
        realms:
          active_directory:
            my_ad:
              order: 0 <1>
              domain_name: ad.example.com <2>
              url: ldaps://ad.example.com:636 <3>
  ```

  1. The order in which the `active_directory` realm is consulted during an authentication attempt.
  2. The primary domain in Active Directory. Binding to Active Directory fails if the domain name is not mapped in DNS.
  3. The LDAP URL pointing to the Active Directory Domain Controller that should handle authentication. If you don’t specify the URL, it defaults to `ldap:<domain_name>:389`.

  :::

  :::{tab-item} Forest
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
  2. The URLs for two different Domain Controllers, which are also Global Catalog servers. Port 3268 is the default port for unencrypted communication with the Global Catalog. Port 3269 is the default port for SSL connections. The servers that are being connected to can be in any domain of the forest as long as they are also Global Catalog servers.
  3. A load balancing setting is provided to indicate the desired behavior when choosing the server to connect to.


  In this configuration, users will need to use either their full User Principal Name (UPN) or their down-level logon name:
  * A UPN is typically a concatenation of the username with `@<DOMAIN_NAME` such as `johndoe@ad.example.com`.
  * The down-level logon name is the NetBIOS domain name, followed by a `\` and the username, such as `AD\johndoe`.

    Use of down-level logon name requires a connection to the regular LDAP ports (389 or 636) in order to query the configuration container to retrieve the domain name from the NetBIOS name.
  :::

  ::::

  ::::{important}
  When you configure realms in `elasticsearch.yml`, only the realms you specify are used for authentication. If you also want to use the `native` or `file` realms, you must include them in the realm chain.
  ::::

1. (Optional) Configure how {{es}} should interact with multiple Active Directory servers.

    The `load_balance.type` setting can be used at the realm level. Two modes of operation are supported: failover and load balancing. See [Active Directory realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ad-settings).

2. (Optional) To protect passwords, [encrypt communications](/deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#tls-active-directory) between {{es}} and the Active Directory server.

    * **For self-managed clusters and {{eck}} deployments**, clients and nodes that connect using SSL/TLS to the Active Directory server need to have the Active Directory server’s certificate or the server’s root CA certificate installed in their keystore or trust store.

    * **For {{ece}} and {{ech}} deployments**, if your Domain Controller is configured to use LDAP over TLS and it uses a self-signed certificate or a certificate that is signed by your organization’s CA, you need to enable the deployment to trust this certificate.

3. Restart {{es}}.

## Step 2: Configure a bind user (Optional) [ece-ad-configuration-with-bind-user]

You can choose to configure an Active Directory realm using a bind user.

The Active Directory realm authenticates users using an LDAP bind request. By default, all of the LDAP operations are run by the user that {{es}} is authenticating. In some cases, regular users may not be able to access all of the necessary items within Active Directory and a bind user is needed. A bind user can be configured and is used to perform all operations other than the LDAP bind request, which is required to authenticate the credentials provided by the user.

When you specify a `bind_dn`, this specific user is used to search for the Distinguished Name (`DN`) of the authenticating user based on the provided username and an LDAP attribute. If found, this user is authenticated by attempting to bind to the LDAP server using the found `DN` and the provided password.

The use of a bind user enables the [run as feature](/deploy-manage/users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md) to be used with the Active Directory realm.

In self-managed clusters, use of a bind user also enables the ability to maintain a set of pooled connections to Active Directory. These pooled connections reduce the number of resources that must be created and destroyed with every user authentication.

To configure a bind user:

1. [Add your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `active_directory` realm as follows:

    ::::{important}
    In {{ece}}, you must apply the user settings to each [deployment template](/deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md).
    ::::

    ```yaml
    xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 2
                domain_name: ad.example.com
                url: ldap://ad.example.com:389
                bind_dn: es_svc_user@ad.example.com <1>
    ```

    1. The user to run as for all Active Directory search requests.

1. Configure the password for the `bind_dn` user by adding the appropriate `xpack.security.authc.realms.active_directory.<my_ad>.secure_bind_password` setting [to the {{es}} keystore](/deploy-manage/security/secure-settings.md).

   In self-managed deployments, when a bind user is configured, connection pooling is enabled by default. Connection pooling can be disabled using the `user_search.pool.enabled` setting.

   :::{warning}
   In {{ech}} and {{ece}}, after you configure `secure_bind_password`, any attempt to restart the deployment will fail until you complete the rest of the configuration steps. If you want to rollback the Active Directory realm configurations, you need to remove the `xpack.security.authc.realms.active_directory.<my_ad>.secure_bind_password` that was just added.
   :::

## Step 3: Map Active Directory users and groups to roles

An integral part of a realm authentication process is to resolve the roles associated with the authenticated user. Roles define the privileges a user has in the cluster.

Because users are managed externally in the Active Directory server, the expectation is that their roles are managed there as well. Active Directory groups often represent user roles for different systems in the organization.

The `active_directory` realm enables you to map Active Directory users to roles using their Active Directory groups or other metadata.

You can map Active Directory groups to roles for your users in the following ways:

* Using the role mappings page in {{kib}}.
* Using the [role mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping).
* Using a role mapping file.

For more information, see [Mapping users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

::::{important}
Only Active Directory security groups are supported. You can't map distribution groups to roles.
::::

### Example: using the role mapping API

```console
POST /_security/role_mapping/ldap-superuser
{
"enabled": true,
"roles": [ "superuser" ], <1>
"rules": {
"all" : [
{ "field": { "realm.name": "my_ad" } }, <2>
{ "field": { "groups": "cn=administrators, dc=example, dc=com" } } <3>
    ]
},
"metadata": { "version": 1 }
}
```

1. The name of the role we want to assign, in this case `superuser`.
2. The name of our active_directory realm.
3. The Distinguished Name of the Active Directory group whose members should get the `superuser` role in the deployment.

### Example: Using a role mapping file [ece_using_the_role_mapping_files_2]

:::{tip}
If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.

If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

If you're using a self-managed cluster, then the file must be present on each node.
:::

```sh
superuser:
- cn=Senior Manager, cn=management, dc=example, dc=com
- cn=Senior Admin, cn=management, dc=example, dc=com
```

Referencing the file in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack:
  security:
    authc:
      realms:
        active_directory:
          my_ad:
            order: 2
            domain_name: ad.example.com
            url: ldaps://ad.example.com:636
            bind_dn: es_svc_user@ad.example.com
            ssl:
              certificate_authorities: ["/app/config/cacerts/ca.crt"]
              verification_mode: certificate
            files:
              role_mapping: "/app/config/mappings/role-mappings.yml"
```

## User metadata in Active Directory realms [ad-user-metadata]

When a user is authenticated using an Active Directory realm, the following properties are populated in the user’s metadata:

| Field | Description |
| --- | --- |
| `ldap_dn` | The distinguished name of the user. |
| `ldap_groups` | The distinguished name of each of the groups that were                        resolved for the user (regardless of whether those                        groups were mapped to a role). |

This metadata is returned in the [authenticate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-authenticate) and can be used with [templated queries](../../../deploy-manage/users-roles/controlling-access-at-document-field-level.md#templating-role-query) in roles.

Additional metadata can be extracted from the Active Directory server by configuring the `metadata` setting on the Active Directory realm.


## Load balancing and failover [ad-load-balancing]

The `load_balance.type` setting can be used at the realm level to configure how the {{security-features}} should interact with multiple Active Directory servers. Two modes of operation are supported: failover and load balancing.

See [Load balancing and failover](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#load-balancing).


## Encrypting communications between {{es}} and Active Directory [tls-active-directory]

$$$ece-ad-configuration-encrypt-communications$$$

To protect the user credentials that are sent for authentication, you should encrypt communications between {{es}} and your Active Directory server. Connecting using SSL/TLS ensures that the identity of the Active Directory server is authenticated before {{es}} transmits the user credentials and the usernames and passwords are encrypted in transit.

Clients and nodes that connect using SSL/TLS to the Active Directory server need to have the Active Directory server’s certificate or the server’s root CA certificate installed in their keystore or trust store.

If you're using {{ech}} or {{ece}}, then you must [upload your certificate as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.

If you're using {{eck}}, then install the certificate as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

:::{tip}

If you're using {{ece}} or {{ech}}, then these steps are required only if TLS is enabled and the Active Directory controller is using self-signed certificates.
:::

::::{admonition} Certificate formats
The following example uses a PEM encoded certificate. If your CA certificate is available as a `JKS` or `PKCS#12` keystore, you can reference it in the user settings. For example:

```yaml
xpack.security.authc.realms.active_directory.my_ad.ssl.truststore.path:
"/app/config/truststore/ca.p12"
```

If the keystore is also password protected (which isn’t typical for keystores that only contain CA certificates), you can also provide the password for the keystore by adding `xpack.security.authc.realms.active_directory.my_ad.ssl.truststore.password: password` in the user settings.

::::

The following example demonstrates how to trust a CA certificate (`cacert.pem`), which is located within the configuration directory.

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

For more information about these settings, see [Active Directory realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ad-settings).

::::{note}
By default, when you configure {{es}} to connect to Active Directory using SSL/TLS, it attempts to verify the hostname or IP address specified with the `url` attribute in the realm configuration with the values in the certificate. If the values in the certificate and realm configuration do not match, {{es}} does not allow a connection to the Active Directory server. This is done to protect against man-in-the-middle attacks. If necessary, you can disable this behavior by setting the `ssl.verification_mode` property to `certificate`.
::::

### Using {{kib}} with Active Directory [ad-realm-kibana]

The Active Directory security realm uses the {{kib}}-provided [basic authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#basic-authentication) login form. Basic authentication is enabled by default.