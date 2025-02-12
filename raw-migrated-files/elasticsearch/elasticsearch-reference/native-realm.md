# Native user authentication [native-realm]

The easiest way to manage and authenticate users is with the internal `native` realm. You can use the REST APIs or Kibana to add and remove users, assign user roles, and manage user passwords.

## Configuring a native realm [native-realm-configuration]

The native realm is available and enabled by default. You can disable it explicitly with the following snippet.

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

The {{stack}} {security-features} enable you to easily manage users in {{kib}} on the **Management / Security / Users** page.

Alternatively, you can manage users through the `user` API. For more information and examples, see [Users](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security).


