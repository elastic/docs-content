---
navigation_title: "decode_xml"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/decode_xml-processor.html
---

# Decode XML [decode_xml-processor]


The `decode_xml` processor decodes XML data that is stored under the `field` key. It outputs the result into the `target_field`.


## Examples [_examples_6]

This example demonstrates how to decode an XML string contained in the `message` field and write the resulting fields into the root of the document. Any fields that already exist are overwritten.

```yaml
  - decode_xml:
      field: message
      target_field: ""
      overwrite_keys: true
```

By default any decoding errors that occur will stop the processing chain, and the error will be added to the `error.message` field. To ignore all errors and continue to the next processor, set `ignore_failure: true`. To specifically ignore failures caused by `field` not existing, set `ignore_missing: true`.

```yaml
  - decode_xml:
      field: example
      target_field: xml
      ignore_missing: true
      ignore_failure: true
```

By default the names of all keys converted from XML are converted to lowercase. To disable this behavior, set `to_lower: false`, for example:

```yaml
  - decode_xml:
      field: message
      target_field: xml
      to_lower: false
```

Example XML input:

```xml
<catalog>
  <book seq="1">
    <author>William H. Gaddis</author>
    <title>The Recognitions</title>
    <review>One of the great seminal American novels of the 20th century.</review>
  </book>
</catalog>
```

Will produce the following output:

```json
{
	"xml": {
		"catalog": {
			"book": {
				"author": "William H. Gaddis",
				"review": "One of the great seminal American novels of the 20th century.",
				"seq": "1",
				"title": "The Recognitions"
			}
		}
	}
}
```


## Configuration settings [_configuration_settings_23]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes | `message` | Source field containing the XML. |
| `target_field` | No |  | The field under which the decoded XML will be written. By default the decoded XML object replaces the field from which it was read. To merge the decoded XML fields into the root of the event, specify `target_field` with an empty string (`target_field: ""`). Note that the `null` value (`target_field:`) is treated as if the field was not set at all. |
| `overwrite_keys` | No | `true` | Whether keys that already exist in the event are overwritten by keys from the decoded XML object. |
| `to_lower` | No | `true` | Whether to convert all keys to lowercase. |
| `document_id` | No |  | XML key to use as the document ID. If configured, the field will be removed from the original XML document and stored in `@metadata._id`. |
| `ignore_missing` | No | `false` | Whether to return an error if a specified field does not exist. |
| `ignore_failure` | No | `false` | Whether to ignore all errors produced by the processor. |

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

