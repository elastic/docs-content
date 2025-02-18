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


