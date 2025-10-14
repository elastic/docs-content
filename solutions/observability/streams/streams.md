---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Streams

Streams provides a single, centralized UI within {{kib}} that streamlines common tasks like extracting fields, setting data retention, and routing data, so you don't need to use multiple applications or manually configure underlying {{es}} components.

## Classic vs. wired streams

Streams can operate in two modes: wired and classic. Both manage data streams in {{es}}, but differ in configuration, inheritance, and field mapping.

### Classic streams

Classic streams work with existing Elasticsearch data streams. Use classic streams when you want the ease of extracting fields and configuring data retention while working with data that's already being ingested into {{es}}.

Classic streams:

- Are based on existing data streams, index templates, and component templates.
- Can follow the data retention policy set in the existing index template.
- Do not support hierarchical inheritance or cascading configuration updates.

### Wired streams
```{applies_to}
stack: preview 9.2
serverless: preview
```

Wired streams data is sent directly to a single endpoint, from which you can route data into child streams based on [partitioning](./management/partitioning.md) set up manually or with the help of AI suggestions.

Wired streams:
- Allow you to organize streams in a parent-child hierarchy.
- Let child streams automatically inherit mappings, lifecycle settings, and processors.
- Send configuration changes through the hierarchy to keep streams consistent.

For more information, refer to [sending data to wired streams](./wired-streams.md).

## Required permissions

Streams requires the following permissions:

::::{tab-set}

:::{tab-item} Serverless
Streams requires these Elastic Cloud Serverless roles:

- Admin: ability to manage all Streams.
- Editor/Viewer: limited access, unable to perform all actions.

:::

:::{tab-item} Stack
To manage all Streams, you need the following permissions:

- Cluster permissions: `manage_index_templates`, `manage_ingest_pipelines`, `manage_pipeline`, `read_pipeline`
- Data stream level permissions: `read`, `write`, `create`, `manage`, `monitor`, `manage_data_stream_lifecycle`, `read_failure_store`, `manage_failure_store`, `manage_ilm`.

To view streams, you need the following permissions:
- Data stream level: `read`, v`iew_index_metadata`, `monitor`

:::

::::

## Access Streams

Open Streams from the following places in {{kib}}:

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

- Open the data stream for a specific document from **Discover**. To do this, expand the details flyout for a document that's stored in a data stream, and select **Stream** or an action associated with the document's data stream. Streams will open filtered to the selected data stream.

## Manage individual streams [streams-management-tab]

Interact with and configure your streams in the following ways:

- [Retention](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size.
- [Partitioning](./management/partitioning.md): {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Route data into child streams.
- [Processing](./management/extract.md): Parse and extract information from documents into dedicated fields.
- [Schema](./management/schema.md): Manage field mappings.
- [Data quality](./management/data-quality.md): Get information about failed and degraded documents in your stream.
- [Advanced](./management/advanced.md): Review and manually modify underlying {{es}} components of your stream.