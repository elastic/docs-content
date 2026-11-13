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

Use this guide to understand how detection, also called Significant Events, affects your project, what it costs, and how to manage it. It's for operators. For how detection works from a user's point of view, refer to [How detection works](../detection/index.md).

- [What runs where](#sig-events-op-components): Which components run on {{kib}}, {{es}}, and Workflows
- [System impact](#sig-events-op-impact): Query load, pipeline lag, and storage growth
- [Cost drivers](#sig-events-op-costs): Large language model (LLM) call sites and token usage by phase
- [Pause and resume](#sig-events-op-disable): How to pause Significant Events activity or stop Knowledge Indicator (KI) refresh
- [Recovery procedures](#sig-events-op-recovery): Symptoms and actions for common degraded states

## What runs where [sig-events-op-components]

The following table shows each pipeline component, where it runs, what triggers it, and what it reads and writes:

| Component | Uses | Trigger | Reads | Writes |
|---|---|---|---|---|
| KI feature identification | Workflow + Agent Builder agent | Source onboarding, on demand or continuous | Source data | `.significant_events-knowledge_indicators` |
| KI query generation | Workflow + Agent Builder agent | Source onboarding, after feature identification | Feature KIs + existing queries | Query KIs |
| Alerting rule execution | {{alerting-v2-system}} → {{es}} | Shared schedule | Source data using {{esql}} | `.rule-events` |
| Detection Workflow | Workflows | Scheduled discovery, every 10 min by default | `.rule-events` | `.significant_events-detections` |
| Discovery Workflow | Workflows + Agent Builder | Scheduled discovery review, every 10 min by default | `.significant_events-detections` + KIs | `.significant_events-discoveries`, `.rule-events` |

To change the schedules, refer to [Scheduled detection](../settings.md#nightshift-settings-scheduled).

## System impact [sig-events-op-impact]

The following sections describe the query load, pipeline lag, and storage growth you can expect when running Significant Events. These are observable signals, not hard guarantees.

**Alerting rule query load**

One {{alerting-v2-system-short}} rule runs for each promoted query KI, in [**Collect evidence** mode](/explore-analyze/alerting/esql/rules/configure-rule-mode.md). All of these rules run on the same [shared schedule](how-it-works.md#sig-events-hiw-execution), and each run records a match count in `.rule-events` for each time bucket. These matches don't open alerts or appear on the **Alerts** page. On each detection cycle, change point aggregation runs separately for each active rule, against that rule's per-time-bucket match counts. Document volume in `.rule-events` grows with the number of promoted rules and how often they execute.

**Pipeline lag**

The following table provides illustrative estimates of how long each phase takes from trigger to output, based on workflow schedules, after rules exist:

| Phase | Typical lag |
|---|---|
| First detection | ~10 min |
| Discovery | ~10 min after detection |
| Significant event raised | Same run as discovery |
| Stale re-review | Up to ~10 min |

**Ingest assumptions**

Sources must have recent data for KI extraction to produce useful results. Empty sources or sources with very sparse data produce weak KIs, which produce weak query KIs, which produce fewer promoted rules.

**Storage growth**

Significant Events writes to the following data streams:

| Data stream | Written by | Growth driver |
|---|---|---|
| `.significant_events-detections` | Detection Workflow | Append-only; one document per observed state transition per rule |
| `.significant_events-discoveries` | Discovery agent | Append-only; one document per discovery state change |

The Discovery agent writes significant events as alert documents to `.rule-events`, the same index that holds rule execution results, so you can manage and route them like any other alert.

The `.significant_events-detections` data stream uses a data stream lifecycle (DSL) with a default 90-day retention. You can override retention using the data stream lifecycle API. For the full index layout and traceability guidance, refer to [{{esql}} traceability](./how-it-works.md#sig-events-hiw-traceability).

## Cost drivers [sig-events-op-costs]

LLM costs scale with the number of sources, the number of promoted rules, and whether you enable continuous extraction. The pipeline has the following LLM call sites with different cost profiles:

| Phase | Cadence | Cost profile |
|---|---|---|
| Feature identification | Per source onboarding + optional continuous (up to 5 sources per 35-minute run) | Highest token volume; uses a fast classification model |
| Query generation | Per source after feature KIs exist | Medium; requires reasoning and ES\|QL validation |
| Discovery agent (including triage) | ~10 min cycles when unprocessed detections exist | Bursty; scales with the number of active alerting rules firing |

Continuous extraction is the largest cost multiplier. When enabled, feature identification runs on a recurring schedule across all eligible sources. Enabling it on many sources significantly increases token consumption.

Daily run limits cap scheduled runs. Refer to [Detection run limits](../settings.md#nightshift-settings-detection-limits).

## Pause and resume [sig-events-op-disable]

Pausing stops all detection activity in the space and keeps your data. Refer to [Pause or resume detection](../settings.md#nightshift-settings-pause).

### Stop background KI refresh only [sig-events-op-stop-ki]

Turn off **Enable continuous KI onboarding**. Refer to [Continuous KI onboarding](../settings.md#nightshift-settings-ki-onboarding).

## Recovery procedures [sig-events-op-recovery]

### KI extraction running constantly [sig-events-op-ki-constant]

**Symptom**: Continuous extraction appears to be running continuously or processing sources more frequently than expected.

**Action**: Check the **Continuous KI onboarding** setting. If enabled, check the number of sources eligible for extraction. More sources mean more runs per cycle.

### High LLM cost [sig-events-op-high-cost]

**Symptom**: Unexpectedly high token usage or inference costs.

**Action**:

1. Turn off **Enable continuous KI onboarding** first — this is the primary cost multiplier.
2. Check how many sources are eligible for continuous extraction.

### Events not clearing [sig-events-op-not-clearing]

**Symptom**: A significant event remains open after the underlying condition appears to have resolved.

**Action**: This is expected. Refer to [Status](../detection/significant-events.md#nightshift-detection-events-status).

## Learn more [sig-events-operator-learn-more]

- [How detection works](../detection/index.md): Get an overview of how detection works
- [{{nightshift}}](../nightshift.md): Get an overview of {{nightshift}} and its requirements
- [How Significant Events works](./how-it-works.md): Understand how Significant Events processes data, what runs where, and how to trace results across the system
- [Knowledge Indicators](../context/knowledge-indicators.md): Get an in-depth overview of how KIs work
