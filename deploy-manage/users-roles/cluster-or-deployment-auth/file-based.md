---
navigation_title: File-based
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/file-realm.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-users-and-roles.html
applies_to:
  deployment:
    self: ga
    eck: ga
products:
  - id: elasticsearch
  - id: cloud-kubernetes
---

# File-based user authentication [file-realm]

You can manage and authenticate users with the built-in `file` realm. With the `file` realm, users are defined in local files on each node in the cluster.

The `file` realm is useful as a fallback or recovery realm. For example, you might use this realm in cases where the cluster is unresponsive or the security index is unavailable, or when you forget the password for your administrative users. In this type of scenario, the `file` realm is a convenient workaround: you can define a new `admin` user in the `file` realm and use it to log in and reset the credentials of all other users. For a walkthrough of this process, refer to [](/troubleshoot/elasticsearch/file-based-recovery.md). Refer to [enabling a file realm user for recovery](https://www.youtube.com/watch?v=sueO7sz1buw) for a video walkthrough. 

::::{important}
* In self-managed deployments, as the administrator of the cluster, it is your responsibility to ensure the same users are defined on every node in the cluster. The {{stack}} {{security-features}} do not deliver any mechanism to guarantee this.
* You can't add or manage users in the `file` realm using the [user APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security), or using the {{kib}} **Management > Security > Users** page.
::::

## Configure a file realm [file-realm-configuration]

You don’t need to explicitly configure a `file` realm. The `file` and `native` realms are added to the realm chain by default. Unless configured otherwise, the `file` realm is added first, followed by the `native` realm. You can define only one `file` realm on each node.

1. (Optional) Add a realm configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) under the `xpack.security.authc.realms.file` namespace. At a minimum, you must set the realm’s `order` attribute.

    For example, the following snippet shows a `file` realm configuration that sets the `order` to zero so the realm is checked first:

    ```yaml
    xpack.security.authc.realms.file.file1.order: 0
    ```

2. (Optional) For self-managed deployments, you can change how often the `users` and `users_roles` files are checked.

    By default, {{es}} checks these files for changes every 5 seconds. You can change this default behavior by changing the `resource.reload.interval.high` setting in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file.

    :::{{warning}}
    Because `resource.reload.interval.high` is a common setting in {{es}}, changing its value may effect other schedules in the system.
    :::

3. In self-managed deployments, if either of these settings is modified, perform a [rolling restart](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) of the {{es}} nodes for your changes to take effect. 

    In {{eck}}, changes are automatically propagated.


## Add users

