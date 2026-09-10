---
navigation_title: How it works
description: Pipeline internals for engineers and adopters — KI extraction, rule generation, detection, discovery, storage model, and ES|QL traceability.
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

# How Significant Events works [sig-events-how-it-works]

This page describes the pipeline behavior for engineers and adopters who need to understand how Significant Events processes data, what runs where, and how to trace results across the system.

The pipeline has four sequential phases, each building on the outputs of the previous:

- [Phase 1: Knowledge Indicators (KIs) extraction](#sig-events-hiw-ki): LLM and programmatic analysis of stream logs
- [Phase 2: Rule generation](#sig-events-hiw-rules): LLM generates detection rules using KIs as input
- [Phase 3: Rule execution](#sig-events-hiw-execution): Alerting framework runs promoted rules continuously
- [Phase 4: Discovery](#sig-events-hiw-discovery): Detection, discovery, and triage workflows convert alert signals into confirmed Significant Events

## Phase 1: KI extraction [sig-events-hiw-ki]

KIs are stable, evidence-backed facts about the services and infrastructure present in a stream's log data. The LLM that generates detection operates entirely on KIs. This keeps rule generation deterministic and decouples detection logic from data format specifics.

### How KIs are extracted

The pipeline runs up to five iterations, sampling up to 20 documents per round from entity-filtered, diverse, and random buckets. KIs found in one iteration are excluded from the next, steering each round toward undiscovered patterns. LLM analysis and deterministic code generators run in parallel; deterministic KIs always score 100 confidence. See [KI extraction](./knowledge-indicators.md#sig-events-ki-extraction) for the full extraction flow.

### KI types

KIs cover five types: Entity, Infrastructure, Technology, Dependency, and Schema. The model is instructed to prioritize services and databases over individual instances like pods or hosts. See [KI types](./knowledge-indicators.md#sig-events-ki-types) for the full data model.

### KI lifecycle

KIs are written to `.significant_events-knowledge_indicators` and deduplicated on `type`, `subtype`, and `properties`. KIs expire after 30 days if they aren't re-observed. See [KI lifecycles](./knowledge-indicators.md#sig-events-ki-lifecycle) for lifecycle and continuous extraction details.

## Phase 2: Rule generation [sig-events-hiw-rules]

Once a stream has KIs, the LLM generates detection rules using the KIs as input. The generated rule is an {{esql}} query with conditions derived from the stream's KIs:

```
FROM {stream},{stream}.* METADATA _id | WHERE <esql_expression>
```

The LLM operates in a reasoning loop: it calls `get_stream_features` to retrieve KIs for the stream, analyzes what entities and technologies are present, then calls `add_queries` to submit a batch of rules. This means rules are scoped to the specific services and failure modes present in each stream.

## Phase 3: Rule execution and detection [sig-events-hiw-execution]

Each promoted MATCH rule runs as an alerting rule on a single shared cadence of every 5 minutes with a 7-minute lookback. Each run writes compact metric series (`{ bucket, metric_value }` pairs) to `.rule-events`, not copies of matching source documents.

The 7-minute lookback on a 5-minute cadence means adjacent runs cover the same minutes. Readers use `MAX(metric_value)` per minute when building occurrence charts and change-point input, so overlapping runs do not double-count.

**Severity and cadence**: All MATCH rules share the same 5 minute cadence with a 7 minute lookback schedule. Severity drives the detection analysis profile applied in Phase 4: the lookback window and bucket size used for change-point analysis (critical: ~40m window / 1m buckets; default: ~125m window / 5m buckets).

**STATS rules**: STATS KIs are generated but not yet backed as alerting rules.

## Phase 4: Discovery [sig-events-hiw-discovery]

Discovery converts raw alert signals into confirmed Significant Events. It runs as three sequenced workflows (detection, discovery, and triage) coordinated by an Orchestrator workflow.

- [Detection Workflow](#sig-events-hiw-detection): Change point aggregation per alerting rule, written to the detections index
- [Discovery Workflow](#sig-events-hiw-discovery-agent): Discovery agent generates hypotheses, written to the discoveries index
- [Triage Workflow](#sig-events-hiw-triage): Judge agent independently verifies and promotes, written to the events index

### Detection [sig-events-hiw-detection]

A Detection workflow reads `.rule-events`, buckets each rule's alerts by time, and runs the change point aggregation function against those counts to detect statistically significant shifts. When a shift is found, a document is appended to the detections index. The most recent detection document for a rule reflects its current state, for example, whether it's still producing an unusual rate of alerts or has returned to normal.

Change point detection is per-rule. A stream can have many independent rules, and one rule recovering does not collapse the signal from others still anomalous on the same stream.

### Discovery agent [sig-events-hiw-discovery-agent]

A Discovery workflow reads unhandled detection documents and calls the Discovery agent. The Discovery agent is a hypothesis agent. It reads detection signals and produces structured discovery documents describing what is happening. Its scope is observation only, describing the anomaly, not prescribing remediation.

### Triage and the Judge agent [sig-events-hiw-triage]

The Triage workflow reads unassessed discovery documents and calls the Judge agent. The Judge agent independently verifies the Discovery agent's hypothesis and sets the event status to open (page on-call), closed (confirmed settled), or dismissed (low severity and low confidence). The Judge agent runs in a separate invocation with no shared state. It receives the Discovery agent's output as input but is explicitly instructed to treat it as a hypothesis to challenge, not a conclusion to ratify. Status transitions are written as new documents to the events index.

The two-agent design is intended to prevent a single agent that both investigates and judges from confirming its own hypothesis.

## {{esql}} traceability [sig-events-hiw-traceability]

{{esql}} is the exclusive query language across the pipeline. Every rule is expressed as {{esql}}. Every artifact is stored as an {{es}} document. This means any point in the pipeline is queryable without leaving {{esql}}.

| What to query | {{esql}} target |
|---|---|
| Knowledge Indicators | `FROM .significant_events-knowledge_indicators` |
| Alert documents (rule execution results) | `FROM .rule-events` |
| Detection state per rule | `FROM .significant_events-detections` |
| Significant Events | `FROM .significant_events-events` |

**Traceability**: To trace a Significant Event back to its origin, use `event_id` as the durable key linking events to detections. From the events index, use `signals[].metadata.detection_id` to reach the detection document in `.significant_events-detections`, and `signals[].metadata.rule_uuid` to reach the alerting rule in `.rule-events`.

## Learn more [sig-events-hiw-learn-more]

- [Significant Events overview](./index.md): Get an overview and prerequisites for Significant Events
- [Operator guide](./operator-guide.md): Learn more about system impact, cost drivers, and operational procedures
- [Knowledge Indicators](./knowledge-indicators.md): Get an in-depth overview of how KIs work