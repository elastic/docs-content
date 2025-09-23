---
applies_to:
  deployment:
    ece:
    ess:
    eck:
    self:
---

# Role structure

A role is defined by the following JSON structure:

```js
{
  "run_as": [ ... ], <1>
  "cluster": [ ... ], <2>
  "global": { ... }, <3>
  "indices": [ ... ], <4>
  "applications": [ ... ], <5>
  "remote_indices": [ ... ], <6>
  "remote_cluster": [ ... ], <7>
  "metadata": { ... }, <8>
  "description": "..." <9>
}
```

1. A list of usernames the owners of this role can [impersonate](/deploy-manage/users-roles/cluster-or-deployment-auth/submitting-requests-on-behalf-of-other-users.md).
2. A list of cluster privileges. These privileges define the cluster level actions users with this role are able to execute.

   This field is optional (missing `cluster` privileges effectively mean no cluster level permissions).
3. An object defining global privileges. A global privilege is a form of cluster privilege that is request sensitive. A standard cluster privilege makes authorization decisions based solely on the action being executed. A global privilege also considers the parameters included in the request. Support for global privileges is currently limited to the management of application privileges. This field is optional.
4. A list of indices permissions entries.

   This field is optional (missing `indices` privileges effectively mean no index level permissions).
5. A list of application privilege entries. This field is optional.
6. A list of indices permissions entries for [remote clusters configured with the API key based model](/deploy-manage/remote-clusters/remote-clusters-api-key.md).

   This field is optional (missing `remote_indices` privileges effectively mean no index level permissions for any API key based remote clusters).
7. A list of cluster permissions entries for [remote clusters configured with the API key based model](/deploy-manage/remote-clusters/remote-clusters-api-key.md).

   This field is optional (missing `remote_cluster` privileges effectively means no additional cluster permissions for any API key based remote clusters).
