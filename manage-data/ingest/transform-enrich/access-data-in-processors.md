---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
description: Read and write source fields, metadata fields, and ingest metadata in ingest pipeline processors, and choose between the classic and flexible field access patterns.
type: reference
---

# Access data in processors

When you [create a pipeline](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md), you configure each processor with field names and values. Ingest processors read and write the data in each document as it passes through a pipeline. You access a field by name, so you can, for example, copy a value into another field, build a value from other fields, or route a document by changing a metadata field such as `_index`.

This page describes how to access source fields, metadata fields, and ingest metadata. For shorter ways to write field access in your processors, refer to [Create readable and maintainable ingest pipelines](/manage-data/ingest/transform-enrich/readable-maintainable-ingest-pipelines.md).

## Access source fields in a processor [access-source-fields]

Processors have read and write access to an incoming document's source fields. To access a field key in a processor, use its field name. The following `set` processor accesses `my-long-field`.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "field": "my-long-field",
        "value": 10
      }
    }
  ]
}
```

You can also prepend the `_source` prefix.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "field": "_source.my-long-field",
        "value": 10
      }
    }
  ]
}
```

Use dot notation to access object fields.

If your document contains flattened objects, use the [`dot_expander`](elasticsearch://reference/ingest-processor/dot-expand-processor.md) processor to expand them. Otherwise, processors that use the default `classic` access pattern can't access dotted field names.

{applies_to}`stack: ga 9.2+` {applies_to}`serverless: ga` To keep your document structure as is, use the [`flexible`](#access-source-pattern-flexible) access pattern in your pipeline definition instead.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "dot_expander": {
        "description": "Expand 'my-object-field.my-property'",
        "field": "my-object-field.my-property"
      }
    },
    {
      "set": {
        "description": "Set 'my-object-field.my-property' to 10",
        "field": "my-object-field.my-property",
        "value": 10
      }
    }
  ]
}
```

## Insert field values with template snippets [template-snippets]

Several processor parameters support [Mustache](https://mustache.github.io) template snippets. To access field values in a template snippet, enclose the field name in triple curly brackets: `{{{field-name}}}`. You can use template snippets to dynamically set field names.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Set dynamic '<service>' field to 'code' value",
        "field": "{{{service}}}",
        "value": "{{{code}}}"
      }
    }
  ]
}
```

## Set the field access pattern [access-source-pattern]
```{applies_to}
serverless: ga
stack: ga 9.2+
```

The field access pattern controls how processors read and write fields in a document. Set the `field_access_pattern` property on a pipeline to choose the pattern for all processors in that pipeline. It accepts two values: `classic` (the default) and `flexible`.

```console
PUT _ingest/pipeline/my-pipeline
{
  "field_access_pattern": "classic", <1>
  "processors": [
    {
      "set": {
        "description": "Set some searchable tags in our document's flattened field",
        "field": "event.tags.ingest.processed_by", <2>
        "value": "my-pipeline"
      }
    }
  ]
}
```
1. All processors in this pipeline use the `classic` access pattern.
2. The access pattern determines how the processor resolves this field path to read and write values.

### Choose an access pattern [access-source-pattern-choose]

| Access pattern | Use it when |
| --- | --- |
| `classic` | Your documents use nested objects, or your pipelines rely on processors not recognizing dotted field names. This is the default. |
| `flexible` | Your documents contain dotted field names, such as `http.host`, and you want to read them without the `dot_expander` processor. Also use it if you prefer that processors write missing fields as dotted names. |

With the `classic` pattern, the way to read dotted field names is to expand them with the `dot_expander` processor. Expanding isn't always possible, because the expanded fields can collide. Consider the following document:

```json
{
  "event": {
    "tags": {
      "http.host": "localhost:9200",
      "http.host.name": "localhost",
      "http.host.port": 9200
    }
  }
}
```

