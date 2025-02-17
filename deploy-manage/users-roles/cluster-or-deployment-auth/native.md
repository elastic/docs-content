---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/native-realm.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-users-and-roles.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/change-passwords-native-users.html
  - https://www.elastic.co/guide/en/kibana/current/tutorial-secure-access-to-kibana.html
applies:
  stack: all
  hosted: all
  ece: all
  eck: all
---

# Native user authentication [native-realm]

The easiest way to manage and authenticate users is with the internal `native` realm. You can use the Elasticsearch REST APIs or Kibana to add and remove users, assign user roles, and manage user passwords.

## Configuring a native realm [native-realm-configuration]

The native realm is available and enabled by default. You can disable it explicitly with the following setting.

```yaml
xpack.security.authc.realms.native.native1:
  enabled: false
```

You can configure a `native` realm in the `xpack.security.authc.realms.native` namespace in `elasticsearch.yml`. Explicitly configuring a native realm enables you to set the order in which it appears in the realm chain, temporarily disable the realm, and control its cache options.

1. Add a realm configuration to `elasticsearch.yml` under the `xpack.security.authc.realms.native` namespace. It is recommended that you explicitly set the `order` attribute for the realm.

    ::::{note} 
    You can configure only one native realm on {{es}} nodes.
    ::::


    See [Native realm settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-native-settings) for all of the options you can set for the `native` realm. For example, the following snippet shows a `native` realm configuration that sets the `order` to zero so the realm is checked first:

    ```yaml
    xpack.security.authc.realms.native.native1:
      order: 0
    ```

    ::::{note} 
    To limit exposure to credential theft and mitigate credential compromise, the native realm stores passwords and caches user credentials according to security best practices. By default, a hashed version of user credentials is stored in memory, using a salted `sha-256` hash algorithm and a hashed version of passwords is stored on disk salted and hashed with the `bcrypt` hash algorithm. To use different hash algorithms, see [User cache and password hash algorithms](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#hashing-settings).
    ::::

2. Restart {{es}}.


## Managing native users [managing-native-users]

The {{stack}} {{security-features}} enable you to easily manage users in {{kib}} on the **Management / Security / Users** page.

Alternatively, you can manage users through the `user` API. For more information and examples, see [Users](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security).

### Create a user [_create_a_user]

Now that you created a role, create a user account.

1. Navigate to **Stack Management**, and under **Security**, select **Users**.
2. Click **Create user**.
3. Give this user a descriptive username, and choose a secure password.
4. Assign the **marketing_dashboards_role** that you previously created to this new user.
5. Click **Create user**.

:::{image} ../../../images/kibana-tutorial-secure-access-example-1-user.png
:alt: Create user UI
:class: screenshot
:::

## Reset passwords for native users

After you implement security, you might need or want to change passwords for different users. You can use the [`elasticsearch-reset-password`](https://www.elastic.co/guide/en/elasticsearch/reference/current/reset-password.html) tool or the [change passwords API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password) to change passwords for native users.

For example, the following command changes the password for a user with the username `user1` to an auto-generated value, and prints the new password to the terminal:

```shell
bin/elasticsearch-reset-password -u user1
```

To explicitly set a password for a user, include the `-i` parameter with the intended password.

```shell
bin/elasticsearch-reset-password -u user1 -i <password>
```

If you’re working in {{kib}} or don’t have command-line access, you can use the change passwords API to change a user’s password:

```console
POST /_security/user/user1/_password
{
  "password" : "new-test-password"
}
```