8. Metadata field associated with the role, such as `metadata.app_tag`. Metadata is internally indexed as a [flattened](elasticsearch://reference/elasticsearch/mapping-reference/flattened.md) field type. This means that all sub-fields act like `keyword` fields when querying and sorting. Metadata values can be simple values, but also lists and maps. This field is optional.
9.  A string value with the description text of the role. The maximum length of it is `1000` chars. The field is internally indexed as a [text](elasticsearch://reference/elasticsearch/mapping-reference/text.md#text-field-type) field type (with default values for all parameters). This field is optional.


::::{note}
:name: valid-role-name

Role names must be at least 1 and no more than 507 characters. They can contain alphanumeric characters (`a-z`, `A-Z`, `0-9`), spaces, punctuation, and printable symbols in the [Basic Latin (ASCII) block](https://en.wikipedia.org/wiki/Basic_Latin_(Unicode_block)). Leading or trailing whitespace is not allowed.
::::


## Indices privileges [roles-indices-priv]

The following describes the structure of an indices permissions entry:

```js
{
  "names": [ ... ], <1>
  "privileges": [ ... ], <2>
  "field_security" : { ... }, <3>
  "query": "...", <4>
  "allow_restricted_indices": false <5>
}
```

1. A list of data streams, indices, and aliases to which the permissions in this entry apply. Supports wildcards (`*`).
2. The index level privileges the owners of the role have on the associated data streams and indices specified in the `names` argument.
3. Specification for document fields the owners of the role have read access to. See [Setting up field and document level security](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) for details.
4. A search query that defines the documents the owners of the role have read access to. A document within the associated data streams and indices must match this query in order for it to be accessible by the owners of the role.
5. Restricted indices are a special category of indices that are used internally to store configuration data and should not be directly accessed. Only internal system roles should normally grant privileges over the restricted indices. **Toggling this flag is very strongly discouraged because it could effectively grant unrestricted operations on critical data, making the entire system unstable or leaking sensitive information.** If however, for administrative purposes, you need to create a role with privileges covering restricted indices, you must set this field to `true` (default is `false`), and then the `names` field will cover the restricted indices as well.


::::{admonition} Using wildcards and regex
The `names` parameter accepts wildcard and regular expressions that may refer to multiple data streams, indices, and aliases.

* Wildcard (default): Simple wildcard matching where `*` is a placeholder for zero or more characters, `?` is a placeholder for a single character and `\` may be used as an escape character.
* Regular Expressions: A more powerful syntax for matching more complex patterns. This regular expression is based on Lucene’s regexp automaton syntax. To enable this syntax, it must be wrapped within a pair of forward slashes (`/`). Any pattern starting with `/` and not ending with `/` is considered to be malformed.

```js
"foo-bar": <1>
"foo-*": <2>
"logstash-201?-*": <3>
"/.*-201[0-9]-.*/": <4>
"/foo": <5>
```
1. Match the literal `foo-bar`
2. Match anything beginning with "foo-"
3. `?` matches any one character
4. Use a regex to match anything containing 2010-2019
5. syntax error - missing final `/`
::::


## Global privileges [roles-global-priv]

The following describes the structure of the global privileges entry:

```js
{
  "application": {
    "manage": {    <1>
      "applications": [ ... ] <2>
    }
  },
  "profile": {
    "write": { <3>
      "applications": [ ... ] <4>
    }
  }
}
```

1. The privilege for the ability to manage application privileges
2. The list of application names that may be managed. This list supports wildcards (e.g. `"myapp-*"`) and regular expressions (e.g. `"/app[0-9]*/"`)
3. The privilege for the ability to write the `access` and `data` of any user profile
4. The list of names, wildcards and regular expressions to which the write privilege is restricted to

## Application privileges [roles-application-priv]

The following describes the structure of an application privileges entry:

```js
{
  "application": "my_app", <1>
  "privileges": [ ... ],   <2>
  "resources": [ ... ]     <3>
}
```

1. The name of the application.
2. The list of the names of the application privileges to grant to this role.
3. The resources to which those privileges apply. These are handled in the same way as index name pattern in `indices` permissions. These resources do not have any special meaning to the {{es}} {{security-features}}.

For details about the validation rules for these fields, see the [add application privileges API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-privileges).

A role may refer to application privileges that do not exist - that is, they have not yet been defined through the add application privileges API (or they were defined, but have since been deleted). In this case, the privilege has no effect, and will not grant any actions in the [has privileges API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-has-privileges).


## Remote indices privileges [roles-remote-indices-priv]

For [remote clusters configured with the API key based model](/deploy-manage/remote-clusters/remote-clusters-api-key.md), remote indices privileges can be used to specify desired indices privileges for matching remote clusters. The final effective index privileges will be an intersection of the remote indices privileges and the [cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key)'s indices privileges.

::::{note}
Remote indices are effective for remote clusters configured with the API key based model. They have no effect for remote clusters configured with the certificate based model.
::::


The remote indices privileges entry has an extra mandatory `clusters` field compared to an [indices privileges entry](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-indices-priv). Otherwise the two have identical structure. The following describes the structure of a remote indices permissions entry:

```js
{
  "clusters": [ ... ], <1>
  "names": [ ... ], <2>
  "privileges": [ ... ], <3>
  "field_security" : { ... }, <4>
  "query": "...", <5>
  "allow_restricted_indices": false <6>
}
```

1. A list of remote cluster aliases. It supports literal strings as well as [wildcards](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index) and [regular expressions](elasticsearch://reference/query-languages/query-dsl/regexp-syntax.md). This field is required.
2. A list of data streams, indices, and aliases to which the permissions in this entry apply. Supports wildcards (`*`).
3. The index level privileges the owners of the role have on the associated data streams and indices specified in the `names` argument.
4. Specification for document fields the owners of the role have read access to. See [Setting up field and document level security](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) for details.
5. A search query that defines the documents the owners of the role have read access to. A document within the associated data streams and indices must match this query in order for it to be accessible by the owners of the role.
6. Restricted indices are a special category of indices that are used internally to store configuration data and should not be directly accessed. Only internal system roles should normally grant privileges over the restricted indices. **Toggling this flag is very strongly discouraged because it could effectively grant unrestricted operations on critical data, making the entire system unstable or leaking sensitive information.** If however, for administrative purposes, you need to create a role with privileges covering restricted indices, you must set this field to `true` (default is `false`), and then the `names` field will cover the restricted indices as well.


## Remote cluster privileges [roles-remote-cluster-priv]

For [remote clusters configured with the API key based model](/deploy-manage/remote-clusters/remote-clusters-api-key.md), remote cluster privileges can be used to specify additional cluster privileges for matching remote clusters.

::::{note}
Remote cluster privileges are only effective for remote clusters configured with the API key based model. They have no effect on remote clusters configured with the certificate based model.
::::


The following describes the structure of a remote cluster permissions entry:

```js
{
  "clusters": [ ... ], <1>
  "privileges": [ ... ] <2>
}
```

1. A list of remote cluster aliases. It supports literal strings as well as [wildcards](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index) and [regular expressions](elasticsearch://reference/query-languages/query-dsl/regexp-syntax.md). This field is required.
2. The cluster level privileges for the remote cluster. The allowed values here are a subset of the [cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster). The [builtin privileges API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-builtin-privileges) can be used to determine which privileges are allowed here. This field is required.


## Example [_example_9]

The following snippet shows an example definition of a `clicks_admin` role:

```console
POST /_security/role/clicks_admin
{
  "run_as": [ "clicks_watcher_1" ],
  "cluster": [ "monitor" ],
  "indices": [
    {
      "names": [ "events-*" ],
      "privileges": [ "read" ],
      "field_security" : {
        "grant" : [ "category", "@timestamp", "message" ]
      },
      "query": "{\"match\": {\"category\": \"click\"}}"
    }
  ]
}
```

Based on the above definition, users owning the `clicks_admin` role can:

* Impersonate the `clicks_watcher_1` user and execute requests on its behalf.
* Monitor the {{es}} cluster
* Read data from all indices prefixed with `events-`
* Within these indices, only read the events of the `click` category
* Within these document, only read the `category`, `@timestamp` and `message` fields.

::::{tip}
View a complete list of available [cluster and indices privileges](elasticsearch://reference/elasticsearch/security-privileges.md).
::::