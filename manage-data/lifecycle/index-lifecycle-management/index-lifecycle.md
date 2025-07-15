---
navigation_title: Index lifecycle
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-index-lifecycle.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Index lifecycle [ilm-index-lifecycle]


[{{ilm-cap}}](../index-lifecycle-management.md) ({{ilm-init}}) defines five index lifecycle *phases*:

* **Hot**: The index is actively being updated and queried.
* **Warm**: The index is updated infrequently or not at all, but is still being queried.
* **Cold**: The index is updated infrequently or not at all, and is also queried infrequently. The information still needs to be searchable, but it’s okay if those queries are slower.
* **Frozen**: The index is no longer being updated and is queried rarely. The information still needs to be searchable, but it’s okay if those queries are extremely slow.
* **Delete**: The index is no longer needed and can safely be removed.

An index’s *lifecycle policy* specifies which phases are applicable, what actions are performed in each phase, and when it transitions between phases.

You can manually apply a lifecycle policy when you create an index. For time series indices, you need to associate the lifecycle policy with the index template used to create new indices in the series. When an index rolls over, a manually-applied policy isn’t automatically applied to the new index.

If you use {{es}}'s security features, {{ilm-init}} performs operations as the user who last updated the policy. {{ilm-init}} only has the [roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) assigned to the user at the time of the last policy update.


## Phase transitions [ilm-phase-transitions]

{{ilm-init}} moves indices through the lifecycle according to their age. To control the timing of these transitions, you set a *minimum age* for each phase. For an index to move to the next phase, all actions in the current phase must be complete and the index must be older than the minimum age of the next phase. Configured minimum ages must increase between subsequent phases, for example, a "warm" phase with a minimum age of 10 days can only be followed by a "cold" phase with a minimum age either unset, or >= 10 days.

The minimum age defaults to zero, which causes {{ilm-init}} to move indices to the next phase as soon as all actions in the current phase complete.

::::{note}
If an index has been [rolled over](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md), then the `min_age` value is relative to the time the index was rolled over, not the index creation time. [Learn more](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).

::::


If an index has unallocated shards and the [cluster health status](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) is yellow, the index can still transition to the next phase according to its {{ilm}} policy. However, because {{es}} can only perform certain clean up tasks on a green cluster, there might be unexpected side effects.

To avoid increased disk usage and reliability issues, address any cluster health problems in a timely fashion.


## Phase execution [ilm-phase-execution]

{{ilm-init}} controls the order in which the actions in a phase are executed and what *steps* are executed to perform the necessary index operations for each action.

When an index enters a phase, {{ilm-init}} caches the phase definition in the index metadata. This ensures that policy updates don’t put the index into a state where it can never exit the phase. If changes can be safely applied, {{ilm-init}} updates the cached phase definition. If they cannot, phase execution continues using the cached definition.

{{ilm-init}} runs periodically, checks to see if an index meets policy criteria, and executes whatever steps are needed. To avoid race conditions, {{ilm-init}} might need to run more than once to execute all of the steps required to complete an action. For example, if {{ilm-init}} determines that an index has met the rollover criteria, it begins executing the steps required to complete the rollover action. If it reaches a point where it is not safe to advance to the next step, execution stops. The next time {{ilm-init}} runs, {{ilm-init}} picks up execution where it left off. This means that even if `indices.lifecycle.poll_interval` is set to 10 minutes and an index meets the rollover criteria, it could be 20 minutes before the rollover is complete.


## Phase actions [ilm-phase-actions]

