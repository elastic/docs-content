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
---

# Remove processor [streams-remove-processor]

The **Remove** processor removes a field (**Remove**) or removes a field and all its nested fields (**Remove by prefix**) from your documents.

To remove a field:

1. Select **Create** → **Create processor**.
1. From the **Processor** menu, select **Remove** to remove a field or **Remove by prefix** to remove a field and all its nested fields.
1. Set the **Source Field** to the field you want to remove.

This functionality uses the {{es}} [Remove processor](elasticsearch://reference/enrich-processor/remove-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-remove-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the remove processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

### Remove [streams-remove-yaml]

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Field to remove. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the field is missing. |

```yaml
- action: remove
  from: attributes.temp_field
```

### Remove by prefix [streams-remove-by-prefix-processor]

Removes a field and all nested fields matching a prefix.

:::{note}
The `where` clause is not supported on `remove_by_prefix`. You cannot use this processor cannot inside condition blocks.
:::

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Prefix to match. The processor removes all fields under this prefix. |

```yaml
- action: remove_by_prefix
  from: attributes.debug
```
