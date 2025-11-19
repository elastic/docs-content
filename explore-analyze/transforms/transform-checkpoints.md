---
navigation_title: How checkpoints work
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-checkpoints.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# How checkpoints work [transform-checkpoints]

Each time a {{transform}} examines the source indices and creates or updates the destination index, it generates a *checkpoint*.

If your {{transform}} runs only once, there is logically only one checkpoint. If your {{transform}} runs continuously, however, it creates checkpoints as it ingests and transforms new source data. The `sync` property of the {{transform}} configures checkpointing by specifying a time field.

To create a checkpoint, the {{ctransform}}:

1. Checks for changes to source indices.

    Using a simple periodic timer, the {{transform}} checks for changes to the source indices. This check is done based on the interval defined in the transform’s `frequency` property.

    If new data is ingested with a slight delay, it might not be immediately available when the {{transform}} runs. To prevent missing documents, you can use the `delay` parameter in the `sync` configuration. This shifts the search window backward, ensuring that late-arriving data is included before a checkpoint processes it. Adjusting this value based on your data ingestion patterns can help ensure completeness.

    If the source indices remain unchanged or if a checkpoint is already in progress then it waits for the next timer.

    If changes are found a checkpoint is created.

2. Identifies which entities or time buckets have changed.

    The {{transform}} searches to see which entities or time buckets have changed between the last and the new checkpoint. The {{transform}} uses the values to synchronize the source and destination indices with fewer operations than a full re-run.

3. Updates the destination index (the {{dataframe}}) with the changes.

    The {{transform}} applies changes related to either new or changed entities or time buckets to the destination index. The set of changes can be paginated. The {{transform}} performs a composite aggregation similarly to the batch {{transform}} operation, however it also injects query filters based on the previous step to reduce the amount of work. After all changes have been applied, the checkpoint is complete.

This checkpoint process involves both search and indexing activity on the cluster. We have attempted to favor control over performance while developing {{transforms}}. We decided it was preferable for the {{transform}} to take longer to complete, rather than to finish quickly and take precedence in resource consumption. That being said, the cluster still requires enough resources to support both the composite aggregation search and the indexing of its results.

::::{tip}
If the cluster experiences unsuitable performance degradation due to the {{transform}}, stop the {{transform}} and refer to [Performance considerations](transform-overview.md#transform-performance).
::::

## Using the ingest timestamp for syncing the {{transform}} [sync-field-ingest-timestamp]

In most cases, it is strongly recommended to use the ingest timestamp of the source indices for syncing the {{transform}}. This is the most optimal way for {{transforms}} to be able to identify new changes. If your data source follows the [ECS standard](ecs://reference/index.md), you might already have an [`event.ingested`](ecs://reference/ecs-event.md#field-event-ingested) field. In this case, use `event.ingested` as the `sync`.`time`.`field` property of your {{transform}}.

If you don't have a `event.ingested` field or it isn't populated, you can set it by using an ingest pipeline. Create an ingest pipeline either using the [ingest pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) (like the example below) or through {{kib}}'s **Ingest Pipelines** management page. Use a [`set` processor](elasticsearch://reference/enrich-processor/set-processor.md) to set the field and associate it with the value of the ingest timestamp.

```console
PUT _ingest/pipeline/set_ingest_time
{
  "description": "Set ingest timestamp.",
  "processors": [
    {
      "set": {
        "field": "event.ingested",
        "value": "{{{_ingest.timestamp}}}"
      }
    }
  ]
}
```

After you created the ingest pipeline, apply it to the source indices of your {{transform}}. The pipeline adds the field `event.ingested` to every document with the value of the ingest timestamp. Configure the `sync`.`time`.`field` property of your {{transform}} to use the field by using the [create {{transform}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-put-transform) for new {{transforms}} or the [update {{transform}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-update-transform) for existing {{transforms}}. The `event.ingested` field is used for syncing the {{transform}}.

Refer to [Add a pipeline to an indexing request](../../manage-data/ingest/transform-enrich/ingest-pipelines.md#add-pipeline-to-indexing-request) and [Ingest pipelines](../../manage-data/ingest/transform-enrich/ingest-pipelines.md) to learn more about how to use an ingest pipeline.

## Change detection heuristics [ml-transform-checkpoint-heuristics]

When the {{transform}} runs in continuous mode, it updates the documents in the destination index as new data comes in. The {{transform}} uses a set of heuristics called change detection to update the destination index with fewer operations.

In this example, the data is grouped by host names. Change detection detects which host names have changed,  for example, host `A`, `C` and `G` and only updates documents with those hosts but does not update documents that store information about host `B`, `D`, or any other host that are not changed.

Another heuristic can be applied for time buckets when a `date_histogram` is used to group by time buckets. Change detection detects which time buckets have changed and only update those.

## Error handling [ml-transform-checkpoint-errors]

Failures in {{transforms}} tend to be related to searching or indexing. To increase the resiliency of {{transforms}}, the cursor positions of the aggregated search and the changed entities search are tracked in memory and persisted periodically.

Checkpoint failures can be categorized as follows:

* Temporary failures: The checkpoint is retried. If 10 consecutive failures occur, the {{transform}} has a failed status. For example, this situation might occur when there are shard failures and queries return only partial results.
* Irrecoverable failures: The {{transform}} immediately fails. For example, this situation occurs when the source index is not found.
* Adjustment failures: The {{transform}} retries with adjusted settings. For example, if a parent circuit breaker memory errors occur during the composite aggregation, the {{transform}} receives partial results. The aggregated search is retried with a smaller number of buckets. This retry is performed at the interval defined in the `frequency` property for the {{transform}}. If the search is retried to the point where it reaches a minimal number of buckets, an irrecoverable failure occurs.

If the node running the {{transforms}} fails, the {{transform}} restarts from the most recent persisted cursor position. This recovery process might repeat some of the work the {{transform}} had already done, but it ensures data consistency.
