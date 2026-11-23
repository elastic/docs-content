---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
description: Apply an ingest pipeline to your data with a request parameter, a default or final pipeline index setting, Beats, Fleet and Elastic Agent, or search indices.
type: how-to
---

# Apply an ingest pipeline

After you [create and test an ingest pipeline](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md), apply it to your data. Applying a pipeline means specifying it so that {{es}} uses it to process your documents. Choose the option that matches what you want to do:

| Your goal | Go to |
| --- | --- |
| Apply a pipeline to specific requests, such as a one-off load, or use different pipelines for different requests. | [Add a pipeline to an indexing request](#add-pipeline-to-indexing-request) |
| Apply a pipeline to everything sent to an index or data stream, without each request naming it. A request can still specify a different pipeline instead. | [Set a default pipeline](#set-default-pipeline) |
| Enforce a pipeline on every document sent to an index or data stream, so that no request can skip it or replace it. | [Set a final pipeline](#set-final-pipeline) |
| Apply a pipeline to data sent by {{beats}}. | [Pipelines for {{beats}}](#pipelines-for-beats) |
| Apply a pipeline to data collected with {{agent}} integrations or the Custom logs integration. | [Pipelines for {{fleet}} and {{agent}}](#pipelines-for-fleet-elastic-agent) |
| Learn how pipelines work on indices created for search use cases. | [Pipelines for search indices](#pipelines-in-enterprise-search) |

To learn what happens when more than one pipeline applies to a document, refer to [How pipelines run together](#pipeline-order).

## Add a pipeline to an indexing request [add-pipeline-to-indexing-request]

Use the `pipeline` query parameter to apply a pipeline to documents in [individual]({{es-apis}}operation/operation-create) or [bulk]({{es-apis}}operation/operation-bulk) indexing requests. This is useful for one-off loads, or when different requests need different pipelines.

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

## Set a default pipeline [set-default-pipeline]

Use a default pipeline when documents sent to an index or data stream should usually go through the same pipeline, without each request having to name it. {{es}} applies the default pipeline to indexing requests that don't specify a `pipeline` parameter.

Use the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) index setting to set a default pipeline. To set it for every new index or data stream that matches a pattern, include the setting in an [index template](/manage-data/data-store/templates.md).

```console
PUT my-index/_settings
{
  "index.default_pipeline": "my-pipeline"
}
```

Indexing requests fail if the default pipeline is set and the pipeline doesn't exist.

## Set a final pipeline [set-final-pipeline]

Use a final pipeline when a pipeline must run for every document in an index or data stream, whichever pipeline the request or default setting specifies. For example, use it to add a field that every document must have. {{es}} applies the final pipeline after the request or default pipeline, even if the request specifies a different pipeline.

Use the [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting to set a final pipeline.

```console
PUT my-index/_settings
{
  "index.final_pipeline": "my-final-pipeline"
}
```

Indexing requests fail if the final pipeline is set and the pipeline doesn't exist.

## How pipelines run together [pipeline-order]

When more than one pipeline applies to a document, {{es}} runs them in this order:

1. The request pipeline, set with the `pipeline` parameter. A `pipeline` parameter in the metadata line of a bulk action overrides a `pipeline` parameter in the request URL.
2. The default pipeline, only if the request doesn't specify a pipeline.
3. The final pipeline, always, after the request pipeline or default pipeline.

The special pipeline name `_none` means that no pipeline runs. You can use it at the request or default level to skip pipelines set at a lower level of precedence.

## Pipelines for {{beats}} [pipelines-for-beats]

To add an ingest pipeline to an Elastic Beat, specify the `pipeline` parameter under `output.elasticsearch` in `<BEAT_NAME>.yml`. For example, for {{filebeat}}, you specify `pipeline` in `filebeat.yml`.

```yaml
output.elasticsearch:
  hosts: ["localhost:9200"]
  pipeline: my-pipeline
```

% REVIEW (SME): confirm Beats can send data to Serverless with this configuration.
{{beats}} versions follow the {{stack}}, but you can use the same configuration when your {{beats}} send data to {{serverless-short}}.

## Pipelines for {{fleet}} and {{agent}} [pipelines-for-fleet-elastic-agent]

{{agent}} integrations ship with default ingest pipelines that preprocess and enrich data before indexing. [{{fleet}}](/reference/fleet/index.md) applies these pipelines using [index templates](/manage-data/data-store/templates.md) that include [pipeline index settings](#set-default-pipeline). {{es}} matches these templates to your {{fleet}} data streams based on the [stream's naming scheme](/reference/fleet/data-streams.md#data-streams-naming-scheme).

% REVIEW (Fleet owner): this paragraph overlaps the "Ingest pipelines" section of reference/fleet/data-streams.md (#data-streams-pipelines), which also lists the levels of customization (global, type, integration, dataset). Should this page shorten it to a sentence and link to that section and the tutorial, or keep it here?
Each default integration pipeline calls a nonexistent, unversioned `*@custom` ingest pipeline. If unaltered, this pipeline call has no effect on your data. However, you can modify this call to create custom pipelines for integrations that persist across upgrades. To walk through an example, refer to [](/reference/fleet/data-streams-pipeline-tutorial.md).

{{fleet}} doesn't provide a default ingest pipeline for the **Custom logs** integration. You can specify a pipeline for this integration, as described in the next section.

% REVIEW (Fleet owner): the published integrations docs list "Custom Logs" as deprecated in favor of "Custom Logs (Filestream)". Confirm which integration and UI path (Custom log file > Advanced options > Dataset name) this section describes, and whether the "Ingest Pipeline" option still applies (the Filestream changelog says it is ignored when "Use logs stream" is set). Also decide whether this walkthrough should live in the Fleet docs, since no other page covers applying a pipeline to this integration.
### Apply a pipeline to the Custom logs integration [pipelines-custom-logs]

Create the pipeline and set up the integration. Then apply the pipeline.

% REVIEW (Fleet owner): questions on this procedure. (1) The data-streams-pipeline-tutorial covers integrations that ship a default pipeline and call `@custom`, not the Custom logs integration, so it doesn't replace this procedure. Agree? (2) Is the `logs-<dataset-name>-default` pipeline name required, or only a naming convention? Does the name matter for the index template or the `pipeline` policy setting? (3) Elasticsearch's `logs@default-pipeline` calls a `logs@custom` ingest pipeline that doesn't exist by default. Would creating `logs@custom` (or another `@custom` pipeline, such as `global@custom` or a dataset-level one) apply to Custom logs data streams, given the integration has no default pipeline? If so, is it a simpler option to document?
1. [Create](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md#create-manage-ingest-pipelines) and [test](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md#test-pipeline) your ingest pipeline. Name your pipeline `logs-<dataset-name>-default`. This makes it easier to track the pipeline for your integration.

    For example, the following request creates a pipeline for the `my_app` dataset. The pipeline's name is `logs-my_app-default`.

    ```console
    PUT _ingest/pipeline/logs-my_app-default
    {
      "description": "Pipeline for `my_app` dataset",
      "processors": [ ... ]
    }
    ```

2. When you add or edit your **Custom logs** integration in {{fleet}}, select **Configure integration** → **Custom log file** → **Advanced options**. In the **Dataset name** field, enter your dataset's name. {{fleet}} adds new data for the integration to the resulting `logs-<dataset-name>-default` data stream.

    For example, if your dataset's name is `my_app`, {{fleet}} adds new data to the `logs-my_app-default` data stream.

    :::{image} /manage-data/images/elasticsearch-reference-custom-logs.png
    :alt: The Advanced options settings of the Custom logs integration in Fleet, with the Dataset name field
    :screenshot:
    :::

% REVIEW (SME): confirm the rationale for choosing the index template vs. custom configuration option, and whether Fleet and Custom logs apply on Serverless.
3. Apply the pipeline with either an index template or a custom configuration. Use an index template to apply the pipeline to every document written to the data stream, whichever way it's indexed, or to set a final pipeline. Use a custom configuration to set the pipeline in the integration policy, without creating an index template.

    :::::{tab-set}

    ::::{tab-item} Index template
    $$$pipeline-custom-logs-index-template$$$

    1. Create an [index template](/manage-data/data-store/templates.md) that includes your pipeline in the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) or [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting. Ensure the template is [data stream enabled](/manage-data/data-store/data-streams/set-up-data-stream.md#create-index-template). The template's index pattern should match `logs-<dataset-name>-*`.

        You can create this template using {{kib}}'s [**Index Management**](/manage-data/data-store/templates.md) feature or the [create index template API]({{es-apis}}operation/operation-indices-put-index-template).

        For example, the following request creates a template matching `logs-my_app-*`. The template uses a component template that contains the `index.default_pipeline` index setting.

        ```console
        # Creates a component template for index settings
        PUT _component_template/logs-my_app-settings
        {
          "template": {
            "settings": {
              "index.default_pipeline": "logs-my_app-default",
              "index.lifecycle.name": "logs"
            }
          }
        }

        # Creates an index template matching `logs-my_app-*`
        PUT _index_template/logs-my_app-template
        {
          "index_patterns": ["logs-my_app-*"],
          "data_stream": { },
          "priority": 500,
          "composed_of": ["logs-my_app-settings", "logs-my_app-mappings"]
        }
        ```

        The template's `composed_of` list includes a `logs-my_app-mappings` component template. Create it first, or remove it from the list if you don't need custom mappings.

    2. Use the [rollover API]({{es-apis}}operation/operation-indices-rollover) to roll over your data stream. This ensures {{es}} applies the index template and its pipeline settings to any new data for the integration.

        ```console
        POST logs-my_app-default/_rollover/
        ```
    ::::

    ::::{tab-item} Custom configuration
    $$$pipeline-custom-logs-configuration$$$

    In the integration's **Custom Configurations** field, specify your pipeline in the `pipeline` policy setting.

    :::{image} /manage-data/images/elasticsearch-reference-custom-logs-pipeline.png
    :alt: The Custom Configurations field of the Custom logs integration in Fleet, with the pipeline policy setting
    :screenshot:
    :::
    ::::

    :::::

### Standalone {{agent}} [pipelines-agent-standalone]

If you run {{agent}} standalone, you can apply pipelines using an [index template](/manage-data/data-store/templates.md) that includes the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) or [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting. Alternatively, you can specify the `pipeline` policy setting in your `elastic-agent.yml` configuration. Refer to [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md).

## Pipelines for search indices [pipelines-in-enterprise-search]

When you create {{es}} indices for search use cases, for example by using the web crawler or [connectors](elasticsearch://reference/search-connectors/index.md), {{es}} automatically sets up these indices with specific ingest pipelines. These processors help optimize your content for search. Refer to [*Ingest pipelines in Search*](/solutions/search/ingest-for-search.md) for more information.

## Related pages

* [Create and test an ingest pipeline](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md)
* [{{es}} ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md)
* [Access data in processors](/manage-data/ingest/transform-enrich/access-data-in-processors.md)
* [Conditionally run processors and pipelines](/manage-data/ingest/transform-enrich/conditionally-run-ingest-processors.md)
