# Setting up field and document level security [field-and-document-access-control]

You can control access to data within a data stream or index by adding field and document level security permissions to a role. [Field level security permissions](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) restrict access to particular fields within a document. [Document level security permissions](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) restrict access to particular documents.

::::{note} 
Document and field level security is currently meant to operate with read-only privileged accounts. Users with document and field level security enabled for a data stream or index should not perform write operations.
::::


A role can define both field and document level permissions on a per-index basis. A role that doesn’t specify field level permissions grants access to ALL fields. Similarly, a role that doesn’t specify document level permissions grants access to ALL documents in the index.

::::{important} 
When assigning users multiple roles, be careful that you don’t inadvertently grant wider access than intended. Each user has a single set of field level and document level permissions per data stream or index. See [Multiple roles with document and field level security](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#multiple-roles-dls-fls).

::::


## Multiple roles with document and field level security [multiple-roles-dls-fls]

A user can have many roles and each role can define different permissions on the same data stream or index. It is important to understand the behavior of document and field level security in this scenario.

Document level security takes into account each role held by the user and combines each document level security query for a given data stream or index with an "OR". This means that only one of the role queries must match for a document to be returned. For example, if a role grants access to an index without document level security and another grants access with document level security, document level security is not applied; the user with both roles has access to all of the documents in the index.

Field level security takes into account each role the user has and combines all of the fields listed into a single set for each data stream or index. For example, if a role grants access to an index without field level security and another grants access with field level security, field level security is not be applied for that index; the user with both roles has access to all of the fields in the index.

For example, let’s say `role_a` grants access to only the `address` field of the documents in `index1`; it doesn’t specify any document restrictions. Conversely, `role_b` limits access to a subset of the documents in `index1`; it doesn’t specify any field restrictions. If you assign a user both roles, `role_a` gives the user access to all documents and `role_b` gives the user access to all fields.

::::{important} 
If you need to restrict access to both documents and fields, consider splitting documents by index instead.

::::



## Templating a role query [templating-role-query]

When you create a role, you can specify a query that defines the [document level security permissions](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md). You can optionally use Mustache templates in the role query to insert the username of the current authenticated user into the role. Like other places in {{es}} that support templating or scripting, you can specify inline, stored, or file-based templates and define custom parameters. You access the details for the current authenticated user through the `_user` parameter.

For example, the following role query uses a template to insert the username of the current authenticated user:

```console
POST /_security/role/example1
{
  "indices" : [
    {
      "names" : [ "my-index-000001" ],
      "privileges" : [ "read" ],
      "query" : {
        "template" : {
          "source" : {
            "term" : { "acl.username" : "{{_user.username}}" }
          }
        }
      }
    }
  ]
}
```

You can access the following information through the `_user` variable:

| Property | Description |
| --- | --- |
| `_user.username` | The username of the current authenticated user. |
| `_user.full_name` | If specified, the full name of the current authenticated user. |
| `_user.email` | If specified, the email of the current authenticated user. |
| `_user.roles` | If associated, a list of the role names of the current authenticated user. |
| `_user.metadata` | If specified, a hash holding custom metadata of the current authenticated user. |

You can also access custom user metadata. For example, if you maintain a `group_id` in your user metadata, you can apply document level security based on the `group.id` field in your documents:

```console
POST /_security/role/example2
{
  "indices" : [
    {
      "names" : [ "my-index-000001" ],
      "privileges" : [ "read" ],
      "query" : {
        "template" : {
          "source" : {
            "term" : { "group.id" : "{{_user.metadata.group_id}}" }
          }
        }
      }
    }
  ]
}
```

If your metadata field contains an object or array, you can access it using the `{{#toJson}}parameter{{/toJson}}` function.

```console
POST /_security/role/example3
{
  "indices" : [
    {
      "names" : [ "my-index-000001" ],
      "privileges" : [ "read" ],
      "query" : {
        "template" : {
          "source" : "{ \"terms\": { \"group.statuses\": {{#toJson}}_user.metadata.statuses{{/toJson}} }}"
        }
      }
    }
  ]
}
```


## Pre-processing documents to add security details [set-security-user-processor]

To guarantee that a user reads only their own documents, it makes sense to set up document level security. In this scenario, each document must have the username or role name associated with it, so that this information can be used by the role query for document level security. This is a situation where the [set security user processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-node-set-security-user-processor.html) ingest processor can help.

::::{note} 
Document level security doesn’t apply to write APIs. You must use unique ids for each user that uses the same data stream or index, otherwise they might overwrite other users' documents. The ingest processor just adds properties for the current authenticated user to the documents that are being indexed.
::::


The [set security user processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-node-set-security-user-processor.html) attaches user-related details (such as `username`,  `roles`, `email`, `full_name` and `metadata` ) from the current authenticated user to the current document by pre-processing the ingest. When you index data with an ingest pipeline, user details are automatically attached to the document. If the authenticating credential is an API key, the API key `id`, `name` and `metadata` (if it exists and is non-empty) are also attached to the document.

For more information see [Ingest pipelines](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) and [Set security user](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-node-set-security-user-processor.html)


## Field and document level security with Cross-cluster API keys [ccx-apikeys-dls-fls]

[Cross-Cluster API keys](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) can be used to authenticate requests to a remote cluster. The `search` parameter defines permissions for cross-cluster search. The `replication` parameter defines permissions for cross-cluster replication.

`replication` does not support any field or document level security. `search` supports field and document level security.

For reasons similar to those described in [Multiple roles with document and field level security](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#multiple-roles-dls-fls), you can’t create a single cross-cluster API key with both the `search` and `replication` parameters if the `search` parameter has document or field level security defined.

If you need to use both of these parameters, and you need to define document or field level security for the `search` parameter, create two separate cross-cluster API keys, one using the `search` parameter, and one using the `replication` parameter. You will also need to set up two different remote connections to the same cluster, with each named connection using the appropriate cross-cluster API key.


