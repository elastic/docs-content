---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-create-ad-profiles.html
---

# Active Directory [ece-create-ad-profiles]

If you use an Active Directory (AD) server to authenticate users, you can specify the servers, parameters, and the search modes that Elastic Cloud Enterprise uses to locate user credentials. There are several sections to the profile:

* Specify the [general AD settings](#ece-ad-general-settings).
* Optional: Prepare the [trusted CA certificates](#ece-prepare-ad-certificates).
* Supply the [bind credentials](#ece-supply-ad-bind-credentials).
* Select the [search mode and group search](#ece-ad-search-mode) settings.
* Create [role mappings](#ece-ad-role-mapping), either to all users that match the profile or assign roles to specific groups.
* Add any [custom configuration](#ece-ad-custom-configuration) advanced settings to the YAML file.

$$$ece-ad-general-settings$$$Begin the provider profile by adding the general settings:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Go to **Users** and then **Authentication providers**.
3. From the **Add provider** drop-down menu, select **Active Directory**.
4. Provide a unique profile name. This name becomes the realm ID, with any spaces replaced by hyphens.

    The name can be changed, but the realm ID cannot. The realm ID becomes part of the [certificate bundle](ldap.md#ece-prepare-ldap-certificates).

5. Add one or more LDAP URLs pointing to Active Directory domain controller servers. You can use LDAP or LDAPS, but you can’t use a mix of types.

    Example: `ldaps://ad.domain.com:636`

6. Choose how you want your load balancing to work:

    Failover
    :   The LDAP URLs are used in the order they were entered. The first server that we can connect to gets used for all subsequent connections. If the connection to that server fails, the next available will be used for all subsequent connections.

    DNS failover
    :   The request is sent to a DNS hostname and the associated server IP addresses are searched in the order they are listed by the DNS Server. Each request starts at the beginning of the retrieved IP address list, regardless of previous failures.

    Round robin
    :   Connections continuously iterate  through the list of provided URLs until a connection can be made.

    DNS round robin
    :   The request is sent to a DNS hostname that is configured to with multiple IP addresses, rotating through until a connection is made.

7. Provide the top-level domain name.


## Prepare certificates [ece-prepare-ad-certificates] 

Though optional, you can add one or more certificate authorities (CAs) to validate the server certificate that the Domain Controller uses for SSL/TLS. Connecting through SSL/TLS ensures that the identity of the AD server is authenticated before Elastic Cloud Enterprise transmits the user credentials and that the contents of the connection are encrypted.

1. Provide the URL to the ZIP file that contains a keystore with the CA certificate(s).

    The bundle should be a ZIP file containing a single `keystore.ks` file in the directory `/active_directory/:id/truststore`, where `:id` is the value of the **Realm ID** field created in the [General settings](#ece-ad-general-settings). The keystore file can either be a JKS or a PKCS#12 keystore, but the name of the file should be `keystore.ks`.

    ::::{important} 
    Don’t use the same URL to serve a new version of the ZIP file as otherwise the new version may not be picked up.
    ::::

2. Select a keystore type.
3. If the keystore is password protected, add the password to decrypt the keystore.


## Supply the bind credentials [ece-supply-ad-bind-credentials] 

You can either select **Bind anonymously** for user searches or you must specify the distinguished name (DN) of the user to bind and the bind password. When **Bind anonymously** is selected, all requests to Active Directory will be performed with the credentials of the authenticating user. In the case that `Bind DN` and `Bind Password` are provided, requests are performed on behalf of this bind user. This can be useful in cases where the regular users can’t access all of the necessary items within Active Directory.


## Configure the user search settings [ece-ad-search-mode] 

You can configure how Elastic Cloud Enterprise will search for users in the Active Directory

To configure the user search:

1. Provide the **Base DN** as the base context where users are located in the Active Directory.
2. Set the **Search scope**:

    Sub-tree
    :   Searches all entries at all levels *under* the base DN, including the base DN itself.

    One level
    :   Searches for objects one level under the `Base DN` but not the `Base DN` or entries in lower levels.

    Base
    :   Searches only the entry defined as `Base DN`.

3. Optional: Specify an additional LDAP filter, used to lookup a user given a username. The default filter looks up user objects in Active Directory where the username entered by the user matches `sAMAccountName` or `userPrincipalName` attributes.


## Configure the group search settings [ece-ad-search-groups] 

You can configure how Elastic Cloud Enterprise will search for groups in the Active Directory

To configure the group search:

1. Provide the **Base DN** as the base context where groups are located in the Active Directory.
2. Set the **Search scope**:

    Sub-tree
    :   Searches all entries at all levels *under* the base DN, including the base DN itself.

    One level
    :   Searches for objects one level under the `Base DN` but not the `Base DN` or entries in lower levels.

    Base
    :   Searches only the entry defined as `Base DN`.



## Create role mappings [ece-ad-role-mapping] 

When a user is authenticated, the role mapping assigns them roles in Elastic Cloud Enterprise.

To assign all authenticated users a single role, select one of the **Default roles**.

To assign roles according to the **User DN** of the user or **Group DN** of the group they belong to, use the **Add role mapping rule** fields.


## Custom configuration [ece-ad-custom-configuration] 

You can add any additional settings to the **Advanced configuration** YAML file. For example, if you need to ignore the SSL check for the SSL certificate of the Domain Controller in a testing environment, you might add `ssl.verification_mode: none`. Note that all keys should omit the `xpack.security.authc.realms.active_directory.$realm_id` prefix that is required in `elasticsearch.yml`, as ECE will insert this itself and automatically account for any differences in format across Elasticsearch versions.

::::{important} 
API keys created by Active Directory users are not automatically deleted or disabled when the user is deleted or disabled in Active Directory. When you delete a user in Active Directory, make sure to also remove the user’s API key or delete the user in ECE.
::::


