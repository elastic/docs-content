# File-based user authentication [file-realm]

You can manage and authenticate users with the built-in `file` realm. With the `file` realm, users are defined in local files on each node in the cluster.

::::{important}
As the administrator of the cluster, it is your responsibility to ensure the same users are defined on every node in the cluster. The {{stack}} {security-features} do not deliver any mechanism to guarantee this. You should also be aware that you cannot add or manage users in the `file` realm via the [user APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api.html#security-user-apis) and you cannot add or manage them in {{kib}} on the **Management / Security / Users** page
::::


The `file` realm is very useful as a fallback or recovery realm. For example in cases where the cluster is unresponsive or the security index is unavailable, or when you forget the password for your administrative users. In this type of scenario, the `file` realm is a convenient way out - you can define a new `admin` user in the `file` realm and use it to log in and reset the credentials of all other users.

To define users, the {{security-features}} provide the [users](https://www.elastic.co/guide/en/elasticsearch/reference/current/users-command.html) command-line tool. This tool enables you to add and remove users, assign user roles, and manage user passwords.

## Configuring a file realm [file-realm-configuration]

You don’t need to explicitly configure a `file` realm. The `file` and `native` realms are added to the realm chain by default. Unless configured otherwise, the `file` realm is added first, followed by the `native` realm.

::::{important}
While it is possible to define multiple instances of some other realms, you can define only *one* `file` realm per node.
::::


All the data about the users for the `file` realm is stored in two files on each node in the cluster: `users` and `users_roles`. Both files are located in `ES_PATH_CONF` and are read on startup.

::::{important}
The `users` and `users_roles` files are managed locally by the node and are **not** managed globally by the cluster. This means that with a typical multi-node cluster, the exact same changes need to be applied on each and every node in the cluster.

A safer approach would be to apply the change on one of the nodes and have the files distributed or copied to all other nodes in the cluster (either manually or using a configuration management system such as Puppet or Chef).

::::


1. (Optional) Add a realm configuration to `elasticsearch.yml` under the `xpack.security.authc.realms.file` namespace. At a minimum, you must set the realm’s `order` attribute.

    For example, the following snippet shows a `file` realm configuration that sets the `order` to zero so the realm is checked first:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            file:
              file1:
                order: 0
    ```

    ::::{note}
    You can configure only one file realm on {{es}} nodes.
    ::::

2. Restart {{es}}.
3. Add user information to the `ES_PATH_CONF/users` file on each node in the cluster.

    The `users` file stores all the users and their passwords. Each line in the file represents a single user entry consisting of the username and **hashed** and **salted** password.

    ```bash
    rdeniro:$2a$10$BBJ/ILiyJ1eBTYoRKxkqbuDEdYECplvxnqQ47uiowE7yGqvCEgj9W
    alpacino:$2a$10$cNwHnElYiMYZ/T3K4PvzGeJ1KbpXZp2PfoQD.gfaVdImnHOwIuBKS
    jacknich:{PBKDF2}50000$z1CLJt0MEFjkIK5iEfgvfnA6xq7lF25uasspsTKSo5Q=$XxCVLbaKDimOdyWgLCLJiyoiWpA/XDMe/xtVgn1r5Sg=
    ```

    ::::{note}
    To limit exposure to credential theft and mitigate credential compromise, the file realm stores passwords and caches user credentials according to security best practices. By default, a hashed version of user credentials is stored in memory, using a salted `sha-256` hash algorithm and a hashed version of passwords is stored on disk salted and hashed with the `bcrypt` hash algorithm. To use different hash algorithms, see [User cache and password hash algorithms](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#hashing-settings).
    ::::


    While it is possible to modify the `users` files directly using any standard text editor, we strongly recommend using the [*elasticsearch-users*](https://www.elastic.co/guide/en/elasticsearch/reference/current/users-command.html) tool to apply the required changes.

    ::::{important}
    As the administrator of the cluster, it is your responsibility to ensure the same users are defined on every node in the cluster. The {{es}} {security-features} do not deliver any mechanisms to guarantee this.
    ::::

4. Add role information to the `ES_PATH_CONF/users_roles` file on each node in the cluster.

    The `users_roles` file stores the roles associated with the users. For example:

    ```shell
    admin:rdeniro
    power_user:alpacino,jacknich
    user:jacknich
    ```

    Each row maps a role to a comma-separated list of all the users that are associated with that role.

    You can use the [*elasticsearch-users*](https://www.elastic.co/guide/en/elasticsearch/reference/current/users-command.html) tool to update this file. You must ensure that the same changes are made on every node in the cluster.

5. (Optional) Change how often the `users` and `users_roles` files are checked.

    By default, {{es}} checks these files for changes every 5 seconds. You can change this default behavior by changing the `resource.reload.interval.high` setting in the `elasticsearch.yml` file (as this is a common setting in {{es}}, changing its value may effect other schedules in the system).
