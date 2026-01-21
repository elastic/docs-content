---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
---

# Streams

Streams provides a single, centralized UI within {{kib}} that streamlines common tasks like extracting fields, setting data retention, and routing data, so you don't need to use multiple applications or manually configure underlying {{es}} components.

## Classic versus wired streams [streams-classic-vs-wired]

Streams can operate in two modes: wired and classic. Both manage data streams in {{es}}, but differ in configuration, inheritance, and field mapping.

### Classic streams [streams-classic-streams]

Classic streams work with existing {{es}} data streams. Use classic streams when you want the ease of extracting fields and configuring data retention while working with data that's already being ingested into {{es}}.

Classic streams:

- Are based on existing data streams, index templates, and component templates.
- Can follow the data retention policy set in the existing index template.
- Do not support hierarchical inheritance or cascading configuration updates.

### Wired streams [streams-wired-streams]
```{applies_to}
stack: preview 9.2
serverless: preview
```

Wired streams send data directly to a single endpoint, from which you can route data into child streams based on [partitioning](./management/partitioning.md) set up manually or with the help of AI suggestions.

Wired streams:
- Allow you to organize streams in a parent-child hierarchy.
- Let child streams automatically inherit mappings, lifecycle settings, and processors.
- Send configuration changes through the hierarchy to keep streams consistent.

For more information, refer to [sending data to wired streams](./wired-streams.md).

## Managed components [streams-managed-components]
When you configure classic or wired streams through the Streams UI or [Streams API](#streams-api), {{es}}-level components like templates and pipelines are created for the stream. These components are considered *managed* and shouldn't be modified using {{es}} APIs. When managing a stream through the Streams UI or API, continue doing so whenever possible.

You can still edit non-managed ingest pipelines, templates, and other components, but avoid those marked as managed or any per-data-stream mappings and settings. This behavior is similar to how Elasticsearch handles components managed by integrations. Refer to the [**Advanced** tab](./management/advanced.md) to review managed components.

## Required permissions [streams-required-permissions]

Streams requires the following permissions:

::::{applies-switch}

:::{applies-item} serverless:
Streams requires these {{serverless-full}} roles:

- Admin: Ability to manage all Streams
- Editor/Viewer: Limited access, cannot perform all actions

:::

:::{applies-item} stack:
To manage all streams, you need the following permissions:

- **Cluster permissions**: `manage_index_templates`, `manage_ingest_pipelines`, `manage_pipeline`, `read_pipeline`
- **Data stream level permissions**: `read`, `write`, `create`, `manage`, `monitor`, `manage_data_stream_lifecycle`, `read_failure_store`, `manage_failure_store`, `manage_ilm`.

To view streams, you need the following permissions:
- **Data stream level**: `read`, `view_index_metadata`, `monitor`

For more information, refer to [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) and [Granting privileges for data streams and aliases](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md)

:::

::::

## Access Streams [streams-access]

Open Streams from the following places in {{kib}}:

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

- Open the data stream for a specific document from **Discover**. To do this, expand the details flyout for a document that's stored in a data stream, and select **Stream** or an action associated with the document's data stream. Streams then opens filtered to the selected data stream.

### Streams API [streams-api]
``` yaml {applies_to}
stack: preview 9.1
serverless: preview
```

You can also access Streams features using the Streams API. Refer to the [Streams API documentation](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-streams) for more information.

## Manage individual streams [streams-management-tab]

Interact with and configure your streams in the following ways:

- [**Retention**](./management/retention.md): Manage how your stream retains data and get insight into data ingestion and storage size.
- [**Partitioning**](./management/partitioning.md): {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Route data into child streams.
- [**Processing**](./management/extract.md): Parse and extract information from documents into dedicated fields.
- [**Schema**](./management/schema.md): Manage field mappings.
- [**Data quality**](./management/data-quality.md): Get information about failed and degraded documents in your stream.
- [**Advanced**](./management/advanced.md): Review and manually modify underlying {{es}} components of your stream.
