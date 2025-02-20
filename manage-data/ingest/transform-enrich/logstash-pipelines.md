---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/logstash-pipelines.html
---

# Logstash pipelines [logstash-pipelines]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

In **{{project-settings}} → {{manage-app}} → {{ls-pipelines-app}}**, you can control multiple {{ls}} instances and pipeline configurations.

:::{image} ../../../images/serverless-logstash-pipelines-management.png
:alt: {{ls-pipelines-app}}"
:class: screenshot
:::

On the {{ls}} side, you must enable configuration management and register {{ls}} to use the centrally managed pipeline configurations.

::::{important}
After you configure {{ls}} to use centralized pipeline management, you can no longer specify local pipeline configurations. The `pipelines.yml` file and settings such as `path.config` and `config.string` are inactive when centralized pipeline management is enabled.

::::



## Manage pipelines [logstash-pipelines-manage-pipelines]

1. [Configure centralized pipeline management](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/configuring-centralized-pipelines.md).
2. To add a new pipeline, go to **{{project-settings}} → {{manage-app}} → {{ls-pipelines-app}}** and click **Create pipeline**. Provide the following details, then click **Create and deploy**.

    Pipeline ID
    :   A name that uniquely identifies the pipeline. This is the ID that you used when you configured centralized pipeline management and specified a list of pipeline IDs in the `xpack.management.pipeline.id` setting.

    Description
    :   A description of the pipeline configuration. This information is for your use.

    Pipeline
    :   The pipeline configuration. You can treat the editor like any other editor. You don’t have to worry about whitespace or indentation.

    Pipeline workers
    :   The number of parallel workers used to run the filter and output stages of the pipeline.

    Pipeline batch size
    :   The maximum number of events an individual worker thread collects before executing filters and outputs.

    Pipeline batch delay
    :   Time in milliseconds to wait for each event before sending an undersized batch to pipeline workers.

    Queue type
    :   The internal queueing model for event buffering. Options are `memory` for in-memory queueing and `persisted` for disk-based acknowledged queueing.

    Queue max bytes
    :   The total capacity of the queue when persistent queues are enabled.

    Queue checkpoint writes
    :   The maximum number of events written before a checkpoint is forced when persistent queues are enabled.


To delete one or more pipelines, select their checkboxes then click **Delete**.

For more information about pipeline behavior, go to [Centralized Pipeline Management](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/logstash-centralized-pipeline-management.md#_pipeline_behavior).