{{ilm-init}} supports the following actions in each phase. The order in which actions are performed varies for different lifecycle phase. Refer to the [Phases and available actions](#phases-availability) table for a summary of the phases for which each action is available.

### Hot phase

The following actions are available in the `hot` lifecycle phase. Actions are performed in the order listed.

| Action | Description |
| --- | --- |
| [Set priority](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-set-priority.md) | Sets the priority level of the index, which determines the order in which indices are recovered following a node restart. |
| [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md) | Converts a [{{ccr-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ccr) follower index into a regular index, enabling the shrink, rollover, and searchable snapshot actions to be performed safely on follower indices. |
| [Rollover](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) | Rolls over a target to a new index when the existing index satisfies the specified rollover conditions. |
| [Read-only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md) | Makes the index data read-only, disabling data write operations against it. |
| [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) | Aggregates a time series (TSDS) index and stores pre-computed statistical summaries (min, max, sum, value_count and avg) for each metric field grouped by a configured time interval. |
| [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md) | Blocks write operations on a source index and shrinks it into a new index with fewer primary shards. |
| [Force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) | Reduces the number of segments in each shard by merging some of them together. |
| [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) | Takes a snapshot of the managed index in the configured repository and mounts it as a [searchable snapshot](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). |

### Warm phase

The following actions are available in the `warm` lifecycle phase. Actions are performed in the order listed.

| Action | Description |
| --- | --- |
| [Set priority](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-set-priority.md) | Sets the priority level of the index, which determines the order in which indices are recovered following a node restart. |
| [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md) | Converts a [{{ccr-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ccr) follower index into a regular index, enabling the shrink, rollover, and searchable snapshot actions to be performed safely on follower indices. |
| [Read-only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md) | Makes the index data read-only, disabling data write operations against it. |
| [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) | Aggregates a time series (TSDS) index and stores pre-computed statistical summaries (`min`, `max`, `sum`, `value_count`, and `avg`) for each metric field grouped by a configured time interval. |
| [Allocate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md) | Updates the index settings to change which nodes are allowed to host the index shards and change the number of replicas. |
| [Migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) | Moves the index to the [data tier](/manage-data/lifecycle/data-tiers.md) that corresponds to the current phase by updating the `index.routing.allocation.include._tier_preference` index setting. |
| [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md) | Blocks writes on a source index and shrinks it into a new index with fewer primary shards. |
| [Force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) | Reduces the number of segments in each shard by merging some of them together. |

### Cold phase

The following actions are available in the `cold` lifecycle phase. Actions are performed in the order listed.

| Action | Description |
| --- | --- |
| [Set priority](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-set-priority.md) | Sets the priority level of the index, which determines the order in which indices are recovered following a node restart. |
| [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md) | Converts a [{{ccr-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ccr) follower index into a regular index, enabling the shrink, rollover, and searchable snapshot actions to be performed safely on follower indices. |
| [Read-only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md) | Makes the index data read-only, disabling data write operations against it. |
| [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) | Aggregates a time series (TSDS) index and stores pre-computed statistical summaries (min, max, sum, value_count and avg) for each metric field grouped by a configured time interval. |
| [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) | Takes a snapshot of the managed index in the configured repository and mounts it as a [searchable snapshot](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). |
| [Allocate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md) | Updates the index settings to change which nodes are allowed to host the index shards and change the number of replicas. |
| [Migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) | Moves the index to the [data tier](/manage-data/lifecycle/data-tiers.md) that corresponds to the current phase by updating the `index.routing.allocation.include._tier_preference` index setting. |

### Frozen phase

The following actions are available in the `frozen` lifecycle phase. Actions are performed in the order listed.

| Action | Description |
| --- | --- |
| [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md) | Converts a [{{ccr-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ccr) follower index into a regular index, enabling the shrink, rollover, and searchable snapshot actions to be performed safely on follower indices. |
| [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) | Takes a snapshot of the managed index in the configured repository and mounts it as a [searchable snapshot](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md). |

### Delete phase

The following actions are available in the `delete` lifecycle phase. Actions are performed in the order listed.

| Action | Description |
| --- | --- |
| [Wait for snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-wait-for-snapshot.md) | Waits for the specified snapshot lifecycle management (SLM) policy to be executed before removing the index, ensuring that a snapshot of the deleted index is available. |
| [Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md) | Permanently removes the index. |

### Phases and available actions [phases-availability]

The following table summarizes the actions available in each phase.

| Action | `Hot` | `Warm` | `Cold` | `Frozen` | `Delete` |
| --- | --- | --- | --- | --- | --- |
| [Allocate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md) | ✕ | ✓ | ✓ | ✕ | ✕ |
| [Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md) | ✕ | ✕ | ✕ | ✕ | ✓ |
| [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) | ✓ | ✓ | ✓ | ✕ | ✕ |
| [Force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) | ✓ | ✓ | ✕ | ✕ | ✕ |
| [Migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) | ✕ | ✓ | ✓ | ✕ | ✕ |
| [Read-only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md) | ✓ | ✓ | ✓ | ✕ | ✕ |
| [Rollover](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) | ✓ | ✕ | ✕ | ✕ | ✕ |
| [Searchable snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md) | ✓ | ✕ | ✓ | ✓ | ✕ |
| [Set priority](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-set-priority.md) | ✓ | ✓ | ✓ | ✕ | ✕ |
| [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md) | ✓ | ✓ | ✕ | ✕ | ✕ |
| [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md) | ✓ | ✓ | ✓ | ✓ | ✕ |
| [Wait for snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-wait-for-snapshot.md) | ✕ | ✕ | ✕ | ✕ | ✓ |


