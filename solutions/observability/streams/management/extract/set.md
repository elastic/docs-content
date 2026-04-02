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
---
# Set processor [streams-set-processor]

Use the **Set** processor to assign a specific value to a field, creating the field if it doesn't exist or overwriting its value if it does.

To use a set processor:

1. Select **Create** → **Create processor**.
1. Select **Set** from the **Processor** menu.
1. Set **Source Field** to the field you want to insert, upsert, or update.
1. Set **Value** to the value you want the source field to be set to.

This functionality uses the {{es}} [Set processor](elasticsearch://reference/enrich-processor/set-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-set-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the set processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

Specify exactly one of `value` or `copy_from`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `to` | string | Yes | Target field. |
| `value` | any | One of `value` or `copy_from` | A literal value to assign. |
| `copy_from` | string | One of `value` or `copy_from` | A source field to copy the value from. |
| `override` | boolean | No | When `false`, the target field is only set if it doesn't already exist. |

```yaml
- action: set
  to: attributes.environment
  value: production

- action: set
  to: attributes.backup_message
  copy_from: body.message
```
