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

# Redact processor [streams-redact-processor]

The **Redact** processor redacts sensitive data in a string field by matching grok patterns and replacing the matched content with a placeholder.

To redact sensitive information:

1. Select **Create** → **Create processor**.
1. Select **Redact** from the **Processor** menu.
1. Set the **Source Field** to the field containing text you want to redact.
1. Set the **Patterns** to one or more grok patterns that match sensitive data (for example, IP addresses or email addresses).

This functionality uses the {{es}} [Redact processor](elasticsearch://reference/enrich-processor/redact-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-redact-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the redact processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Source field to redact. |
| `patterns` | string[] | Yes | Grok patterns that match sensitive data. |
| `pattern_definitions` | object | No | Custom pattern definitions. |
| `prefix` | string | No | Prefix for the redacted placeholder. Defaults to `<`. |
| `suffix` | string | No | Suffix for the redacted placeholder. Defaults to `>`. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. Defaults to `true`. |

```yaml
- action: redact
  from: body.message
  patterns:
    - "%{IP:client_ip}"
    - "%{EMAILADDRESS:email}"
```