If you expand the `event.tags` field with the [`dot_expander`](elasticsearch://reference/ingest-processor/dot-expand-processor.md) processor, the field values collide. The `http.host` field can't be a text value and an object value at the same time. The `flexible` pattern reads these fields without expanding them.

### Use the classic field access pattern [access-source-pattern-classic]

With the `classic` access pattern, a processor splits a field path such as `event.tags.ingest.processed_by` on the dot character (`.`). It then uses the resulting field names to traverse the document until it finds a value. When a processor writes a value and the parent fields don't exist in the source, it creates nested objects for them.

```console
POST /_ingest/pipeline/_simulate
{
  "pipeline" : {
    "description": "example pipeline",
    "field_access_pattern": "classic", <1>
    "processors": [
      {
        "set" : {
          "description" : "Copy the foo.bar field into the a.b.c.d field if it exists",
          "copy_from" : "foo.bar", <2>
          "field" : "a.b.c.d", <3>
          "ignore_empty_value": true
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo": {
          "bar": "baz" <4>
        }
      }
    },
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo.bar": "baz" <5>
      }
    }
  ]
}
```
1. Sets the `classic` access pattern, which is the default value.
2. Reads a value from the field `foo.bar`.
3. Writes the value to the field `a.b.c.d`.
4. This document uses nested JSON objects.
5. This document uses a dotted field name.

```console-result
{
   "docs": [
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
              "foo": {
                "bar": "baz" <1>
              },
              "a": {
                "b": {
                  "c": {
                    "d": "baz" <2>
                  }
                }
              }
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.187Z"
            }
         }
      },
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
               "foo.bar": "baz" <3>
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.188Z"
            }
         }
      }
   ]
}
```
1. The processor finds the first document's `foo.bar` field because the document uses nested JSON. It looks for a `foo` field, and then a `bar` field.
2. The processor writes the value from `foo.bar` to a nested JSON structure at `a.b.c.d`, and creates an object for each field in the path.
3. The second document uses a dotted field name for `foo.bar`. The `classic` access pattern doesn't recognize dotted field names, so the processor copies nothing.

### Use the flexible field access pattern [access-source-pattern-flexible]

The `flexible` access pattern lets processors access both nested and dotted field names without the [`dot_expander`](elasticsearch://reference/ingest-processor/dot-expand-processor.md) processor. When a processor writes a value to a field that doesn't exist, it also concatenates any missing parent fields to the start of the new key.

```console
POST /_ingest/pipeline/_simulate
{
  "pipeline" : {
    "description": "example pipeline",
    "field_access_pattern": "flexible", <1>
    "processors": [
      {
        "set" : {
          "description" : "Copy the foo.bar field into the a.b.c.d field if it exists",
          "copy_from" : "foo.bar", <2>
          "field" : "a.b.c.d", <3>
          "ignore_empty_value": true
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo": {
          "bar": "baz" <4>
        },
        "a": {} <5>
      }
    },
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "foo.bar": "baz" <6>
      }
    }
  ]
}
```
1. Sets the `flexible` access pattern.
2. Reads a value from the field `foo.bar`.
3. Writes the value to the field `a.b.c.d`.
4. The first document uses nested JSON objects.
5. The first document has an existing `a` field in the root.
6. The second document uses a dotted field name.

```console-result
{
   "docs": [
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
              "foo": {
                "bar": "baz" <1>
              },
              "a": {
                "b.c.d": "baz" <2>
              }
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.187Z"
            }
         }
      },
      {
         "doc": {
            "_id": "id",
            "_index": "index",
            "_version": "-3",
            "_source": {
               "foo.bar": "baz", <3>
               "a.b.c.d": "baz" <4>
            },
            "_ingest": {
               "timestamp": "2017-05-04T22:30:03.188Z"
            }
         }
      }
   ]
}
```
1. The `flexible` access pattern supports nested object fields. The processor looks for a `foo` field, and then a `bar` field.
2. The processor writes the value from `foo.bar` to the dotted field name `b.c.d` under the field `a`. It concatenates the missing field names together as a prefix on the key.
3. The `flexible` access pattern also supports dotted field names. The processor looks for a field named `foo`, and after not finding it, looks for a field named `foo.bar`.
4. The processor writes the value from `foo.bar` to the dotted field name `a.b.c.d`. None of those fields exist in the document yet, so the processor concatenates them into a dotted field name.

## Access metadata fields in a processor [access-metadata-fields]

Processors can access metadata fields by name, including:

* `_index`
* `_id`
* `_routing`
* `_dynamic_templates`

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Set '_routing' to 'geoip.country_iso_code' value",
        "field": "_routing",
        "value": "{{{geoip.country_iso_code}}}"
      }
    }
  ]
}
```

Use a Mustache template snippet to access metadata field values. For example, `{{{_routing}}}` retrieves a document's routing value. If you [automatically generate]({{es-apis}}operation/operation-create#create-document-ids-automatically) document IDs, you can't use `{{{_id}}}` in a processor, because {{es}} assigns auto-generated `_id` values after ingest.

The following `set` processor tells {{es}} to use the dynamic template named `geo_point` for the field `address` if the index mapping doesn't define this field yet. The processor overrides the dynamic template for `address` if the bulk request already defines one, but has no effect on other dynamic templates defined in the bulk request.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Use geo_point dynamic template for address field",
        "field": "_dynamic_templates",
        "value": {
          "address": "geo_point"
        }
      }
    }
  ]
}
```

## Access ingest metadata in a processor [access-ingest-metadata]

Ingest processors can add and access ingest metadata using the `_ingest` key.

Unlike source and metadata fields, {{es}} doesn't index ingest metadata fields by default. {{es}} also allows source fields that start with an `_ingest` key. If your data includes such source fields, use `_source._ingest` to access them.

% REVIEW (SME): confirm `_ingest.pipeline` belongs in this ingest metadata text.
By default, pipelines set the `_ingest.timestamp` ingest metadata field, which contains a timestamp of when {{es}} received the document's indexing request. While a pipeline runs, `_ingest.pipeline` contains the name of the current pipeline. To index `_ingest.timestamp` or other ingest metadata fields, use the `set` processor.

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Index the ingest timestamp as 'event.ingested'",
        "field": "event.ingested",
        "value": "{{{_ingest.timestamp}}}"
      }
    }
  ]
}
```

## Related pages

* [Conditionally run processors and pipelines](/manage-data/ingest/transform-enrich/conditionally-run-ingest-processors.md)
* [Error handling](/manage-data/ingest/transform-enrich/error-handling.md)
* [Create readable and maintainable ingest pipelines](/manage-data/ingest/transform-enrich/readable-maintainable-ingest-pipelines.md)
