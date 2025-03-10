---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/document-level-security.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/field-level-security.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/field-and-document-access-control.html
applies_to:
  deployment:
    ece:
    eck:
    ess:
    self:
navigation_title: Control access at the document and field level
---

# Controlling access at the document and field level [field-and-document-access-control]

You can control access to data within a data stream or index by adding field and document level security permissions to a  role.

**Field level security** restricts the fields that users have read access to. In particular, it restricts which fields can be accessed from document-based read APIs.

**Document level security** restricts the documents that users have read access to. In particular, it restricts which documents can be accessed from document-based read APIs.

::::{note}
Document and field level security is currently meant to operate with read-only privileged accounts. Users with document and field level security enabled for a data stream or index should not perform write operations.
::::

A role can define both field and document level permissions on a per-index basis. A role that doesn’t specify field level permissions grants access to ALL fields. Similarly, a role that doesn’t specify document level permissions grants access to ALL documents in the index.

On this page, you'll learn how to implement [document level security](#document-level-security) and [field level security](#field-level-security).

You'll also learn the following:
* How [multiple roles with document and field level security](#multiple-roles-dls-fls) interact
* Considerations for using document and field level security when [searching across clusters using cross-cluster API keys](#ccx-apikeys-dls-fls).

The examples on this page use the [Role management API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security). However, you can add document and field level security [anywhere you manage custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#managing-custom-roles).


:::{{admonition}} Document and field level security in {{serverless-full}}
This topic explains how to apply document and field level security in {{stack}}. You can also apply document and field level security in {{serverless-full}} projects.

In {{serverless-full}}, you can only manage document and field level security using the {{ecloud}} console. However, document level security is still managed using queries, and you can use the queries on this page as a guideline.

[Learn more](/deploy-manage/users-roles/serverless-custom-roles.md#document-level-and-field-level-security).
:::

## Document level security [document-level-security]

You can use a query to specify the documents that each role can access. The document query is associated with a particular data stream, index, or wildcard (`*`) pattern and operates in conjunction with the privileges specified for the data streams and indices.

The specified document query:

* Expects the same format as if it was defined in the search request
* Supports [templating a role query](#templating-role-query) that can access the details of the currently authenticated user
* Accepts queries written as either string values or nested JSON
* Supports the majority of the {{es}} [Query DSL](/explore-analyze/query-filter/languages/querydsl.md), with [some limitations](../../../deploy-manage/security.md#field-document-limitations) for field and document level security

::::{important}
Omitting the `query` parameter entirely disables document level security for the respective indices permission entry.
::::

### Basic examples

The following role definition grants read access only to documents that belong to the `click` category within all the `events-*` data streams and indices:

```console
POST /_security/role/click_role
{
  "indices": [
    {
      "names": [ "events-*" ],
      "privileges": [ "read" ],
      "query": "{\"match\": {\"category\": \"click\"}}"
    }
  ]
}
```

You can write this same query using nested JSON syntax:

```console
POST _security/role/click_role
{
  "indices": [
    {
      "names": [ "events-*" ],
      "privileges": [ "read" ],
      "query": {
        "match": {
          "category": "click"
        }
      }
    }
  ]
}
```

The following role grants read access only to the documents whose `department_id` equals `12`:

```console
POST /_security/role/dept_role
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "query" : {
        "term" : { "department_id" : 12 }
      }
    }
  ]
}
```

### Templating a role query [templating-role-query]

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

### Pre-processing documents to add security details [set-security-user-processor]

To guarantee that a user reads only their own documents, it makes sense to set up document level security. In this scenario, each document must have the username or role name associated with it, so that this information can be used by the role query for document level security. This is a situation where the [set security user processor](elasticsearch://reference/ingestion-tools/enrich-processor/ingest-node-set-security-user-processor.md) ingest processor can help.

::::{note}
Document level security doesn’t apply to write APIs. You must use unique ids for each user that uses the same data stream or index, otherwise they might overwrite other users' documents. The ingest processor just adds properties for the current authenticated user to the documents that are being indexed.
::::

The [set security user processor](elasticsearch://reference/ingestion-tools/enrich-processor/ingest-node-set-security-user-processor.md) attaches user-related details (such as `username`,  `roles`, `email`, `full_name` and `metadata` ) from the current authenticated user to the current document by pre-processing the ingest. When you index data with an ingest pipeline, user details are automatically attached to the document. If the authenticating credential is an API key, the API key `id`, `name` and `metadata` (if it exists and is non-empty) are also attached to the document.

For more information, see [Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) and [Set security user](elasticsearch://reference/ingestion-tools/enrich-processor/ingest-node-set-security-user-processor.md).


## Field level security [field-level-security]

To enable field level security, specify the fields that each role can access as part of the indices permissions in a role definition. Field level security is thus bound to a well-defined set of data streams or indices (and potentially a set of [documents](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md)).

The following role definition grants read access only to the `category`, `@timestamp`, and `message` fields in all the `events-*` data streams and indices.

```console
POST /_security/role/test_role1
{
  "indices": [
    {
      "names": [ "events-*" ],
      "privileges": [ "read" ],
      "field_security" : {
        "grant" : [ "category", "@timestamp", "message" ]
      }
    }
  ]
}
```

Access to the following metadata fields is always allowed: `_id`, `_type`, `_parent`, `_routing`, `_timestamp`, `_ttl`, `_size` and `_index`. If you specify an empty list of fields, only these metadata fields are accessible.

::::{note}
Omitting the fields entry entirely disables field level security.
::::


You can also specify field expressions. For example, the following example grants read access to all fields that start with an `event_` prefix:

```console
POST /_security/role/test_role2
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "grant" : [ "event_*" ]
      }
    }
  ]
}
```

Use the dot notations to refer to nested fields in more complex documents. For example, assuming the following document:

```js
{
  "customer": {
    "handle": "Jim",
    "email": "jim@mycompany.com",
    "phone": "555-555-5555"
  }
}
```
%  NOTCONSOLE

The following role definition enables only read access to the customer `handle` field:

```console
POST /_security/role/test_role3
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "grant" : [ "customer.handle" ]
      }
    }
  ]
}
```

This is where wildcard support shines. For example, use `customer.*` to enable only read access to the `customer` data:

```console
POST /_security/role/test_role4
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "grant" : [ "customer.*" ]
      }
    }
  ]
}
```

You can deny permission to access fields with the following syntax:

```console
POST /_security/role/test_role5
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "grant" : [ "*"],
        "except": [ "customer.handle" ]
      }
    }
  ]
}
```

The following rules apply:

* The absence of `field_security` in a role is equivalent to * access.
* If permission has been granted explicitly to some fields, you can specify denied fields. The denied fields must be a subset of the fields to which permissions were granted.
* Defining denied and granted fields implies access to all granted fields except those which match the pattern in the denied fields.

For example:

```console
POST /_security/role/test_role6
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "except": [ "customer.handle" ],
        "grant" : [ "customer.*" ]
      }
    }
  ]
}
```

In the above example, users can read all fields with the prefix "customer." except for "customer.handle".

An empty array for `grant` (for example, `"grant" : []`) means that access has not been granted to any fields.

When a user has several roles that specify field level permissions, the resulting field level permissions per data stream or index are the union of the individual role permissions. For example, if these two roles are merged:

```console
POST /_security/role/test_role7
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "grant": [ "a.*" ],
        "except" : [ "a.b*" ]
      }
    }
  ]
}

POST /_security/role/test_role8
{
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "grant": [ "a.b*" ],
        "except" : [ "a.b.c*" ]
      }
    }
  ]
}
```

The resulting permission is equal to:

```js
{
  // role 1 + role 2
  ...
  "indices" : [
    {
      "names" : [ "*" ],
      "privileges" : [ "read" ],
      "field_security" : {
        "grant": [ "a.*" ],
        "except" : [ "a.b.c*" ]
      }
    }
  ]
}
```

::::{note}
Field-level security should not be set on [`alias`](elasticsearch://reference/elasticsearch/mapping-reference/field-alias.md) fields. To secure a concrete field, its field name must be used directly.
::::

## Multiple roles with document and field level security [multiple-roles-dls-fls]

A user can have many roles and each role can define different permissions on the same data stream or index. When assigning users multiple roles, be careful that you don’t inadvertently grant wider access than intended.

**Document level security** takes into account each role held by the user and combines each document level security query for a given data stream or index with an "OR". This means that only one of the role queries must match for a document to be returned. For example, if a role grants access to an index without document level security and another grants access with document level security, document level security is not applied; the user with both roles has access to all of the documents in the index.

**Field level security** takes into account each role the user has and combines all of the fields listed into a single set for each data stream or index. For example, if a role grants access to an index without field level security and another grants access with field level security, field level security is not be applied for that index; the user with both roles has access to all of the fields in the index.

For example, let’s say `role_a` grants access to only the `address` field of the documents in `index1`; it doesn’t specify any document restrictions. Conversely, `role_b` limits access to a subset of the documents in `index1`; it doesn’t specify any field restrictions. If you assign a user both roles, `role_a` gives the user access to all documents and `role_b` gives the user access to all fields.

::::{important}
If you need to restrict access to both documents and fields, consider splitting documents by index instead.
::::

## Field and document level security with Cross-cluster API keys [ccx-apikeys-dls-fls]

[Cross-cluster API keys](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) can be used to authenticate requests to a remote cluster. The `search` parameter defines permissions for cross-cluster search. The `replication` parameter defines permissions for cross-cluster replication.

`replication` does not support any field or document level security. `search` supports field and document level security.

For reasons similar to those described in [Multiple roles with document and field level security](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md#multiple-roles-dls-fls), you can’t create a single cross-cluster API key with both the `search` and `replication` parameters if the `search` parameter has document or field level security defined.

If you need to use both of these parameters, and you need to define document or field level security for the `search` parameter, create two separate cross-cluster API keys, one using the `search` parameter, and one using the `replication` parameter. You will also need to set up two different remote connections to the same cluster, with each named connection using the appropriate cross-cluster API key.

## Limitations

::::{include} /deploy-manage/_snippets/field-doc-sec-limitations.md
::::
