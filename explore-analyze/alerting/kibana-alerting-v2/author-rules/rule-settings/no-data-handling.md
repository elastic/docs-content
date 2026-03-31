---
navigation_title: No-data handling
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Configure Kibana alerting v2 rule behavior when the query returns no results: record no-data, carry forward status, or treat as recovery."
---

# Kibana alerting v2 no-data handling [no-data-handling-v2]

No-data handling controls what happens when a rule executes and the base query returns no results.

## Behaviors

| Behavior | Effect |
|---|---|
| `no_data` (default) | Record a no-data event |
| `last_status` | Carry forward the previous status |
| `recover` | Treat absence as recovery |
