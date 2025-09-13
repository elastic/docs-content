---
navigation_title: File-Based Recovery
applies_to:
  stack:
  deployment:
    eck:
    self:
products:
  - id: elasticsearch
---

# File-based Recovery [file-based-recovery]

The [built-in `file` realm](docs-content://deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md) is commonly used as a fallback or recovery realm. 

The main {{stack}} {{security-features}} rely on the `security` [feature state](/deploy-manage/tools/snapshot-and-restore.md) which is mostly composed of the `.security*` [system indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#system-indices). The `file` realm acts as a failsafe to expand this feature's functionality from the cluster level down to each individual node. The `file` realm cannot be managed using the cluster's [security APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) nor using {{kib}} **Management > Security** pages.

The `file` realm is helpful in cases where the

* Node services are running but cluster is unresponsive
* {{stack}} {{security-features}} is unavailable to the current node
* {{stack}} {{security-features}} is [lost and needs restored](/troubleshoot/elasticsearch/red-yellow-cluster-status.md#fix-cluster-status-restore) 
* Administrative users' passwords are lost and [need reset](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password)

The {{stack}} {{security-features}} only apply the `file` realm to the modified local node and do not apply changes across all nodes within the cluster. Administrators of self-managed deployments are responsible to ensure that either

* The same users and roles are defined across every node in the cluster.
  * Frequently administrators choose to apply the change on one of the {{es}} nodes and have the files distributed or copied to all other nodes in the cluster (either manually or using a configuration management system such as Puppet or Chef).
* The related API requests are directed to the local node rather than any cluster-level load balancer or proxy URL.

Refer to [enabling a file realm user for recovery](https://www.youtube.com/watch?v=sueO7sz1buw) for a video walkthrough.

## Configure realm [file-realm-recovery-configuration]

The `file` and `native` realms are added to the realm chain by default. Unless configured otherwise, the `file` realm is added first, followed by the `native` realm. The `file` realm can only be added once per node. To override the default `file` realm configuration, see [Configure a file realm](https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/file-based#file-realm-configuration).

The `file` realm reads its files upon the local node's initial startup and as periodically refreshed based on the `resource.reload.interval.high` setting. You do not need to restart nodes for changes to take effect. Its files are located under the [`ES_PATH_CONF` directory](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) and contain

* `roles.yml` for [defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md)
* `role_mapping.yml` for [mapping external users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md)
* `users` for [user password-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md)
* `user_roles` for [user role-based authorization](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md)

### Choose roles [file-realm-recovery-roles]

Before granting a `file` realm user its roles, you will want to ensure those desired roles exist. Roles can be defined from

* [built-in roles](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md)
* [custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) defined under the {{stack}} {{security-features}}
* `roles.yml`per [file-based role management](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-file)

{{es}} recommends following the industry's [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) when granting user permissions. {{es}} follows this guidance itself by [restricting system indices](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-indices-priv) by default, even from [`superuser` role](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md#roles) administrators including the [`elastic` built-in user](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md). 

While recovering {{stack}} {{security-features}}, you may need to temporarily define a custom role with [`allow_restricted_indices` setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role) enabled. For example, expanding the `superuser` role to include `allow_restricted_indices: true` would appear like like new role `superduperuser` definition

```yaml
superduperuser:
  cluster: [ 'all' ]
  indices:
    - names: [ '*' ]
      privileges: [ 'all' ]
      allow_restricted_indices: true
```

Once role authorization criteria is decided, you will be ready to add this role into your local node's configuration. We will demonstrate this below.

:::{{warning}}
Restricted indices are a special category of indices that are used to store cluster configuration data and should not normally be directly accessed. **Toggling this flag is normally _strongly_ discouraged because it could effectively grant unrestricted operations on critical data, making the entire system unstable or leaking sensitive information.** If `allow_restricted_indices` needs temporarily enabled for a user in order to recover the {{stack}} {{security-features}}, {{es}} recommends ensuring to remove this role with sensitive access from the user upon task completion.
:::

#### Defining files [file-realm-recovery-files]

For most administrators, {{es}} recommends using the [`elasticsearch-users` tool](elasticsearch://reference/elasticsearch/command-line-tools/users-command.md) which compiles the `users` and `users_roles` files on your behalf.

Expanding on our earlier `superduperuser` role example as part of demonstrating creating an advanced administrative user in order to recover the {{stack}} {{security-features}}, you would run

::::{tab-set}

:::{tab-item} Self-managed

```
bin/elasticsearch-users useradd admin -p changeme -r superduperuser
```
:::

:::{tab-item} {{eck}} secrets
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


:::{tab-item} {{eck}} basic auth

You can also add `file` realm users using [{{k8s}} basic authentication secrets](https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret). For more information, see [`file` realm](https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/file-based#k8s-basic)

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

:::

::::