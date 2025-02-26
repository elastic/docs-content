---
navigation_title: "decode_json_fields"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/decode-json-fields.html
---

# Decode JSON fields [decode-json-fields]


The `decode_json_fields` processor decodes fields containing JSON strings and replaces the strings with valid JSON objects.


## Example [_example_19]

```yaml
  - decode_json_fields:
      fields: ["field1", "field2", ...]
      process_array: false
      max_depth: 1
      target: ""
      overwrite_keys: false
      add_error_key: true
```


## Configuration settings [_configuration_settings_22]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | Fields containing JSON strings to decode. |
| `process_array` | No | `false` | Whether to process arrays. |
| `max_depth` | No | `1` | Maximum parsing depth. A value of `1` decodes the JSON objects in fields indicated in `fields`. A value of `2` also decodes the objects embedded in the fields of these parsed documents. |
| `target` | No |  | Field under which the decoded JSON will be written. By default, the decoded JSON object replaces the string field from which it was read. To merge the decoded JSON fields into the root of the event, specify `target` with an empty string (`target: ""`). Note that the `null` value (`target:`) is treated as if the field was not set. |
| `overwrite_keys` | No | `false` | Whether existing keys in the event are overwritten by keys from the decoded JSON object. |
| `expand_keys` | No |  | Whether keys in the decoded JSON should be recursively de-dotted and expanded into a hierarchical object structure. For example, `{"a.b.c": 123}` would be expanded into `{"a":{"b":{"c":123}}}`. |
| `add_error_key` | No | `false` | If `true` and an error occurs while decoding JSON keys, the `error` field will become a part of the event with the error message. If `false`, there will not be any error in the event’s field. |
| `document_id` | No |  | JSON key that’s used as the document ID. If configured, the field will be removed from the original JSON document and stored in `@metadata._id`. |

