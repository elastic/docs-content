---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
navigation_title: Configure advanced settings
---
# Configure advanced settings for streams [streams-advanced-settings]

The **Advanced** tab shows the underlying {{es}} configuration details and advanced configuration options for your stream.

You can use the **Advanced** tab to manually configure the index or component templates or modify other ingest pipelines used by the stream.

## Stream description

% can we provide more information on what users should put here.

Describe the data in the stream. AI features like system identification and significant events use this description when generating suggestions.

## Stream system configuration

% Why do users want to add systems here?

Streams analyzes your stream and identifies systems. Then, you can select the ones you want to add to your stream.

## Index configuration

% Can we add use cases of when it makes sense to modify shards/replicas/refresh interval

For classic streams, you can manually configure the stream's [index template](../../../../manage-data/data-store/templates.md#index-templates), [component templates](../../../../manage-data/data-store/templates.md#component-templates), [pipeline](../../../../manage-data/ingest/transform-enrich.md), and [data stream](../../../../manage-data/data-store/data-streams.md).

For both wired {applies_to}`stack: preview 9.2` and classic streams, you can configure:

- **Shards:** Control how the index is split across nodes. More shards can improve parallelism but may increase overhead.
- **Replicas:** Define how many copies of the data exist. More replicas improve resilience and read performance but increase storage usage.
- **Refresh interval:** Control how frequently new data becomes visible for search. A longer interval reduces resource usage; a short one makes data searchable sooner.