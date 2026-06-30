---
applies_to:
  serverless: ga
  stack: ga 9.3+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Convert a field value to a different data type such as string, integer, or boolean with the Streams convert processor in Streamlang.
---

# Convert processor [streams-convert-processor]
The **Convert** processor converts a field to a different data type. For example, you could convert a string to an integer.

To convert a field to a different data type:

1. Select **Create** → **Create processor**.
1. Select **Convert** from the **Processor** menu.
1. Set the **Source Field** to the field you want to convert.
1. (Optional) Set **Target field** to write the converted value to a different field.
1. Set **Type** to the output data type.

::::{note}
If you add a **Convert** processor inside a condition group (a **WHERE** block), you must set a **Target field**.
::::

This functionality uses the {{es}} [Convert processor](elasticsearch://reference/enrich-processor/convert-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-convert-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the convert processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Source field containing the value to convert. |
| `type` | string | Yes | Target data type: `integer`, `long`, `double`, `boolean`, or `string`. |
| `to` | string | No | Target field for the converted value. Defaults to the source field. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

:::{note}
When using `convert` inside a condition (`where` block), you must set a `to` field that is different from `from`.
:::

```yaml
- action: convert
  from: attributes.status_code
  type: string
  to: attributes.status_code_int
```
