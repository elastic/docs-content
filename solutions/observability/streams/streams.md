---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Streams
% can we document when to use streams vs when to not use streams?

Streams provides a single, centralized UI within {{kib}} that streamlines common tasks like extracting fields, setting data retention, and routing data, so you don't need to use multiple applications or manually configure underlying {{es}} components.

% add a wired vs classic streams section

A stream directly corresponds to an {{es}} data stream (for example, `logs-myapp-default`). Any updates you perform in Streams configures a specific [data stream](../../../manage-data/data-store/data-streams.md).

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
- [Partitioning](./management/partitioning.md):
- [Processing](./management/extract.md): Parse and extract information from documents into dedicated fields.
- [Schema](./management/schema.md): Manage field mappings.
- [Data quality](./management/data-quality.md): Get information about failed and degraded documents in your stream.
- [Advanced](./management/advanced.md): Review and manually modify underlying {{es}} components of your stream.