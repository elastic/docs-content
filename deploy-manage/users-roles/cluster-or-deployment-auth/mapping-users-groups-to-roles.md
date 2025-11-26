---
navigation_title: Map users and groups to roles
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-roles.html
  - https://www.elastic.co/guide/en/kibana/current/role-mappings.html
applies_to:
  stack: all
products:
  - id: elasticsearch
  - id: kibana
---

# Map external users and groups to roles [mapping-roles]

Role mapping is the process of applying roles to users based on their attributes or context. It is supported by all [external realms](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md) (realms other than `native` and `file`).

To use role mapping, you create roles and role mapping rules. Role mapping rules can be based on realm name, realm type, username, groups, other user metadata, or combinations of those values.

Users with no roles assigned will be unauthorized for any action. In other words, they may be able to authenticate, but they will have no roles. No roles means no privileges, and no privileges means no authorizations to make requests.

You can map external users and groups to roles in the following ways:

* Using the [{{kib}} Role mapping UI](#role-mapping-ui), which leverages the Role mapping API
* Using the [Role mapping API](#mapping-roles-api)
* Using [role mapping files](#mapping-roles-file) (PKI, LDAP, AD realms only)

::::{note}
When [anonymous access](/deploy-manage/users-roles/cluster-or-deployment-auth/anonymous-access.md) is enabled, the roles of the anonymous user are assigned to all the other users as well.
::::

All external realms also support [delegated authorization](/deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md#authorization_realms). You can either map roles for a realm or use delegated authorization; you cannot use both simultaneously.

:::{{tip}}
The native and file realms assign roles directly to users. Native realms use [user management APIs](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md#managing-native-users). File realms use [File-based role management](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-file).
:::

## Role sources

Before you use role mappings to assign roles to users, the roles must exist. You can assign [built-in roles](elasticsearch://reference/elasticsearch/roles.md), or [custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) defined through [the UI](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md), [the API](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-api), or [a roles file](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-file).

Any role mapping method can use any role management method. For example, when you use the role mapping API, you are able to map users to both API-managed roles (added using the UI or directly using the API) and file-managed roles. The same applies to file-based role-mappings.

## Using multiple role mapping methods

You can use a combination of methods to map roles to users. If you create role mapping rules created through the API (and related UI), and create additional rules using a role mapping file, the rules are combined.

It’s possible for a single user to have some roles that were mapped through the UI or API, and others assigned based on the role mapping file.

## Using the role mapping API [mapping-roles-api]

You can define and manage role mappings through the [add role mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping).

To learn about the properties that you can include in a role mapping resource, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/role-mapping-resources.md).

Refer to [Realm-specific details](#_realm_specific_details) for examples of mapping roles using the API.

## The role mapping UI [role-mapping-ui]

You can find the **Role mappings** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

With **Role mappings**, you can:

* View your configured role mappings
* Create, edit, or delete role mappings

![Role mappings](/deploy-manage/images/kibana-role-mappings-grid.png "")

### Required permissions [_required_permissions_8]

The `manage_security` cluster privilege is required to manage role mappings.

### Create a role mapping [_create_a_role_mapping]

1. Go to the **Role mappings** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create role mapping**.
3. Give your role mapping a unique name, and choose which roles you want to assign to your users.

    If you need more flexibility, you can use [role templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping) instead.

4. Define the rules describing which users should receive the roles you defined. Rules can optionally grouped and nested, allowing for sophisticated logic to suite complex requirements.
5. View the [role mapping resources for an overview of the allowed rule types](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

### Example [_example_2]

Let’s create a `sales-users` role mapping, which assigns a `sales` role to users whose username starts with `sls_`, **or** belongs to the `executive` group.

1. Give the role mapping a name, and assign the `sales` role:

  ![Create role mapping, step 1](/deploy-manage/images/kibana-role-mappings-create-step-1.png "")

2. Define the two rules, making sure to set the group to **Any are true**:

  ![Create role mapping, step 2](/deploy-manage/images/kibana-role-mappings-create-step-2.gif "")

1. When you're finished defining rules, click **Save role mapping**.

## Using role mapping files [mapping-roles-file]

While the role mapping API and UI are the preferred way to manage role mappings, using the `role_mapping.yml` file is useful in a few specific cases:

1. If you want to define fixed role mappings that no one (besides an administrator with access to the {{es}} nodes or {{eck}} cluster) would be able to change.
2. If cluster administration depends on users from external realms, and these users need to have their roles mapped to them even when the cluster is RED. For instance, in the case of an administrator that authenticates using LDAP or PKI and gets assigned an administrator role so that they can perform corrective actions.

However, the `role_mapping.yml` file is provided as a minimal administrative function and is not intended to cover and be used to define roles for all use cases.

::::{important}
You can't view, edit, or remove any roles that are defined in the role mapping files by using role mapping APIs or the role mapping UI.
::::

### Add a role mapping file

To use file based role mappings, you must configure the mappings in a YAML file.

To learn about the properties that you can include in a role mapping resource, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/role-mapping-resources.md).

Refer to [Realm-specific details](#_realm_specific_details) for examples of mapping roles using the role mapping file.

:::{tip}
If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.

If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

If you're using a self-managed cluster, then the file must be present on each node. Tools like Puppet or Chef can help with this.
:::

By default, role mappings are stored in `ES_PATH_CONF/role_mapping.yml`. In self-managed clusters, `ES_PATH_CONF` is `ES_HOME/config` (zip/tar installations) or `/etc/elasticsearch` (package installations).

To specify a different location, you configure the `files.role_mapping` setting in the [Active Directory](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ad-settings), [LDAP](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings), and [PKI](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-pki-settings) realm settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md).

Within the role mapping file, the security roles are keys and groups and users are values. The mappings can have a many-to-many relationship. When you map roles to groups, the roles of a user in that group are the combination of the roles assigned to that group and the roles assigned to that user.

By default, {{es}} checks role mapping files for changes every 5 seconds. If you're using a self-managed {{es}} cluster, you can change this default behavior by changing the `resource.reload.interval.high` setting in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file. Because this is a common setting in {{es}}, changing its value might effect other schedules in the system.

## Realm specific details [_realm_specific_details]

Review the following examples to learn how to set up role mapping using the API and using role mapping files for a few common external realms.

### Active Directory and LDAP realms [ldap-role-mapping]

To specify users and groups in the role mappings, you use their *Distinguished Names* (DNs). A DN is a string that uniquely identifies the user or group, for example `"cn=John Doe,cn=contractors,dc=example,dc=com"`.

For example, the following examples map the `admins` group to the `monitoring` role and map the `John Doe` user, the `users` group, and the `admins` group to the `user` role.

::::{note}
The {{es}} {{security-features}} support only Active Directory security groups. You can't map distribution groups to roles.
::::

::::{{tab-set}}
:::{{tab-item}} API
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
:::
:::{{tab-item}} Role mapping file
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
:::
::::

### PKI realms [pki-role-mapping]

PKI realms support mapping users to roles, but you can't map groups as the PKI realm has no concept of a group.

For example, the following examples map the `Admin` user to the `monitoring` role and map the `John Doe` user to the `user` role.

::::{{tab-set}}
:::{{tab-item}} API
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
:::
:::{{tab-item}} Role mapping file
```yaml
monitoring:
  - "cn=Admin,ou=example,o=com"
user:
  - "cn=John Doe,ou=example,o=com"
```
:::
::::