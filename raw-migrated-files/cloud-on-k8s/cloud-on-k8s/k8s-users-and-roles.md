# Users and roles [k8s-users-and-roles]

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


