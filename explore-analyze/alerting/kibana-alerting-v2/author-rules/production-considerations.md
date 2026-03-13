---
navigation_title: Production considerations
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Guidance for running Kibana alerting v2 rules in production — scheduling, query performance, dispatcher capacity, and data retention."
---

% Content will be updated after performance testing is complete.

# Kibana alerting v2 production considerations [production-considerations-v2]

Guidance for running Kibana alerting v2 rules in production, including scaling, query performance, and resource management.

## Rule execution

Kibana alerting v2 rules execute via Task Manager. Each rule evaluation involves:

1. Loading the rule definition.
2. Building and running the ES|QL query against the source indices.
3. Writing signal or alert event documents to `.alerts-events-*`.
4. For alert-mode rules: computing state transitions and writing lifecycle events.

### Scheduling density

The number of rules you can run depends on:

- **Task Manager capacity** — the number of concurrent tasks {{kib}} can execute.
- **{{es}} query load** — each rule evaluation runs an ES|QL query. Complex queries or long lookback windows increase load.
- **Event write volume** — each evaluation writes one document per result row.

As a starting point, monitor Task Manager queue depth and {{es}} query latency to identify bottlenecks.

### Lookback window sizing

Longer lookback windows query more data. For rules that need long lookbacks (for example, 12-hour no-data detection):

- Use `STATS` aggregations to reduce the volume of intermediate results.
- Avoid scanning raw events over long time ranges without aggregation.
- Consider whether a shorter lookback with a different query pattern can achieve the same detection.

## Dispatcher

The dispatcher runs every 10 seconds and processes up to 10,000 episodes per batch. In high-volume environments:

- Episodes are processed oldest-first. If more than 10,000 episodes are pending, the newest ones are deferred.
- Workflow destinations should be designed for at-least-once delivery. Duplicate notifications are possible if the dispatcher restarts mid-batch.

## Data retention

Alert event documents in `.alerts-events-*` are append-only. Over time, the volume grows with each rule evaluation. Plan for:

- **Index lifecycle management (ILM)** — configure ILM policies to roll over, warm, and delete old alert events based on your retention requirements.
- **Storage capacity** — estimate storage by multiplying the number of rules, execution frequency, and average result rows per evaluation.

## Alert actions storage

Alert actions (acknowledge, snooze, fire, suppress) are stored in `.alerts-actions`. This index is used by the dispatcher for suppression tracking. It grows more slowly than the events data stream but should also be managed with ILM.

## Monitoring

Monitor Kibana alerting v2 health by:

- Checking Task Manager metrics for rule execution delays and failures.
- Querying `.alerts-events-*` for rule execution timestamps to detect gaps.
- Reviewing dispatcher outcomes in `.alerts-actions` for suppression rates and delivery failures.
- Using the execution history tab on rule and notification policy detail pages.
