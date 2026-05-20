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
description: Move a field value to a new field name and remove the original with the Streams rename processor in Streamlang.
---
# Rename processor [streams-rename-processor]

Use the **Rename** processor to change the name of a field, moving its value to a new field name and removing the original.

To use a rename processor:

1. Select **Create** → **Create processor**.
1. Select **Rename** from the **Processor** menu.
1. Set **Source Field** to the field you want to rename.
1. Set **Target field** to the new name you want to use for the **Source Field**.

This functionality uses the {{es}} [Rename processor](elasticsearch://reference/enrich-processor/rename-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-rename-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the rename processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Source field to rename. |
| `to` | string | Yes | New field name. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |
| `override` | boolean | No | When `true`, allow overwriting an existing target field. |

```yaml
- action: rename
  from: attributes.old_name
  to: attributes.new_name
```
