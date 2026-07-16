---
navigation_title: Knowledge Indicators
description: Knowledge Indicators automatically extract structured facts about services, infrastructure, and dependencies from raw log data in Streams.
applies_to:
  serverless: preview
  stack: preview 9.4+
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

# Knowledge Indicators [streams-knowledge-indicators]

Knowledge Indicators (KIs) are structured facts that Elastic extracts from your raw log data automatically without requiring schemas, service catalogs, or manual configuration. When you run extraction against a log stream, Elastic analyzes the raw data and returns facts about your environment: which services are running, the underlying infrastructure they rely on, how they depend on each other, and the log schemas they use.

Rather than a static configuration, this knowledge accumulates over time, automatically expires when a service disappears, and feeds directly into downstream capabilities like Rules, topology maps, AI agent investigations, and dashboards.

To access Knowledge Indicators, open **Significant Events** from the Streams main page and select the **Knowledge Indicators** tab.

:::{admonition} Requirements
To use this feature, you need:

- A [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md), which can incur additional costs.
- The `observability:streamsEnableSignificantEvents` {{kib}} setting enabled.
:::

## Generate KIs [streams-ki-generate]

You can trigger KI extraction on demand or set up continuous extraction at a specific interval.

On demand
:   From the **Significant Events** page, select the streams you want to generate KIs for and select **Generate**.

Continuous extraction
:   When enabled, continuous extraction runs automatically on managed streams at the interval you configure. Continuous extraction is off by default. To enable it:

    1. From the **Streams** main page, navigate to **Significant Events** → **Settings**.
   1. Under **Continuous KI extraction**, turn on **Enable continuous KI extraction**.
   1. Set the **Extraction interval** in hours, and list any **Excluded streams** to skip during continuous extraction.

## How KI extraction works [streams-ki-extraction]

The extraction pipeline samples a small batch of logs from a stream and processes them through a combination of large language model (LLM) analysis and deterministic code generators. It accumulates its findings across multiple iterations, entirely configuration-free.

The pipeline runs multiple iterations, each time fetching a small sample of documents using a mix of random and entity-filtered documents to ensure full coverage of the system. KIs found in one iteration are fed back as exclusions into the next, so each round focuses on what the previous one missed — ensuring quieter, less-represented services aren't crowded out by noisier ones.

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

### LLM analysis [streams-ki-llm]

Sampled documents are sent to an LLM that identifies the following feature types:

| Type | What it captures |
|------|-----------------|
| Entity | Distinct system components: services, applications, jobs |
| Infrastructure | Environment context: Kubernetes, cloud provider, OS |
| Technology | Languages, frameworks, libraries, databases |
| Dependency | Relationships between components |
| Schema | Log format conventions: Elastic Common Schema (ECS), OTel, custom |

Every feature must include stable identifying properties and cite direct evidence from the sampled logs. The LLM assigns a confidence score from 0–100 for each KI. Features intentionally excluded by users (false positives) are also tracked and carried forward to prevent re-identification in future runs.

### Deterministic generators [streams-ki-generators]

In parallel with LLM analysis, a set of deterministic code-based generators independently analyze the data to produce statistical summaries, log samples, pattern clusters, and error-specific features. Because these are computed rather than inferred, they always receive a confidence score of 100.

### Merging results [streams-ki-merge]

LLM results and computed features are merged and deduplicated. Known KIs reuse their existing UUIDs, new discoveries get fresh ones, and user-excluded features are dropped. Surviving KIs are saved with an active status and an expiration date set seven days out.

Extraction runs entirely as a background task and never blocks ingestion. You can trigger it on demand from the stream detail view or the Significant Events Discovery UI.

## KI types [streams-ki-types]

Knowledge Indicators fall into two categories: Feature KIs and Query KIs.

### Feature KIs [streams-ki-feature]

Feature KIs are descriptive and explain the contents of the stream: what services are running, the infrastructure housing them, their dependencies, and the active tech stack.

Feature KIs carry a full data model:

- **`type` / `subtype`**: The category of the fact (Entity, Infrastructure, Technology, Dependency, Schema)
- **`title` / `description`**: A human-readable summary
- **`properties`**: Stable key-value pairs used to deduplicate findings across multiple runs
- **`confidence`**: 0–100. LLM-identified KIs score based on evidence quality. Deterministic KIs always score 100.
- **`evidence`**: 2–5 supporting log excerpts that justify the KI's existence
- **`filter`**: An optional [Streamlang](./streamlang.md) condition scoping the KI to specific documents

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

### Query KIs [streams-ki-query]

Query KIs are actionable. They are ready-to-run ES|QL queries targeting notable conditions like connection exhaustion, out-of-memory errors, or fatal exceptions. Each comes with a severity score from 0 to 100, and when promoted to Rules, they fire Events.

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

## Downstream uses [streams-ki-uses]

KIs serve as the contextual foundation for several capabilities:

**Rules**: Query KIs automatically generate active rules to surface signals without manual configuration.

**Topology graphs**: Dependency KIs construct an infrastructure graph inferred entirely from log data. No distributed tracing or manual configuration is required. During an incident, the graph immediately shows which upstream services are affected when a specific database or service goes down.

**AI agent investigations**: Instead of reconstructing basic facts during every incident, an AI agent begins with your system's actual topology and known failure modes. It identifies the relevant streams, runs the applicable queries, and formulates a specific hypothesis using the available KI context.

**Dashboards**: KIs drive AI-generated dashboard suggestions for your streams.

**Grok patterns**: KIs inform Grok pattern generation when you introduce new streams.

## KI lifecycle and maintenance [streams-ki-lifecycle]

KIs auto-expire after 7 days if not observed in subsequent extraction runs. KIs for decommissioned services are automatically removed without manual cleanup. If a service comes back online, its KIs are re-extracted automatically.

Users can mark individual Feature KIs as false positives. The system carries those exclusions forward into future runs to prevent re-identification.

Because KI extraction focuses on a specific classification task, analyzing around 20 log samples to identify services, infrastructure, and dependencies, it does not require a large frontier model. A fast, cost-effective model handles this classification without multi-step reasoning.
