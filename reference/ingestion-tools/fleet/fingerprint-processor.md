---
navigation_title: "fingerprint"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fingerprint-processor.html
---

# Generate a fingerprint of an event [fingerprint-processor]


The `fingerprint` processor generates a fingerprint of an event based on a specified subset of its fields.

The value that is hashed is constructed as a concatenation of the field name and field value separated by `|`. For example `|field1|value1|field2|value2|`.

Nested fields are supported in the following format: `"field1.field2"`, for example: `["log.path.file", "foo"]`


## Example [_example_26]

```yaml
  - fingerprint:
      fields: ["field1", "field2", ...]
```


## Configuration settings [_configuration_settings_31]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | List of fields to use as the source for the fingerprint. The list will be alphabetically sorted by the processor. |
| `ignore_missing` | No | `false` | Whether to ignore missing fields. |
| `target_field` | No | `fingerprint` | Field in which the generated fingerprint should be stored. |
| `method` | No | `sha256` | Algorithm to use for computing the fingerprint. Must be one of: `md5`, `sha1`, `sha256`, `sha384`, `sha512`, or `xxhash`. |
| `encoding` | No | `hex` | Encoding to use on the fingerprint value. Must be one of: `hex`, `base32`, or `base64`. |

