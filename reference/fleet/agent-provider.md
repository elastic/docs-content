---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/agent-provider.html
---

# Agent provider [agent-provider]

Provides information about the {{agent}}. The available keys are:

| Key | Type | Description |
| --- | --- | --- |
| `agent.id` | `string` | Current agent ID |
| `agent.version` | `object` | Current agent version information object |
| `agent.version.version` | `string` | Current agent version |
| `agent.version.commit` | `string` | Version commit |
| `agent.version.build_time` | `date` | Version build time |
| `agent.version.snapshot` | `boolean` | Version is snapshot build |

