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
- [Cost drivers](#sig-events-op-costs): Large language model (LLM) call sites and token usage by phase
- [Pause and resume](#sig-events-op-disable): How to pause Significant Events activity or stop Knowledge Indicator (KI) refresh
- [Recovery procedures](#sig-events-op-recovery): Symptoms and actions for common degraded states

## What runs where [sig-events-op-components]

The following table shows each pipeline component, where it runs, what triggers it, and what it reads and writes:

| Component | Uses | Trigger | Reads | Writes |
|---|---|---|---|---|
| KI feature identification | Task Manager + Workflow | On-demand / continuous extraction | Source data | `.significant_events-knowledge_indicators` |
| KI query generation | Workflow | On-demand | Feature KIs + existing queries | Query KI assets |
| Alerting rule execution | {{alerting-v2-system}} → {{es}} | Shared schedule | Source data using {{esql}} | `.rule-events` |
| Detection Workflow | Workflows | Cron 10m | `.rule-events` | `.significant_events-detections` |
| Discovery Workflow | Workflows + Agent Builder | Cron 10m | `.significant_events-detections` + KIs | `.significant_events-discoveries`, `.rule-events` |

% TODO(verify): Is this table still accurate for Tech Preview? Source: nightshift-program#1103 and #1104 moved KI feature identification and query generation to Agent Builder agents, and #1760 added a status workflow that runs without an agent. I couldn't confirm the workflow triggers or the `.significant_events-discoveries` data stream in the Kibana code.

## System impact [sig-events-op-impact]

The following sections describe the query load, pipeline lag, memory, and storage growth you can expect when running Significant Events. These are observable signals, not hard guarantees.

**Alerting rule query load**

One {{alerting-v2-system-short}} rule runs for each promoted query KI, in [**Collect evidence** mode](/explore-analyze/alerting/esql/rules/configure-rule-mode.md). All of these rules run on the same [shared schedule](how-it-works.md#sig-events-hiw-execution), and each run records a match count in `.rule-events` for each time bucket. These matches don't open alerts or appear on the **Alerts** page. On each detection cycle, change point aggregation runs separately for each active rule, against that rule's per-time-bucket match counts. Document volume in `.rule-events` grows with the number of promoted rules and how often they execute.

**Pipeline lag**

The following table provides illustrative estimates of how long each phase takes from trigger to output, based on workflow schedules:

| Phase | Typical lag |
|---|---|
| First detection | ~10 min |
| Discovery | ~10 min after detection |
| New significant event | Sync with discovery |
| Stale re-review | Up to ~10 min |

**{{kib}} memory**

Agent runs add memory pressure. Observe {{kib}} memory under realistic load. Exact memory requirements depend on your workload. Measure under realistic load before committing to a configuration.

**Ingest assumptions**

Sources must have recent data for KI extraction to produce useful results. Empty sources or sources with very sparse data produce weak KIs, which produce weak query KIs, which produce fewer promoted rules.

**Storage growth**

Significant Events writes to the following data streams:

| Data stream | Written by | Growth driver |
|---|---|---|
| `.significant_events-detections` | Detection Workflow | Append-only; one document per observed state transition per rule |
| `.significant_events-discoveries` | Discovery agent | Append-only; one document per discovery state change |

The Discovery agent writes significant events as alert documents to `.rule-events`, the same index that holds rule execution results, so you can manage and route them like any other alert.

The `.significant_events-detections` data stream uses a data stream lifecycle (DSL) with a default 90-day retention. You can override retention using the data stream lifecycle API. See [{{esql}} traceability](./how-it-works.md#sig-events-hiw-traceability) for the full index layout and traceability guidance.

## Cost drivers [sig-events-op-costs]

LLM costs scale with the number of sources, the number of promoted rules, and whether you enable continuous extraction. The pipeline has the following LLM call sites with different cost profiles:

| Phase | Cadence | Cost profile |
|---|---|---|
| Feature identification | Per source onboarding + optional continuous (up to 5 sources per 35-minute run) | Highest token volume; uses a fast classification model |
| Query generation | Per source after feature KIs exist | Medium; requires reasoning and ES\|QL validation |
| Discovery agent (including triage) | ~10 min cycles when unprocessed detections exist | Bursty; scales with the number of active alerting rules firing |

Continuous extraction is the largest cost multiplier. When enabled, feature identification runs on a recurring schedule across all eligible sources. Enabling it on many sources significantly increases token consumption.

### Daily run limits [sig-events-op-cost-limits]

Deployment-wide daily run limits cap how many scheduled runs each activity can start per UTC day, so scheduled automation can't consume an unbounded token budget. When a limit is reached, new scheduled runs in that category can be denied until the UTC day resets. The limits apply only to scheduled automation: manual runs are never limited.

## Pause and resume [sig-events-op-disable]

To pause detection, select the {icon}`boxes_vertical` menu on the Elastic nightshift home page, then **Settings**, and open the **Detections** tab. Managing these settings requires the manage engines privilege.

Select **Pause detection engine**, then confirm. Pausing stops detection activity in the current space, including knowledge indicator extraction, query alerting, rule creation, and significant event discovery. It disables the Significant Events workflows in the space and cancels their in-flight executions, and it disables the alerting rules that back knowledge indicator queries. Workflows that every space shares stay on, but their executions in this space are cancelled. Other spaces keep running, and no data is deleted.

Resuming restores the managed workflows and rules that pause disabled, and turns scheduled discovery and continuous onboarding back on only if they were enabled before the pause.

### Stop background KI refresh only

To stop continuous onboarding without pausing Significant Events:

1. From the Elastic nightshift home page, select the {icon}`boxes_vertical` menu, then **Settings**, and open the **Detections** tab.
2. Under **Continuous KI onboarding**, turn off **Enable continuous KI onboarding**.

Already-extracted KIs aren't deleted, and manually triggered extractions continue to work.


## Recovery procedures [sig-events-op-recovery]

### KI extraction running constantly

**Symptom**: Continuous extraction appears to be running continuously or processing sources more frequently than expected.

**Action**: Check the **Continuous KI onboarding** setting. If enabled, check the number of sources eligible for extraction — more sources means more runs per cycle.

### High LLM cost

**Symptom**: Unexpectedly high token usage or inference costs.

**Action**:

1. Turn off **Enable continuous KI onboarding** first — this is the primary cost multiplier.
2. Check how many sources are eligible for continuous extraction.

### Incidents not clearing

**Symptom**: A significant event remains open after the underlying condition appears to have resolved.

**Action**: This is expected behavior. An event moves to recovering when every member rule was last judged healthy. It becomes inactive only after every confirming signal on it has been re-checked and cleared, and while any of them is unresolved, the event stays active. A rule going quiet isn't sufficient on its own.

## Learn more [sig-events-operator-learn-more]

- [Detection engine](../core-components/detection-engine.md): Get an overview of how detection works
- [Elastic nightshift](../nightshift.md): Get an overview of Elastic nightshift and its requirements
- [How Significant Events works](./how-it-works.md): Understand how Significant Events processes data, what runs where, and how to trace results across the system
- [Knowledge Indicators](./knowledge-indicators.md): Get an in-depth overview of how KIs work
