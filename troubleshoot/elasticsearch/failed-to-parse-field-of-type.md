---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: failed to parse field of type in document with id"
# is mapped_pages needed for newly created docs?
---

# Fix failed to parse field of type in document with id [failed-to-parse-field-of-type]

```console
Error: failed to parse field [field] of type [type] in document with id [id]
```

This error occurs when you try to index a document into an existing index, and one of your fields' values doesn't match the expected data type. {{es}} rejects the document when it encounters incompatible values, like a string in a numeric field or an invalid IP address.

To fix, ensure the field's value matches the expected data type in the mapping.

## Understand field types and mapping

By default, {{es}} uses [dynamic mappings](../../manage-data/data-store/mapping/dynamic-mapping.md) to infer a field's type based on the **first value indexed** when no explicit mapping exists.

For example, if you index:

```console
PUT test/_doc/1
{
  "ip_address": "179.152.62.82",
  "boolean_field": "off"
}
```

Without explicit mapping, {{es}} will treat `ip_address` and `boolean_field` as `text` which may not be what is intended. 

To avoid this, define your mapping explicitly:

```console
PUT test
{
  "mappings": {
    "properties": {
      "ip_address": { "type": "ip" },
      "boolean_field": { "type": "boolean" }
    }
  }
}
```

## Troubleshoot and resolve the error

1. Check the mapping of your index:

```console
GET your-index-name/_mapping
```

2. Confirm the data type of the field causing the error.

3. Ensure the incoming data matches the expected type.

4. If necessary, create a new index with the correct mapping and reindex your data.
