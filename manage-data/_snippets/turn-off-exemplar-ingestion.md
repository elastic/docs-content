* {applies_to}`serverless: unavailable` **Turn off exemplar ingestion in {{es}}**: Set the dynamic cluster setting [`xpack.metrics.exemplars.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md) to `false`. {{es}} then discards the exemplars of incoming OTLP metrics and Prometheus remote write requests and only indexes the metric samples. The setting takes effect immediately and applies to both endpoints, including metrics that reach them through the [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) on {{ech}}.

  ```console
  PUT /_cluster/settings
  {
    "persistent": {
      "xpack.metrics.exemplars.enabled": false
    }
  }
  ```

  On {{serverless-full}}, cluster settings can't be changed. Stop sending exemplars at the source instead, as described in the previous option, or, if you can't change the sender, drop them with an ingest pipeline.

* **Drop exemplars with an ingest pipeline**: If you can't change the sender or the cluster setting, create an [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md) with a [drop processor](elasticsearch://reference/enrich-processor/drop-processor.md) and set it as the `index.default_pipeline` of all exemplar data streams through the `exemplars@custom` component template. Exemplars are still sent to {{es}}, but are discarded before they are indexed. This approach works on all deployment types, including {{serverless-short}}. Because component templates only apply to backing indices created after the change, also update the index settings of any existing exemplar data streams.
