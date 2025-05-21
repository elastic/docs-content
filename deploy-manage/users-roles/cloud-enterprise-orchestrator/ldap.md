---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-create-ldap-profiles.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# LDAP [ece-create-ldap-profiles]

If you use a Lightweight Directory Access Protocol (LDAP) server to authenticate users, you can specify the servers, parameters, and the search modes that {{ece}} uses to locate user credentials. To set up LDAP authentication, perform the following steps:

1. Specify the [general LDAP settings](#ece-ldap-general-settings).
2. Optional: Prepare the [trusted CA certificates](#ece-prepare-ldap-certificates).
3. Supply the [bind credentials](#ece-supply-ldap-bind-credentials).
4. Select the [search mode and group search](#ece-ldap-search-mode) settings.
5. Create [role mappings](#ece-ldap-role-mapping), either to all users that match the profile, or assign roles to specific groups.
6. Add any [custom configuration](#ece-ldap-custom-configuration) advanced settings to the YAML file.

## Add the general settings [ece-ldap-general-settings]

Begin the provider profile by adding the general settings:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Go to **Users** and then **Authentication providers**.
3. From the **Add provider** drop-down menu, select **LDAP**.
4. Provide a unique profile name. This name becomes the realm ID, with any spaces replaced by hyphens.

    The name can be changed, but the realm ID cannot. The realm ID becomes part of the [certificate bundle](#ece-prepare-ldap-certificates).

5. Add one or more LDAP server URLs and the port. You can use LDAP or LDAPS, but you can’t use a mix of types.

    Example: `ldaps://ldap.example.com:636`

6. Choose how you want your load balancing to work:

    Failover
    :   The LDAP URLs are used in the order they were entered. The first LDAP server that we can connect to gets used for all subsequent connections. If the connection to that server fails, the next available will be used for all subsequent connections.

    DNS failover
    :   The request is sent to a DNS hostname and the associated server IP addresses are searched in the order they are listed by the DNS Server. Each request starts at the beginning of the retrieved IP address list, regardless of previous failures.

    Round robin
    :   Connections continuously iterate  through the list of provided URLs until a connection can be made.

    DNS round robin
    :   The request is sent to a DNS hostname that is configured to with multiple IP addresses, rotating through until a connection is made.



## Prepare certificates (optional)[ece-prepare-ldap-certificates] 

You can add one or more certificate authorities (CAs) to validate the server certificate that the Domain Controller uses for SSL/TLS. Connecting through SSL/TLS ensures that the identity of the AD server is authenticated before {{ece}} transmits the user credentials and that the contents of the connection are encrypted.

1. Provide the URL to the ZIP file that contains a keystore with the CA certificate(s).

    The bundle should be a ZIP file containing a single `keystore.ks` file in the directory `/ldap/:id/truststore`, where `:id` is the value of the **Realm ID** field created in the [General settings](active-directory.md#ece-ad-general-settings). The keystore file can either be a JKS or a PKCS#12 keystore, but the name of the file should be `keystore.ks`.

2. Select a keystore type.
3. If the keystore is password protected, add the password to decrypt the keystore.


## Supply the bind credentials [ece-supply-ldap-bind-credentials] 

You can either select **Bind anonymously** for user searches or you must specify the distinguished name (DN) of the user to bind and the bind password. When **Bind anonymously** is selected, all requests to the LDAP server will be performed with the credentials of the authenticating user. In the case that `Bind DN` and `Bind Password` are provided, requests are performed on behalf of this bind user. This can be useful in cases where the regular users can’t access all of the necessary items within your LDAP server.

For user search templates, bind settings are not used even if configured.


## Configure the user search settings [ece-ldap-search-mode] 

The profile supports two modes of operation for searching users in the LDAP server, User search mode and Template mode.

To configure the user search:

1. Provide the **Base DN** as the base context where users are located in the LDAP server.
2. Set the **Search scope**:

    Sub-tree
    :   Searches all entries at all levels *under* the base DN, including the base DN itself.

    One level
    :   Searches for objects one level under the `Base DN` but not the `Base DN` or entries in lower levels.

    Base
    :   Searches only the entry defined as `Base DN`.

3. Optional: Specify an additional LDAP filter used to search the directory in attempts to match an entry with the username provided by the user. Defaults to `(uid={{0}})`. `{{0}}` is substituted with the username provided by the user for authentication.
4. Optional: Specify the attribute to examine on the user object in LDAP for group membership. If any Group Search settings are specified, this setting is ignored. Defaults to `memberOf`.

To configure the template search:

1. Select **Template**.
2. Provide one or more **User DN templates**. This DN template can contain a single `{{0}}` which will be replaced by the username the user enters for authentication. For example: `cn={{0}}, ou=users, o=marketing, dc=example, dc=com`


## Configure the group search settings [ece-ldap-search-groups] 

You can configure how {{ece}} searches for groups in the LDAP Server.

To configure the group search:

1. Provide the **Base DN** as the base context where groups are located in the LDAP server.
2. Set the **Search scope**:

    Sub-tree
    :   Searches all entries at all levels *under* the base DN, including the base DN itself.

    One level
    :   Searches for objects one level under the `Base DN` but not the `Base DN` or entries in lower levels.

    Base
    :   Searches only the entry defined as `Base DN`.



## Create role mappings [ece-ldap-role-mapping] 

When a user is authenticated, the role mapping assigns them roles in {{ece}}.

To assign all authenticated users a single role, select one of the **Default roles**.

To assign roles according to the **User DN** of the user or **Group DN** of the group they belong to, use the **Add role mapping rule** fields.

For a list of roles, refer to [Available roles and permissions](/deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md#ece-user-role-permissions).


## Custom configuration [ece-ldap-custom-configuration] 

You can add any additional settings to the **Advanced configuration** YAML file. For example, if you need to ignore the SSL check in a testing environment, you might add `ssl.verification_mode: none`. 

:::{note}
All entries added should omit the `xpack.security.authc.realms.ldap.$realm_id` prefix, as ECE will insert this itself and automatically account for any differences in format across {{es}} versions.
:::

::::{important} 
API keys created by LDAP users are not automatically deleted or disabled when the user is deleted or disabled in LDAP. When you delete a user in LDAP, make sure to also remove the user’s API key or delete the user in ECE.
::::


