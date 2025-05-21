---
navigation_title: Index lifecycle
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-index-lifecycle.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---



# Index lifecycle [ilm-index-lifecycle]


[{{ilm-init}}](../index-lifecycle-management.md) defines five index lifecycle *phases*:

* **Hot**: The index is actively being updated and queried.
* **Warm**: The index is no longer being updated but is still being queried.
* **Cold**: The index is no longer being updated and is queried infrequently. The information still needs to be searchable, but it’s okay if those queries are slower.
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

{{ilm-init}} supports the following actions in each phase. {{ilm-init}} executes the actions in the order listed.

* Hot

    * [Set Priority](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-set-priority.md)
    * [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md)
    * [Rollover](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md)
    * [Read-Only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md)
    * [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md)
    * [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md)
    * [Force Merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md)
    * [Searchable Snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md)

* Warm

    * [Set Priority](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-set-priority.md)
    * [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md)
    * [Read-Only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md)
    * [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md)
    * [Allocate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md)
    * [Migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md)
    * [Shrink](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md)
    * [Force Merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md)

* Cold

    * [Set Priority](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-set-priority.md)
    * [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md)
    * [Read-Only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md)
    * [Downsample](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md)
    * [Searchable Snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md)
    * [Allocate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md)
    * [Migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md)

* Frozen

    * [Unfollow](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-unfollow.md)
    * [Searchable Snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md)

* Delete

    * [Wait For Snapshot](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-wait-for-snapshot.md)
    * [Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md)
