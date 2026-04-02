---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/manage-agents.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# {{agent}}s [manage-agents]


::::{tip}
To learn how to add {{agent}}s to {{fleet}}, see [Install {{fleet}}-managed {{agent}}s](/reference/fleet/install-fleet-managed-elastic-agent.md).
::::


To manage your {{agent}}s, go to **Management > {{fleet}} > Agents** in {{kib}}. On the **Agents** tab, you can perform the following actions:

| User action | Result |
| --- | --- |
| [Unenroll {{agent}}s](/reference/fleet/unenroll-elastic-agent.md) | Unenroll {{agent}}s from {{fleet}}. |
| [Set inactivity timeout](/reference/fleet/set-inactivity-timeout.md) | Set inactivity timeout to move {{agent}}s to inactive status after being offline for the set amount of time. |
| [Upgrade {{agent}}s](/reference/fleet/upgrade-elastic-agent.md) | Upgrade {{agent}}s to the latest version. |
| [Migrate {{agent}}s](/reference/fleet/migrate-elastic-agent.md) | Migrate {{agent}}s from one cluster to another. |
| [Monitor {{agent}}s](/reference/fleet/monitor-elastic-agent.md) | Monitor {{fleet}}-managed {{agent}}s by viewing agent status, logs, and metrics. |
| [Add tags to filter the Agents list](/reference/fleet/filter-agent-list-by-tags.md) | Add tags to {{agent}}, then use the tags to filter the Agents list in {{fleet}}. |








