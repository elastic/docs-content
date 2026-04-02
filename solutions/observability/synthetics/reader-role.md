---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-role-read.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Reader role [synthetics-role-read]

For users who need to view and create visualizations that access Synthetics data, provide read access. Two types of read access are outlined below:

* **General read access**: For most users, you can use [General read access](#synthetics-read-privileges-general), which grants read access to all {{kib}} apps and requires little configuration.
* **Limited read access**: If you want to limit read access to the {{synthetics-app}} only, you can use [Limited read access](#synthetics-read-privileges-limited), which requires additional configuration.

## General read access [synthetics-read-privileges-general]

For users who only need to view results in {{kib}}, use the `viewer` [built-in role](elasticsearch://reference/elasticsearch/roles.md).

## Limited read access [synthetics-read-privileges-limited]

If you want to limit read access to the {{synthetics-app}} only, do *not* use the `viewer` [built-in role](elasticsearch://reference/elasticsearch/roles.md).

Instead to you can create a reader role, called something like `synthetics_reader_limited`, and grant the following privileges:

| Type | Privilege | Purpose |
| --- | --- | --- |
| [Index](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) | `synthetics-*`: `read` | Read-only access to synthetics indices. |
| [Index](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) | `.alerts-observability.uptime.alerts-*`: `read` | Read-only access to synthetics alert indices. |
| [Kibana](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) | `Synthetics and Uptime`: `read` | Access to the {{synthetics-app}} in {{kib}}. |

