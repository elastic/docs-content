---
applies_to:
  stack:
navigation_title: "Error: Failed to parse field of type in document with id"
---

# Fix error: Failed to parse field [failed-to-parse-field-of-type]

```console
Error: failed to parse field [field] of type [type] in document with id [id]
```

This error occurs when you try to index a document, but one of the field values doesn't match the expected data type. {{es}} rejects the document when it encounters incompatible values, like a string in a numeric field or an invalid IP address.

To fix this issue, make sure each field value matches the data type defined in the mapping.

## Field types and mapping

When no explicit mapping exists, {{es}} uses [dynamic mappings](../../manage-data/data-store/mapping/dynamic-field-mapping.md) to infer a field's type based on the **first value indexed**.

For example, if you index:

```console
PUT test/_doc/1
{
  "ip_address": "179.152.62.82",
  "boolean_field": "off"
}
```

Without explicit mapping, {{es}} will treat `ip_address` and `boolean_field` as `text`, which might not be the intended result. 

To avoid this, define the mapping explicitly:

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

To check the data type of the field causing the error, first get the mapping:

    ```console
        GET your-index-name/_mapping
    ```

Make sure the incoming data matches the expected type. If not, you'll need to fix the data or update the mapping. If necessary, create a new index with the correct mapping and reindex your data.