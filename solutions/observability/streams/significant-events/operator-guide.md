---
navigation_title: Operator guide
description: System impact, cost drivers, and operational procedures for cluster operators running Significant Events.
applies_to:
  serverless:
    observability: preview
products:
  - id: observability
  - id: kibana
  - id: cloud-serverless
---

# Operator guide [sig-events-operator]

Use this guide to understand how Significant Events affects your cluster and how to manage it.

- [What runs where](#sig-events-op-components): Which components run on {{kib}}, {{es}}, and Workflows
- [System impact](#sig-events-op-impact): Query load, pipeline lag, memory, and storage growth
- [Cost drivers](#sig-events-op-costs): LLM call sites and token usage by phase
- [Pause and resume](#sig-events-op-disable): How to pause Significant Events activity or stop Knowledge Indicator (KI) refresh
- [Recovery procedures](#sig-events-op-recovery): Symptoms and actions for common degraded states

## What runs where [sig-events-op-components]

The following table shows each pipeline component, where it runs, what triggers it, and what it reads and writes:

<!-- DRAFT NOTE: It seems nothing defines or writes to `.significant_events-discoveries`. Need to verify if it was retired. -->

| Component | Uses | Trigger | Reads | Writes |
|---|---|---|---|---|
| KI feature identification | Task Manager + Workflow | On-demand / continuous extraction | Stream logs | `.significant_events-knowledge_indicators` |
| KI query generation | Workflow | On-demand | Features + existing queries | Query KI assets |
| Alerting rule execution | {{kib}} alerting → {{es}} | Per-rule schedule | Stream data using {{esql}} | `.rule-events` |
| Detection Workflow | Workflows | Cron 10m | `.rule-events` | `.significant_events-detections` |
| Discovery Workflow | Workflows + Agent Builder | Cron 10m | `.significant_events-detections` + KIs | `.significant_events-discoveries`, `.rule-events` |

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

The Discovery agent writes Significant Events as alert documents to `.rule-events`, the same index that holds rule execution results, so you can manage and route them like any other alert.

The `.significant_events-detections` data stream uses DSL with a default 90-day retention. You can override retention using the DSL API. See [{{esql}} traceability](./how-it-works.md#sig-events-hiw-traceability) for the full index layout and traceability guidance.

## Cost drivers [sig-events-op-costs]

LLM costs scale with the number of streams, the number of promoted rules, and whether you enable continuous extraction. The pipeline has the following LLM call sites with different cost profiles:

| Phase | Cadence | Cost profile |
|---|---|---|
| Feature identification | Per stream onboarding + optional continuous (up to 5 streams per 35-minute run) | Highest token volume; uses a fast classification model |
| Query generation | Per stream after features exist | Medium; requires reasoning and ES\|QL validation |
| Discovery agent (including triage) | ~10 min cycles when unprocessed detections exist | Bursty; scales with the number of active alerting rules firing |

Continuous extraction is the largest cost multiplier. When enabled, feature identification runs on a recurring schedule across all eligible streams. Enabling it on a large number of streams significantly increases token consumption.

### Daily run limits [sig-events-op-cost-limits]

Deployment-wide daily run limits cap how many scheduled runs each activity can start per UTC day, so scheduled automation can't consume an unbounded token budget. When a limit is reached, new scheduled runs in that category can be denied until the UTC day resets. The limits apply only to scheduled automation: manual runs are never limited.

## Pause and resume [sig-events-op-disable]

You can pause all Significant Events activity from the settings page. Managing these settings requires the manage engines privilege.

Select **Pause Significant Events activity** to stop scheduled discovery, continuous onboarding, detections, investigations, and the alerting rules backing knowledge indicator queries. The pause applies across the entire deployment — every {{kib}} space — not only the current space. Existing data is kept.

Resuming restores the managed workflows and rules that pause disabled, and turns scheduled discovery and continuous onboarding back on only if they were enabled before the pause.

### Stop background KI refresh only

To stop continuous onboarding without pausing Significant Events:

1. Go to the Significant Events settings.
2. Under **Continuous KI onboarding**, turn off **Enable continuous KI onboarding**.

Already-extracted KIs are not deleted, and manually-triggered extractions continue to work.


## Recovery procedures [sig-events-op-recovery]

### KI extraction running constantly

**Symptom**: Continuous extraction appears to be running continuously or processing streams more frequently than expected.

**Action**: Check the **Continuous KI onboarding** setting. If enabled, check the number of streams eligible for extraction — more streams means more runs per cycle.

### High LLM cost

**Symptom**: Unexpectedly high token usage or inference costs.

**Action**:

1. Turn off **Enable continuous KI onboarding** first — this is the primary cost multiplier.
2. Check how many streams are eligible for continuous extraction.

### Incidents not clearing

**Symptom**: A Significant Event remains open after the underlying condition appears to have resolved.

**Action**: This is expected behavior. The Discovery agent must verify that the underlying condition has resolved. Detections clearing alone is not sufficient.

## Learn more [sig-events-operator-learn-more]

- [Significant Events overview](./index.md): Get an overview and prerequisites for Significant Events
- [Elastic nightshift](../../nightshift/nightshift.md): Get an overview of Elastic nightshift and its requirements
- [How Significant Events works](./how-it-works.md): Understand how Significant Events processes data, what runs where, and how to trace results across the system
- [Knowledge Indicators](./knowledge-indicators.md): Get an in-depth overview of how KIs work
