---
navigation_title: Native
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/native-realm.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-users-and-roles.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/change-passwords-native-users.html
  - https://www.elastic.co/guide/en/kibana/current/tutorial-secure-access-to-kibana.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
  - id: cloud-kubernetes
  - id: kibana
---

# Native user authentication [native-realm]

The easiest way to manage and authenticate users is with the internal `native` realm. You can use [{{es}} REST APIs](#native-users-api) or [Kibana](#managing-native-users) to add and remove users, assign user roles, and manage user passwords.

In self-managed {{es}} clusters, you can also reset passwords for users in the native realm [using the command line](#reset-pw-cmd-line).

:::{{tip}}
This topic describes using the native realm at the cluster or deployment level, for the purposes of authenticating with {{es}} and {{kib}}.

You can also manage and authenticate users natively at the following levels:

* For an [{{ece}} installation](/deploy-manage/users-roles/cloud-enterprise-orchestrator/native-user-authentication.md).
* For an [{{ecloud}} organization](/deploy-manage/users-roles/cloud-organization/manage-users.md).
:::


## Configure a native realm [native-realm-configuration]

The native realm is available and enabled by default. You can disable it explicitly with the following setting.

```yaml
xpack.security.authc.realms.native.native1:
  enabled: false
```

You can configure a `native` realm in the `xpack.security.authc.realms.native` namespace in [`elasticsearch.yml`](/deploy-manage/stack-settings.md). Explicitly configuring a native realm enables you to set the order in which it appears in the realm chain, temporarily disable the realm, and control its cache options.

1. Add a realm configuration to `elasticsearch.yml` under the `xpack.security.authc.realms.native` namespace. It is recommended that you explicitly set the `order` attribute for the realm.

    ::::{note}
    You can configure only one native realm on {{es}} nodes.
    ::::


    See [Native realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-native-settings) for all of the options you can set for the `native` realm. For example, the following snippet shows a `native` realm configuration that sets the `order` to zero so the realm is checked first:

    ```yaml
    xpack.security.authc.realms.native.native1:
      order: 0
    ```

    ::::{note}
    To limit exposure to credential theft and mitigate credential compromise, the native realm stores passwords and caches user credentials according to security best practices. By default, a hashed version of user credentials is stored in memory, using a salted `sha-256` hash algorithm and a hashed version of passwords is stored on disk salted and hashed with the `bcrypt` hash algorithm. To use different hash algorithms, see [User cache and password hash algorithms](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#hashing-settings).
    ::::

2. Restart {{es}}.


## Manage native users using {{kib}} [managing-native-users]

Elastic enables you to easily manage users in {{kib}}. To manage users in {{kib}}, go to the **Users** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

From this page, you can create users, edit users, assign roles to users, and change user passwords. You can also deactivate or delete existing users.

### Example: Create a user [_create_a_user]

1. Go to the **Users** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create user**.
3. Give the user a descriptive username, and choose a secure password.
4. Optional: assign [roles](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md) to the user.
5. Click **Create user**.

:::{image} /deploy-manage/images/kibana-tutorial-secure-access-example-1-user.png
:alt: Create user UI
:screenshot:
:::

## Manage native users using the `user` API [native-users-api]

You can manage users through the {{es}} `user` API.

For example, you can change a user's password:

```console
POST /_security/user/user1/_password
{
  "password" : "new-test-password"
}
```

For more information and examples, see [Users](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security).

## Reset passwords for native users using the command line [reset-pw-cmd-line]

```{applies_to}
deployment:
  self: all
```

You can also reset passwords for users in the native realm through the command line using the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool.

For example, the following command changes the password for a user with the username `user1` to an auto-generated value, and prints the new password to the terminal:

```shell
bin/elasticsearch-reset-password -u user1
```

To explicitly set a password for a user, include the `-i` parameter with the intended password.

```shell
bin/elasticsearch-reset-password -u user1 -i <password>
```
