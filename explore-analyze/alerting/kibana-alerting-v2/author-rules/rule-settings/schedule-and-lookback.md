---
navigation_title: Schedule and lookback
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Configure how often a Kibana alerting v2 rule runs and how far back it looks when evaluating data."
---

# Kibana alerting v2 schedule and lookback [schedule-lookback-v2]

The schedule and lookback settings control how often a rule runs and how far back it looks when evaluating data.

## Execution interval

The execution interval (`schedule.every`) determines how frequently the rule evaluates.

## Lookback window

The lookback window (`schedule.lookback`) determines the time range that the ES|QL query covers.

Choose a lookback window that is at least as long as the execution interval to avoid gaps in coverage.
