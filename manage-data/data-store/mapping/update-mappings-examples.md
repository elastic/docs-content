---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/8.18/indices-put-mapping.html#put-mapping-api-example
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Update mapping API examples

This page provides examples of how to use the [update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) to modify index mappings after creation. 

You can learn how to:

- [Add a new field to a single index](#example-with-single-target)
- [Update multiple indices at once](#multiple-targets)
- [Add new properties to an object field](#add-new-properties-to-an-existing-object-field)
- [Enable multi-fields for an existing field](#add-multi-fields-to-an-existing-field)
- [Update supported mapping parameters](#change-supported-mapping-parameters-for-an-existing-field)
- [Change the mapping of a field using reindexing](#change-the-mapping-of-an-existing-field)
- [Rename a field using field aliases](#rename-a-field)

## Example with single target

The update mapping API requires an existing data stream or index. The following [create index](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) API request creates the `publications` index with no mapping.

```console
PUT /publications
```

The following update mapping API request adds `title`, a new [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) field, to the `publications` index.

```json
PUT /publications/_mapping
{
  "properties": {
    "title": { "type": "text" }
  }
}
```

## Multiple targets

The update mapping API can be applied to multiple data streams or indices in a single request. For example, you can update mappings for the `my-index-000001` and `my-index-000002` indices at the same time:

```json
# Create the two indices
PUT /my-index-000001
PUT /my-index-000002

# Update both mappings
PUT /my-index-000001,my-index-000002/_mapping
{
  "properties": {
    "user": {
      "properties": {
        "name": {
          "type": "keyword"
        }
      }
    }
  }
}
```

## Add new properties to an existing object field

You can use the update mapping API to add new properties to an existing [`object`](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html) field.

First, create an index with the `name` object field and an inner `first` text field:

```json
PUT /my-index-000001
{
  "mappings": {
    "properties": {
      "name": {
        "properties": {
          "first": {
            "type": "text"
          }
        }
      }
    }
  }
}
```

Then, use the update mapping API to add a new inner `last` text field to the `name` field:

```json
PUT /my-index-000001/_mapping
{
  "properties": {
    "name": {
      "properties": {
        "last": {
          "type": "text"
        }
      }
    }
  }
}
```

## Add multi-fields to an existing field

[Multi-fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html) let you index the same field in different ways. You can use the update mapping API to update the `fields` mapping parameter and enable multi-fields for an existing field.

::::{warning}
If an index (or data stream) contains documents when you add a multi-field, those documents will not have values for the new multi-field. You can populate the new multi-field with the [update by query API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update-by-query.html).
::::

To see how this works, try the following example.

Use the [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) to create an index with the `city` [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) field:

```json
PUT /my-index-000001
{
  "mappings": {
    "properties": {
      "city": {
        "type": "text"
      }
    }
  }
}
```

Enable a multi-field for `city`:

```json
PUT /my-index-000001/_mapping
{
  "properties": {
    "city": {
      "type": "text",
      "fields": {
        "raw": {
          "type": "keyword"
        }
      }
    }
  }
}
```

## Change supported mapping parameters for an existing field

Not all mapping parameters are updateable, but some like [`ignore_above`](https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-above.html) can be changed.

Create an index with `ignore_above: 20`:

```json
PUT /my-index-000001
{
  "mappings": {
    "properties": {
      "user_id": {
        "type": "keyword",
        "ignore_above": 20
      }
    }
  }
}
```

Update `ignore_above` to `100`:

```json
PUT /my-index-000001/_mapping
{
  "properties": {
    "user_id": {
      "type": "keyword",
      "ignore_above": 100
    }
  }
}
```

## Change the mapping of an existing field

You **cannot** change the field type of an existing field. Instead, create a new index with the desired mapping and [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) your data.

Create an index with a `user_id` field of type `long`:

```json
PUT /my-index-000001
{
  "mappings": {
    "properties": {
      "user_id": {
        "type": "long"
      }
    }
  }
}
```

Index some documents:

```json
POST /my-index-000001/_doc?refresh=wait_for
{
  "user_id": 12345
}

POST /my-index-000001/_doc?refresh=wait_for
{
  "user_id": 12346
}
```

Create a new index with the `user_id` field as `keyword`:

```json
PUT /my-new-index-000001
{
  "mappings": {
    "properties": {
      "user_id": {
        "type": "keyword"
      }
    }
  }
}
```

Reindex the data:

```json
POST /_reindex
{
  "source": {
    "index": "my-index-000001"
  },
  "dest": {
    "index": "my-new-index-000001"
  }
}
```

## Rename a field

You **can't** rename a field directly. Instead, use a [`field alias`](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html).

Create an index with the `user_identifier` field:

```json
PUT /my-index-000001
{
  "mappings": {
    "properties": {
      "user_identifier": {
        "type": "keyword"
      }
    }
  }
}
```

Add the `user_id` alias:

```json
PUT /my-index-000001/_mapping
{
  "properties": {
    "user_id": {
      "type": "alias",
      "path": "user_identifier"
    }
  }
}
