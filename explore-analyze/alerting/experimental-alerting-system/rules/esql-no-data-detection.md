---
navigation_title: No-data detection
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Detect silent hosts and stopped data sources in Kibana's experimental alerting system using ES|QL last-seen queries."
---

# No-data detection in the {{alerting-v2-system}} [no-data-esql-query]

No-data detection identifies sources that have gone silent, such as a host that stopped reporting metrics. A silent host produces no rows at all, so a threshold query has nothing to evaluate a condition against.

The pattern inverts the normal approach: use a broad lookback to find all known hosts, then surface only those that have not reported recently.

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 12 hours            // Cover the longest expected reporting gap for your hosts.
                                                  // Too short: silent hosts fall outside the window and are never checked.
                                                  // Too long: increases query cost on high-frequency data streams.
| STATS last_seen = MAX(@timestamp) BY host.name  // Find the most recent event timestamp per host
| WHERE last_seen < NOW() - 15 minutes            // Silence threshold: set slightly above your expected maximum reporting interval
                                                  // to avoid false positives from brief gaps
| KEEP host.name, last_seen                       // Each returned row is a silent host
```

Every row returned is a host that has gone silent. The query result itself drives the alert. A separate alert condition isn't needed.

:::{note}
This pattern detects specific silent sources. For controlling what the rule records when the entire base query returns zero rows, for example when an index is completely empty, refer to [No-data handling](configure-no-data-handling.md).
:::

## Related pages

- [{{esql}} query patterns](esql-query-patterns.md): Browse query patterns ordered by complexity, from a basic event filter to SLO burn rate and persistent breach detection.
- [No-data handling](configure-no-data-handling.md): Configure what the rule records when the base query returns zero rows.
