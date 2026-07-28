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
description: Extract browser, OS, and device details from a user agent string with the Streams user agent processor in Streamlang.
---

# User agent processor [streams-user-agent-processor]

The **User agent** processor extracts browser, operating system, and device details from a user agent string.

To extract user agent details:

1. Select **Create** → **Create processor**.
1. Select **User agent** from the **Processor** menu.
1. Set the **Source Field** to the field containing the user agent string.
1. (Optional) Set **Target field** to the field that will contain the extracted details. Defaults to `user_agent`.
1. (Optional) Expand the accordion to configure:
   - **Regex file**: A custom regex file name containing the regular expressions used to parse the user agent string.
   - **Properties**: The specific properties to extract. Defaults to all: `name`, `os`, `device`, `original`, `version`.
   - **Extract device type**: Extracts the device type from the user agent string. This functionality is in beta and is subject to change.

This functionality uses the {{es}} [User agent processor](elasticsearch://reference/ingest-processor/user-agent-processor.md) internally, but you configure it in Streamlang. Streamlang doesn't always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../streamlang.md#streams-processor-inconsistencies).

## YAML reference [streams-user-agent-yaml-reference]

In [YAML mode](../parse-and-process.md#streams-editing-yaml-mode), configure the user agent processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from` | string | Yes | Field containing the user agent string. |
| `to` | string | No | Field that will contain the extracted user agent details. Defaults to `user_agent`. |
| `regex_file` | string | No | Custom regex file name containing the regular expressions for parsing the user agent string. |
| `properties` | string[] | No | Properties to extract: `name`, `os`, `device`, `original`, `version`. Defaults to all. |
| `extract_device_type` | boolean | No | When `true`, extracts the device type from the user agent string. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if the source field is missing. |

```yaml
- action: user_agent
  from: attributes.user_agent.original
  to: attributes.user_agent
```

Given a document with:

```json
{
  "attributes": {
    "user_agent": {
      "original": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0"
    }
  }
}
```

The processor adds `attributes.user_agent.name: "Chrome"` and `attributes.user_agent.os.name: "Mac OS X"`, alongside the other extracted properties.
