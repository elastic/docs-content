---
navigation_title: Knowledge Indicators
description: Knowledge Indicators automatically extract structured facts about services, infrastructure, and dependencies from raw log data in Streams, and generate ES|QL alerting rules that feed the Significant Events pipeline.
applies_to:
  serverless:
    observability: preview
products:
  - id: observability
  - id: kibana
  - id: cloud-serverless
---

# Knowledge Indicators [sig-events-ki]

Knowledge Indicators (KIs) are structured facts that Elastic extracts from your raw log data automatically without requiring schemas, service catalogs, or manual configuration. When you run extraction against a log stream, Elastic analyzes the raw data and returns facts about your environment: which services are running, the underlying infrastructure they rely on, how they depend on each other, and the log schemas they use.

Rather than a static configuration, this knowledge accumulates over time, automatically expires when a service disappears, and feeds directly into downstream capabilities like the [Significant Events detection pipeline](./how-it-works.md), topology maps, AI agent investigations, and dashboards.

To access Knowledge Indicators, open **Significant Events** from the Streams main page and select the **Knowledge Indicators** tab.

## Generate KIs [sig-events-ki-generate]

You can trigger KI extraction on demand or set up continuous KI onboarding at a specific interval.

On demand
:   From the **Significant Events** page, select the streams you want to generate KIs for and select **Generate**.

Continuous KI onboarding
:   When enabled, KI onboarding runs automatically on managed streams at the configured interval. Continuous KI onboarding is off by default. To enable it:

    1. Open the Significant Events settings.
    1. Under **Continuous KI onboarding**, turn on **Enable continuous KI onboarding**.
    1. Set the **Onboarding interval (hours)**, the minimum number of hours between onboarding runs for a given stream. Set it to `0` for no cooldown between runs.

    Continuous KI onboarding covers the streams that match the index patterns in the **Data sources** section of the settings, plus query streams, which are always eligible regardless of index patterns.

## How KI extraction works [sig-events-ki-extraction]

The extraction pipeline samples a small batch of logs from a stream and processes them through a combination of large language model (LLM) analysis and deterministic code generators. It accumulates its findings across multiple iterations, entirely configuration-free.

The pipeline runs up to five iterations. Each iteration fetches a batch of up to 20 documents assembled from three prioritized buckets:

| Bucket | Share | Strategy |
|---|---|---|
| Entity-filtered | 40% | Random sample that excludes documents matching already-discovered feature filters (features excluded by users), steering toward undiscovered patterns |
| Diverse | 40% | One representative document per log category, based on message structure |
| Random | 20% | Plain random sample to avoid systematic blind spots |

KIs found in one iteration are fed back as exclusions into the next, so each round focuses on what the previous one missed. This ensures quieter, less-represented services are not crowded out by high-volume log categories.

For example, from a single nginx access log line:

```
192.168.1.45 - - [31/Mar/2026:14:23:01 +0000] "POST /api/v2/claims HTTP/1.1" 200 1247 "-" "claim-intake/1.4.2"
```

The pipeline extracts:

- **Entity**: `claim-intake` (identifiable as a service from the User-Agent)
- **Version**: `1.4.2` (extracted from the User-Agent string)
- **Technology**: nginx (the web server fielding the request)
- **Schema**: Combined Log Format

Similarly, from a Java service log:

```
2026-03-31T14:23:03.412Z INFO fraud-check --- [nio-8080-exec-3] c.e.FraudCheckService : Calling upstream POST http://policy-lookup:8081/v1/policy latency=142ms status=200
```

The pipeline extracts:

- **Entity**: `fraud-check` (a Spring Boot service)
- **Dependency**: `fraud-check` → `policy-lookup` (through an outbound HTTP call)
- **Technology**: Java, Spring Boot

### LLM analysis [sig-events-ki-llm]

Sampled documents are sent to an LLM that identifies the following feature types:

| Type | What it captures |
|------|-----------------|
| Entity | Distinct system components: services, applications, jobs |
| Infrastructure | Environment context: {{k8s}}, cloud provider, OS |
| Technology | Languages, frameworks, libraries, databases |
| Dependency | Relationships between components |
| Schema | Log format conventions: {{product.ecs}}, OTel, custom |

Every feature must include stable identifying properties and cite direct evidence from the sampled logs. The LLM assigns a confidence score from 0–100 (where 0 is the lowest confidence and 100 is the highest) for each KI. The pipeline also tracks features excluded by users (false positives) and carries them forward to prevent re-identification in future runs.

### Deterministic generators [sig-events-ki-generators]

In parallel with LLM analysis, a set of deterministic code-based generators independently analyze the data to produce statistical summaries, log samples, pattern clusters, and error-specific features. Because these are computed rather than inferred, they always receive a confidence score of 100.

### Results handling [sig-events-ki-merge]

LLM results and computed features are merged and deduplicated. Known KIs reuse their existing UUIDs, new discoveries get fresh ones, and the pipeline drops user-excluded features. Surviving KIs are saved with an active status and an expiration date set 30 days out.

Extraction runs entirely as a background task and never blocks ingestion.

## KI types [sig-events-ki-types]

Knowledge Indicators fall into two categories: Feature KIs and Query KIs.

