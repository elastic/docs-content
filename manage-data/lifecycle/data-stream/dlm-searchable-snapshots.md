---
applies_to:
  stack: ga 9.5
  serverless: unavailable
navigation_title: Searchable snapshots
description: Learn how data stream lifecycle converts older backing indices to frozen {{search-snaps}} for low-cost, long-term retention.
type: overview
products:
  - id: elasticsearch
---

# {{search-snaps-cap}} for data streams

The data stream lifecycle ({{dlm-init}}) can automatically convert older backing indices to [{{search-snaps}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) on the [frozen tier](/manage-data/lifecycle/data-tiers.md). This lets you retain data for long periods at low storage cost while keeping it searchable, without manual snapshot or mount operations.

This page explains how frozen transitions work, what you need before they can run, and how to diagnose blocked conversions. To configure `frozen_after` on a new or existing data stream, refer to [Next steps](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md#next-steps).

## Requirements [dlm-frozen-transition-requirements]

Frozen transitions run only when the following conditions are met:

- A **default snapshot repository** is registered. {{dlm-init}} uses the cluster's default snapshot repository to store the frozen snapshot. Refer to [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md) for details.
- The data stream has [data stream lifecycle](/manage-data/lifecycle/data-stream.md) configured with the `frozen_after` field. This field is valid only on the main data stream lifecycle and cannot be set on the failure-store lifecycle.

::::{note}
The frozen phase transition feature is a commercial feature that requires an appropriate license. For more information, refer to [{{es}} pricing and subscriptions]({{subscriptions}}).
::::

## How it works [dlm-frozen-transition-process]

When a backing index's creation date is older than the `frozen_after` period configured on the data stream lifecycle, {{dlm-init}} converts it to a [partially mounted {{search-snap}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#partially-mounted) index allocated on frozen nodes. The conversion happens automatically in the background.

The `frozen_after` field controls when backing indices become eligible for conversion. You set it on the data stream lifecycle when you create or update a stream. To stop future frozen conversions, update the lifecycle and omit or null the `frozen_after` field. However, after an index is past its `frozen_after` time and marked as eligible for conversion, changing `frozen_after` does not stop that conversion.

The `frozen_after` value must be a positive [time unit value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units).

For example, if you set `frozen_after` to `30d` and `data_retention` to `365d`, backing indices older than 30 days are converted to frozen {{search-snaps}}. {{dlm-init}} continues to apply the `data_retention` period: indices older than 365 days are deleted even after they have been frozen. For more about retention, refer to [](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md).

When a backing index becomes eligible for frozen conversion, {{dlm-init}} performs the following steps on the master node:

1. **Mark the index eligible for transition** — The index is marked as needing conversion, ready for a worker to pick up that index and start the conversion process.
2. **Mark the index read-only** — A write block is applied and a flush is issued to ensure no in-flight writes are lost.
3. **Clone the index** — If the original index has replicas, {{dlm-init}} creates a zero-replica clone (named `dlm-clone-<original-index>`) to reduce snapshot size. The clone is deleted during cleanup.
4. **Force merge to one segment** — The index (or its clone) is force-merged to a single segment per shard, which improves query performance and reduces snapshot size.
5. **Take a snapshot** — {{dlm-init}} snapshots the force-merged index to the default snapshot repository. The snapshot is named `dlm-frozen-<original-index>`.
6. **Mount as a {{search-snap}}** — The snapshot is mounted as a partially mounted index on the frozen tier (named `dlm-frozen-<original-index>`).
7. **Swap and delete originals** — The frozen index replaces the original in the data stream. The original and any clone created during the process are then deleted. This swap is atomic, and queries remain consistent before, during, and after the swap.

### Transition service and cleanup [dlm-frozen-transition-tuning]

A background transition service on the master node scans for indices ready for conversion and runs conversions concurrently. You can tune poll intervals, thread pool size, and queue size using the [frozen tier transition settings](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#_frozen_tier_transition_settings) in `elasticsearch.yml`.

If a conversion is interrupted, {{dlm-init}} might leave behind orphaned clone indices (`dlm-clone-*`) or snapshots. A separate cleanup service on the master node periodically removes these artifacts. The cleanup interval is controlled by the [`dlm.frozen.cleanup.poll_interval`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md) setting (default: `1d`, minimum: `1h`).

## Troubleshooting [dlm-frozen-transition-troubleshooting]

### Symptoms [dlm-frozen-transition-symptoms]

Conversion errors appear in the lifecycle explain output for individual backing indices.
Use the [explain data lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle) to inspect status:

```console
GET .ds-my-stream-*/_lifecycle/explain
```

For transient failures, {{dlm-init}} records the error and retries the conversion on the next poll cycle. Each conversion step is idempotent, so retries resume from the point at which the error occurred.

Conversions stop retrying when the explain output reports an unrecoverable error, such as a missing snapshot repository or a license compliance failure.

### Resolution [dlm-frozen-transition-resolution]

1. Run the explain API on the affected backing indices and note the reported error.
2. If the error indicates a missing snapshot repository, re-register the default snapshot repository. Refer to [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md).
3. If the error indicates a license compliance failure, renew the license. Refer to [{{es}} pricing and subscriptions]({{subscriptions}}).

## Next steps [next-steps]

- **New data streams:** Include `frozen_after` in the index template lifecycle when you create a data stream. Refer to [Creating a data stream with a lifecycle](/manage-data/lifecycle/data-stream/tutorial-create-data-stream-with-lifecycle.md).
- **Existing data streams:** Add or update `frozen_after` on an individual data stream using the lifecycle API. Refer to [Update the lifecycle of a data stream](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#configure-dlm-searchable-snapshots).

## Related pages [related-pages]

- [Data stream lifecycle](/manage-data/lifecycle/data-stream.md)
- [Data stream retention](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md)
- [{{search-snaps-cap}}](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md)
- [Data tiers](/manage-data/lifecycle/data-tiers.md)
