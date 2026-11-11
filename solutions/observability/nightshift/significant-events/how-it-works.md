---
navigation_title: How it works
description: Pipeline internals for engineers and adopters — KI extraction, rule generation, detection, discovery, storage model, and ES|QL traceability.
applies_to:
  serverless:
    observability: preview
products:
  - id: observability
  - id: kibana
  - id: cloud-serverless
---

# How Significant Events works [sig-events-how-it-works]

This page describes the pipeline behavior for engineers and adopters who need to understand how Significant Events processes data, what runs where, and how to trace results across the system.

The pipeline has four sequential phases, each building on the outputs of the previous:

- [Phase 1: Knowledge Indicators (KIs) extraction](#sig-events-hiw-ki): large language model (LLM) and programmatic analysis of source data
- [Phase 2: Rule generation](#sig-events-hiw-rules): LLM generates detection rules using KIs as input
- [Phase 3: Rule execution](#sig-events-hiw-execution): Alerting framework runs promoted rules continuously
- [Phase 4: Discovery](#sig-events-hiw-discovery): Detection and discovery workflows convert alert signals into confirmed significant events

## Phase 1: KI extraction [sig-events-hiw-ki]

KIs are stable, evidence-backed facts about the services and infrastructure present in a source's data. The LLM that generates detection operates entirely on KIs. This keeps rule generation deterministic and decouples detection logic from data format specifics.

### How KIs are extracted

The pipeline runs up to five iterations, sampling up to 20 documents per round from entity-filtered, diverse, and random buckets. KIs found in one iteration are excluded from the next, steering each round toward undiscovered patterns. LLM analysis and deterministic code generators run in parallel; deterministic KIs always score 100 confidence. See [KI extraction](./knowledge-indicators.md#sig-events-ki-extraction) for the full extraction flow.

### KI types

KIs cover five types: Entity, Infrastructure, Technology, Dependency, and Schema. The model is instructed to prioritize services and databases over individual instances like pods or hosts. See [KI types](./knowledge-indicators.md#sig-events-ki-types) for the full data model.

### KI lifecycle

KIs are written to `.significant_events-knowledge_indicators` and deduplicated on `type`, `subtype`, and `properties`. KIs expire after 30 days if they aren't re-observed. See [KI lifecycles](./knowledge-indicators.md#sig-events-ki-lifecycle) for lifecycle and continuous extraction details.

## Phase 2: Rule generation [sig-events-hiw-rules]

Once a source has KIs, the LLM generates detection rules using the KIs as input. The generated rule is an {{esql}} query with conditions derived from the source's KIs.

The LLM operates in a reasoning loop: it retrieves the KIs for the source, analyzes what entities and technologies are present, then submits a batch of rules. This means rules are scoped to the specific services and failure modes present in each source.

% TODO(verify): What does a generated rule's {{esql}} query look like now that detection works on sources? Source: this page showed `FROM {stream},{stream}.*` and the `get_stream_features` and `add_queries` tools. nightshift-program#1311 moved the tools to source ids, and the Kibana significant_events plugin says KIs and events are keyed by source id.

## Phase 3: Rule execution and detection [sig-events-hiw-execution]

Each promoted MATCH rule runs as an alerting rule on a single shared cadence of every 5 minutes with a 7-minute lookback. Each run writes compact metric series (`{ bucket, metric_value }` pairs) to `.rule-events`, not copies of matching source documents.

The 7-minute lookback on a 5-minute cadence means adjacent runs cover the same minutes. Readers use `MAX(metric_value)` per minute when building occurrence charts and change-point input, so overlapping runs don't double-count.

**Severity and cadence**: All MATCH rules share the same 5-minute cadence with a 7-minute lookback schedule. Severity drives the detection analysis profile applied in Phase 4: the lookback window and bucket size used for change-point analysis (critical: ~40m window / 1m buckets; default: ~125m window / 5m buckets).

**STATS rules**: STATS KIs are generated but not yet backed as alerting rules.

## Phase 4: Discovery [sig-events-hiw-discovery]

Discovery converts raw alert signals into confirmed significant events in two stages:

- [Detection Workflow](#sig-events-hiw-detection): Change point aggregation per alerting rule, written to the detections index
- [Discovery Workflow](#sig-events-hiw-discovery-agent): Discovery agent generates hypotheses, performs triage, and promotes confirmed significant events

### Detection [sig-events-hiw-detection]

A Detection workflow reads `.rule-events`, buckets each rule's alerts by time, and runs the change point aggregation function against those counts to detect statistically significant shifts. When a shift is found, a document is appended to the detections index. The most recent detection document for a rule reflects its current state, for example, whether it's still producing an unusual rate of alerts or has returned to normal.

Change point detection is per-rule. A source can have many independent rules, and one rule recovering doesn't collapse the signal from others still anomalous on the same stream.

### Discovery agent [sig-events-hiw-discovery-agent]

A Discovery workflow reads unhandled detection documents and calls the Discovery agent. The Discovery agent reads detection signals, produces structured discovery documents describing what is happening, and verifies each hypothesis, and opens a significant event when a current failure is confirmed or remains plausibly unverified.

A significant event has one of three statuses:

- **Active**: A current failure is confirmed, or remains plausibly unverified.
- **Recovering**: Every member rule was last judged healthy. Only the lifecycle process sets this status, never a person or the agent, and an event never starts as recovering. A breach in any member rule returns it to active.
- **Inactive**: Every confirming signal on the event was re-checked and cleared. An event never starts as inactive. An operator can also deactivate an event with **Mark inactive**, in the **Actions** menu of the event's details.

Status transitions are written as alert documents to `.rule-events`.

Significant events are also written as alerts, so they can be managed, routed, and acted on like any other Elastic alert.

## {{esql}} traceability [sig-events-hiw-traceability]

{{esql}} is the exclusive query language across the pipeline. Every rule is expressed as {{esql}}. Every artifact is stored as an {{es}} document. This means any point in the pipeline is queryable without leaving {{esql}}.

| What to query | {{esql}} target |
|---|---|
| Knowledge Indicators | `FROM .significant_events-knowledge_indicators` |
| Alert documents (rule execution results) | `FROM .rule-events` |
| Detection state per rule | `FROM .significant_events-detections` |
| Significant events | `FROM .rule-events` |

**Traceability**: Significant-event alert documents are stored in `.rule-events`. Use `group_hash` to group versions of the same event. Queries must filter to alert documents from the Significant Events source.

## Learn more [sig-events-hiw-learn-more]

- [Detection engine](../core-components/detection-engine.md): Get an overview of how detection works
- [Operator guide](./operator-guide.md): Learn more about system impact, cost drivers, and operational procedures
- [Knowledge Indicators](./knowledge-indicators.md): Get an in-depth overview of how KIs work