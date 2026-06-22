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
description: Replace portions of a string field matching a regular expression with the Streams replace processor in Streamlang.
---

# Replace processor [streams-replace-processor]

The **Replace** processor replaces portions of a string field that match a regular expression with a replacement string.

To use the **Replace** processor:

1. Select **Create** → **Create processor**.
1. Select **Replace** from the **Processor** menu.
1. Set the **Source Field** to the field that contains the string you want to replace.
1. Set the **Pattern** to the regular expression or text that you want to replace.
1. Set the **Replacement** to the value that will replace the portion of the string matching your pattern. Replacements can be text, an empty value, or a capture group reference.

This functionality uses the {{es}} [Gsub processor](elasticsearch://reference/enrich-processor/gsub-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-replace-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the replace processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Source field containing the string. |
| `pattern` | string | Yes | Regular expression pattern to match (Java regex). |
| `replacement` | string | Yes | Replacement string. Supports capture group references (for example, `$1`, `$2`). |
| `to` | string | No | Target field for the result. Defaults to the source field. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: replace
  from: attributes.email
  pattern: "(\\w+)@(\\w+\\.\\w+)"
  replacement: "***@$2"
```
