---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-users-and-roles.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html
  - https://www.elastic.co/guide/en/kibana/current/tutorial-secure-access-to-kibana.html
  - https://www.elastic.co/guide/en/kibana/current/kibana-role-management.html
applies_to:
  deployment:
    ece:
    ess:
    eck:
    self:
products:
  - id: elasticsearch
  - id: cloud-kubernetes
  - id: kibana
---

# Defining roles [defining-roles]

If [built-in roles](elasticsearch://reference/elasticsearch/roles.md) do not address your use case, then you can create additional custom roles.

In this section, you'll learn about the [data structure of a role](#role-structure), and about the [methods for defining and managing custom roles](#managing-custom-roles).

You can also implement custom roles providers. If you need to integrate with another system to retrieve user roles, you can build a custom roles provider plugin. For more information, see [](/deploy-manage/users-roles/cluster-or-deployment-auth/authorization-plugins.md).

After you create your custom roles, you can [learn how to assign them to users](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md#assign-roles-to-users).

## Role structure

% temporary anchors

$$$roles-indices-priv$$$
$$$roles-global-priv$$$
$$$roles-application-priv$$$
$$$roles-remote-indices-priv$$$
$$$roles-remote-cluster-priv$$$

Custom roles follow a strict data structure. If you're working with custom roles using the role management API or role files, then you need to understand and follow the structure when parsing role information or making changes.

[Learn about the data structure of a role and its entries](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md).

:::{{note}}
You don't need to use this structure when interacting with roles using the role management UI.
:::

## Managing custom roles

You can manage custom roles using the following methods:

* Using the {{kib}} [role management UI](#roles-management-ui)
* Using [role management APIs](#roles-management-api)
* Using [local files](#roles-management-file).

When you use the UI or APIs to manage roles, the roles are stored in an internal {{es}} index. When you use local files, the roles are only stored in those files.

### Role management UI [roles-management-ui]
$$$adding_kibana_privileges$$$

You can manage users and roles easily in {{kib}}.

To manage roles, log in to {{kib}} and go to **Management > Security > Roles**.

[Learn more about using the role management UI](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md).

### Role management API [roles-management-api]

The Role Management APIs enable you to add, update, remove and retrieve roles dynamically. For more information and examples, see [Roles](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security).


### File-based role management [roles-management-file]

```{applies_to}
deployment:
  self:
  eck:
```

Roles can also be defined in local `roles.yml` file. This is a YAML file where each role definition is keyed by its name.

::::{important}
If the same role name is used in the `roles.yml` file and through role management APIs, the role found in the file will be used.

::::


While role management APIs and the role management UI are the preferred mechanism to define roles, using the `roles.yml` file becomes useful if you want to define fixed roles that no one, beside an administrator having access to the {{es}} nodes or Kubernetes cluster, would be able to change. However, the `roles.yml` file is provided as a minimal administrative function and is not intended to cover and be used to define roles for all use cases.

::::{important}
You can't view, edit, or remove any roles that are defined in `roles.yml` by using the role management UI or the role management APIs.
::::

The following snippet shows an example of the `roles.yml` file configuration, specifying one role named `click_admins`:

```yaml
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

To configure file-based role management:

::::{tab-set}
:::{tab-item} Self hosted

Place the `roles.yml` file in `ES_PATH_CONF`. {{es}} continuously monitors the `roles.yml` file and automatically picks up and applies any changes to it.

The `roles.yml` file is managed locally by the node and is not globally by the cluster. This means that with a typical multi-node cluster, the exact same changes need to be applied on each and every node in the cluster.

A safer approach would be to apply the change on one of the nodes and have the `roles.yml` distributed/copied to all other nodes in the cluster (either manually or using a configuration management system such as Puppet or Chef).
:::
:::{tab-item} ECK

You can set up file-based role management in {{eck}} by referencing Kubernetes secrets containing the roles specification.

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

Several secrets can be referenced in the {{es}} specification. ECK aggregates their content into a single secret, mounted in every {{es}} Pod.

Each secret must have a `roles.yml` entry, containing the roles definition.

If you specify multiple roles with the same name in more than one secret, the last one takes precedence.

The following Secret applies the same `roles.yml` configuration, specifying one role named `click_admins`:

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
:::
::::