---
applies_to:
  serverless: ga
  stack: ga 9.5+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Extract the domain, registered domain, subdomain, and top-level domain from a fully qualified domain name with the Streams registered domain processor in Streamlang.
---

# Registered domain processor [streams-registered-domain-processor]

The **Registered domain** processor extracts the domain, registered domain, top-level domain, and subdomain from a fully qualified domain name (FQDN).

To extract the parts of a domain:

1. Select **Create** → **Create processor**.
1. Select **Registered domain** from the **Processor** menu.
1. Set the **Field** to the field containing the FQDN.
1. Set **Prefix** to the prefix used for the output fields. The extracted parts are written as `<prefix>.domain`, `<prefix>.registered_domain`, `<prefix>.subdomain`, and `<prefix>.top_level_domain`.

This functionality uses the {{es}} [Registered domain processor](elasticsearch://reference/ingest-processor/registered-domain-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-registered-domain-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the registered domain processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `expression` | string | Yes | Field containing the FQDN to parse. |
| `prefix` | string | Yes | Prefix for the output fields. The extracted parts are available as `<prefix>.domain`, `<prefix>.registered_domain`, `<prefix>.subdomain`, and `<prefix>.top_level_domain`. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: registered_domain
  expression: attributes.url.domain
  prefix: attributes.domain
```

Given a document with `attributes.url.domain` set to `www.example.com`, the processor adds:

- `attributes.domain.domain: "www.example.com"`
- `attributes.domain.registered_domain: "example.com"`
- `attributes.domain.subdomain: "www"`
- `attributes.domain.top_level_domain: "com"`
