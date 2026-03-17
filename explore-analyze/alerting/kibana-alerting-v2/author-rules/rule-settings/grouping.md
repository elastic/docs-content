---
navigation_title: Rule grouping
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Split Kibana alerting v2 alert event generation by fields like host or service so each entity has independent lifecycle tracking."
---

# Kibana alerting v2 rule grouping [rule-grouping-v2]

Grouping splits alert event generation by one or more fields so that each unique combination of field values produces its own alert series. Each series has independent lifecycle tracking, recovery detection, and per-series snooze.

## Configure grouping

In YAML:

```yaml
grouping:
  fields: [host.name]
```

The grouping fields must correspond to the `BY` clause in your ES|QL query's `STATS` command.
