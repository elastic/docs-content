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

# Join processor [streams-join-processor]

The **Join** processor concatenates the values of multiple fields into a single field with a delimiter between them.

To join fields:

1. Select **Create** → **Create processor**.
1. Select **Join** from the **Processor** menu.
1. Set the **Source Fields** to the fields you want to join.
1. Set the **Delimiter** to the separator placed between values.
1. Set the **Target field** where the joined result is stored.

## YAML reference [streams-join-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the join processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string[] | Yes | Source fields to join. |
| `delimiter` | string | Yes | Delimiter placed between values. |
| `to` | string | Yes | Target field. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if any source field is missing. |

```yaml
- action: join
  from:
    - attributes.first_name
    - attributes.last_name
  delimiter: " "
  to: attributes.full_name
```