**In a self-managed {{es}} cluster**, all the data about the users for the `file` realm is stored in two files on each node in the cluster: [`users` and `users_roles`](#using-users-and-users_roles-files). Both files are located in `ES_PATH_CONF` and are read on startup.

**In an {{eck}} deployment**, you can pass file realm user information in two ways:

1. Using [`users` and `user_roles`](#using-users-and-users_roles-files) files, which are passed using file realm content secrets
2. [Using Kubernetes basic authentication secrets](#k8s-basic)

You can reference several secrets in the {{es}} specification. ECK aggregates their content into a single secret, mounted in every {{es}} Pod.

::::{important}
In a self-managed cluster, the `users` and `users_roles` files are managed locally by the node and are **not** managed globally by the cluster. This means that with a typical multi-node cluster, the exact same changes need to be applied on each and every node in the cluster.

A safer approach would be to apply the change on one of the nodes and have the files distributed or copied to all other nodes in the cluster (either manually or using a configuration management system such as Puppet or Chef).
::::

### Using `users` and `users_roles` files

`users` and `users_roles` files contain all of the information about users in the file realm.

#### `users`

The `users` file stores all the users and their passwords. Each line in the file represents a single user entry consisting of the username and hashed and salted password.

```
rdeniro:$2a$10$BBJ/ILiyJ1eBTYoRKxkqbuDEdYECplvxnqQ47uiowE7yGqvCEgj9W
alpacino:$2a$10$cNwHnElYiMYZ/T3K4PvzGeJ1KbpXZp2PfoQD.gfaVdImnHOwIuBKS
jacknich:{PBKDF2}50000$z1CLJt0MEFjkIK5iEfgvfnA6xq7lF25uasspsTKSo5Q=$XxCVLbaKDimOdyWgLCLJiyoiWpA/XDMe/xtVgn1r5Sg=
```

:::{tip}
To limit exposure to credential theft and mitigate credential compromise, the file realm stores passwords and caches user credentials according to security best practices. By default, a hashed version of user credentials is stored in memory, using a salted sha-256 hash algorithm and a hashed version of passwords is stored on disk salted and hashed with the bcrypt hash algorithm. To use different hash algorithms, see [User cache and password hash algorithms](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#hashing-settings).
:::

#### `users_roles`

The `users_roles` file stores the roles associated with the users. For example:

```
admin:rdeniro
power_user:alpacino,jacknich
user:jacknich
```

Each row maps a role to a comma-separated list of all the users that are associated with that role.

#### Editing `users` and `users_roles` files

You can edit files and secrets that contain `users` and `users_roles` manually, or you can edit them using a tool.

**Manually**

::::{applies-switch}

:::{applies-item} self:
In a self-managed cluster, you can edit the contents of `ES_PATH_CONF/users` and `ES_PATH_CONF/users_roles` directly.
:::

:::{applies-item} eck:
You can pass `users` and `user_roles` files to {{eck}} using a file realm secret:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: {{version.stack}}
  auth:
    fileRealm:
    - secretName: my-filerealm-secret-1
    - secretName: my-filerealm-secret-2
  nodeSets:
  - name: default
    count: 1
```

A file realm secret is composed of two entries: a `users` entry and a `users_roles` entry. You can provide either one entry or both entries in each secret.

If you specify multiple users with the same name in more than one secret, the last one takes precedence. If you specify multiple roles with the same name in more than one secret, a single entry per role is derived from the concatenation of its corresponding users from all secrets.

The following secret specifies three users and their respective roles:

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: my-filerealm-secret
stringData:
  users: |-
    rdeniro:$2a$10$BBJ/ILiyJ1eBTYoRKxkqbuDEdYECplvxnqQ47uiowE7yGqvCEgj9W
    alpacino:$2a$10$cNwHnElYiMYZ/T3K4PvzGeJ1KbpXZp2PfoQD.gfaVdImnHOwIuBKS
    jacknich:{PBKDF2}50000$z1CLJt0MEFjkIK5iEfgvfnA6xq7lF25uasspsTKSo5Q=$XxCVLbaKDimOdyWgLCLJiyoiWpA/XDMe/xtVgn1r5Sg=
  users_roles: |-
    admin:rdeniro
    power_user:alpacino,jacknich
    user:jacknich
```
:::

::::

**Using a tool**

To avoid editing these files manually, you can use the [elasticsearch-users](elasticsearch://reference/elasticsearch/command-line-tools/users-command.md) tool:

::::{applies-switch}

:::{applies-item} self:

```
bin/elasticsearch-users useradd myuser -p mypassword -r monitoring_user
```
:::

:::{applies-item} eck:
The following is an example of invoking the `elasticsearch-users` tool in a Docker container:

```sh
# create a folder with the 2 files
mkdir filerealm
touch filerealm/users filerealm/users_roles

# create user 'myuser' with role 'monitoring_user'
docker run \
    -v $(pwd)/filerealm:/usr/share/elasticsearch/config \
    docker.elastic.co/elasticsearch/elasticsearch:8.16.1 \
    bin/elasticsearch-users useradd myuser -p mypassword -r monitoring_user

# create a Kubernetes secret with the file realm content
kubectl create secret generic my-file-realm-secret --from-file filerealm
```
:::

::::

### Using {{k8s}} basic authentication secrets [k8s-basic]
```{applies_to}
eck: all
```
You can also add file-based authentication users using [Kubernetes basic authentication secrets](https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret).

A basic authentication secret can optionally contain a [`roles`](#users_roles) entry. It must contain a comma separated list of roles to be associated with the user. The following example illustrates this combination:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-basic-auth
type: kubernetes.io/basic-auth
stringData:
  username: rdeniro    # required field for kubernetes.io/basic-auth
  password: mypassword # required field for kubernetes.io/basic-auth
  roles: kibana_admin,ingest_admin  # optional, not part of kubernetes.io/basic-auth
```

::::{tip}
To create custom roles that can be referenced in this list refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-file).
::::

You can make this file available to {{eck}} by adding it as a file realm secret:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  auth:
    fileRealm:
    - secretName: secret-basic-auth
  nodeSets:
  - name: default
    count: 1
```

::::{note}
If you specify the password for the `elastic` user through a basic authentication secret, then the secret holding the password described in [](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md) will not be created by the operator.
::::
