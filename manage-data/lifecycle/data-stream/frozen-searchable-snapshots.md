---
applies_to:
  stack: ga 9.5
  serverless: unavailable
navigation_title: "Move data to frozen phase snapshots"
products:
  - id: elasticsearch
---
# Move data stream backing indices to the frozen phase with the data stream lifecycle

The data stream lifecycle (DLM) can automatically convert older backing indices to [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) on the [frozen phase](/manage-data/lifecycle/data-tiers.md). This lets you retain data for long periods at low storage cost while keeping it searchable.

When a backing index's creation date is older than the `frozen_after` period configured on the data stream lifecycle, DLM converts it to a [partially mounted searchable snapshot](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) index on the frozen phase. The conversion happens automatically in the background without requiring any manual intervention.

## Prerequisites [dlm-frozen-transition-prerequisites]

Before using DLM frozen phase transitions:

- A **default snapshot repository** must be registered. DLM uses the cluster's default snapshot repository to store the frozen snapshot. See [Register a snapshot repository](/deploy-manage/tools/snapshot-and-restore/self-managed.md) for details.
- The data stream must have [data stream lifecycle](/manage-data/lifecycle/data-stream.md) configured with the `frozen_after` field. This field is only valid on the data lifecycle and cannot be set on the failure-store lifecycle.

::::{note}
The frozen phase transition feature is a commercial feature that requires an appropriate license. For more information, refer to [Elasticsearch pricing and subscriptions]({{subscriptions}}).
::::

## Configure `frozen_after` [dlm-frozen-transition-configure]

Set the `frozen_after` field when creating or updating a data stream's lifecycle using the [update data stream lifecycle API]({{es-apis}}operation/operation-indices-put-data-lifecycle):

```console
PUT _data_stream/my-stream/_lifecycle
{
  "data_retention": "365d",
  "frozen_after": "30d"
}
```

In this example, backing indices older than 30 days are automatically converted to the frozen phase. {{dlm-init}} continues to apply the `data_retention` period: indices older than 365 days are deleted even after they have been frozen.

The `frozen_after` value must be a positive [time unit value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units). To stop future frozen conversions, update the lifecycle and omit or null the `frozen_after` field. However, once an index has been seen to be past its `frozen_after` time and marked as eligible for conversion, changing the `frozen_after` will not stop the conversion.

## Conversion process [dlm-frozen-transition-process]

When a backing index becomes eligible for frozen conversion, DLM performs the following steps on the master node:

1. **Mark eligible for transition** — The index is marked as needing conversion, ready for a worker to pick up that index and start the conversion process.
2. **Mark index read-only** — A write block is applied and a flush is issued to ensure no in-flight writes are lost.
3. **Clone the index (if needed)** — If the original index has replicas, DLM creates a zero-replica clone (named `dlm-clone-<original-index>`) to reduce snapshot size. The clone is deleted during cleanup.
4. **Force merge to one segment** — The index (or its clone) is force-merged to a single segment per shard, which improves query performance and reduces snapshot size.
5. **Take a snapshot** — DLM snapshots the force-merged index to the default snapshot repository. The snapshot is named `dlm-frozen-<original-index>`.
6. **Mount as a searchable snapshot** — The snapshot is mounted as a partially mounted index on the frozen phase (named `dlm-frozen-<original-index>`).
7. **Swap and delete originals** — The frozen index replaces the original in the data stream. The original and any clone created during the process are then deleted. This swap is atomic, and queries will remain consistent before, during, and after the swap.

## Tune the transition service [dlm-frozen-transition-tuning]

You can configure the following [settings](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#_frozen_tier_transition_settings) in `elasticsearch.yml` to control the frozen transition service:

- `dlm.frozen_transition.poll_interval` — How often the master node scans for indices ready for conversion.
- `dlm.frozen.transition.thread_pool.size` — Maximum number of concurrent in-flight conversions.
- `dlm.frozen.transition.thread_pool.queue_size` — Maximum number of indices that can be queued for conversion at once.

## Cleanup of orphaned artifacts [dlm-frozen-transition-cleanup]

If a conversion is interrupted, {{dlm-init}} might leave behind orphaned clone indices (`dlm-clone-*`) or snapshots. A background cleanup service running on the master node periodically removes these artifacts.

The cleanup interval is controlled by [`dlm.frozen_cleanup.poll_interval`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md (default: `1d`, minimum: `1h`).
<!-- TO-DO: Add link to #dlm-frozen-cleanup-poll-interval anchor -->

## Failures and retries [dlm-frozen-transition-failures]

Each step of the conversion is idempotent. If a step fails, DLM records the error and retries the conversion on the next poll cycle from the point at which the error occurred.

Conversion errors are visible in the data stream's lifecycle explain output. Use the [explain data lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle) to inspect the status of individual backing indices:

```console
GET .ds-my-stream-*/_lifecycle/explain
```

Certain errors are classified as unrecoverable and will block retries until the underlying cause is resolved:

- **Missing snapshot repository** — The default snapshot repository has been removed or is unreachable. Re-register the repository to resume conversions.
- **License compliance failure** — The required license has expired or been removed. Renew the license to resume conversions.
