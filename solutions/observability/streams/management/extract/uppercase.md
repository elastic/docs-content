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
---

# Uppercase processor [streams-uppercase-processor]

The **Uppercase** processor converts a string field to uppercase.

To convert a field to uppercase:

1. Select **Create** → **Create processor**.
1. Select **Uppercase** from the **Processor** menu.
1. Set the **Source Field** to the field you want to convert.
1. (Optional) Set **Target field** to write the result to a different field.

## YAML reference [streams-uppercase-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the uppercase processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Source field. |
| `to` | string | No | Target field. Defaults to the source field. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: uppercase
  from: attributes.level
```
