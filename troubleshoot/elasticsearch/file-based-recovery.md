---
applies_to:
  deployment:
    eck: ga 
    self: ga
products:
  - id: elasticsearch
  - id: cloud-kubernetes
---

# File-based access recovery

The [built-in `file` realm](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md) is commonly used as a fallback or recovery realm. 

The main {{stack}} {{security-features}} rely on the `security` [feature state](/deploy-manage/tools/snapshot-and-restore.md) which is mostly composed of the `.security*` [system indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#system-indices). The `file` realm acts as a failsafe to expand this feature's functionality from the cluster level down to each individual node.

The `file` realm is especially helpful for recovery scenarios where normal security mechanisms aren't accessible:

* Node services are running but cluster is unresponsive
* {{stack}} {{security-features}} are unavailable to the current node
* {{stack}} {{security-features}} are [lost and need to be restored](/troubleshoot/elasticsearch/red-yellow-cluster-status.md#fix-cluster-status-restore) 
* Administrative users' passwords are lost and [need to be reset](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password)

The {{stack}} {{security-features}} only apply the `file` realm to the modified local node and do not apply changes across all nodes within the cluster. Administrators of self-managed deployments are responsible for ensuring one of the following:

* The same users and roles are defined across every node in the cluster.
  
  Frequently, administrators choose to apply the change on one {{es}} node and then distribute or copy the files to all other nodes in the cluster. Files can be distributed either manually or using a configuration management system such as Puppet or Chef.
* The related API requests are directed to the local node rather than to any cluster-level load balancer or proxy URL.

:::{tip}
Refer to [enabling a file realm user for recovery](https://www.youtube.com/watch?v=sueO7sz1buw) for a video walkthrough of this process.
:::

## Step 1 (Optional): Configure the realm [file-realm-recovery-configuration]

You don’t need to explicitly configure a `file` realm. The `file` and `native` realms are added to the realm chain by default. Unless configured otherwise, the `file` realm is added first, followed by the `native` realm. You can define only one `file` realm on each node. 

To learn how to override the default `file` realm configuration, refer to [Configure a file realm](https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/file-based#file-realm-configuration).

{{es}} reads security-related files upon the local node's initial startup and as periodically refreshed based on the `resource.reload.interval.high` setting. You do not need to restart nodes for changes to take effect. These files are located under the [`ES_PATH_CONF` directory](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) and contain the following information:

* `roles.yml` for [defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md)
* `role_mapping.yml` for [mapping external users and groups to roles](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md)
* `users` for [user password-based authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md)
* `user_roles` for [user role-based authorization](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md)

## Step 2: Choose roles for recovery [file-realm-recovery-roles]

Before granting a `file` realm user any roles, you need to ensure that those desired roles exist. You can use the following types of roles:

* [Built-in roles](elasticsearch://reference/elasticsearch/roles.md)
* [Custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) defined under the {{stack}} {{security-features}}
* Roles defined in [`roles.yml`](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#roles-management-file)

{{es}} recommends following the industry's [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) when granting user permissions. {{es}} follows this guidance itself by [restricting system indices](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-indices-priv) by default, even from [`superuser` role](elasticsearch://reference/elasticsearch/roles.md) administrators including the [`elastic` built-in user](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md). 

The main {{stack}} {{security-features}} rely on the `security` [feature state](/deploy-manage/tools/snapshot-and-restore.md) which is mostly composed of the `.security*` [system indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#system-indices). When recovering {{stack}} {{security-features}}, you will likely need to temporarily define a custom role with the [`allow_restricted_indices` setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role) enabled.

For example, to grant the administrative privileges of `superuser` role alongside `allow_restricted_indices: true` you can create a new role called `superduperuser` with the following definition:

```yaml
superduperuser:
  cluster: [ 'all' ]
  indices:
    - names: [ '*' ]
      privileges: [ 'all' ]
      allow_restricted_indices: true
```

After you decide on your role definitions, you can add your users and any custom roles to your local node's configuration.

:::{{warning}}
Restricted indices are a special category of indices that are used to store cluster configuration data and should not normally be directly accessed. **Toggling this flag is normally _strongly_ discouraged because it could effectively grant unrestricted operations on critical data, making the entire system unstable or leaking sensitive information.** 

If `allow_restricted_indices` needs temporarily enabled for a user in order to recover the {{stack}} {{security-features}}, {{es}} recommends ensuring to remove this role with sensitive access from the user upon task completion.
:::

## Step 3: Add the recovery user and role to the node [file-realm-recovery-files]

For most administrators, {{es}} recommends that you use the [`elasticsearch-users` tool](elasticsearch://reference/elasticsearch/command-line-tools/users-command.md), which compiles the `users` and `users_roles` files on your behalf.

In this example, we create an advanced administrative user with the `superduperuser` role we designed [in the previous step](#file-realm-recovery-roles).

::::{tab-set}

:::{tab-item} Self-managed

```
bin/elasticsearch-users useradd admin -p changeme -r superduperuser
```
:::

:::{tab-item} ECK secrets
The following is an example of invoking the `elasticsearch-users` tool in a Docker container:

```sh subs=true
# create a folder with the 2 files
mkdir filerealm
touch filerealm/users filerealm/users_roles

# create user 'admin' with role 'superduperuser'
docker run \
    -v $(pwd)/filerealm:/usr/share/elasticsearch/config \
    docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}} \
    bin/elasticsearch-users useradd admin -p changeme -r superduperuser

# create a Kubernetes secret with the file realm content
kubectl create secret generic my-file-realm-secret --from-file filerealm
```

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


:::{tab-item} ECK basic auth

You can also add `file` realm users using [{{k8s}} basic authentication secrets](https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret). For more information, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md#k8s-basic).

1. Create a secret `my-roles-secret` that adds the `superduperuser` role definition:
  
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

2. Set up a basic authentication secret `secret-basic-auth` which contains its `username`, `password`, and a comma-separated list of `roles`:

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

3. Make the secrets available to {{eck}} by adding them to your {{es}} manifest:

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: elasticsearch-sample
    spec:
      version: {{version.stack}}
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

## Step 4: Recover {{security-features}} [file-realm-recovery-curl]

At this point, the local {{es}} node will accept [Elasticsearch API requests](https://www.elastic.co/docs/reference/elasticsearch/rest-apis) with the created `file` based username and password. 

For example, if you created a user with the username `admin`, password `changeme`, and role `superduperuser`, then you can now send a cURL request to the [Get cluster info API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-info) from the node's local shell:
```bash
curl -X GET -sk -u "admin:changeme" "https://localhost:9200/" 
```

:::{{tip}}
The related API requests need to be directed to the local nodes where `file` has been configured, rather than to any cluster-level load balancer or proxy URL.
:::

You can confirm that the desired `superduperuser` role is applied to your `admin` username using the [Authenticate a user API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-authenticate):
```bash
curl -X GET -sk -u "admin:changeme" "https://localhost:9200/_security/_authenticate?pretty=true" 
```

Now that you have regained recovery access to the cluster, you can investigate and recover the {{stack}} {{security-features}} as needed. For more information, refer to [Restore a feature state](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-feature-state).