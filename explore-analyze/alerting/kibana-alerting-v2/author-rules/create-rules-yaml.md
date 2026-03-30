---
navigation_title: Using YAML
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Define Kibana alerting v2 rules in YAML for version control and infrastructure-as-code workflows, with full field reference."
---

# Create Kibana alerting v2 rules with YAML [create-rules-yaml-v2]

Define Kibana alerting v2 rules as YAML documents for version control, infrastructure-as-code workflows, and bulk provisioning.

## YAML rule structure

A complete alert-mode rule in YAML:

```yaml
kind: alert

metadata:
  name: checkout-error-rate-by-route
  owner: platform
  labels: ["production", "checkout"]

time_field: "@timestamp"

schedule:
  every: 1m
  lookback: 20m

evaluation:
  query:
    base: |
      FROM metrics-*
      | STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name
      | WHERE env == "production"
    condition: "WHERE avg_cpu > 0.9"

recovery_policy:
  type: query
  query:
    base: |
      FROM metrics-*
      | STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name
    condition: "WHERE avg_cpu < 0.67"

state_transition:
  pending_operator: OR
  pending_count: 3
  pending_timeframe: 5m
  recovering_operator: AND
  recovering_count: 2
  recovering_timeframe: 10m

grouping:
  fields: [host.name]

no_data:
  behavior: no_data
  timeframe: 15m

notification_policies:
  - ref: "policies/service-alerts-v1"
  - ref: "policies/pagerduty-sev1-v1"
```

## Detect mode example

A minimal detect-mode rule:

```yaml
kind: signal

metadata:
  name: http-500-errors

schedule:
  every: 5m
  lookback: 5m

evaluation:
  query:
    base: |
      FROM logs-*
      | WHERE http.response.status_code >= 500
      | STATS error_count = COUNT(*) BY service.name
      | KEEP service.name, error_count
```

## Toggle between GUI and YAML

In the rule creation UI, you can toggle between the interactive form and YAML mode at any time. Changes made in one mode are reflected in the other.
