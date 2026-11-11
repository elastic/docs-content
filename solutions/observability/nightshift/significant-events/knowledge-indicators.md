---
navigation_title: Knowledge Indicators
description: Knowledge Indicators automatically extract structured facts about services, infrastructure, and dependencies from raw log data in your sources, and generate ES|QL alerting rules that feed the Significant Events pipeline.
applies_to:
  serverless:
    observability: preview
products:
  - id: observability
  - id: kibana
  - id: cloud-serverless
---

# Knowledge Indicators [sig-events-ki]

Knowledge Indicators (KIs) are structured facts that Elastic extracts from your raw log data automatically without requiring schemas, service catalogs, or manual configuration. When you run extraction against a source, Elastic analyzes the raw data and returns facts about your environment: which services are running, the underlying infrastructure they rely on, how they depend on each other, and the log schemas they use.

Rather than a static configuration, this knowledge accumulates over time, automatically expires when a service disappears, and feeds directly into downstream capabilities like the [Significant Events detection pipeline](./how-it-works.md), topology maps, AI agent investigations, and dashboards.

To access Knowledge Indicators, select the {icon}`boxes_vertical` menu on the Elastic nightshift home page, then **Knowledge**, and open the **Knowledge Indicators** tab.

## Generate KIs [sig-events-ki-generate]

You can trigger KI extraction on demand or set up continuous KI onboarding at a specific interval.

On demand
:   To trigger KI extraction manually, select **Sources** at the top of the **Detections** page, select one or more sources, and select **Generate**. **Generate** stays unavailable until you select at least one source. To run only one step, open the menu next to **Generate**. **Generate KI Features** runs only feature identification on the selected sources, and **Generate KI Queries** runs only query generation. Each option uses the model that you choose in its submenu.

Continuous KI onboarding
:   When enabled, KI onboarding runs automatically on the enabled sources of the current space at the configured interval. Continuous KI onboarding turns on automatically when the space gets its first source. To change it:

    1. From the Elastic nightshift home page, select the {icon}`boxes_vertical` menu, then **Settings**, and open the **Detections** tab.
    1. Under **Continuous KI onboarding**, turn **Enable continuous KI onboarding** on or off.
    1. Set the **Onboarding interval (hours)**, the minimum number of hours between onboarding runs for a given source. Set it to `0` for no cooldown between runs.

    Continuous KI onboarding covers the enabled sources in the space.

## How KI extraction works [sig-events-ki-extraction]

The extraction pipeline samples a small batch of logs from a source and processes them through a combination of large language model (LLM) analysis and deterministic code generators. It accumulates its findings across multiple iterations, entirely configuration-free.

The pipeline runs up to five iterations. Each iteration fetches a batch of up to 20 documents assembled from three prioritized buckets:

| Bucket | Share | Strategy |
|---|---|---|
| Entity-filtered | 40% | Random sample that excludes documents matching already-discovered feature KI filters (feature KIs excluded by users), steering toward undiscovered patterns |
| Diverse | 40% | One representative document per log category, based on message structure |
| Random | 20% | Plain random sample to avoid systematic blind spots |

KIs found in one iteration are fed back as exclusions into the next, so each round focuses on what the previous one missed. This ensures quieter, less-represented services aren't crowded out by high-volume log categories.

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

Sampled documents are sent to an LLM that identifies the following feature KI types:

| Type | What it captures |
|------|-----------------|
| Entity | Distinct system components: services, applications, jobs |
| Infrastructure | Environment context: {{k8s}}, cloud provider, OS |
| Technology | Languages, frameworks, libraries, databases |
| Dependency | Relationships between components |
| Schema | Log format conventions: {{product.ecs}}, OpenTelemetry, custom |

Every feature KI must include stable identifying properties and cite direct evidence from the sampled logs. The LLM assigns a confidence score from 0–100 (where 0 is the lowest confidence and 100 is the highest) for each KI. The pipeline also tracks feature KIs excluded by users (false positives) and carries them forward to prevent re-identification in future runs.

