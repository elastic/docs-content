---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
description: Apply an ingest pipeline to your data in an indexing request, in index settings or templates, in Beats, or in Fleet and Elastic Agent integrations.
type: how-to
---

# Apply an ingest pipeline

After you [create and test an ingest pipeline](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md), apply it to your data. Applying a pipeline means specifying it so that {{es}} uses it to process your documents. In {{es}}, you can apply a pipeline in two ways:

* [In an indexing request](#add-pipeline-to-indexing-request), with the `pipeline` parameter. This gives you direct control over each request, for example when you use a client library.
* [In index settings](#apply-with-index-settings), with the `index.default_pipeline` or `index.final_pipeline` setting. This is the most common way to apply a pipeline. You can set these on an index directly, or in an index template or component template so that every new index or data stream that matches the template gets them.

If you collect data with {{beats}}, {{fleet}}, or {{agent}}, you can also configure the pipeline in those tools. 

To go straight to the instructions that apply to your setup, find your goal in the following table:

| Your goal | Go to |
| --- | --- |
| Apply a pipeline to specific requests, such as a one-off load, or use different pipelines for different requests. | [Add a pipeline to an indexing request](#add-pipeline-to-indexing-request) |
| Apply a pipeline to all documents sent to an index or data stream, without each request naming it. Set it directly on the index or through an index or component template. Use a default pipeline that a request can replace, or a final pipeline that always runs. | [Set a pipeline in index settings](#apply-with-index-settings) |
| Apply a pipeline to data sent by {{beats}}. | [Pipelines for {{beats}}](#pipelines-for-beats) |
| Apply a pipeline to data collected with {{fleet}}, {{agent}}, or integrations. | [Pipelines for {{fleet}}, {{agent}}, and integrations](#pipelines-for-fleet-elastic-agent) |
| Learn how pipelines work on indices created for search use cases. | [Pipelines for search indices](#pipelines-in-enterprise-search) |

## How pipelines run together [pipeline-order]

When more than one pipeline applies to a document, {{es}} runs them in this order:

1. The request pipeline, set with the `pipeline` parameter. A `pipeline` parameter in the metadata line of a bulk action overrides a `pipeline` parameter in the request URL.
2. The default pipeline, only if the request doesn't specify a pipeline.
3. The final pipeline, always, after the request pipeline or default pipeline.

The special pipeline name `_none` means that no pipeline runs. You can use it at the request or default level to skip pipelines set at a lower level of precedence.

## Add a pipeline to an indexing request [add-pipeline-to-indexing-request]

Use the `pipeline` query parameter to apply a pipeline to documents in [individual]({{es-apis}}operation/operation-create) or [bulk]({{es-apis}}operation/operation-bulk) indexing requests. This gives you direct control over each request, which is useful when you use a client library, for one-off loads, or when different requests need different pipelines.

```console
POST my-data-stream/_doc?pipeline=my-pipeline
{
  "@timestamp": "2099-03-07T11:04:05.000Z",
  "my-keyword-field": "foo"
}

PUT my-data-stream/_bulk?pipeline=my-pipeline
{ "create":{ } }
{ "@timestamp": "2099-03-07T11:04:06.000Z", "my-keyword-field": "foo" }
{ "create":{ } }
{ "@timestamp": "2099-03-07T11:04:07.000Z", "my-keyword-field": "bar" }
```

In a bulk request, a `pipeline` parameter in the URL applies to every action. To use a different pipeline for a single action, set `pipeline` in that action's metadata line instead.

```console
PUT my-data-stream/_bulk
{ "create": { "pipeline": "my-pipeline" } }
{ "@timestamp": "2099-03-07T11:04:08.000Z", "my-keyword-field": "foo" }
```

You can also use the `pipeline` parameter with the [update by query]({{es-apis}}operation/operation-update-by-query) or [reindex]({{es-apis}}operation/operation-reindex) APIs.

```console
POST my-data-stream/_update_by_query?pipeline=my-pipeline

POST _reindex
{
  "source": {
    "index": "my-data-stream"
  },
  "dest": {
    "index": "my-new-data-stream",
    "op_type": "create",
    "pipeline": "my-pipeline"
  }
}
```

## Set a pipeline in index settings [apply-with-index-settings]

Use index settings to apply a pipeline to every document sent to an index or data stream, without each request naming it. Two settings are available:

* [`index.default_pipeline`](#set-default-pipeline) applies a pipeline to requests that don't specify one.
* [`index.final_pipeline`](#set-final-pipeline) applies a pipeline to every document, after any other pipeline.

You can set these on an existing index, or include them in an [index template](/manage-data/data-store/templates.md#index-templates) or [component template](/manage-data/data-store/templates.md#component-templates). Every new index or data stream that matches the template then gets the settings. The following request creates an index template that sets a default pipeline for data streams whose names start with `my-data-stream`.

```console
PUT _index_template/my-template
{
  "index_patterns": ["my-data-stream*"],
  "data_stream": { },
  "priority": 500,
  "template": {
    "settings": {
      "index.default_pipeline": "my-pipeline"
    }
  }
}
```

Templates apply only when an index is created. To apply a template change to an existing data stream, [roll over]({{es-apis}}operation/operation-indices-rollover) the data stream, or update the setting directly on the index, as shown in the following sections.

### Set a default pipeline [set-default-pipeline]

Use a default pipeline when documents sent to an index or data stream should usually go through the same pipeline, without each request having to name it. {{es}} applies the default pipeline to indexing requests that don't specify a `pipeline` parameter.

Use the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) index setting to set a default pipeline.

```console
PUT my-index/_settings
{
  "index.default_pipeline": "my-pipeline"
}
```

Indexing requests fail if the default pipeline is set and the pipeline doesn't exist.

### Set a final pipeline [set-final-pipeline]

Use a final pipeline when a pipeline must run for every document in an index or data stream, whichever pipeline the request or default setting specifies. For example, use it to add a field that every document must have. {{es}} applies the final pipeline after the request or default pipeline, even if the request specifies a different pipeline.

Use the [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting to set a final pipeline.

```console
PUT my-index/_settings
{
  "index.final_pipeline": "my-final-pipeline"
}
```

Indexing requests fail if the final pipeline is set and the pipeline doesn't exist.

## Pipelines for {{beats}} [pipelines-for-beats]

To add an ingest pipeline to an Elastic Beat, specify the `pipeline` parameter under `output.elasticsearch` in `<BEAT_NAME>.yml`. For example, for {{filebeat}}, you specify `pipeline` in `filebeat.yml`.

```yaml
output.elasticsearch:
  hosts: ["localhost:9200"]
  pipeline: my-pipeline
```

% REVIEW (Beats SME): please confirm this section against the Beats behavior. First draft, based on `libbeat/outputs/elasticsearch` in elastic/beats (the `getPipeline` function and the `BulkMeta` struct, same in 8.15, 9.0, and main). (1) {{beats}} send the configured pipeline name in the metadata of each bulk action, so this is the "indexing request" method and not an index setting. (2) The `pipeline` setting doesn't add `index.default_pipeline` or `index.final_pipeline` to the index template that {{beats}} load with `setup.template`. I found no code that does this, but can't rule it out. (3) A `pipeline` value in the event metadata (for example, set by a module) takes precedence over the output setting.
With this setting, the Beat [adds the pipeline to its indexing requests](#add-pipeline-to-indexing-request). The {{es}} output includes the pipeline name in the metadata of each action in the bulk request. The Beat doesn't change your index template or [index settings](#apply-with-index-settings), so the pipeline applies only to data sent by that Beat.

Because the pipeline is named in the request, it takes precedence over any `index.default_pipeline` setting, and any `index.final_pipeline` setting still runs afterwards. Refer to [How pipelines run together](#pipeline-order). To apply a pipeline to all data sent to an index, whichever tool sends it, [set it in index settings](#apply-with-index-settings) instead.

% REVIEW (SME): confirm Beats can send data to Serverless with this configuration.
{{beats}} versions follow the {{stack}}, but you can use the same configuration when your {{beats}} send data to {{serverless-short}}.

## Pipelines for {{fleet}}, {{agent}}, and integrations [pipelines-for-fleet-elastic-agent]

{{agent}} integrations ship with default ingest pipelines that preprocess and enrich data before indexing. [{{fleet}}](/reference/fleet/index.md) applies these pipelines using [index templates](/manage-data/data-store/templates.md) that include [pipeline index settings](#apply-with-index-settings). {{es}} matches these templates to your {{fleet}} data streams based on the [stream's naming scheme](/reference/fleet/data-streams.md#data-streams-naming-scheme).

To add your own processing to the data an integration collects, such as parsing, enrichment, or redaction, without editing the integration's default pipeline, use one of the following methods. They are in order of preference, so start with the recommended method if it fits.

% REVIEW (Fleet owner): please confirm this table and its order. (1) That most integration default pipelines call a `@custom` pipeline, and that it is the recommended first choice. (2) That the `pipeline` policy setting is available for the integrations that need method 2, and which integrations those are. (3) That setting `index.default_pipeline` in a `@custom` component template replaces the integration's default pipeline, so only `index.final_pipeline` should be recommended there. (4) Whether the Custom logs walkthrough in the {{fleet}} docs is accurate; it now lives at reference/fleet/data-streams-pipeline-custom-logs.md.
| Method | Use it when | What you change | Risk |
| --- | --- | --- | --- |
| 1. [Create a `@custom` ingest pipeline](/reference/fleet/data-streams.md#data-streams-pipelines) (recommended) | The integration's default pipeline calls a `@custom` pipeline, as most do, and you only need to add processing. | Only your own pipeline. In {{fleet}}, the **Ingest pipelines** settings of an integration data stream help you create it. For a walkthrough, refer to [](/reference/fleet/data-streams-pipeline-tutorial.md). | Lowest. Your pipeline persists across upgrades. |
| 2. [Add a pipeline to the integration configuration](/reference/fleet/data-streams-pipeline-custom-logs.md) | The integration doesn't ship a default pipeline, such as Custom logs, so there is no `@custom` pipeline to create. | The `pipeline` setting in the integration policy. | Low. You don't manage any templates. |
| 3. [Edit the integration's `@custom` component template](/reference/fleet/data-streams.md#data-streams-index-templates-edit) | You need more than a pipeline: a final pipeline that runs on every document, or other index settings or mappings. | `index.final_pipeline`, or other settings or mappings, in the component template. | Higher. Settings or mappings can conflict with the integration's own. Don't set `index.default_pipeline`, which replaces the integration's pipeline. |
| 4. [Create a new index template](/reference/fleet/data-streams-scenario3.md) | The changes must apply to a specific namespace, or no integration template fits. | A new index template for your data. | Highest. The template isn't updated when the integration is upgraded, and Elastic can't test it. |

Editing the integration's `@custom` component template and creating a new index template change how {{es}} configures the integration's indices, so a mistake can cause indexing to fail, lose data, or break integration upgrades. For example, a custom setting can conflict with the integration's own if a later version of the integration changes the index mode, and overriding the type of a field that the integration's dashboards use can break them. Both methods apply only to newly created indices, so roll over existing data streams for the change to take effect. For details, refer to [Creating custom component templates](/reference/fleet/integrations-assets-best-practices.md#assets-restrictions-custom-component-templates) and [the risks of replacing an integration's index template](/reference/fleet/integrations-assets-best-practices.md#assets-restrictions-cloning-index-template).

### Standalone {{agent}} [pipelines-agent-standalone]

If you run {{agent}} standalone, you can apply pipelines using an [index template](/manage-data/data-store/templates.md) that includes the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) or [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting. Alternatively, you can specify the `pipeline` policy settings in your `elastic-agent.yml` configuration. Refer to [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md) and [Create a standalone agent policy](/reference/fleet/create-standalone-agent-policy.md) for more details.

## Pipelines for search indices [pipelines-in-enterprise-search]

When you create {{es}} indices for search use cases, for example by using the web crawler or [connectors](elasticsearch://reference/search-connectors/index.md), {{es}} automatically sets up these indices with specific ingest pipelines. These processors help optimize your content for search. Refer to [*Ingest pipelines in Search*](/solutions/search/ingest-for-search.md) for more information.

## Related pages

* [Create and test an ingest pipeline](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md)
* [{{es}} ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md)
* [Access data in processors](/manage-data/ingest/transform-enrich/access-data-in-processors.md)
* [Conditionally run processors and pipelines](/manage-data/ingest/transform-enrich/conditionally-run-ingest-processors.md)
