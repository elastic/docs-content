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

### Create a `@custom` pipeline (recommended) [pipelines-custom-pipeline]

Most integration pipelines call a nonexistent, unversioned `@custom` ingest pipeline. If you don't create it, the call has no effect on your data. To customize how an integration processes data, create the `@custom` pipeline. You don't need to change the integration configuration or index templates, and your pipeline persists across upgrades. In {{fleet}}, the **Ingest pipelines** settings of an integration data stream list the pipelines that run and help you create the `@custom` pipeline.

To learn more, refer to [](/reference/fleet/data-streams-pipeline-tutorial.md) and [Ingest pipelines](/reference/fleet/data-streams.md#data-streams-pipelines) in the {{fleet}} documentation.

% REVIEW (Fleet owner): please confirm this section. (1) That "most integrations" call a `@custom` pipeline, and the recommendation to use it first. (2) That the Ingest pipelines settings in Fleet list the pipelines and help create the `@custom` pipeline for any integration data stream. (3) That the two options below are accurate, and that an index or component template is best described as a last resort.
### Other options: Set the pipeline in the policy or a template [pipelines-fleet-other-options]

If a `@custom` pipeline doesn't fit your use case, you have two other options:

* **Configure the pipeline in the integration policy.** Set the pipeline to call in the integration's settings. For example, for the Custom logs integration, specify it in the `pipeline` policy setting, as shown in the [Custom logs example](#pipelines-custom-logs).
* **Set the pipeline in an index template or component template.** Add `index.default_pipeline` or `index.final_pipeline` to the template's settings. Use this option when the pipeline must apply to every data stream that matches the template, or when you also need to change other index settings. Templates apply only when a data stream or index is created, so roll over existing data streams for the change to take effect. Because the change affects all matching data streams, use this option with caution and only when the other options don't meet your needs. For an example, refer to [step 3 of the Custom logs example](#pipelines-custom-logs-apply).

{{fleet}} doesn't provide a default ingest pipeline for the **Custom logs** integration, so the `@custom` approach doesn't apply to it. Use one of the options above, as shown in the following example.

% REVIEW (Fleet owner): the published integrations docs list "Custom Logs" as deprecated in favor of "Custom Logs (Filestream)". Confirm which integration and UI path (Custom log file > Advanced options > Dataset name) this section describes, and whether the "Ingest Pipeline" option still applies (the Filestream changelog says it is ignored when "Use logs stream" is set). Also decide whether this walkthrough should live in the Fleet docs and be replaced here with a link, since no other page covers applying a pipeline to this integration.
#### Example: Apply a pipeline to the Custom logs integration [pipelines-custom-logs]

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
3. $$$pipelines-custom-logs-apply$$$Apply the pipeline with either an index template or a custom configuration. Use an index template to apply the pipeline to every document written to the data stream, whichever way it's indexed, or to set a final pipeline. Use a custom configuration to set the pipeline in the integration policy, without creating an index template.

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

If you run {{agent}} standalone, you can apply pipelines using an [index template](/manage-data/data-store/templates.md) that includes the [`index.default_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline) or [`index.final_pipeline`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-final-pipeline) index setting. Alternatively, you can specify the `pipeline` policy settings in your `elastic-agent.yml` configuration. Refer to [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md) and [Create a standalone agent policy](/reference/fleet/create-standalone-agent-policy.md) for more details.

## Pipelines for search indices [pipelines-in-enterprise-search]

When you create {{es}} indices for search use cases, for example by using the web crawler or [connectors](elasticsearch://reference/search-connectors/index.md), {{es}} automatically sets up these indices with specific ingest pipelines. These processors help optimize your content for search. Refer to [*Ingest pipelines in Search*](/solutions/search/ingest-for-search.md) for more information.

## Related pages

* [Create and test an ingest pipeline](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md)
* [{{es}} ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md)
* [Access data in processors](/manage-data/ingest/transform-enrich/access-data-in-processors.md)
* [Conditionally run processors and pipelines](/manage-data/ingest/transform-enrich/conditionally-run-ingest-processors.md)