### Deterministic generators [sig-events-ki-generators]

In parallel with LLM analysis, a set of deterministic code-based generators independently analyze the data to produce statistical summaries, log samples, pattern clusters, and error-specific feature KIs. Because these are computed rather than inferred, they always receive a confidence score of 100.

### Results handling [sig-events-ki-merge]

LLM results and computed feature KIs are merged and deduplicated. Known KIs reuse their existing UUIDs, new discoveries get fresh ones, and the pipeline drops user-excluded feature KIs. Surviving KIs are saved with an active status and an expiration date set 30 days out.

Extraction runs entirely as a background task and never blocks ingestion.

## KI types [sig-events-ki-types]

Knowledge Indicators fall into two categories: Feature KIs and Query KIs.

### Feature KIs [sig-events-ki-feature]

Feature KIs are descriptive and explain the contents of the source: what services are running, the infrastructure housing them, their dependencies, and the active tech stack.

Feature KIs carry a full data model:

- **`type` / `subtype`**: The category of the fact (Entity, Infrastructure, Technology, Dependency, Schema)
- **`title` / `description`**: A human-readable summary
- **`properties`**: Stable key-value pairs used to deduplicate findings across multiple runs
- **`confidence`**: 0–100. LLM-identified KIs score based on evidence quality. Deterministic KIs always score 100.
- **`evidence`**: 2–5 supporting log excerpts that justify the KI's existence
- **`filter`**: An optional [StreamLang](../../streams/streamlang.md) condition scoping the KI to specific documents


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

**MATCH queries** filter for specific log events, such as errors, exceptions, or failure messages:

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

Elastic nightshift turns query KIs into alerting rules automatically, with no review step. Each rule runs its {{esql}} query on a schedule and writes a match count to `.rule-events` for each time bucket. Only MATCH queries become rules; STATS queries can't be converted to alerting rules yet. The number of rules, and how often each one executes, is the main driver of alerting query load on your cluster.

To see the rules that detection is running, or to remove one that isn't useful, refer to [Review rules and signals](../audit-and-manage-detections.md#nightshift-detections-rules-signals). Deleting a rule keeps its query KI.

The Significant Events pipeline picks up from there. A Detection workflow runs change point aggregation against those per-rule counts and writes a document to `.significant_events-detections` when statistically significant shifts are found. A Discovery workflow then uses an LLM to process those documents.

## Continuous KI onboarding [sig-events-ki-continuous]

When continuous KI onboarding is enabled, a workflow runs every 35 minutes and processes up to five eligible sources per run. A source is eligible if:

- It's enabled
- No feature identification is running for it
- Enough time has elapsed since its last extraction (controlled by the **Onboarding interval (hours)** setting, default 12 hours)

Sources that have never been processed are always prioritized. Among remaining candidates, sources with the oldest last-completed extraction run are processed first.

The continuous onboarding workflow has a 34-minute timeout (one minute shorter than the 35-minute schedule, to prevent overlapping runs). If multiple runs would overlap, excess triggers are silently dropped.

Turning off continuous KI onboarding cancels any in-flight extraction tasks and disables the workflow. Re-enabling turns it back on. Already-extracted KIs are preserved throughout.

### Continuous KI onboarding settings

| Setting | Default | Description |
|---|---|---|
| `observability:nightshiftContinuousOnboardingEnabled` | `false` | Enables or disables continuous KI onboarding in the current space |
| `observability:nightshiftContinuousOnboardingIntervalHours` | `12` | Minimum hours between onboarding runs for a single source. `0` means no cooldown between runs |

These settings are only modifiable through the **Settings** page, which you reach from the {icon}`boxes_vertical` menu on the Elastic nightshift home page.

## KI lifecycle and maintenance [sig-events-ki-lifecycle]

KIs auto-expire after 30 days if not observed in subsequent extraction runs. KIs for decommissioned services are automatically removed without manual cleanup. If a service comes back online, its KIs are re-extracted automatically.

Users can mark individual Feature KIs as false positives. The system carries those exclusions forward into future runs to prevent re-identification.