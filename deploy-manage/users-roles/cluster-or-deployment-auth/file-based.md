---
navigation_title: File-based
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/file-realm.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-users-and-roles.html
applies_to:
  deployment:
    self: all
    eck: all
products:
  - id: elasticsearch
  - id: cloud-kubernetes
---

# File-based user authentication [file-realm]

You can manage and authenticate users with the built-in `file` realm. With the `file` realm, users and roles are defined in local files on each node. 

The main {{stack}} {{security-features}} rely on the `security` [feature state](/deploy-manage/tools/snapshot-and-restore) which is mostly composed of the `.security*` [system indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions#system-indices). The `file` realm acts as a failsafe to expand this feature's functionality from the cluster level down to each individual node. The `file` realm cannot be managed using the cluster's [security APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) nor using {{kib}} **Management > Security** pages.

Therefore, the `file` realm is commonly used as a fallback or recovery realm. It is helpful in cases where the

* Cluster is unresponsive
* {{stack}} {{security-features}} is unavailable to the current node
* {{stack}} {{security-features}} is [lost and needs restored](/troubleshoot/elasticsearch/red-yellow-cluster-status#fix-cluster-status-restore) 
* Administrative users' passwords are lost and [need reset](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password)

The {{stack}} {{security-features}} only apply the `file` realm to the modified local node and do not apply changes across all nodes within the cluster. Administators of self-managed deployments are responsible to ensure that either

* The same users and roles are defined across every node in the cluster.
  * Frequently administrators choose to apply the change on one of the {{es}} nodes and have the files distributed or copied to all other nodes in the cluster (either manually or using a configuration management system such as Puppet or Chef).
* The related API requests are directed to the local node rather than any cluster-level load balancer or proxy URL.

Refer to [enabling a file realm user for recovery](https://www.youtube.com/watch?v=sueO7sz1buw) for a video walkthrough. 

## Configure realm [file-realm-configuration]

You don’t need to explicitly configure the `file` realm. The `file` and `native` realms are added to the realm chain by default. Unless configured otherwise, the `file` realm is added first, followed by the `native` realm. You can define only one `file` realm per node. To override the default `file` realm configuration

1. (Optional) Add a realm configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) under the `xpack.security.authc.realms.file` namespace. At a minimum, you must set the realm’s `order` attribute.

    For example, the following snippet shows a `file` realm configuration that sets the `order` to zero so the realm is checked first:

    ```yaml
    xpack.security.authc.realms.file.file1.order: 0
    ```

2. (Optional) For self-managed deployments, you may change how often `file` realm backing files are checked.

    By default, {{es}} checks these files for changes every 5 seconds. You can override this default behavior by changing the `resource.reload.interval.high` setting's value in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file.

    :::{{warning}}
    Because `resource.reload.interval.high` is a foundational setting for {{es}}, changing its value may effect other schedules in the system.
    :::

3. In self-managed deployments, if either prior setting is modified, you will need to [rolling restart](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures#restart-cluster-rolling) those {{es}} nodes for your changes to take effect. In {{eck}}, changes are automatically propagated.

## Configure files [file-realm-files]

The `file` realm reads its files upon the local node's initial startup and as periodically refreshed based on the `resource.reload.interval.high` setting. You do not need to restart nodes for changes to take effect. Its files are located under the [`ES_PATH_CONF` directory](/deploy-manage/deploy/self-managed/configure-elasticsearch#config-files-location) and contain

* `roles.yml` for [defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles)
* `role_mapping.yml` for [mapping external users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles)
* `users` for [user password-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication)
* `user_roles` for [user role-based authorization](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles)

### Define roles [file-realm-roles]

Before granting a `file` realm user its roles, you will want to ensure those desired roles exists. Roles can be defined from

* [built-in roles](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles)
* [custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles) defined under the {{stack}} {{security-features}}
* `roles.yml`per [File-based Role Management](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles#roles-management-file)

{{es}} recommends following the industry's [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) when granting user permissions. {{es}} follows this guidance itself by [restricting system indices](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure#roles-indices-priv) by default, even from [`superuser` role](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles#roles) administrators including the [`elastic` built-in user](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users). While recovering {{stack}} {{security-features}}, you may need to temporarily define a role with `allow_restricted_indices` access enabled. For example, expanding the `superuser` role to include `allow_restricted_indices: true` would appear like like new role `superduperuser` definition

```yaml
superduperuser:
  cluster: [ 'all' ]
  indices:
    - names: [ '*' ]
      privileges: [ 'all' ]
      allow_restricted_indices: true
```

:::{{warning}}
Restricted indices are a special category of indices that are used to store cluster configuration data and should not normally be directly accessed. **Toggling this flag is normally very strongly discouraged because it could effectively grant unrestricted operations on critical data, making the entire system unstable or leaking sensitive information.** If `allow_restricted_indices` needs temporarily enabled for a user in order to recover the {{stack}} {{security-features}}, {{es}} recommends ensuring to remove this role with sensitive access from the user upon task completion.
:::

### Define role mappings [file-realm-role-mappings]

For clusters with high authentication volume or with extremely large [role mappings](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles), you may potentially find performance improvement by defining custom `role_mapping.yml` locally on each node in the cluster. For more information, see [using role mapping files](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles#mapping-roles-file).

### Add users [file-realm-users]

The `file` realm can [define users](#file-realm-user-files) from files

* `users` for password-based authentication
* `users_roles` for role-based authorization

For {{eck}} deployments, these can also be passed through [{{k8s}} basic authentication secrets](#file-realm-user-k8s).

#### Defining user files [file-realm-user-files]

For most administrators, {{es}} recommends using the [`elasticsearch-users` tool](elasticsearch://reference/elasticsearch/command-line-tools/users-command) which compiles the `users` and `users_roles` files on your behalf. 

Expanding on our earlier `superduperuser` role example as part of demonstrating creating an advanced administrative user in order to recover the {{stack}} {{security-features}}, you would run

::::{tab-set}

:::{tab-item} Self-managed

```
bin/elasticsearch-users useradd admin -p changeme -r superduperuser
```
:::

:::{tab-item} {{eck}}
The following is an example of invoking the `elasticsearch-users` tool in a Docker container:

```sh
# create a folder with the 2 files
mkdir filerealm
touch filerealm/users filerealm/users_roles

# create user 'admin' with role 'superduperuser'
docker run \
    -v $(pwd)/filerealm:/usr/share/elasticsearch/config \
    docker.elastic.co/elasticsearch/elasticsearch:9.1.0 \
    bin/elasticsearch-users useradd admin -p changeme -r superduperuser

# create a Kubernetes secret with the file realm content
kubectl create secret generic my-file-realm-secret --from-file filerealm
```
:::

::::

For advanced users, you may choose to edit the `users` and `users_roles` files directly.

::::{tab-set}

:::{tab-item} Self-managed
In a self-managed cluster, you can edit the contents of `$ES_PATH_CONF/users` and `$ES_PATH_CONF/users_roles` directly.

* `users`

  The `users` file stores all the users and their passwords. Each line in the file represents a single user entry consisting of the username and hashed and salted password. For example:

  ```
  rdeniro:$2a$10$BBJ/ILiyJ1eBTYoRKxkqbuDEdYECplvxnqQ47uiowE7yGqvCEgj9W
  alpacino:$2a$10$cNwHnElYiMYZ/T3K4PvzGeJ1KbpXZp2PfoQD.gfaVdImnHOwIuBKS
  jacknich:{PBKDF2}50000$z1CLJt0MEFjkIK5iEfgvfnA6xq7lF25uasspsTKSo5Q=$XxCVLbaKDimOdyWgLCLJiyoiWpA/XDMe/xtVgn1r5Sg=
  ```

  To limit exposure to credential theft and mitigate credential compromise, the file realm stores passwords and caches user credentials according to security best practices. By default, a hashed version of user credentials is stored in memory, using a salted sha-256 hash algorithm and a hashed version of passwords is stored on disk salted and hashed with the bcrypt hash algorithm. To use different hash algorithms, see [User cache and password hash algorithms](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#hashing-settings).

* `users_roles`

  The `users_roles` file stores the roles associated with the users. Each row maps a role to a comma-separated list of all the users that are associated with that role. For example:

  ```
  admin:rdeniro
  superduperuser:alpacino,jacknich
  user:jacknich
  ```
:::

:::{tab-item} {{eck}}
You can pass `users` and `user_roles` files to {{eck}} using a file realm secret:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
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

The following secret specifies three users and their respective built-in and custom roles:

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: my-filerealm-secret
stringData:
  roles.yml: |-
      superduperuser:
        cluster:
          - all
        indices:
          - names: [ '*' ]
            privileges: [ 'all' ]
            allow_restricted_indices: true
  users: |-
    rdeniro:$2a$10$BBJ/ILiyJ1eBTYoRKxkqbuDEdYECplvxnqQ47uiowE7yGqvCEgj9W
    alpacino:$2a$10$cNwHnElYiMYZ/T3K4PvzGeJ1KbpXZp2PfoQD.gfaVdImnHOwIuBKS
    jacknich:{PBKDF2}50000$z1CLJt0MEFjkIK5iEfgvfnA6xq7lF25uasspsTKSo5Q=$XxCVLbaKDimOdyWgLCLJiyoiWpA/XDMe/xtVgn1r5Sg=
  users_roles: |-
    admin:rdeniro
    superduperuser:alpacino,jacknich
    user:jacknich
```
:::

::::

#### Using {{k8s}} basic authentication secrets [file-realm-user-k8s]
```{applies_to}
eck: all
```
You can also add `file` realm users using [{{k8s}} basic authentication secrets](https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret). You can reference several secrets in the {{es}} specification. {{eck}} aggregates their content into a single secret, mounted in every {{es}} Pod.

If you specify the password for the `elastic` user through a basic authentication secret, then the secret holding the password described in [](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md) will not be created by the operator.

Expanding on our earlier `superduperuser` role example as part of demonstrating creating an advanced user in order to recover the {{stack}} {{security-features}}, you would

1. Create a secret `my-roles-secret` adding our `superduperuser` role definition:
  
  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: my-roles-secret
  stringData:
    roles.yml: |-
      superduperuser:
        cluster:
          - all
        indices:
          - names: [ '*' ]
            privileges: [ 'all' ]
            allow_restricted_indices: true
  ```

2. Setup a basic authentication secret `secret-basic-auth` which contains its `username`, `password`, and a comma-separated list of `roles`:

  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: secret-basic-auth
  type: kubernetes.io/basic-auth
  stringData:
    username: admin    # required field for kubernetes.io/basic-auth
    password: changeme # required field for kubernetes.io/basic-auth
    roles: superduperuser,superuser  # optional, not part of kubernetes.io/basic-auth
  ```

3. then make these available to {{eck}} by adding them to your {{es}} manifest:

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
      roles:
      - secretName: my-roles-secret
    nodeSets:
    - name: default
      count: 1
  ```
