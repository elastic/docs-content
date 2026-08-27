---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elastic-agent
  - id: logstash
description: Split one incoming event into multiple Elasticsearch documents, either at collection time or with a Logstash pipeline that uses the split filter.
---

# Split an event into multiple documents

Sometimes a single incoming event contains multiple records. For example, an API response or a batched TCP payload might hold an array of items, and you want to index each item as its own document in {{es}}.

{{agent}} processors and {{es}} ingest pipelines process each event individually: they can transform or drop an event, but they can't generate multiple documents from a single event. In particular, the {{es}} [`split` processor](elasticsearch://reference/enrich-processor/split-processor.md) splits a field value into an array within the same document. It doesn't create new documents.

To split one event into multiple documents, you have two options:

* [Split events at collection time](#split-events-at-collection-time), if your data source's input supports it.
* [Split events with {{ls}}](#split-events-with-logstash), for everything else.

Most data sources don't need splitting. Elastic {{integrations}} are designed to deliver one document per record. Splitting mainly matters for custom and input-only integrations, such as a Custom TCP Logs integration that receives batched JSON payloads.

## Splitting compared to rerouting

Splitting turns one event into many documents. Rerouting sends each document to a different destination based on its content. If your goal is to route documents to different data streams or indices, you don't need to split, and you don't need {{ls}}. Instead, use the {{es}} [`reroute` processor](elasticsearch://reference/enrich-processor/reroute-processor.md), typically in a [`@custom` ingest pipeline](/reference/fleet/data-streams-pipeline-tutorial.md).

## Split events at collection time [split-events-at-collection-time]

Some {{agent}} and {{filebeat}} inputs can split an incoming payload into separate events as the data is collected, before anything reaches {{es}}. If your data source uses one of these inputs, this is the simplest option: no extra components, and no changes to how your data flows.

For example:

* The [Custom API integration](integration-docs://reference/httpjson.md) and the underlying [HTTP JSON input](beats://reference/filebeat/filebeat-input-httpjson.md) can split API responses into separate events with the `response.split` setting.
* The [CEL Custom API input integration](integration-docs://reference/cel.md) can emit multiple events per request when the CEL program returns a list of events.
* The [AWS S3 input](beats://reference/filebeat/filebeat-input-aws-s3.md) can create one event per element of a JSON array with the `expand_event_list_from_field` setting.

Check your input's reference documentation for similar settings before adding {{ls}} to your ingest path.

## Split events with {{ls}} [split-events-with-logstash]

When your input has no native split option, run a {{ls}} pipeline between {{agent}} and {{es}}. The {{ls}} [`split` filter](logstash-docs-md://lsr/plugins-filters-split.md) creates a copy of the event for each element of an array field, so each element becomes its own document.

If your data flows through an Elastic integration, pair the `split` filter with the [`elastic_integration` filter](logstash-docs-md://lsr/plugins-filters-elastic_integration.md), which runs the integration's ingest pipeline inside {{ls}}. This keeps the integration's processing intact while letting you split the results. For more details about this pattern, refer to [Using {{ls}} with Elastic integrations](logstash://reference/using-logstash-with-elastic-integrations.md).

:::{warning}
Splitting multiplies your document count. An event with hundreds of array elements becomes hundreds of documents, which can significantly increase ingest volume, storage, and indexing load. Test with realistic data volumes before you rely on splitting in production.
:::

### Requirements

* A [{{ls}} instance](logstash://reference/index.md) that your {{agent}}s can reach.
* {{agent}}s [configured to output to {{ls}}](/reference/fleet/logstash-output.md).
* If you use the `elastic_integration` filter: an active Elastic Enterprise subscription, and credentials with the `monitor`, `read_pipeline`, and `manage_index_templates` privileges on your {{es}} cluster. Refer to the [plugin documentation](logstash-docs-md://lsr/plugins-filters-elastic_integration.md) for details.

### Example pipeline

This pipeline receives events from {{agent}}, runs the integration's ingest pipeline, and then splits each event on the `items` array field:

```text
input {
  elastic_agent {
    port => 5044
  }
}

filter {
  elastic_integration { <1>
    cloud_id => "<cloud-id>"
    api_key => "<api-key>"
  }

  split { <2>
    field => "items"
  }
}

output {
  elasticsearch { <3>
    cloud_id => "<cloud-id>"
    api_key => "<api-key>"
    data_stream => true
    ecs_compatibility => "v8"
  }
}
```

1. The [`elastic_integration` filter](logstash-docs-md://lsr/plugins-filters-elastic_integration.md) runs the event's integration ingest pipeline inside {{ls}}. It must be the first filter in the pipeline. If your data doesn't flow through an integration, omit this filter.
2. The [`split` filter](logstash-docs-md://lsr/plugins-filters-split.md) creates one copy of the event per element of the `items` array. Each copy becomes its own document. If the array arrives as an unparsed string, parse it first, for example with the [`json` filter](logstash-docs-md://lsr/plugins-filters-json.md), before splitting.
3. Elastic integrations are designed to work with data streams and ECS-compatible output, so set `data_stream => true` and `ecs_compatibility` to `v1` or `v8` in the [`elasticsearch` output](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md).
