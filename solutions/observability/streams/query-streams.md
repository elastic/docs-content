---
applies_to:
  stack: preview 9.4+
  serverless: preview
description: Query streams are virtual, read-only streams defined by an ES|QL query that let you create reusable named views of your data without affecting ingestion.
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

# Query streams [streams-query-streams]

Query streams are virtual, read-only streams defined by an ES|QL query. Unlike classic and wired streams that store ingested data, query streams resolve at query-time — no data is written to storage, and no ingestion pipeline, routing rules, or retention policies are affected.

Use query streams to create persistent, named views of your data that you can attach assets to, organize hierarchically, and reference by name in ES|QL queries.

## Root and nested query streams [streams-query-streams-types]

Query streams can be **root-level** or **nested**:

- **Root-level query streams** reference any existing stream in the `FROM` clause and stand alone in the stream hierarchy.
- **Nested query streams** are logically grouped under a parent stream. The ES|QL query must reference the parent stream. Nesting organizes streams visually without affecting data routing or storage.

## Create a query stream [streams-query-streams-create]

### Create a root-level query stream [streams-query-streams-create-root]

1. Go to **Streams** in the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select **Create stream**, then choose **Query stream**.
1. Enter a name for the stream.
1. Write an ES|QL query that defines the data this stream represents. The query must reference at least one existing stream.
1. Preview the query results, then select **Save**.

### Create a nested query stream [streams-query-streams-create-nested]

1. Go to **Streams** and open a wired stream.
1. Go to the **Partitioning** tab.
1. Select **Add child stream**, then choose **Query stream**.
1. Enter a name and write the ES|QL query. The query should reference the parent stream.
1. Select **Save**.

## Query a query stream [streams-query-streams-query]

When you create a query stream named `logs.nginx`, the system creates an ES|QL view named `$.logs.nginx`. The `$.` prefix keeps query stream views in a separate namespace from ingest streams, so they never shadow or interfere with your underlying data streams.

To query a query stream directly in ES|QL, use its prefixed view name:

```esql
FROM $.logs.nginx
| WHERE status_code >= 500
```

When you open a query stream in Discover, the query is pre-populated automatically using the correct prefixed name.

## What you can do with query streams [streams-query-streams-capabilities]

Query streams are read-only views, so features that modify ingestion, storage, or routing aren't available. The following table shows which Streams features apply:

| Feature | Available |
|---|---|
| [Significant events](./management/significant-events.md) | Yes |
| [Schema](./management/schema.md) — add field descriptions | Yes — field types are derived from ES|QL output and can't be changed, but descriptions can be added |
| Attach dashboards, alerts, SLOs | Yes |
| [Partitioning](./management/partitioning.md) | No — query streams don't route ingested data |
| [Processing](./management/extract.md) | No — query streams don't run ingest pipelines |
| [Retention](./management/retention.md) | No — query streams don't store data |
| [Data quality](./management/data-quality.md) | No — query streams don't store data |

## Query streams vs ES|QL in Discover [streams-query-streams-vs-discover]

You can write ES|QL queries directly in Discover without creating a query stream. The right choice depends on whether you need the result to persist as a governed product entity.

| | Query stream | ES|QL in Discover |
|---|---|---|
| **Persistence** | Saved as a named, reusable entity | Session-only unless saved as a saved search |
| **Governance** | Named, owned, appears in Streams listing | None |
| **Asset attachment** | Dashboards, alerts, SLOs | Not supported |
| **Significant events** | Yes | No |
| **Stream hierarchy** | Appears in the Streams listing, can be nested under a parent stream | Not part of stream hierarchy |
| **ES|QL reference** | Queryable by prefixed name (`FROM $.stream-name`) | Not directly referenceable by name |
| **Best for** | Persistent views you need to monitor, share, or attach alerts to | Exploratory or one-off analysis |

### When to create a query stream [streams-query-streams-when-to-use]

Create a query stream when you need to:

- **Attach an alert, SLO, or dashboard** to a specific slice of your data.
- **Monitor significant events** — significant events discovery runs against the query on a schedule.
- **Share a reusable data view** — teammates can find the stream by name in the Streams listing or reference it in ES|QL.
- **Organize data logically** — nest the stream under a parent to keep related views grouped without changing ingestion.

### When to use ES|QL in Discover [streams-query-streams-when-to-use-discover]

Use ES|QL directly in Discover when you're:

- Exploring data to understand its shape before committing to a view.
- Running a one-off analysis you don't need to revisit.
- Iterating on a query before deciding whether to save it as a stream.
