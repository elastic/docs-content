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
description: Concatenate field values and literal strings into a single field with the Streams concat processor in Streamlang.
---

# Concat processor [streams-concat-processor]

The **Concat** processor concatenates a mix of field values and literal strings into a single field.

To concatenate values:

1. Select **Create** → **Create processor**.
1. Select **Concat** from the **Processor** menu.
1. Set the items to concatenate. Each item is either a field reference or a literal string value.
1. Set the **Target field** where the concatenated result is stored.

## YAML reference [streams-concat-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the concat processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | array | Yes | Items to concatenate. Each item is either `{ type: "field", value: "<field_name>" }` or `{ type: "literal", value: "<text>" }`. |
| `to` | string | Yes | Target field. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if any referenced field is missing. |

```yaml
- action: concat
  from:
    - type: literal
      value: "User: "
    - type: field
      value: attributes.username
    - type: literal
      value: " (ID: "
    - type: field
      value: attributes.user_id
    - type: literal
      value: ")"
  to: attributes.user_summary
```
