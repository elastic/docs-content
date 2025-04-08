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
This error occurs when you try to index a document into an existing index, a field value doesn't match the expected data types in the mapping. Elasticsearch rejects the document when it encounters incompatible values like a string in a numeric field or an invalid IP address. When this happens, Elasticsearch is unable to process the document and rejects it. 

## Understand field types and mapping

### Implicit vs. explicit mapping

Elasticsearch can assign field types automatically using a feature called dynamic mapping, which infers the type of a field based on the first value indexed. Alternatively, you can define field types explicitly in the index mapping before indexing any documents, which gives you full control over how data is stored and queried.

#### Example: dynamic mapping

```console
PUT test/_doc/1
{
  "non_existent_field_1": "some text",
  "non_existent_field_2": 123,
  "non_existent_field_3": true
}
```

Check how Elasticsearch inferred the types:

```console
GET test/_mapping
```

This might return:

```console-result
{
  "test": {
    "mappings": {
      "properties": {
        "non_existent_field_1": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "non_existent_field_2": { "type": "long" },
        "non_existent_field_3": { "type": "boolean" }
      }
    }
  }
}
```

To avoid inference errors, define fields explicitly:

```console
PUT test
{
  "mappings": {
    "properties": {
      "description": { "type": "text" },
      "username": { "type": "keyword" },
      "age": { "type": "byte" },
      "location": { "type": "geo_point" },
      "source_ip": { "type": "ip" }
    }
  }
}
```

## Troubleshoot and resolve the error

If you’re seeing the error `failed to parse field [field] of type [type] in document with id [id]`, Elasticsearch is telling you it couldn’t convert the data you submitted into the expected type. The document was rejected, and the underlying issue is usually a mismatch between the field’s mapping and the actual data.

Here’s how to debug and fix it.

### Step 1: Confirm the field’s expected type
Use the mapping API to inspect how Elasticsearch expects the field to be structured:

```console
GET your-index-name/_mapping
```

Look for the exact type of the problematic field. You may find it was auto-mapped as something too permissive (like `text`) or too strict (like `byte`).

### Step 2: Review the rejected document
Double-check the value you tried to index. Is it a number where only text is allowed? Is it a string that should be an IP address?

Here’s an example where multiple field types are violated:

```console
PUT test/_doc/1
{
  "boolean_field": "off",
  "byte_field": "not a number",
  "ip_field": "355.255.255.255"
}
```

```console-result
{
  "error": {
    "type": "mapper_parsing_exception",
    "reason": "failed to parse field [boolean_field] of type [boolean] in document with id '1'. Preview of field's value: 'off'",
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Failed to parse value [off] as only [true] or [false] are allowed."
    }
  },
  "status": 400
}
```

To catch all issues, simplify your test case and test fields individually.

### Step 3: Check for unexpected string coercion
This is common when working with fields that seem valid but are interpreted incorrectly.

Example:

```console
PUT test1/_doc/1
{
  "my_ip_address": "179.152.62.82",
  "my_location": "-30.0346471,-51.2176584"
}
```

Unless you explicitly defined these fields as `ip` and `geo_point`, Elasticsearch will treat them as strings.

Use the mapping API to confirm:

```console
GET test1/_mapping
```

If both fields are mapped as `text`, you’ll need to remap them:

```console
PUT test2
{
  "mappings": {
    "properties": {
      "my_ip_address": { "type": "ip" },
      "my_location": { "type": "geo_point" }
    }
  }
}

PUT test2/_doc/1
{
  "my_ip_address": "179.152.62.82",
  "my_location": "-30.0346471,-51.2176584"
}
```

Now Elasticsearch can validate the data correctly.

### Step 4: Decide what to fix—your mapping or your data
If the data is coming from a reliable source but varies in format (e.g., numbers in strings, booleans as 1/0), consider normalizing the data before indexing.

If the field’s current type is too restrictive for real-world input, you may need to remap it—changing `byte` to `integer`, for example. This requires creating a new index and reindexing your data.

### Step 5: Monitor for recurring issues
- Use ingest pipelines or external validators to catch formatting issues early.
- If you work with semi-structured data, prefer explicit mappings over dynamic ones.
- Keep your mapping definitions as close to your actual data as possible.

Solving this error often comes down to knowing your data and mapping structure—and making sure they play nicely together.

- Double-check the field type’s [official documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).
- Consider adjusting the mapping to a more appropriate type (e.g., switch `byte` to `short`).
- Ensure incoming data from different sources is clean and consistently formatted.
- Validate and sanitize data before indexing.