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

# Enrich processor [streams-enrich-processor]

The **Enrich** processor adds data from an existing [enrich policy](elasticsearch://reference/enrich-processor/enrich-processor.md) to incoming documents during processing. Use it to look up and append supplemental data, such as geographic coordinates from an IP address or account details from a user ID, without modifying the original source.

Before using the enrich processor, you must have at least one enrich policy configured in {{es}}. Refer to [Enrich your data](/manage-data/ingest/transform-enrich/data-enrichment.md) for setup instructions.

To enrich documents:

1. Select **Create** → **Create processor**.
1. Select **Enrich** from the **Processor** menu.
1. Select an **Enrich policy** from the list of available policies.
1. Set **Target field** to the field where the enriched data is stored.

This functionality uses the {{es}} [Enrich processor](elasticsearch://reference/enrich-processor/enrich-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-enrich-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the enrich processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `policy_name` | string | Yes | The name of the enrich policy to use. |
| `to` | string | Yes | Target field for the enriched data. |
| `override` | boolean | No | When `true`, overwrite pre-existing non-null field values. Defaults to `true`. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: enrich
  policy_name: ip_location
  to: attributes.geo
  override: true
```
