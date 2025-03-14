---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/host-provider.html
---

# Host provider [host-provider]

Provides information about the current host. The available keys are:

| Key | Type | Description |
| --- | --- | --- |
| `host.name` | `string` | Host name |
| `host.platform` | `string` | Host platform |
| `host.architecture` | `string` | Host architecture |
| `host.ip[]` | `[]string` | Host IP addresses |
| `host.mac[]` | `[]string` | Host MAC addresses |

