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

This reference describes how the detection pipeline, Significant Events, processes data, what runs where, and how to trace results with {{esql}}. It's for operators and engineers. For how detection works from a user's point of view, refer to [How detection works](../detection/index.md).

The pipeline has four sequential phases, each building on the outputs of the previous:

- [Phase 1: Knowledge Indicators (KIs) extraction](#sig-events-hiw-ki): large language model (LLM) and programmatic analysis of source data
- [Phase 2: Rule generation](#sig-events-hiw-rules): An agent generates query KIs from the feature KIs, and the high-severity match queries become rules
- [Phase 3: Rule execution](#sig-events-hiw-execution): Alerting framework runs promoted rules continuously
- [Phase 4: Discovery](#sig-events-hiw-discovery): Detection and discovery workflows convert alert signals into confirmed significant events

## Phase 1: KI extraction [sig-events-hiw-ki]

KIs are stable, evidence-backed facts about the services and infrastructure present in a source's data. Rule generation works from KIs, not from raw documents, which keeps detection logic independent of the data format. For what KIs are and how to review them, refer to [Knowledge Indicators](../context/knowledge-indicators.md).

### How KI extraction works [sig-events-ki-extraction]

Extraction samples a small batch of logs from a source, analyzes it with a language model and with code-based generators in parallel, and merges the results. It runs in the background and never blocks ingestion.

The process runs up to five rounds. Each round looks at up to 20 documents and steers toward patterns that earlier rounds didn't find, so quiet services aren't crowded out by noisy ones. Each round assembles its batch from three buckets:

| Bucket | Share | Strategy |
| --- | --- | --- |
| Entity-filtered | 40% | A random sample that leaves out documents that match KIs already found or excluded, to steer toward patterns not yet found |
| Diverse | 40% | One document for each log category, based on message structure |
| Random | 20% | A plain random sample, to avoid blind spots |

KIs found in one round are fed into the next as exclusions.

### Language model analysis [sig-events-ki-llm]

{{nightshift}} sends the sampled documents to a language model, which identifies feature KIs of the five types: Entity, Infrastructure, Technology, Dependency, and Schema. The model is instructed to prioritize services and databases over individual instances like pods or hosts. Every KI must have stable identifying properties and cite evidence from the sample. The model assigns each KI a confidence score from 0 to 100. Feature KIs that users excluded are passed along, so the model doesn't identify them again.

### Code-based generators [sig-events-ki-generators]

In parallel, code-based generators compute statistical summaries, log samples, pattern clusters, and error-specific KIs. Because they're computed, not inferred, they always have a confidence of 100. To show them on the **Knowledge Indicators** tab, turn on **Show computed features**.

### Merging the results [sig-events-ki-merge]

{{nightshift}} merges and deduplicates the results of both on `type`, `subtype`, and `properties`. Known KIs keep their IDs, KIs found for the first time get an ID, and excluded KIs are dropped. The rest are written to `.significant_events-knowledge_indicators` as active, with an expiry date 30 days out. KIs that aren't observed again expire.

### KI data model [sig-events-hiw-ki-types]

A feature KI has these fields:

- **`type` / `subtype`**: The category of the fact, such as Entity or Dependency.
- **`title` / `description`**: A human-readable summary.
- **`properties`**: Stable key-value pairs. They identify the KI across runs, so a later extraction updates the KI instead of creating a duplicate.
- **`confidence`**: 0 to 100. KIs from the language model score by evidence quality. Computed KIs always score 100.
- **`evidence`**: Two to five log excerpts that support the KI.
- **`filter`**: An optional [StreamLang](/solutions/observability/streams/streamlang.md) condition that scopes the KI to specific documents.

Example dependency KI:

```json
{
  "type": "dependency",
  "subtype": "service_dependency",
  "title": "inventory-api → encore",
  "description": "inventory-api queries the Postgres database encore, observed in error logs",
  "properties": {
    "source": "inventory-api",
    "target": "encore",
    "protocol": "postgresql"
  },
  "confidence": 85,
  "evidence": [
    "ERROR inventory-api GET /tickets failed: canceling statement due to lock timeout (SQLSTATE 55P03) db=encore",
    "inventory-api pool=encore active=20 idle=0 waiting=14"
  ],
  "filter": { "field": "service.name", "eq": "inventory-api" },
  "status": "active",
  "expires_at": "2026-12-11T00:00:00Z"
}
```

### Continuous onboarding schedule [sig-events-hiw-ki-lifecycle]

[Continuous KI onboarding](../context/knowledge-indicators.md#sig-events-ki-continuous) schedules sources like this:

- A run starts every 35 minutes and processes up to five eligible sources.
- A source is eligible when it's enabled, no extraction is running for it, and its onboarding interval has passed since its last extraction.
- Sources that were never processed go first. Then sources with the oldest extraction go first.
- A run times out after 34 minutes, so runs never overlap. If a run would overlap, the trigger is dropped.

The **Settings** page stores these values in two advanced settings, which you can't change anywhere else:

| Setting | Default | Description |
| --- | --- | --- |
| `observability:nightshiftContinuousOnboardingEnabled` | `false`, set to `true` when the space gets its first source | Turns continuous KI onboarding on or off in the current space |
| `observability:nightshiftContinuousOnboardingIntervalHours` | `12` | Minimum hours between onboarding runs for one source. `0` means no wait. |

## Phase 2: Rule generation [sig-events-hiw-rules]

Once a source has feature KIs, an agent generates query KIs for it. It reads the source's feature KIs, writes {{esql}} queries against the source for the failure modes of the services and technologies it found, and validates each query before it saves it. Each query KI gets a severity score from 0 to 100.

Rules are therefore scoped to the services and failure modes present in each source. Match query KIs with a high severity score become rules.

### From query KIs to rules [sig-events-ki-downstream]

Each rule runs its query on a schedule and counts the matches. When the count changes in a way that stands out, detection records a signal, and related signals become a significant event.

For which query KIs become rules and how to promote others, refer to [Where rules come from](../detection/rules-and-signals.md#nightshift-detection-rules-origins).

The number of rules, and how often they run, is the main driver of query load on your cluster. To review or delete rules, refer to [Rules and signals](../detection/rules-and-signals.md).

## Phase 3: Rule execution and detection [sig-events-hiw-execution]

Each promoted MATCH rule runs as an alerting rule on a single shared cadence of every 5 minutes with a 7-minute lookback. Each run writes compact metric series (`{ bucket, metric_value }` pairs) to `.rule-events`, not copies of matching source documents.

The 7-minute lookback on a 5-minute cadence means adjacent runs cover the same minutes. Readers use `MAX(metric_value)` per minute when building occurrence charts and change-point input, so overlapping runs don't double-count.

**Severity and cadence**: All MATCH rules share the same 5-minute cadence with a 7-minute lookback schedule. Severity drives the detection analysis profile applied in Phase 4: the lookback window and bucket size used for change-point analysis (critical: ~40m window / 1m buckets; default: ~125m window / 5m buckets).

## Phase 4: Discovery [sig-events-hiw-discovery]

Discovery converts raw alert signals into confirmed significant events in two stages:

- [Detection Workflow](#sig-events-hiw-detection): Change point aggregation per alerting rule, written to the detections index
- [Discovery Workflow](#sig-events-hiw-discovery-agent): Discovery agent generates hypotheses, performs triage, and promotes confirmed significant events

### Detection [sig-events-hiw-detection]

A Detection workflow reads `.rule-events`, buckets each rule's alerts by time, and runs the change point aggregation function against those counts to detect statistically significant shifts. When a shift is found, a document is appended to the detections index. The most recent detection document for a rule reflects its current state, for example, whether it's still producing an unusual rate of alerts or has returned to normal.

Change point detection is per-rule. A source can have many independent rules, and one rule recovering doesn't collapse the signal from others still anomalous on the same source.

### Discovery agent [sig-events-hiw-discovery-agent]

A Discovery workflow reads unhandled detection documents and calls the Discovery agent. The Discovery agent reads detection signals, writes discovery documents that describe what is happening, and verifies each hypothesis. It opens a significant event when a current failure is confirmed or remains plausibly unverified.

Only the lifecycle process sets **Recovering**, never a person or the agent. An event never starts as **Recovering** or **Inactive**. For what each status means, refer to [Status](../detection/significant-events.md#nightshift-detection-events-status).

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

- [How detection works](../detection/index.md): Get an overview of how detection works
- [Operator guide](./operator-guide.md): Learn more about system impact, cost drivers, and operational procedures
- [Knowledge Indicators](../context/knowledge-indicators.md): Review, exclude, and keep KIs