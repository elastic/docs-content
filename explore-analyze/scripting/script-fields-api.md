---
navigation_title: Access fields in a document
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/script-fields-api.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---



# Access fields in a document [script-fields-api]


::::{warning} 
The `field` API is still in development and should be considered a beta feature. The API is subject to change and this iteration is likely not the final state. For feature status, refer to [#78920](https://github.com/elastic/elasticsearch/issues/78920).
::::


Use the `field` API to access document fields:

```painless
field('my_field').get(<default_value>)
```

Alternatively use the shortcut of `$` to get a field.

```painless
$('my_field', <default_value>)
```

This API fundamentally changes how you access documents in Painless. Previously, you had to access the `doc` map with the field name that you wanted to access:

```painless
doc['my_field'].value
```

Accessing document fields this way didn’t handle missing values or missing mappings, which meant that to write robust Painless scripts, you needed to include logic to check that both fields and values exist.

Instead, use the `field` API, which is the preferred approach to access documents in Painless. The `field` API handles missing values, and will evolve to abstract access to `_source` and `doc_values`.

::::{note} 
Some fields aren’t yet compatible with the `fields` API, such as `text` or `geo` fields. Continue using `doc` to access field types that the `field` API doesn’t support.
::::


The `field` API returns a `Field` object that iterates over fields with multiple values, providing access to the underlying value through the `get(<default_value>)` method, as well as type conversion and helper methods.

The `field` API returns the default value that you specify, regardless of whether the field exists or has any values for the current document. This means that the `field` API can handle missing values without requiring additional logic. For a reference type such as `keyword`, the default value can be `null`. For a primitive type such as `boolean` or `long`, the default value must be a matching primitive type, such as `false` or `1`.


## Convenient, simpler access [_convenient_simpler_access] 

Instead of explicitly calling the `field` API with the `get()` method, you can include the `$` shortcut. Just include the `$` symbol, field name, and a default value, in case the field doesn’t have a value:

```painless
$(‘field’, <default_value>)
```

With these enhanced capabilities and simplified syntax, you can write scripts that are shorter, less complex, and easier to read. For example, the following script uses the outdated syntax to determine the difference in milliseconds between two complex `datetime` values from an indexed document:

```painless
if (doc.containsKey('start') && doc.containsKey('end')) {
   if (doc['start'].size() > 0 && doc['end'].size() > 0) {
       ZonedDateTime start = doc['start'].value;
       ZonedDateTime end = doc['end'].value;
       return ChronoUnit.MILLIS.between(start, end);
   } else {
       return -1;
   }
} else {
   return -1;
}
```

Using the `field` API, you can write this same script much more succinctly, without requiring additional logic to determine whether fields exist before operating on them:

```painless
ZonedDateTime start = field('start').get(null);
ZonedDateTime end = field('end').get(null);
return start == null || end == null ? -1 : ChronoUnit.MILLIS.between(start, end)
```

## Supported mapped field types [_supported_mapped_field_types] 

The following table indicates the mapped field types that the `field` API supports. For each supported type, values are listed that are returned by the `field` API (from the `get` and `as<Type>` methods) and the `doc` map (from the `getValue` and `get` methods).

::::{note} 
The `fields` API currently doesn’t support some fields, but you can still access those fields through the `doc` map. For the most current list of supported fields, refer to [#79105](https://github.com/elastic/elasticsearch/issues/79105).
::::


| Mapped field type | Returned type from `field` | Returned type from `doc` |
| --- | --- | --- |
|  | `get` | `as<Type>` | `getValue` | `get` |
| `binary` | `ByteBuffer` | - | `BytesRef` | `BytesRef` |
| `boolean` | `boolean` | - | `boolean` | `Boolean` |
| `keyword` | `String` | - | `String` | `String` |
| `long` | `long` | - | `long` | `Long` |
| `integer` | `int` | - | `long` | `Long` |
| `short` | `short` | - | `long` | `Long` |
| `byte` | `byte` | - | `long` | `Long` |
| `double` | `double` | - | `double` | `Double` |
| `scaled_float` | `double` | - | `double` | `Double` |
| `half_float` | `float` | - | `double` | `Double` |
| `unsigned_long` | `long` | `BigInteger` | `long` | `Long` |
| `date` | `ZonedDateTime` | - | `ZonedDateTime` | `ZonedDateTime` |
| `date_nanos` | `ZonedDateTime` | - | `ZonedDateTime` | `ZonedDateTime` |
| `ip` | `IpAddress` | `String` | `String` | `String` |
| `_version` | `long` | - | `long` | `Long` |
| `_seq_no` | `long` | - | `long` | `Long` |
| `version` | `Version` | `String` | `String` | `String` |
| `murmur3` | `long` | - | `long` | `Long` |
| `constant_keyword` | `String` | - | `String` | `String` |
| `wildcard` | `String` | - | `String` | `String` |
| `flattened` | `String` | - | `String` | `String` |

## Manipulation of the fields data

The field API provides a `set(<value>)` operation that will take the field name and create the necessary structure. Calling this inside an ingest pipelines script processor context:

```painless
field("foo.bar").set("abc")
```

leads to the generation of this JSON representation.

```json
{
  "foo": {
    "bar": "abc"
  }
}
```
