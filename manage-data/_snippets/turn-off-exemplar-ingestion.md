* **Turn off exemplar ingestion in {{es}}**: Set the dynamic cluster setting [`xpack.metrics.exemplars.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md) to `false`. {{es}} then discards the exemplars of incoming OTLP metrics and Prometheus remote write requests and only indexes the metric samples. The setting takes effect immediately and applies to both endpoints, including metrics that reach them through the [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) on {{ech}}.

  ```console
  PUT /_cluster/settings
  {
    "persistent": {
      "xpack.metrics.exemplars.enabled": false
    }
  }
  ```

  On {{serverless-full}}, cluster settings can't be changed. Stop sending exemplars at the source instead, as described in the previous option, or, if you can't change the sender, drop them with an ingest pipeline.

* **Drop exemplars with an ingest pipeline**: If you can't change the sender or the cluster setting, create an ingest pipeline with a [drop processor](elasticsearch://reference/enrich-processor/drop-processor.md) and make it the default pipeline of all exemplar data streams through the `exemplars@custom` component template. Exemplars are still sent to {{es}}, but are discarded before they are indexed. This approach works on all deployment types, including {{serverless-short}}.

  ```console
  PUT _ingest/pipeline/drop-exemplars
  {
    "processors": [
      { "drop": {} }
    ]
  }

  PUT _component_template/exemplars@custom
  {
    "template": {
      "settings": {
        "index.default_pipeline": "drop-exemplars"
      }
    }
  }
  ```

  The component template only applies to backing indices created after the change. To also stop existing exemplar data streams from indexing new exemplars, set the pipeline on them directly:

  ```console
  PUT exemplars-*/_settings
  {
    "index.default_pipeline": "drop-exemplars"
  }
  ```
