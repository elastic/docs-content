---
navigation_title: Knowledge Indicators
applies_to:
  serverless:
    observability: preview
description: Understand the Knowledge Indicators that Elastic nightshift extracts from your data, how detection uses them, and how to review, exclude, or keep them.
products:
  - id: observability
  - id: cloud-serverless
---

# Knowledge Indicators [sig-events-ki]

Knowledge Indicators (KIs) are what {{nightshift}} learns about your system from your data: which services run, what they depend on, which technologies they use, and which log patterns point to trouble. You don't need a service catalog or a schema. {{nightshift}} reads samples of the logs in your detection sources and writes the KIs itself.

Detection uses KIs to create rules and to find significant events. As your system changes, KIs follow: services that appear get KIs, and KIs for services that disappear expire.

## From a log line to Knowledge Indicators [nightshift-ki-example]

Say one of your detection sources contains this log line from `inventory-api`:

```text
2026-11-11T19:52:14.201Z ERROR inventory-api GET /tickets failed: canceling statement due to lock timeout (SQLSTATE 55P03) db=encore table=section_inventory
```

From this line and others like it, {{nightshift}} extracts:

| KI | Type | What it says |
| --- | --- | --- |
| `inventory-api` | Entity | A service called `inventory-api` exists. |
| `inventory-api` → `encore` | Dependency | `inventory-api` depends on the Postgres database `encore`. |
| PostgreSQL | Technology | The `encore` database runs on PostgreSQL. |
| Lock timeouts on `encore` | Query | An {{esql}} query that finds lock timeouts, with a severity score. Detection turns it into a rule. |

The first three are **feature KIs**: they describe your system. The last one is a **query KI**: it finds a known failure pattern.

## Where KIs come from [nightshift-ki-sources]

Detection samples the logs in each [source](../detection/sources.md) and extracts feature KIs and query KIs, then turns query KIs into rules. Refer to [How detection works](../detection/index.md#nightshift-detection-flow).

In Tech Preview, detection learns from logs only. Refer to [Known issues](../known-issues.md).

## Review KIs [nightshift-ki-review]

On the [**Knowledge** page](./index.md#nightshift-context-open), select the **Knowledge Indicators** tab.

:::{image} ../../../images/nightshift-knowledge-indicators.png
:alt: The Knowledge Indicators tab with filters for status, type, subtype, and source, and a table of KIs with their events, type, source, and durability
:screenshot:
:::

The table lists each KI with the number of **Events** it matched, its **Type** (**Match query**, **Stats query**, or a feature type), its **Source**, and its **Durability** (**Durable** or **Expiring**). Filter by type, subtype, source, or status (**Active** or **Excluded**). Turn on **Show computed features** to include statistical KIs.

Select a KI to read its description, confidence, evidence from your logs, and properties. Select **Open in Discover** to find the matching documents.

Is the tab empty? Detection hasn't learned anything yet. Select **Go to Sources** to add a source, or wait for the first extraction to finish.

## Generate KIs [sig-events-ki-generate]

{{nightshift}} extracts KIs when you add a source, and then again with [continuous KI onboarding](#sig-events-ki-continuous). To start an extraction yourself, refer to [Manage sources](../detection/sources.md#nightshift-detection-sources-manage).

## KI types [sig-events-ki-types]

| Kind | What it does | Types |
| --- | --- | --- |
| [Feature KIs](#sig-events-ki-feature) | Describe your system | Entity, Infrastructure, Technology, Dependency, Schema |
| [Query KIs](#sig-events-ki-query) | Find a notable condition in your logs | Match query, Stats query |

### Feature KIs [sig-events-ki-feature]

| Type | What it captures |
| --- | --- |
| Entity | Services, applications, and jobs |
| Infrastructure | Where things run, such as {{k8s}}, a cloud provider, or an operating system |
| Technology | Languages, frameworks, libraries, and databases |
| Dependency | Which component calls which |
| Schema | Log format conventions, such as {{product.ecs}}, OpenTelemetry, or a custom format |

Each feature KI cites evidence from your logs and has a confidence score from 0 to 100. KIs that {{nightshift}} computed from statistics always have 100. For the fields of a KI, refer to [KI data model](../significant-events/how-it-works.md#sig-events-hiw-ki-types).

### Query KIs [sig-events-ki-query]

Query KIs are ready-to-run {{esql}} queries for notable conditions, such as connection exhaustion, out-of-memory errors, or lock timeouts. Each has a severity score from 0 to 100.

- **Match query**: Finds specific log events, such as errors or failure messages.

  ```esql
  FROM logs-* METADATA _id, _source
  | WHERE service.name == "inventory-api" AND message : "lock timeout"
  ```

- **Stats query**: Counts or aggregates over time, for when the signal is a change in volume rather than one event.

  ```esql
  FROM logs-*
  | STATS error_count = COUNT(*) WHERE log.level == "ERROR" BY service.name, @timestamp
  ```

High-severity match queries become rules automatically, and you can promote the others. Stats queries can't become rules yet. Refer to [Where rules come from](../detection/rules-and-signals.md#nightshift-detection-rules-origins).

## KI lifecycle [sig-events-ki-lifecycle]

KIs stay current without manual cleanup:

- **Expiring**: By default, a KI expires 30 days after the last extraction that found it. KIs for a decommissioned service disappear on their own, and come back with the next extraction if the service returns.
- **Durable**: To keep a KI, select it and select **Make durable**. A durable KI doesn't expire. Select **Make expiring** to undo this.
- **Excluded**: If a feature KI is wrong, select **Exclude**. Later extractions skip it. Filter by **Excluded** and select **Restore** to use it again.
- **Deleted**: Select **Delete** to remove a KI permanently.

## Continuous KI onboarding [sig-events-ki-continuous]

Continuous KI onboarding learns each enabled source again every **Onboarding interval (hours)**, 12 by default. Refer to [When learning runs](../detection/learning.md#nightshift-detection-learning-when) and [Continuous KI onboarding](../settings.md#nightshift-settings-ki-onboarding).

For how extraction samples your logs and schedules sources, refer to [How KI extraction works](../significant-events/how-it-works.md#sig-events-ki-extraction).

## Learn more [nightshift-ki-next]

- [How detection learns your system](../detection/learning.md): Start and track KI extraction for your sources.
- [Rules and signals](../detection/rules-and-signals.md): Review the rules that detection creates from query KIs.
- [How {{nightshift}} builds context](./index.md): Compare KIs with the Wiki and Memory.
- [How Significant Events works](../significant-events/how-it-works.md): Follow KIs through the full detection pipeline.
