# Mapping users and groups to roles [mapping-roles]

Role mapping is supported by all realms except `native` and `file`.

The native and file realms assign roles directly to users. Native realms use [user management APIs](../../../deploy-manage/users-roles/cluster-or-deployment-auth/native.md#managing-native-users). File realms use [File-based role management](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-file).

You can map roles through the [Role mapping API](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-api) (recommended) or a [Role mapping file](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file).

The PKI, LDAP, AD, Kerberos, OpenID Connect, JWT, and SAML realms support the [Role mapping API](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-api). Only PKI, LDAP, and AD realms support [Role mapping files](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file).

The PKI, LDAP, AD, Kerberos, OpenID Connect, JWT, and SAML realms also support [delegated authorization](../../../deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md#authorization_realms). You can either map roles for a realm or use delegated authorization; you cannot use both simultaneously.

To use role mapping, you create roles and role mapping rules. Role mapping rules can be based on realm name, realm type, username, groups, other user metadata, or combinations of those values.

::::{note} 
When [anonymous access](../../../deploy-manage/users-roles/cluster-or-deployment-auth/anonymous-access.md) is enabled, the roles of the anonymous user are assigned to all the other users as well.
::::


If there are role-mapping rules created through the API as well as a role mapping file, the rules are combined. It’s possible for a single user to have some roles that were mapped through the API, and others assigned based on the role mapping file. You can define role-mappings via an [API](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-api) or manage them through [files](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file). These two sources of role-mapping are combined inside of the {{es}} {security-features}, so it is possible for a single user to have some roles that have been mapped through the API, and other roles that are mapped through files.

::::{note} 
Users with no roles assigned will be unauthorized for any action. In other words, they may be able to authenticate, but they will have no roles. No roles means no privileges, and no privileges means no authorizations to make requests.
::::


When you use role mappings to assign roles to users, the roles must exist. There are two sources of roles. The available roles should either be added using the [role management APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api.html#security-role-apis) or defined in the [roles file](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-file). Either role-mapping method can use either role management method. For example, when you use the role mapping API, you are able to map users to both API-managed roles and file-managed roles (and likewise for file-based role-mappings).

## Using the role mapping API [mapping-roles-api]

You can define role-mappings through the [add role mapping API](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role-mapping.html).


## Using role mapping files [mapping-roles-file]

To use file based role-mappings, you must configure the mappings in a YAML file and copy it to each node in the cluster. Tools like Puppet or Chef can help with this.

By default, role mappings are stored in `ES_PATH_CONF/role_mapping.yml`, where `ES_PATH_CONF` is `ES_HOME/config` (zip/tar installations) or `/etc/elasticsearch` (package installations). To specify a different location, you configure the `files.role_mapping` setting in the [Active Directory](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ad-settings), [LDAP](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ldap-settings), and [PKI](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-pki-settings) realm settings in `elasticsearch.yml`.

Within the role mapping file, the security roles are keys and groups and users are values. The mappings can have a many-to-many relationship. When you map roles to groups, the roles of a user in that group are the combination of the roles assigned to that group and the roles assigned to that user.

By default, {{es}} checks role mapping files for changes every 5 seconds. You can change this default behavior by changing the `resource.reload.interval.high` setting in the `elasticsearch.yml` file. Since this is a common setting in Elasticsearch, changing its value might effect other schedules in the system.

While the *role mapping APIs* is the preferred way to manage role mappings, using the `role_mapping.yml` file becomes useful in a couple of use cases:

1. If you want to define fixed role mappings that no one (besides an administrator with physical access to the {{es}} nodes) would be able to change.
2. If cluster administration depends on users from external realms and these users need to have their roles mapped to them even when the cluster is RED. For instance an administrator that authenticates via LDAP or PKI and gets assigned an administrator role so that they can perform corrective actions.

Please note however, that the `role_mapping.yml` file is provided as a minimal administrative function and is not intended to cover and be used to define roles for all use cases.

::::{important} 
You cannot view, edit, or remove any roles that are defined in the role mapping files by using the role mapping APIs.
::::



## Realm specific details [_realm_specific_details]


#### Active Directory and LDAP realms [ldap-role-mapping] 

To specify users and groups in the role mappings, you use their *Distinguished Names* (DNs). A DN is a string that uniquely identifies the user or group, for example `"cn=John Doe,cn=contractors,dc=example,dc=com"`.

::::{note} 
The {{es}} {security-features} support only Active Directory security groups. You cannot map distribution groups to roles.
::::


For example, the following snippet uses the file-based method to map the `admins` group to the `monitoring` role and map the `John Doe` user, the `users` group, and the `admins` group to the `user` role.

```yaml
monitoring: <1>
  - "cn=admins,dc=example,dc=com" <2>
user:
  - "cn=John Doe,cn=contractors,dc=example,dc=com" <3>
  - "cn=users,dc=example,dc=com"
  - "cn=admins,dc=example,dc=com"
```

1. The name of a role.
2. The distinguished name of an LDAP group or an Active Directory security group.
3. The distinguished name of an LDAP or Active Directory user.


You can use the role-mapping API to define equivalent mappings as follows:

```console
PUT /_security/role_mapping/admins
{
  "roles" : [ "monitoring", "user" ],
  "rules" : { "field" : { "groups" : "cn=admins,dc=example,dc=com" } },
  "enabled": true
}
```

```console
PUT /_security/role_mapping/basic_users
{
  "roles" : [ "user" ],
  "rules" : { "any" : [
      { "field" : { "dn" : "cn=John Doe,cn=contractors,dc=example,dc=com" } },
      { "field" : { "groups" : "cn=users,dc=example,dc=com" } }
  ] },
  "enabled": true
}
```


#### PKI realms [pki-role-mapping] 

PKI realms support mapping users to roles, but you cannot map groups as the PKI realm has no notion of a group.

This is an example using a file-based mapping:

```yaml
monitoring:
  - "cn=Admin,ou=example,o=com"
user:
  - "cn=John Doe,ou=example,o=com"
```

The following example creates equivalent mappings using the API:

```console
PUT /_security/role_mapping/admin_user
{
  "roles" : [ "monitoring" ],
  "rules" : { "field" : { "dn" : "cn=Admin,ou=example,o=com" } },
  "enabled": true
}
```

```console
PUT /_security/role_mapping/basic_user
{
  "roles" : [ "user" ],
  "rules" : { "field" : { "dn" : "cn=John Doe,ou=example,o=com" } },
  "enabled": true
}
```


