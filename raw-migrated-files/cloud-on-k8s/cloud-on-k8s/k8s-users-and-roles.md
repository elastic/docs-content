# Users and roles [k8s-users-and-roles]

## Default elastic user [k8s-default-elastic-user]

When the Elasticsearch resource is created, a default user named `elastic` is created automatically, and is assigned the `superuser` role.

Its password can be retrieved in a Kubernetes secret, whose name is based on the Elasticsearch resource name: `<elasticsearch-name>-es-elastic-user`.

For example, the password of the `elastic` user for an Elasticsearch cluster named `quickstart` can be retrieved with:

```sh
kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
```

To rotate this password, refer to: [Rotate auto-generated credentials](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).

### Disabling the default `elastic` user [k8s_disabling_the_default_elastic_user]

If your prefer to manage all users via SSO, for example using [SAML Authentication](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md) or OpenID Connect, you can disable the default `elastic` superuser by setting the `auth.disableElasticUser` field in the Elasticsearch resource to `true`:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  auth:
    disableElasticUser: true
  nodeSets:
  - name: default
    count: 1
```



## Creating custom users [k8s_creating_custom_users]

::::{warning}
Do not run the `elasticsearch-service-tokens` command inside an Elasticsearch Pod managed by the operator. This would overwrite the service account tokens used internally to authenticate the Elastic stack applications.
::::


### Native realm [k8s_native_realm]

You can create custom users in the [Elasticsearch native realm](https://www.elastic.co/guide/en/elasticsearch/reference/current/native-realm.html) using [Elasticsearch user management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security).


### File realm [k8s_file_realm]

Custom users can also be created by providing the desired [file realm content](https://www.elastic.co/guide/en/elasticsearch/reference/current/file-realm.html) or a username and password in Kubernetes secrets, referenced in the Elasticsearch resource.

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

You can reference several secrets in the Elasticsearch specification. ECK aggregates their content into a single secret, mounted in every Elasticsearch Pod.

Referenced secrets may be of one of two types:

1. a combination of username and password as in [Kubernetes basic authentication secrets](https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret)
2. a raw file realm content secret

A basic authentication secret can optionally also contain a `roles` file. It must contain a comma separated list of roles to be associated with the user. The following example illustrates this combination:

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

::::{note}
If you specify the password for the `elastic` user through such a basic authentication secret then the secret holding the password described in [Default elastic user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/native.md#k8s-default-elastic-user) will not be created by the operator.
::::


The second option, a file realm secret, is composed of 2 entries. You can provide either one entry or both entries in each secret:

* `users`: content of the `users` file. It specifies user names and password hashes, as described in the [file realm documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/file-realm.html).
* `users_roles`: content of the `users_roles` file. It associates each role to a list of users, as described in the [file realm documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/file-realm.html).

If you specify multiple users with the same name in more than one secret, the last one takes precedence. If you specify multiple roles with the same name in more than one secret, a single entry per role is derived from the concatenation of its corresponding users from all secrets.

The following Secret specifies three users and their respective roles:

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

You can populate the content of both `users` and `users_roles` using the [elasticsearch-users](https://www.elastic.co/guide/en/elasticsearch/reference/current/users-command.html) tool.

For example, invoking the tool in a Docker container:

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



## Creating custom roles [k8s_creating_custom_roles]

[Roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html) can be specified using the [Role management API](https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html#roles-management-api), or the [Role management UI in Kibana](https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html#roles-management-ui).

Additionally, [file-based role management](https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html#roles-management-file) can be achieved by referencing Kubernetes secrets containing the roles specification.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  auth:
    roles:
    - secretName: my-roles-secret-1
    - secretName: my-roles-secret-2
  nodeSets:
  - name: default
    count: 1
```

Several secrets can be referenced in the Elasticsearch specification. ECK aggregates their content into a single secret, mounted in every Elasticsearch Pod.

Each secret must have a `roles.yml` entry, containing the [roles definition](https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html#roles-management-file).

If you specify multiple roles with the same name in more than one secret, the last one takes precedence.

The following Secret specifies one role named `click_admins`:

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: my-roles-secret
stringData:
  roles.yml: |-
    click_admins:
      run_as: [ 'clicks_watcher_1' ]
      cluster: [ 'monitor' ]
      indices:
      - names: [ 'events-*' ]
        privileges: [ 'read' ]
        field_security:
          grant: ['category', '@timestamp', 'message' ]
        query: '{"match": {"category": "click"}}'
```


