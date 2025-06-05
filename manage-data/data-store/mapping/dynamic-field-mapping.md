---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-field-mapping.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Dynamic field mapping [dynamic-field-mapping]

When {{es}} detects a new field in a document, it *dynamically* adds the field to the type mapping by default. The [`dynamic`](elasticsearch://reference/elasticsearch/mapping-reference/dynamic.md) parameter controls this behavior.

You can explicitly instruct {{es}} to dynamically create fields based on incoming documents by setting the `dynamic` parameter to `true` or `runtime`. When dynamic field mapping is enabled, {{es}} uses the rules in the following table to determine how to map data types for each field.

::::{note}
The field data types in the following table are the only [field data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) that {{es}} detects dynamically. You must explicitly map all other data types.
::::


$$$dynamic-field-mapping-types$$$

| JSON data type | {{es}} data type<br>(`"dynamic":"true"`) | {{es}} data type<br>(`"dynamic":"runtime"`) |
| --- | --- | --- |
| `null` | No field added | No field added |
| `true` or `false` | `boolean` | `boolean` |
| `double` | `float` | `double` |
| `long` | `long` | `long` |
| `object` | `object` | No field added |
| `array` | Depends on the first non-`null` value in the array | Depends on the first non-`null` value in the array |
| `string` that passes [date detection](#date-detection) | `date` | `date` |
| `string` that passes [numeric detection](#numeric-detection) | `float` or `long` | `double` or `long` |
| `string` that doesn’t pass `date` detection or `numeric` detection | `text` with a `.keyword` sub-field | `keyword` |

You can disable dynamic mapping, both at the document and at the [`object`](elasticsearch://reference/elasticsearch/mapping-reference/object.md) level. Setting the `dynamic` parameter to `false` ignores new fields, and `strict` rejects the document if {{es}} encounters an unknown field.

::::{tip}
Use the [update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) to update the `dynamic` setting on existing fields.
::::


You can customize dynamic field mapping rules for [date detection](#date-detection) and [numeric detection](#numeric-detection). To define custom mappings rules that you can apply to additional dynamic fields, use [`dynamic_templates`](dynamic-templates.md).

## Date detection [date-detection]

If `date_detection` is enabled (default), then new string fields are checked to see whether their contents match any of the date patterns specified in `dynamic_date_formats`. If a match is found, a new [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) field is added with the corresponding format.

The default value for `dynamic_date_formats` is:

[ [`"strict_date_optional_time"`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-date-format.md#strict-date-time),`"yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"`]

For example:

```console
PUT my-index-000001/_doc/1
{
  "create_date": "2015/09/02"
}

GET my-index-000001/_mapping <1>
```

1. The `create_date` field has been added as a [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) field with the [`format`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-date-format.md):<br> `"yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"`.


### Disabling date detection [_disabling_date_detection]

Dynamic date detection can be disabled by setting `date_detection` to `false`:

```console
PUT my-index-000001
{
  "mappings": {
    "date_detection": false
  }
}

PUT my-index-000001/_doc/1 <1>
{
  "create_date": "2015/09/02"
}
```

1. The `create_date` field has been added as a [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) field.



### Customizing detected date formats [_customizing_detected_date_formats]

Alternatively, the `dynamic_date_formats` can be customized to support your own [date formats](elasticsearch://reference/elasticsearch/mapping-reference/mapping-date-format.md):

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_date_formats": ["MM/dd/yyyy"]
  }
}

PUT my-index-000001/_doc/1
{
  "create_date": "09/25/2015"
}
```

::::{note}
There is a difference between configuring an array of date patterns and configuring multiple patterns in a single string separated by `||`. When you configure an array of date patterns, the pattern that matches the date in the first document with an unmapped date field will determine the mapping of that field:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_date_formats": [ "yyyy/MM", "MM/dd/yyyy"]
  }
}

PUT my-index-000001/_doc/1
{
  "create_date": "09/25/2015"
}
```

The resulting mapping will be:

```console-result
{
  "my-index-000001": {
    "mappings": {
      "dynamic_date_formats": [
        "yyyy/MM",
        "MM/dd/yyyy"
      ],
      "properties": {
        "create_date": {
          "type": "date",
          "format": "MM/dd/yyyy"
        }
      }
    }
  }
}
```

Configuring multiple patterns in a single string separated by `||` results in a mapping that supports any of the date formats. This enables you to index documents that use different formats:

```console
PUT my-index-000001
{
  "mappings": {
    "dynamic_date_formats": [ "yyyy/MM||MM/dd/yyyy"]
  }
}

PUT my-index-000001/_doc/1
{
  "create_date": "09/25/2015"
}
```

The resulting mapping will be:

```console-result
{
  "my-index-000001": {
    "mappings": {
      "dynamic_date_formats": [
        "yyyy/MM||MM/dd/yyyy"
      ],
      "properties": {
        "create_date": {
          "type": "date",
          "format": "yyyy/MM||MM/dd/yyyy"
        }
      }
    }
  }
}
```

::::


::::{note}
Epoch formats (`epoch_millis` and `epoch_second`) are not supported as dynamic date formats.

::::




## Numeric detection [numeric-detection]

While JSON has support for native floating point and integer data types, some applications or languages may sometimes render numbers as strings. Usually the correct solution is to map these fields explicitly, but numeric detection (which is disabled by default) can be enabled to do this automatically:

```console
PUT my-index-000001
{
  "mappings": {
    "numeric_detection": true
  }
}

PUT my-index-000001/_doc/1
{
  "my_float":   "1.0", <1>
  "my_integer": "1" <2>
}
```

1. The `my_float` field is added as a [`float`](elasticsearch://reference/elasticsearch/mapping-reference/number.md) field.
2. The `my_integer` field is added as a [`long`](elasticsearch://reference/elasticsearch/mapping-reference/number.md) field.



