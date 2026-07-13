---
applies_to:
  serverless: ga
  stack: ga 9.4+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Extract values from JSON strings using JSONPath-like selectors with the Streams JSON extract processor in Streamlang.
---

# JSON extract processor [streams-json-extract-processor]

The **JSON extract** processor extracts values from a JSON-encoded string field using JSONPath-like selectors, and writes each extracted value to its own target field.

To extract values from a JSON string:

1. Select **Create** → **Create processor**.
1. Select **JSON extract** from the **Processor** menu.
1. Set **Field with JSON string** to the field containing the JSON string to parse.
1. For each value you want to extract, select **Add extraction** and set:
   - **Selector**: A JSONPath-like selector for the value to extract, for example `user.id`, `$.metadata.client.ip`, or `items[0].name`.
   - **Target**: The field to store the extracted value in.
   - **Type**: The data type for the extracted value: `Keyword`, `Integer`, `Long`, `Double`, or `Boolean`. Defaults to `Keyword`.

## YAML reference [streams-json-extract-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the JSON extract processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `field` | string | Yes | Source field containing the JSON string to parse. |
| `extractions` | array | Yes | List of extraction specifications. Each item requires a `selector` and `target_field`, and accepts an optional `type`. |
| `extractions[].selector` | string | Yes | JSONPath-like selector to extract a value, for example `user.id`, `$.metadata.client.ip`, or `items[0].name`. |
| `extractions[].target_field` | string | Yes | Target field to store the extracted value. |
| `extractions[].type` | string | No | Data type for the extracted value: `keyword`, `integer`, `long`, `double`, or `boolean`. Defaults to `keyword`. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: json_extract
  field: attributes.message
  extractions:
    - selector: metadata.client.ip
      target_field: attributes.client.ip
```

Given a document with `attributes.message` set to `{"metadata": {"client": {"ip": "192.168.1.1"}}}`, the processor adds `attributes.client.ip: "192.168.1.1"`.
