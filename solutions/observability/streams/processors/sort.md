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
description: Sort the elements of an array field in ascending or descending order with the Streams sort processor in Streamlang.
---

# Sort processor [streams-sort-processor]

The **Sort** processor sorts the elements of an array field in ascending or descending order.

To sort an array field:

1. Select **Create** → **Create processor**.
1. Select **Sort** from the **Processor** menu.
1. Set the **Source Field** to the array field you want to sort.
1. Set **Order** to **Ascending** or **Descending**. Defaults to **Ascending**.
1. (Optional) Set **Target field** to write the sorted array to a different field. Leave empty to update the **Source Field**.

This functionality uses the {{es}} [Sort processor](elasticsearch://reference/ingest-processor/sort-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-sort-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the sort processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Array field to sort. |
| `to` | string | No | Target field for the sorted array. Defaults to the source field. |
| `order` | string | No | Sort order: `asc` or `desc`. Defaults to `asc`. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: sort
  from: attributes.tags
  order: desc
```

Given a document with `attributes.tags` set to `["charlie", "alpha", "bravo"]`, the processor updates the field to `["charlie", "bravo", "alpha"]`.