### Feature KIs [sig-events-ki-feature]

Feature KIs are descriptive and explain the contents of the stream: what services are running, the infrastructure housing them, their dependencies, and the active tech stack.

Feature KIs carry a full data model:

- **`type` / `subtype`**: The category of the fact (Entity, Infrastructure, Technology, Dependency, Schema)
- **`title` / `description`**: A human-readable summary
- **`properties`**: Stable key-value pairs used to deduplicate findings across multiple runs
- **`confidence`**: 0–100. LLM-identified KIs score based on evidence quality. Deterministic KIs always score 100.
- **`evidence`**: 2–5 supporting log excerpts that justify the KI's existence
- **`filter`**: An optional [StreamLang](../streamlang.md) condition scoping the KI to specific documents

Example dependency KI:

```json
{
  "type": "dependency",
  "subtype": "service_dependency",
  "title": "api_gateway → inference_service",
  "description": "Service-to-service HTTP dependency from api_gateway to inference_service, observed in request logs",
  "properties": {
    "source": "api_gateway",
    "target": "inference_service",
    "protocol": "http"
  },
  "confidence": 85,
  "evidence": [
    "service.name=api_gateway http.url=/v1/inference peer.service=inference_service",
    "upstream=inference_service:8080 request=POST /v1/inference 200"
  ],
  "filter": { "field": "service.name", "eq": "api_gateway" },
  "status": "active",
  "expires_at": "2026-04-09T00:00:00Z"
}
```

The `properties` field keeps Feature KIs stable across multiple pipeline runs. When extraction runs again, Elastic recognizes an existing relationship and updates the KI's `last_seen` timestamp rather than creating a duplicate.

### Query KIs [sig-events-ki-query]

Query KIs are actionable. They are ready-to-run {{esql}} queries targeting notable conditions like connection exhaustion, out-of-memory errors, or fatal exceptions. Each comes with a severity score from 0 to 100.

Example query KI:

```json
{
  "kind": "query",
  "title": "PostgreSQL connection slot exhaustion",
  "description": "Fires when Postgres runs out of available connection slots",
  "severity_score": 90,
  "esql": {
    "query": "FROM logs-* | WHERE service.name == \"postgres\" AND message : \"remaining connection slots\""
  }
}
```

Query KIs are generated in two {{esql}} forms depending on what the LLM determines is most useful for detection:

**MATCH queries** filter for specific log events, such as errors, exceptions, failure messages:

```esql
FROM logs-mystream,logs-mystream.* METADATA _id, _source
| WHERE message : "connection refused" AND service.name == "api_gateway"
```

**STATS queries** aggregate metrics over time, such as rates, counts, or derived values. These are useful when the signal is a change in volume rather than the presence of a specific event:

```esql
FROM logs-mystream,logs-mystream.*
| STATS error_count = COUNT(*) WHERE level == "ERROR" BY service.name, @timestamp
```

### Downstream path: From query KIs to alerting rules [sig-events-ki-downstream]

When you promote a query KI, it becomes an alerting rule that runs its {{esql}} query on a schedule and writes a match count to `.rule-events` for each time bucket. Only MATCH queries can be promoted; STATS queries cannot be converted to alerting rules yet. The number of promoted query KIs, and how often each one executes, is the main driver of alerting query load on your cluster.

The Significant Events pipeline picks up from there. A Detection workflow runs change point aggregation against those per-rule counts and writes a document to `.significant_events-detections` when statistically significant shifts are found. A Discovery workflow then uses an LLM to process those documents.

## Continuous KI onboarding [sig-events-ki-continuous]

When continuous KI onboarding is enabled, a workflow runs every 35 minutes and processes up to five eligible streams per run. A stream is eligible if:

- It matches the configured index patterns, or a query stream (query streams are always eligible, regardless of index patterns)
- No feature identification is currently running for it
- No feature identification task is currently running for it
- Enough time has elapsed since its last extraction (controlled by the **Onboarding interval (hours)** setting, default 12 hours)

Streams that have never been processed are always prioritized. Among remaining candidates, streams with the oldest last-completed extraction run are processed first.

The continuous onboarding workflow has a 34-minute timeout (one minute shorter than the 35-minute schedule, to prevent overlapping runs). If multiple runs would overlap, excess triggers are silently dropped.

Turning off continuous KI onboarding cancels any in-flight extraction tasks and disables the workflow. Re-enabling turns it back on. Already-extracted KIs are preserved throughout.

### Continuous KI onboarding settings

| Setting | Default | Description |
|---|---|---|
| `observability:streamsContinuousKiExtractionEnabled` | `false` | Enables or disables continuous KI onboarding |
| `observability:streamsContinuousKiExtractionIntervalHours` | `12` | Minimum hours between onboarding runs for a single stream. `0` means no cooldown between runs |

These settings are only modifiable through the Significant Events Settings page.

## KI lifecycle and maintenance [sig-events-ki-lifecycle]

KIs auto-expire after 30 days if not observed in subsequent extraction runs. KIs for decommissioned services are automatically removed without manual cleanup. If a service comes back online, its KIs are re-extracted automatically.

Users can mark individual Feature KIs as false positives. The system carries those exclusions forward into future runs to prevent re-identification.