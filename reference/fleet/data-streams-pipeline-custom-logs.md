---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
description: Apply a custom ingest pipeline to an integration that doesn't ship a default ingest pipeline, using the Custom logs integration as an example.
---

# Apply a custom ingest pipeline to an integration without a default pipeline [data-streams-pipeline-custom-logs]

Most {{agent}} integrations ship with a default ingest pipeline that calls a `@custom` ingest pipeline, so you can add processing by creating that pipeline. Refer to [](/reference/fleet/data-streams-pipeline-tutorial.md). Some integrations, such as the **Custom logs** integration, don't ship a default ingest pipeline, so there is no `@custom` pipeline call to rely on. To process their data, you apply your own pipeline to the data stream instead.

% REVIEW (Fleet owner): the published integrations docs list "Custom Logs" as deprecated in favor of "Custom Logs (Filestream)". Confirm which integration and UI path (Custom log file > Advanced options > Dataset name) this page describes, and whether the "Ingest Pipeline" option still applies (the Filestream changelog says it is ignored when "Use logs stream" is set). Also confirm that {{fleet}} doesn't provide a default ingest pipeline for this integration, and which other integrations behave the same way.

**Scenario:** You collect application logs with the Custom logs integration, and you want to parse them before they are indexed.

**Goal:** Create an ingest pipeline and apply it to the data stream that the integration writes to.

% REVIEW (Fleet owner): questions on this procedure. (1) The data-streams-pipeline-tutorial covers integrations that ship a default pipeline and call `@custom`, not the Custom logs integration, so it doesn't replace this procedure. Agree? (2) Is the `logs-<dataset-name>-default` pipeline name required, or only a naming convention? Does the name matter for the index template or the `pipeline` policy setting? (3) Elasticsearch's `logs@default-pipeline` calls a `logs@custom` ingest pipeline that doesn't exist by default. Would creating `logs@custom` (or another `@custom` pipeline, such as `global@custom` or a dataset-level one) apply to Custom logs data streams, given the integration has no default pipeline? If so, is it a simpler option to document?
## Step 1: Create the ingest pipeline [data-streams-pipeline-custom-logs-one]

[Create](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md#create-manage-ingest-pipelines) and [test](/manage-data/ingest/transform-enrich/create-ingest-pipelines.md#test-pipeline) your ingest pipeline. Name your pipeline `logs-<dataset-name>-default`. This makes it easier to track the pipeline for your integration.

For example, the following request creates a pipeline for the `my_app` dataset. The pipeline's name is `logs-my_app-default`.

```console
PUT _ingest/pipeline/logs-my_app-default
{
  "description": "Pipeline for `my_app` dataset",
  "processors": [ ... ]
}
```

## Step 2: Set the dataset name [data-streams-pipeline-custom-logs-two]

When you add or edit your **Custom logs** integration in {{fleet}}, select **Configure integration** → **Custom log file** → **Advanced options**. In the **Dataset name** field, enter your dataset's name. {{fleet}} adds new data for the integration to the resulting `logs-<dataset-name>-default` data stream.

For example, if your dataset's name is `my_app`, {{fleet}} adds new data to the `logs-my_app-default` data stream.

:::{image} /reference/fleet/images/elasticsearch-reference-custom-logs.png
:alt: The Advanced options settings of the Custom logs integration in Fleet, with the Dataset name field
:screenshot:
:::

## Step 3: Apply the pipeline [data-streams-pipeline-custom-logs-three]

% REVIEW (SME): confirm the rationale for choosing the index template vs. custom configuration option, and whether Fleet and Custom logs apply on Serverless.
Apply the pipeline with either an index template or a custom configuration. Use an index template to apply the pipeline to every document written to the data stream, whichever way it's indexed, or to set a final pipeline. Use a custom configuration to set the pipeline in the integration policy, without creating an index template.

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

:::{image} /reference/fleet/images/elasticsearch-reference-custom-logs-pipeline.png
:alt: The Custom Configurations field of the Custom logs integration in Fleet, with the pipeline policy setting
:screenshot:
:::
::::

:::::

## Related pages

* [](/reference/fleet/data-streams-pipeline-tutorial.md): Add a `@custom` pipeline to an integration that ships a default ingest pipeline, which is the recommended method for most integrations.
* [Pipelines for {{fleet}}, {{agent}}, and integrations](/manage-data/ingest/transform-enrich/apply-ingest-pipelines.md#pipelines-for-fleet-elastic-agent): Compare the ways to apply a custom pipeline to an integration, and choose the one that fits.
* [](/manage-data/ingest/transform-enrich/readable-maintainable-ingest-pipelines.md): Make your pipeline readable and maintainable.
