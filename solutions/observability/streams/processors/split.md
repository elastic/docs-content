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
description: Split a field value into an array using a separator with the Streams split processor in Streamlang.
---

# Split processor [streams-split-processor]

The **Split** processor splits a field value into an array using a separator.

To split a field into an array:

1. Select **Create** → **Create processor**.
1. Select **Split** from the **Processor** menu.
1. Set the **Source Field** to the field you want to split into an array.
1. Set **Separator** to a regex that matches the separator. For example, use `,` for commas, `\s+` for whitespace, or `\.` for a literal dot.
1. (Optional) Set **Target field** to write the resulting array to a different field. Leave empty to update the **Source Field**.

This functionality uses the {{es}} [Split processor](elasticsearch://reference/ingest-processor/split-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../streamlang.md#streams-processor-inconsistencies).

## YAML reference [streams-split-yaml-reference]

In [YAML mode](../parse-and-process.md#streams-editing-yaml-mode), configure the split processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Source field to split into an array. |
| `separator` | string | Yes | Regex separator used to split the field value into an array. |
| `to` | string | No | Target field for the split array. Defaults to the source field. |
| `preserve_trailing` | boolean | No | When `true`, preserve empty trailing fields in the split result. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: split
  from: attributes.tags
  separator: ","
```

Given a document with `attributes.tags` set to `foo,bar,baz`, the processor updates the field to `["foo", "bar", "baz"]`.
