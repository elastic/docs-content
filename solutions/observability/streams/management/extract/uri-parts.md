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
description: Parse a URI string into its components, such as scheme, domain, path, and query, with the Streams URI parts processor in Streamlang.
---

# URI parts processor [streams-uri-parts-processor]

The **URI parts** processor parses a URI string into its components: scheme, domain, path, query, fragment, port, user info, and file extension.

To parse a URI:

1. Select **Create** → **Create processor**.
1. Select **URI parts** from the **Processor** menu.
1. Set the **Field** to the field containing the URI string to parse.
1. (Optional) Set **Target prefix** to the prefix used for the extracted components, for example `<prefix>.scheme`, `<prefix>.domain`, and `<prefix>.path`. Defaults to `url`.
1. (Optional) Toggle **Keep original** to preserve the raw URI string at `<prefix>.original`. Enabled by default.
1. (Optional) Toggle **Remove source on success** to remove the source field after a successful parse. The source field is kept when parsing fails. Disabled by default.

This functionality uses the {{es}} [URI parts processor](elasticsearch://reference/ingest-processor/uri-parts-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

## YAML reference [streams-uri-parts-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the URI parts processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Field containing the URI string to parse. |
| `to` | string | No | Target field / column prefix for the extracted URI components. Defaults to `url`. |
| `keep_original` | boolean | No | When `true` (default), preserve the original URI string at `<prefix>.original`. |
| `remove_if_successful` | boolean | No | When `true`, remove the source field after a successful parse. The source field is kept when parsing fails. Defaults to `false`. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: uri_parts
  from: attributes.url.original
  to: attributes.url
```

Given a document with `attributes.url.original` set to `http://myusername:mypassword@www.example.com:80/foo.gif?key1=val1&key2=val2#fragment`, the processor adds:

- `attributes.url.scheme: "http"`
- `attributes.url.domain: "www.example.com"`
- `attributes.url.path: "/foo.gif"`
- `attributes.url.extension: "gif"`
- `attributes.url.port: 80`
- `attributes.url.query: "key1=val1&key2=val2"`
- `attributes.url.fragment: "fragment"`
- `attributes.url.user_info: "myusername:mypassword"`
- `attributes.url.username: "myusername"`
- `attributes.url.password: "mypassword"`
