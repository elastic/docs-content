---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Add values to an existing array field or create the field as an array with the Streams append processor in Streamlang.
---
# Append processor [streams-append-processor]

Use the **Append** processor to add a value to an existing array field, or create the field as an array if it doesn't exist.

To use an append processor:

1. Select **Create** → **Create processor**.
1. Select **Append** from the **Processor** menu.
1. Set **Source Field** to the field you want append values to.
1. Set **Target field** to the values you want to append to the **Source Field**.

This functionality uses the {{es}} [append processor](elasticsearch://reference/enrich-processor/append-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-append-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the append processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `to` | string | Yes | Array field to append to. |
| `value` | array | Yes | Values to append. |
| `allow_duplicates` | boolean | No | When `false`, duplicate values are not appended. |

```yaml
- action: append
  to: attributes.tags
  value:
    - processed
    - reviewed
```
