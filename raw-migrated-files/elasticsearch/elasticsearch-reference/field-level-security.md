# Field level security [field-level-security]

Field level security restricts the fields that users have read access to. In particular, it restricts which fields can be accessed from document-based read APIs.

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
Field-level security should not be set on [`alias`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/field-alias.md) fields. To secure a concrete field, its field name must be used directly.
::::


For more information, see [Setting up field and document level security](../../../deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md).

