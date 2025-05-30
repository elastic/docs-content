---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-templates.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Dynamic templates [dynamic-templates]

Dynamic templates allow you greater control over how {{es}} maps your data beyond the default [dynamic field mapping rules](dynamic-field-mapping.md). You enable dynamic mapping by setting the dynamic parameter to `true` or `runtime`. You can then use dynamic templates to define custom mappings that can be applied to dynamically added fields based on the matching condition:

* [`match_mapping_type` and `unmatch_mapping_type`](#match-mapping-type) operate on the data type that {{es}} detects
* [`match` and `unmatch`](#match-unmatch) use a pattern to match on the field name
* [`path_match` and `path_unmatch`](#path-match-unmatch) operate on the full dotted path to the field
* If a dynamic template doesn’t define `match_mapping_type`, `match`, or `path_match`, it won’t match any field. You can still refer to the template by name in `dynamic_templates` section of a [bulk request](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings).

Use the `{{name}}` and `{{dynamic_type}}` [template variables](#template-variables) in the mapping specification as placeholders.

::::{important}
Dynamic field mappings are only added when a field contains a concrete value. {{es}} doesn’t add a dynamic field mapping when the field contains `null` or an empty array. If the `null_value` option is used in a `dynamic_template`, it will only be applied after the first document with a concrete value for the field has been indexed.
::::


Dynamic templates are specified as an array of named objects:

```js
  "dynamic_templates": [
    {
      "my_template_name": { <1>
        ... match conditions ... <2>
        "mapping": { ... } <3>
      }
    },
    ...
  ]
```

1. The template name can be any string value.
2. The match conditions can include any of : `match_mapping_type`, `match`, `match_pattern`, `unmatch`, `path_match`, `path_unmatch`.
3. The mapping that the matched field should use.


## Validating dynamic templates [dynamic-templates-validation]

If a provided mapping contains an invalid mapping snippet, a validation error is returned. Validation occurs when applying the dynamic template at index time, and, in most cases, when the dynamic template is updated. Providing an invalid mapping snippet may cause the update or validation of a dynamic template to fail under certain conditions:

* If no `match_mapping_type` has been specified but the template is valid for at least one predefined mapping type, the mapping snippet is considered valid. However, a validation error is returned at index time if a field matching the template is indexed as a different type. For example, configuring a dynamic template with no `match_mapping_type` is considered valid as string type, but if a field matching the dynamic template is indexed as a long, a validation error is returned at index time. It is recommended to configure the `match_mapping_type` to the expected JSON type or configure the desired `type` in the mapping snippet.
* If the `{{name}}` placeholder is used in the mapping snippet, validation is skipped when updating the dynamic template. This is because the field name is unknown at that time. Instead, validation occurs when the template is applied at index time.

Templates are processed in order — the first matching template wins. When putting new dynamic templates through the [update mapping](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) API, all existing templates are overwritten. This allows for dynamic templates to be reordered or deleted after they were initially added.


## Mapping runtime fields in a dynamic template [dynamic-mapping-runtime-fields]

If you want {{es}} to dynamically map new fields of a certain type as runtime fields, set `"dynamic":"runtime"` in the index mappings. These fields are not indexed, and are loaded from `_source` at query time.

Alternatively, you can use the default dynamic mapping rules and then create dynamic templates to map specific fields as runtime fields. You set `"dynamic":"true"` in your index mapping, and then create a dynamic template to map new fields of a certain type as runtime fields.

Let’s say you have data where each of the fields start with `ip_`. Based on the [dynamic mapping rules](#match-mapping-type), {{es}} maps any `string` that passes `numeric` detection as a `float` or `long`. However, you can create a dynamic template that maps new strings as runtime fields of type `ip`.

The following request defines a dynamic template named `strings_as_ip`. When {{es}} detects new `string` fields matching the `ip*` pattern, it maps those fields as runtime fields of type `ip`. Because `ip` fields aren’t mapped dynamically, you can use this template with either `"dynamic":"true"` or `"dynamic":"runtime"`.

```console
PUT my-index-000001/
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_as_ip": {
          "match_mapping_type": "string",
          "match": "ip*",
          "runtime": {
            "type": "ip"
          }
        }
      }
    ]
  }
}
```

See [this example](#text-only-mappings-strings) for how to use dynamic templates to map `string` fields as either indexed fields or runtime fields.


## `match_mapping_type` and `unmatch_mapping_type` [match-mapping-type]

The `match_mapping_type` parameter matches fields by the data type detected by the JSON parser, while `unmatch_mapping_type` excludes fields based on the data type.

Because JSON doesn’t distinguish a `long` from an `integer` or a `double` from a `float`, any parsed floating point number is considered a `double` JSON data type, while any parsed `integer` number is considered a `long`.

::::{note}
With dynamic mappings, {{es}} will always choose the wider data type. The one exception is `float`, which requires less storage space than `double` and is precise enough for most applications. Runtime fields do not support `float`, which is why `"dynamic":"runtime"` uses `double`.
::::


{{es}} automatically detects the following data types:

|     |     |
| --- | --- |
|  | {{es}} data type |
| JSON data type | `"dynamic":"true"` | `"dynamic":"runtime"` |
| `null` | No field added | No field added |
| `true` or `false` | `boolean` | `boolean` |
| `double` | `float` | `double` |
| `long` | `long` | `long` |
| `object` | `object` | No field added |
| `array` | Depends on the first non-`null` value in the array | Depends on the first non-`null` value in the array |
| `string` that passes [date detection](dynamic-field-mapping.md#date-detection) | `date` | `date` |
| `string` that passes [numeric detection](dynamic-field-mapping.md#numeric-detection) | `float` or `long` | `double` or `long` |
| `string` that doesn’t pass `date` detection or `numeric` detection | `text` with a `.keyword` sub-field | `keyword` |

You can specify either a single data type or a list of data types for either the `match_mapping_type` or `unmatch_mapping_type` parameters. You can also use a wildcard (`*`) for the `match_mapping_type` parameter to match all data types.

For example, if we wanted to map all integer fields as `integer` instead of `long`, and all `string` fields as both `text` and `keyword`, we could use the following template:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "numeric_counts": {
          "match_mapping_type": ["long", "double"],
          "match": "count",
          "mapping": {
            "type": "{dynamic_type}",
            "index": false
          }
        }
      },
      {
        "integers": {
          "match_mapping_type": "long",
          "mapping": {
            "type": "integer"
          }
        }
      },
      {
        "strings": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text",
            "fields": {
              "raw": {
                "type":  "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      },
      {
        "non_objects_keyword": {
          "match_mapping_type": "*",
          "unmatch_mapping_type": "object",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}

PUT my-index-000001/_doc/1
{
  "my_integer": 5, <1>
  "my_string": "Some string", <2>
  "my_boolean": "false", <3>
  "field": {"count": 4} <4>
}
```

1. The `my_integer` field is mapped as an `integer`.
2. The `my_string` field is mapped as a `text`, with a `keyword` [multi-field](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md).
3. The `my_boolean` field is mapped as a `keyword`.
4. The `field.count` field is mapped as a `long`.



## `match` and `unmatch` [match-unmatch]

The `match` parameter uses one or more patterns to match on the field name, while `unmatch` uses one or more patterns to exclude fields matched by `match`.

The `match_pattern` parameter adjusts the behavior of the `match` parameter to support full Java regular expressions matching on the field name instead of simple wildcards. For example:

```js
  "match_pattern": "regex",
  "match": "^profit_\d+$"
```

The following example matches all `string` fields whose name starts with `long_` (except for those which end with `_text`) and maps them as `long` fields:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "longs_as_strings": {
          "match_mapping_type": "string",
          "match":   "long_*",
          "unmatch": "*_text",
          "mapping": {
            "type": "long"
          }
        }
      }
    ]
  }
}

PUT my-index-000001/_doc/1
{
  "long_num": "5", <1>
  "long_text": "foo" <2>
}
```

1. The `long_num` field is mapped as a `long`.
2. The `long_text` field uses the default `string` mapping.


You can specify a list of patterns using a JSON array for either the `match` or `unmatch` fields.

The next example matches all fields whose name starts with `ip_` or ends with `_ip`, except for fields which start with `one` or end with `two` and maps them as `ip` fields:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "ip_fields": {
          "match":   ["ip_*", "*_ip"],
          "unmatch": ["one*", "*two"],
          "mapping": {
            "type": "ip"
          }
        }
      }
    ]
  }
}

PUT my-index/_doc/1
{
  "one_ip":   "will not match", <1>
  "ip_two":   "will not match", <2>
  "three_ip": "12.12.12.12", <3>
  "ip_four":  "13.13.13.13" <4>
}
```

1. The `one_ip` field is unmatched, so uses the default mapping of `text`.
2. The `ip_two` field is unmatched, so uses the default mapping of `text`.
3. The `three_ip` field is mapped as type `ip`.
4. The `ip_four` field is mapped as type `ip`.



## `path_match` and `path_unmatch` [path-match-unmatch]

The `path_match` and `path_unmatch` parameters work in the same way as `match` and `unmatch`, but operate on the full dotted path to the field, not just the final name, e.g. `some_object.*.some_field`.

This example copies the values of any fields in the `name` object to the top-level `full_name` field, except for the `middle` field:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "full_name": {
          "path_match":   "name.*",
          "path_unmatch": "*.middle",
          "mapping": {
            "type":       "text",
            "copy_to":    "full_name"
          }
        }
      }
    ]
  }
}

PUT my-index-000001/_doc/1
{
  "name": {
    "first":  "John",
    "middle": "Winston",
    "last":   "Lennon"
  }
}
```

And the following example uses an array of patterns for both `path_match` and `path_unmatch`.

The values of any fields in the `name` object or the `user.name` object are copied to the top-level `full_name` field, except for the `middle` and `midinitial` fields:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "full_name": {
          "path_match":   ["name.*", "user.name.*"],
          "path_unmatch": ["*.middle", "*.midinitial"],
          "mapping": {
            "type":       "text",
            "copy_to":    "full_name"
          }
        }
      }
    ]
  }
}

PUT my-index-000001/_doc/1
{
  "name": {
    "first":  "John",
    "middle": "Winston",
    "last":   "Lennon"
  }
}

PUT my-index-000001/_doc/2
{
  "user": {
    "name": {
      "first":      "Jane",
      "midinitial": "M",
      "last":       "Salazar"
    }
  }
}
```

Note that the `path_match` and `path_unmatch` parameters match on object paths in addition to leaf fields. As an example, indexing the following document will result in an error because the `path_match` setting also matches the object field `name.title`, which can’t be mapped as text:

```console
PUT my-index-000001/_doc/2
{
  "name": {
    "first":  "Paul",
    "last":   "McCartney",
    "title": {
      "value": "Sir",
      "category": "order of chivalry"
    }
  }
}
```


## Template variables [template-variables]

The `{{name}}` and `{{dynamic_type}}` placeholders are replaced in the `mapping` with the field name and detected dynamic type. The following example sets all string fields to use an [`analyzer`](elasticsearch://reference/elasticsearch/mapping-reference/analyzer.md) with the same name as the field, and disables [`doc_values`](elasticsearch://reference/elasticsearch/mapping-reference/doc-values.md) for all non-string fields:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "named_analyzers": {
          "match_mapping_type": "string",
          "match": "*",
          "mapping": {
            "type": "text",
            "analyzer": "{name}"
          }
        }
      },
      {
        "no_doc_values": {
          "match_mapping_type":"*",
          "mapping": {
            "type": "{dynamic_type}",
            "doc_values": false
          }
        }
      }
    ]
  }
}

PUT my-index-000001/_doc/1
{
  "english": "Some English text", <1>
  "count":   5 <2>
}
```

1. The `english` field is mapped as a `string` field with the `english` analyzer.
2. The `count` field is mapped as a `long` field with `doc_values` disabled.



## Dynamic template examples [template-examples]

Here are some examples of potentially useful dynamic templates:

### Structured search [_structured_search]

When you set `"dynamic":"true"`, {{es}} will map string fields as a `text` field with a `keyword` subfield. If you are only indexing structured content and not interested in full text search, you can make {{es}} map your fields only as `keyword` fields. However, you must search on the exact same value that was indexed to search those fields.

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_as_keywords": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}
```


### `text`-only mappings for strings [text-only-mappings-strings]

Contrary to the previous example, if you only care about full-text search on string fields and don’t plan on running aggregations, sorting, or exact searches, you could tell instruct {{es}} to map strings as `text`:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_as_text": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text"
          }
        }
      }
    ]
  }
}
```

Alternatively, you can create a dynamic template to map your string fields as `keyword` fields in the runtime section of the mapping. When {{es}} detects new fields of type `string`, those fields will be created as runtime fields of type `keyword`.

Although your `string` fields won’t be indexed, their values are stored in `_source` and can be used in search requests, aggregations, filtering, and sorting.

For example, the following request creates a dynamic template to map `string` fields as runtime fields of type `keyword`. Although the `runtime` definition is blank, new `string` fields will be mapped as `keyword` runtime fields based on the [dynamic mapping rules](dynamic-field-mapping.md#dynamic-field-mapping-types) that {{es}} uses for adding field types to the mapping. Any `string` that doesn’t pass date detection or numeric detection is automatically mapped as a `keyword`:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_as_keywords": {
          "match_mapping_type": "string",
          "runtime": {}
        }
      }
    ]
  }
}
```

You index a simple document:

```console
PUT my-index-000001/_doc/1
{
  "english": "Some English text",
  "count":   5
}
```

When you view the mapping, you’ll see that the `english` field is a runtime field of type `keyword`:

```console
GET my-index-000001/_mapping
```

```console-result
{
  "my-index-000001" : {
    "mappings" : {
      "dynamic_templates" : [
        {
          "strings_as_keywords" : {
            "match_mapping_type" : "string",
            "runtime" : { }
          }
        }
      ],
      "runtime" : {
        "english" : {
          "type" : "keyword"
        }
      },
      "properties" : {
        "count" : {
          "type" : "long"
        }
      }
    }
  }
}
```


### Disabled norms [_disabled_norms]

Norms are index-time scoring factors. If you do not care about scoring, which would be the case for instance if you never sort documents by score, you could disable the storage of these scoring factors in the index and save some space.

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_as_keywords": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text",
            "norms": false,
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    ]
  }
}
```

The sub `keyword` field appears in this template to be consistent with the default rules of dynamic mappings. Of course if you do not need them because you don’t need to perform exact search or aggregate on this field, you could remove it as described in the previous section.


### Time series [_time_series]

When doing time series analysis with Elasticsearch, it is common to have many numeric fields that you will often aggregate on but never filter on. In such a case, you could disable indexing on those fields to save disk space and also maybe gain some indexing speed:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_templates": [
      {
        "unindexed_longs": {
          "match_mapping_type": "long",
          "mapping": {
            "type": "long",
            "index": false
          }
        }
      },
      {
        "unindexed_doubles": {
          "match_mapping_type": "double",
          "mapping": {
            "type": "float", <1>
            "index": false
          }
        }
      }
    ]
  }
}
```

1. Like the default dynamic mapping rules, doubles are mapped as floats, which are usually accurate enough, yet require half the disk space.




