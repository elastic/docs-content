---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
navigation_title: Configure advanced settings
---
# Configure advanced settings for streams [streams-advanced-settings]

The **Advanced** tab shows the underlying {{es}} configuration details and advanced configuration options for your stream.

You can use the **Advanced** tab to add [descriptions](#streams-advanced-description) or [features](#streams-advanced-features) that provide useful information to Stream's AI components. You can also  [manually configure](#streams-advanced-index-config) the index or component templates or modify other ingest pipelines used by the stream.

## Stream description [streams-advanced-description]

Describe the data in the stream. AI features like system identification and significant events use this description when generating suggestions.

## Stream feature configuration [streams-advanced-features]

Streams analyzes your data and identifies features. Features are a way to classify some of the data you have in your stream.

Each feature has a natural language description and an optional filter which points to a subset of your data.

For example, in a stream of Kubernetes logs, the feature identification process would be able to identify that you have data from "nginx" which can be found by filtering for `WHERE service.name==nginx`. It would also include a description defining nginx.

Features provide useful information for AI processes, such as significant events, and are used as the foundation for them.

## Index configuration [streams-advanced-index-config]

:::{Important}
Avoid editing components marked as **managed** or any per-data-stream mappings and settings. Processing and schema changes should typically be done through the Streams interface or API, and none of these configuration processes are required. This feature mainly exists to help advanced users maintain familiar workflows.
:::

For classic streams, you can access the following components:

- [Index templates](../../../../manage-data/data-store/templates.md#index-templates)
- [Component templates](../../../../manage-data/data-store/templates.md#component-templates)
- [Pipelines](../../../../manage-data/ingest/transform-enrich.md)
- [Data streams](../../../../manage-data/data-store/data-streams.md)

For both wired ({applies_to}`stack: preview 9.2` {applies_to}`serverless: preview`) and classic streams, you can manually configure:

- **Shards:** Control how the index is split across nodes. More shards can improve parallelism but may increase overhead.
- **Replicas:** Define how many copies of the data exist. More replicas improve resilience and read performance but increase storage usage.
- **Refresh interval:** Control how frequently new data becomes visible for search. A longer interval reduces resource usage; a short one makes data searchable sooner.
