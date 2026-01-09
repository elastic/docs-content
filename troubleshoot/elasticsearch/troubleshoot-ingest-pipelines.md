---
navigation_title: Ingest Pipelines
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Troubleshoot Ingest pipelines [troubleshooting-pipelines]

{{es}} [Ingest Pipelines](https://www.elastic.co/docs/manage-data/ingest/transform-enrich/ingest-pipelines) allow you to transform data during ingest. Per [write model](https://www.elastic.co/docs/deploy-manage/distributed-architecture/reading-and-writing-documents#basic-write-model), they run from `ingest` [node roles](https://www.elastic.co/docs/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles) under the `write` [thread pool](https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/thread-pool-settings).

You can edit ingest pipelines in {{kib}}'s **Ingest Pipelines** management page or from {{es}}'s [Modify Pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline). They store under {{es}}'s [cluster state](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-state) as accessed from [List Pipelines](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-get-pipeline).

Ingest pipelines can be [Simulated](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate) during testing, but after go-live are triggered during event ingest from

* The query parameter `pipeline` flag the [create doc](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) or [update doc](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update) or [bulk modify docs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) API request.
* The ingest target's backing [index setting](https://www.elastic.co/docs/reference/elasticsearch/index-settings/index-modules#dynamic-index-settings) for `index.default_pipeline` and/or `index.final_pipeline`.
* An Ingest Pipeline may sub-call another as a [pipelinen processor](https://www.elastic.co/docs/reference/enrich-processor/pipeline-processor).

## Symptoms [troubleshooting-pipelines-symptoms]

You might notice an Ingest Pipeline is not running as performant as possible under load testing from one of the following symptoms.


### High CPU usage [troubleshooting-pipelines-symptoms-cpu]

While running, if Ingest Pipelines cause [high CPU usage](https://www.elastic.co/docs/troubleshoot/elasticsearch/high-cpu-usage), their logger `org.elasticsearch.ingest.Pipeline` will show under [Node Hot Threads](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads). An example output might prefix like this:

```text
::: {instance-0000000001}{XXXXX}{XXXXX}{instance-0000000001}{XXXXX}{XXXXX}{hirst}{9.0.0}{XXXXX}{XXXXX}
   Hot threads at XXXXX, interval=500ms, busiestThreads=10000, ignoreIdleThreads=true:

   100.0% [cpu=98.9%, other=1.1%] (500ms out of 500ms) cpu usage by thread 'elasticsearch[instance-0000000001][write][T#8]'

     10/10 snapshots sharing following 93 elements
       app/org.elasticsearch.server@9.0.0/org.elasticsearch.ingest.CompoundProcessor.execute(CompoundProcessor.java:145)
       app/org.elasticsearch.server@9.0.0/org.elasticsearch.ingest.Pipeline.execute(Pipeline.java:129)
```

The most common sub-processor to flag is a [Script processor](https://www.elastic.co/docs/reference/enrich-processor/script-processor) running [Painless](https://www.elastic.co/docs/reference/scripting-languages/painless/painless) as noted by logger `org.elasticsearch.painless`.


### Task Queue [troubleshooting-pipelines-symptoms-queue]

A non-performant Ingest Pipeline may cause a [Task Queue Backlog](https://www.elastic.co/docs/troubleshoot/elasticsearch/task-queue-backlog) potentially with [Hot Spotting](https://www.elastic.co/docs/troubleshoot/elasticsearch/hotspotting). Once sufficiently severe it would start causing [Rejected Requests](https://www.elastic.co/docs/troubleshoot/elasticsearch/rejected-requests#check-rejected-tasks).


### Delayed timestamps [troubleshooting-pipelines-symptoms-delayed]

There can be multiple timestamps associated with a single data event. By default in Elastic-built [Integrations](https://www.elastic.co/docs/reference/integrations), every event [records](https://www.elastic.co/docs/reference/ecs/ecs-principles-implementation#_timestamps) the following:

* `@timestamp` for when an event originated.
* `event.created` for when an event first reached an Elastic product.
* `event.ingested` for when an event finished processing through an {{es}} Ingest Pipeline.

{{kib}} [Data Views](https://www.elastic.co/docs/explore-analyze/find-and-organize/data-views) default to `@timestamp` to fit most user's default expectations. While troubleshooting ingestion lag, we recommend creating a temporary Data View based on `event.ingested`. 

This potential timing difference is why Security Detection Rules allow for [setting a "Timestamp override"](https://www.elastic.co/docs/troubleshoot/security/detection-rules#troubleshoot-ingestion-pipeline-delay) which defaults to `event.ingested` when enabled.

For user-managed Ingest Pipelines, you can create similar functionality by adding [Set Processor](https://www.elastic.co/docs/reference/enrich-processor/set-processor) to the end of your Ingest Pipeline. As a simplified example if `event.ingested` is not already being set upstream in your data pipeline:

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Log the event's ingestion timestamp as 'event.ingested'",
        "field": "event.ingested",
        "value": "{{{_ingest.timestamp}}}"
      }
    }
  ]
}
```

This will update every time the event is modifed when passing through pipeline. If you need to troubleshoot the original event creation only and the field `event.created` is not already being set upstream in your data pipeline you might consider adding this processor example at the beginning of the first Ingest Pipeline:

```console
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "description": "Log the event's first ingest timestamp as 'event.created', does not modify for updates.",
        "field": "event.created",
        "value": "{{{_ingest.timestamp}}}",
        "override": false
      }
    }
  ]
}
```


## Metrics [troubleshooting-pipelines-metrics]

When Ingest Pipelines run, they log their cumulative statistics to [List Node Statistics](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats). 

```console
GET _nodes/stats/ingest
```

This reports the overall Ingest Pipelines's statistics as well as statistics for each of its processors. If a pipeline calls a sub-pipeline the parent's statistics will record the total time and not subtract time spent waiting on the other. 

Storing this output into `nodes_stats.json` and then using [third-party tool JQ](https://jqlang.github.io/jq/) to parse through this JSON, some common views reported during troubleshooting include:

* Ingest Pipeline's processor has more than 10% failed events

  ```bash
  $ cat nodes_stats.json | jq -c '.nodes[]|.name as $node| .ingest.pipelines|to_entries[]| .key as $pipeline| .value.processors[] | to_entries[]|.key as $process| { pipeline:$pipeline, process:$process, node:$node, total:.value.stats.count, failed:.value.stats.failed, failed_percent:(try (100*.value.stats.failed/.value.stats.count|round) catch 0)}| select(.total>0 and .failed_percent>10)'
  ```

  Especially where `ignore_failure` is enabled, this might reflect an incomplete setup or wasted processing time.

* Ingest Pipeline's time per event is above 60 milliseconds or 1 second

  ```bash
  $ cat nodes_stats.json | jq -rc '.nodes[]|.name as $n| .ingest.pipelines|to_entries[]| .key as $pi|.value| { name:$n, pipeline:$pi, total_count:.count, total_millis:.time_in_millis, total_failed:.failed }| select(.total_count>0)|.+{time_per:(.total_millis/.total_count|round)}|select(.time_per>60)'
  ```

* Ingest Pipeline processor's time per event if it's processed at least 1 event and takes more than 0 milliseconds after rounding

  ```bash
  $ cat nodes_stats.json | jq -rc '.nodes[]|.name as $n| .ingest.pipelines|to_entries[]| .key as $pi|.value.processors[]| to_entries[]|.key as $pr| .value.stats|{ name:$n, pipeline:$pi, processor:$pr, total_count:.count, total_millis:.time_in_millis, total_failed:.failed }|select(.total_count>0)|.+{time_per:(.total_millis/.total_count|round)}|select(.time_per>0)'
  ```

{{es}}'s Ingest Pipeline processors don't have associated `id` like {{ls}}'s Pipelines to distinguish them so these emit in sequential order as seen in pipeline's definition. 

The statistics report per node since its uptime, so will reset with node restarts. As a rough heuristic, you could look at an individual node's output knowing proportions will usually be about equal. 
