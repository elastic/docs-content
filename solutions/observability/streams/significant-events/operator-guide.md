---
navigation_title: Operator guide
description: System impact, cost drivers, and operational procedures for cluster operators running Significant Events.
applies_to:
  serverless: experimental
  stack: experimental 9.5+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Operator guide [sig-events-operator]

Use this guide to understand how Significant Events affects your cluster and how to manage it.

- [What runs where](#sig-events-op-components): Which components run on {{kib}}, {{es}}, and Workflows
- [System impact](#sig-events-op-impact): Query load, pipeline lag, memory, and storage growth
- [Cost drivers](#sig-events-op-costs): LLM call sites and token usage by phase
- [Disable and re-enable](#sig-events-op-disable): How to stop the pipeline or pause Knowledge Indicator (KI) refresh
- [Recovery procedures](#sig-events-op-recovery): Symptoms and actions for common degraded states

## What runs where [sig-events-op-components]

The following table shows each pipeline component, where it runs, what triggers it, and what it reads and writes:

| Component | Uses | Trigger | Reads | Writes |
|---|---|---|---|---|
| KI feature identification | Task Manager + Workflow | On-demand / continuous extraction | Stream logs | `.significant_events-knowledge_indicators` |
| KI query generation | Workflow | On-demand | Features + existing queries | Query KI assets |
| Alerting rule execution | {{kib}} alerting → {{es}} | Per-rule schedule | Stream data using {{esql}} | `.rule-events` |
| Detection Workflow | Workflows | Cron 10m | `.rule-events` | `.significant_events-detections` |
| Discovery Workflow | Workflows + Agent Builder | Cron 10m | `.significant_events-detections` + KIs | `.significant_events-discoveries` |
| Triage workflow | {{kib}} Workflows + Agent Builder | Cron 10m | `.significant_events-discoveries` | `.significant_events-events` |

## System impact [sig-events-op-impact]

The following sections describe the query load, pipeline lag, memory, and storage growth you can expect when running Significant Events. These are observable signals, not hard guarantees.

**Alerting rule query load**

One {{esql}} alerting rule runs for each promoted query KI. Each rule executes on its own schedule, creating an alert when its query matches. On each detection cycle, change point aggregation runs separately for each active rule, against that rule's per-time-bucket alert counts. Document volume in `.rule-events` grows with the number of promoted rules and how often they execute.

**Pipeline lag**

The following table provides illustrative estimates of how long each phase takes from trigger to output, based on workflow schedules:

| Phase | Typical lag |
|---|---|
| First detection | ~10 min |
| Discovery | ~10 min after detection |
| New Significant Event | Sync with discovery |
| Stale re-review | Up to ~10 min |

**{{kib}} memory**

Agent runs add memory pressure. Observe {{kib}} memory under realistic load. Exact memory requirements depend on your workload. Measure under realistic load before committing to a configuration.

**Ingest assumptions**

Streams must have recent log data for KI extraction to produce useful results. Empty streams or streams with very sparse data produce weak KIs, which produce weak query KIs, which produce fewer promoted rules.

**Storage growth**

Significant Events writes to the following data streams:

| Data stream | Written by | Growth driver |
|---|---|---|
| `.significant_events-detections` | Detection Workflow | Append-only; one document per observed state transition per rule |
| `.significant_events-discoveries` | Discovery agent | Append-only; one document per discovery state change |
| `.significant_events-events` | Judge | Append-only; one document per Significant Event state change |

The `.significant_events-detections` and `.significant_events-discoveries` data streams use DSL with a default 90-day retention (the events data stream currently has no default retention configured). You can override retention per stream using the DSL API. See [{{esql}} traceability](./how-it-works.md#sig-events-hiw-traceability) for the full index layout and traceability guidance.

## Cost drivers [sig-events-op-costs]

LLM costs scale with the number of streams, the number of promoted rules, and whether you enable continuous extraction. The pipeline has the following LLM call sites with different cost profiles:

| Phase | Cadence | Cost profile |
|---|---|---|
| Feature identification | Per stream onboarding + optional continuous (up to 5 streams per 35-minute run) | Highest token volume; uses a fast classification model |
| Query generation | Per stream after features exist | Medium; requires reasoning and ES\|QL validation |
| Discovery agent | ~10 min cycles when unprocessed detections exist | Bursty; scales with the number of active alerting rules firing |
| Judge agent | Sync on new discoveries; stale re-review ~10 min | Lower frequency; scales with the number of open discoveries |

Continuous extraction is the largest cost multiplier. When enabled, feature identification runs on a recurring schedule across all eligible streams. Enabling it on a large number of streams significantly increases token consumption.

<!-- Billing policy still needs to be defined/documented -->

## Disable and re-enable [sig-events-op-disable]

### Disable Significant Events entirely

Set `observability:streamsSigEventsScheduledDiscoveryEnabled` to `false` in {{kib}} settings. This stops the detection, discovery, and triage workflows.

### Stop background KI refresh only

To stop continuous extraction without disabling Significant Events:

1. Select **Significant Events** → **Settings**.
2. Under **Continuous KI extraction**, turn off **Enable continuous KI extraction**.

Turning off continuous extraction cancels all in-flight feature identification tasks and turns off the continuous extraction workflow. Already-extracted KIs are not deleted. Manually-triggered extractions continue to work.


## Recovery procedures [sig-events-op-recovery]

### KI extraction running constantly

**Symptom**: Continuous extraction appears to be running continuously or processing streams more frequently than expected.

**Action**: Check the continuous extraction setting. If enabled, check the number of streams eligible for extraction — more streams means more runs per cycle.

### High LLM cost

**Symptom**: Unexpectedly high token usage or inference costs.

**Action**:

1. Disable continuous extraction first — this is the primary cost multiplier.
2. Check how many streams are eligible for continuous extraction.

### Incidents not clearing

**Symptom**: A Significant Event remains open after the underlying condition appears to have resolved.

**Action**: This is expected behavior. The judge agent must independently verify that the underlying condition has resolved. Detections clearing alone is not sufficient.

## Learn more [sig-events-operator-learn-more]

- [Significant Events overview](./index.md): Get an overview and prerequisites for Significant Events
- [How Significant Events works](./how-it-works.md): Understand how Significant Events processes data, what runs where, and how to trace results across the system
- [Knowledge Indicators](./knowledge-indicators.md): Get an in-depth overview of how KIs work