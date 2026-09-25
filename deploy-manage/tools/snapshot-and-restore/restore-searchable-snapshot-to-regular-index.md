---
navigation_title: Restore data to a regular index
description: Restore fully or partially mounted Elasticsearch searchable snapshots as regular indices.
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
---

# Restore {{search-snap}} data to a regular index [restore-searchable-snapshot-data-to-regular-index]

A [{{search-snap}}](searchable-snapshots.md) index is a read-only index whose data is stored in a snapshot repository.

Use this procedure for fully mounted and partially mounted {{search-snaps}} when you need to:

* Modify documents that are stored in a read-only {{search-snap}}.
* Move the data to another snapshot repository by restoring it before creating a new snapshot.
* Remove a data tier, such as the frozen tier, while keeping its data available as regular indices on another tier.
* Return the data to regular index storage and recovery behavior instead of keeping it backed by a mounted snapshot.

This procedure restores the data from the source snapshot as a new regular index. It does not modify the mounted index in place.

The result is sometimes described as converting a {{search-snap}} back to a regular index or *rehydrating* it.

The procedure covers {{search-snaps}} mounted manually or managed by the [{{ilm}} ({{ilm-init}}) `searchable_snapshot` action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md). It also covers data stream backing indices managed by {{ilm-init}} or by [data stream lifecycle ({{dlm-init}}) with `frozen_after`](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).

:::{note}
If you want to restore {{search-snap}} indices and keep them as {{search-snaps}}, follow [Back up and restore {{search-snaps}}](searchable-snapshots.md#back-up-restore-searchable-snapshots). This guide covers a different goal: bringing the data back as a regular index instead of recreating it as a {{search-snap}} index.
:::

## Before you begin [restore-searchable-snapshot-before-you-begin]

Before restoring {{search-snap}} data to a regular index:

* Confirm that searchable snapshot index's source repository is registered and source snapshot is available.
* Ensure that the destination data nodes or tier have enough local storage for the complete regular index and its replicas. During the restore, the mounted and regular indices exist at the same time.
* If the cluster uses data tiers, select a destination tier other than the frozen tier. The frozen tier is reserved for partially mounted {{search-snaps}}.
* Ensure that you have the [permissions required to restore a snapshot](restore-snapshot.md#prerequisites) and manage the affected indices, aliases, lifecycle policies, and data streams.

::::{warning}
The source snapshot is the sole complete copy of the {{search-snap}} data. Do not delete it until the regular index is fully restored and verified and the mounted index has been deleted. Before deleting a source snapshot, also verify that no other mounted index depends on it.
::::

## Restore the data as a regular index [restore-searchable-snapshot-data]

Follow these steps to restore the data from a mounted {{search-snap}} as a regular index. To restore multiple indices, complete the procedure separately for each index.

:::::{stepper}

::::{step} Gather details and prepare the restore

**Get the mounted index settings.**

Use the mounted index settings to gather the information required for the restore and any later lifecycle decisions:

```console
GET /<searchable-snapshot-index-name>/_settings?filter_path=**.index.store.snapshot.index_name,**.index.store.snapshot.snapshot_name,**.index.store.snapshot.repository_name,**.index.lifecycle.name,**.index.lifecycle.rollover_alias&expand_wildcards=all
```

For example, the following response shows the relevant settings for the mounted index `partial-.ds-logs-app-2026.09.01-000123`:

```console-result
{
  "partial-.ds-logs-app-2026.09.01-000123": {
    "settings": {
      "index": {
        "store": {
          "snapshot": {
            "repository_name": "my_repository",
            "snapshot_name": "my_snapshot",
            "index_name": "fm-clone-a1b2c3-.ds-logs-app-2026.09.01-000123"
          }
        },
        "lifecycle": {
          "name": "logs-app-policy"
        }
      }
    }
  }
}
```

**Record the source details.**

From the response, record the following details:

* `index.store.snapshot.repository_name` and `index.store.snapshot.snapshot_name`: The repository and snapshot to use in the restore API path. In this example, use `my_repository` and `my_snapshot`.
* `index.store.snapshot.index_name`: The name of the index stored in the source snapshot. It usually matches the regular index name before it was mounted, but it can identify an intermediate index such as `fm-clone-*` or `dlm-clone-*`. Use the exact returned value in the `indices` field of the restore request. In this example, use `fm-clone-a1b2c3-.ds-logs-app-2026.09.01-000123`.
* **{{ilm-init}} settings**: If present, record `index.lifecycle.name` and `index.lifecycle.rollover_alias` in case you want to reuse the previous policy after the restore.

**Define the restore values.**

Define the following values to use in the restore request:

* **Restored index name**: Select a name that does not already exist. For {{ilm-init}}-created {{search-snaps}}, this is typically the mounted index name without the `restored-` or `partial-` prefix. For {{dlm-init}}-created {{search-snaps}}, remove the `dlm-frozen-` prefix. For manually mounted snapshots, select any available index name. In this example, use `.ds-logs-app-2026.09.01-000123`.
* **Allocation**: If the cluster uses data tiers, select the destination and fallback tiers for the regular index. If the cluster uses nodes with the generic `data` role instead, plan to clear the inherited tier preference. The example in this guide uses the cold tier, with the warm and hot tiers as fallbacks.
* **Number of replicas**: Select the number of replicas required for the regular index. The example uses one replica.

::::

::::{step} Record how the mounted index is accessed

Use the get index API to identify any aliases and determine whether the mounted index belongs to a data stream:

```console
GET /<searchable-snapshot-index-name>?filter_path=*.aliases,*.data_stream
```

For example, the mounted index used throughout this guide is a backing index of the `logs-app` data stream and has no aliases:

```console-result
{
  "partial-.ds-logs-app-2026.09.01-000123": {
    "aliases": {},
    "data_stream": "logs-app"
  }
}
```

* If `aliases` contains any entries, record their names and complete configuration so that you can transfer them to the regular index.
* If `data_stream` is present, the index is a backing index. Record the data stream name. If the field is absent, the index does not belong to a data stream.

::::

::::{step} Restore the data from the source snapshot

Use the restore API to create a regular index from the source snapshot:

```console
POST /_snapshot/<snapshot_repository_name>/<searchable_snapshot_name>/_restore <1>
{
  "indices": "<snapshot_index_name>", <2>
  "rename_pattern": "(.+)",
  "rename_replacement": "<restored_index_name>", <3>
  "include_aliases": false, <4>
  "index_settings": {
    "index.routing.allocation.include._tier_preference": "<data_tiers>", <5>
    "index.number_of_replicas": 1, <6>
    "index.lifecycle.name": null,
    "index.lifecycle.rollover_alias": null
  }
}
```

1. Use the repository and snapshot name recorded in the first step.
2. Use the `index.store.snapshot.index_name` value. This selects the actual index stored in the source snapshot.
3. Use the selected regular index name. The rename prevents an internal source name such as `fm-clone-*` or `dlm-clone-*` from becoming the regular index name. You can omit `rename_pattern` and `rename_replacement` if the source name already matches the desired name.
4. Do not restore aliases from the snapshot. Snapshot aliases might be absent or might not reflect the aliases on the mounted index. You [transfer the current aliases after verifying the restore](#update-aliases-and-data-stream-membership).
5. If the cluster uses data tiers, specify an ordered list of destination and fallback tiers. Do not include `data_frozen` because the restored index is a regular index. If the cluster does not use data tiers, set `index.routing.allocation.include._tier_preference` to `null` so that an inherited tier preference does not restrict allocation to nodes with the generic `data` role.
6. Set the number of replicas required for the regular index.

Snapshot restore does not apply current index templates. It restores the index metadata from the snapshot and then applies the overrides in the request. If the source index has custom `require`, `include`, or `exclude` allocation filters, add the appropriate `null` overrides to `index_settings` so that they do not prevent allocation on the destination tier.

**Example:** Using the values gathered for `partial-.ds-logs-app-2026.09.01-000123` in the previous steps, restore the data with the following request:

```console
POST /_snapshot/my_repository/my_snapshot/_restore
{
  "indices": "fm-clone-a1b2c3-.ds-logs-app-2026.09.01-000123",
  "rename_pattern": "(.+)",
  "rename_replacement": ".ds-logs-app-2026.09.01-000123",
  "include_aliases": false,
  "index_settings": {
    "index.routing.allocation.include._tier_preference": "data_cold,data_warm,data_hot",
    "index.number_of_replicas": 1,
    "index.lifecycle.name": null,
    "index.lifecycle.rollover_alias": null
  }
}
```

::::

::::{step} Verify the restored index

Wait for the restore to finish and verify the regular index:

```console
GET /<restored-index-name>/_recovery?active_only=true
GET /_cat/indices/<restored-index-name>?v=true
GET /<restored-index-name>/_settings?filter_path=**.index.store.snapshot
```

Confirm that:

* The recovery response shows no active recoveries.
* The index health is `green`.
* `docs.count` and `store.size` have the expected values.
* The settings response contains no `index.store.snapshot` settings. Their absence confirms that the restored index is a regular index rather than a mounted {{search-snap}}.

::::

::::{step} Clear restored {{ilm-init}} metadata

If {{ilm-init}} managed the index before it became a {{search-snap}}, remove the restored lifecycle execution state:

```console
POST /<restored-index-name>/_ilm/remove
```

The restore request sets `index.lifecycle.name` and `index.lifecycle.rollover_alias` to `null` so that the restored index does not automatically resume its previous policy. The [remove policy API]({{es-apis}}operation/operation-ilm-remove-policy) then clears inherited lifecycle execution metadata, including the cached phase definition and any previous error state. Together, these actions provide a predictable starting point before you deliberately apply a policy to the regular index.

For more information about controlling lifecycle execution when restoring managed indices, refer to [Restore managed indices and manage {{ilm-init}} actions](/manage-data/lifecycle/index-lifecycle-management/restore-managed-data-stream-index.md).

For the restored index in this guide, use:

```console
POST /.ds-logs-app-2026.09.01-000123/_ilm/remove
```

::::

::::{step} Modify the restored data (optional)

If your reason for restoring the data is to update or delete documents, make and verify those changes now. The restored index is already verified as a regular index, but aliases, the data stream, or clients still use the mounted {{search-snap}} index.

Skip this step if you do not need to modify the restored data.

::::

::::{step} Update aliases and data stream membership

Use the access details recorded earlier to make aliases and the data stream use the restored regular index. Complete each action that applies before deleting the mounted {{search-snap}} index.

#### Transfer aliases

If the mounted {{search-snap}} index uses aliases, transfer them to the regular index in one request:

  ```console
  POST /_aliases
  {
    "actions": [
      {
        "remove": {
          "index": "<searchable-snapshot-index-name>",
          "alias": "<alias-name>"
        }
      },
      {
        "add": { <1>
          "index": "<restored-index-name>",
          "alias": "<alias-name>"
        }
      }
    ]
  }
  ```
  1. Add one `remove` and `add` action pair for each alias. Include any filter, routing, or other alias configuration recorded earlier. The request applies all actions atomically.

#### Replace a data stream backing index

If the mounted {{search-snap}} index is a data stream backing index, replace it with the regular index.

:::{warning}
:applies_to: {"stack": "ga 9.5+"}

If [{{dlm-init}}](/manage-data/lifecycle/data-stream.md) manages the data stream, review its lifecycle settings before adding the regular index:

* If `frozen_after` is configured, the restored backing index might become eligible for conversion back to a {{search-snap}} based on its age. Depending on the intended behavior, remove the setting to stop future frozen conversions for the data stream, or increase its value to delay when the restored index becomes eligible.
* Any configured `data_retention` also applies after you add the regular index. Confirm that the retention period will not delete it earlier than intended.

Refer to [Update the lifecycle of a data stream](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md) and [{{search-snaps-cap}} for data streams](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).
:::

Use the modify data stream API to replace the backing index atomically:

```console
POST /_data_stream/_modify
{
  "actions": [
    {
      "remove_backing_index": {
        "data_stream": "<data-stream-name>",
        "index": "<searchable-snapshot-index-name>"
      }
    },
    {
      "add_backing_index": {
        "data_stream": "<data-stream-name>",
        "index": "<restored-index-name>"
      }
    }
  ]
}
```

Refer to [Modify a data stream](/manage-data/data-store/data-streams/modify-data-stream.md#data-streams-modify-backing-indices).

For the `logs-app` data stream example, use:

```console
POST /_data_stream/_modify
{
  "actions": [
    {
      "remove_backing_index": {
        "data_stream": "logs-app",
        "index": "partial-.ds-logs-app-2026.09.01-000123"
      }
    },
    {
      "add_backing_index": {
        "data_stream": "logs-app",
        "index": ".ds-logs-app-2026.09.01-000123"
      }
    }
  ]
}
```

Verify that the data stream contains the regular backing index:

```console
GET /_data_stream/<data-stream-name>
```

::::

::::{step} Delete the mounted index

After confirming that aliases, the data stream, or clients use the regular index, delete the mounted {{search-snap}} index:

```console
DELETE /<searchable-snapshot-index-name>
```

::::

::::{step} Delete the source snapshot (optional)

Delete the source snapshot if you no longer need it:

:::{warning}
Delete the source snapshot only after verifying the restored regular index and deleting the mounted {{search-snap}} index.

Before deleting the snapshot, confirm that no other mounted index in this or another cluster depends on it and that it contains no other data you need. Manually created snapshots can contain multiple indices. A snapshot created by the {{ilm-init}} `searchable_snapshot` action contains only the managed index, but you must still confirm that you no longer need it.

If the restored index has no replicas, consider retaining the source snapshot until a new snapshot containing the restored data is available.
:::

```console
DELETE /_snapshot/<snapshot_repository_name>/<searchable_snapshot_name>
```

::::

:::::

## Manage the regular index lifecycle [manage-restored-index-lifecycle]

The restored regular index is not managed by {{ilm-init}} because the restore process removes its previous policy assignment and lifecycle execution state. Choose how to manage it based on why you restored the data and how you want to retain it:

* Leave the index unmanaged.
* Apply an {{ilm-init}} policy designed for an existing index.
* Return the index to an existing rollover-based lifecycle.
* {applies_to}`stack: ga 9.5+` Let {{dlm-init}} manage the index automatically if it belongs to a {{dlm-init}}-managed data stream.

If you might reuse the previous policy, retrieve its definition:

```console
GET /_ilm/policy/<policy-name>
```

Before applying an {{ilm-init}} policy, review its phases, actions, and `min_age` values. If {{ilm-init}} uses an earlier origination date, the restored index might become eligible for multiple phases or deletion immediately.

### Apply an {{ilm-init}} policy without rollover [apply-policy-without-rollover]

When possible, [create a dedicated policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) for restored historical indices. Because these indices are generally not active write indices, they typically do not need rollover or the same phases and actions as indices managed from creation. Include only the actions you need, such as moving data between available tiers, converting the index to a new {{search-snap}}, or deleting it according to your retention requirements.

If the policy includes resource-intensive actions such as force merge, apply it to restored indices gradually and monitor the cluster to avoid running too many actions concurrently.

If the index name contains its original creation date in the supported format, set `index.lifecycle.parse_origination_date` to `true` so that {{ilm-init}} calculates its age from that date:

```console
PUT /.ds-logs-app-2026.09.01-000123/_settings
{
  "index.lifecycle.name": "restored-index-policy",
  "index.lifecycle.parse_origination_date": true
}
```

Refer to [Apply an {{ilm-init}} policy to an existing index](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md) and [Manage existing indices](/manage-data/lifecycle/index-lifecycle-management/manage-existing-indices.md#ilm-existing-indices-apply).

### Reuse an {{ilm-init}} policy with rollover [reuse-policy-with-rollover]

You can reuse a policy with rollover when its rollover mechanism is already active and the restored index is not the write index. Set `index.lifecycle.indexing_complete` to `true` when you reapply the policy so that {{ilm-init}} does not attempt to roll over the historical index. You do not need this setting during the restore because the remove policy API clears it.

If the reused policy contains a `searchable_snapshot` action, {{ilm-init}} can convert the regular index to a new {{search-snap}} after it completes any preceding actions.

The following examples assume that the index name contains its original creation date in the supported format. Otherwise, omit `index.lifecycle.parse_origination_date` or set `index.lifecycle.origination_date` explicitly. Refer to [{{ilm-cap}} settings](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md) for details about these settings.

#### Backing index of an {{ilm-init}}-managed data stream

After adding the restored backing index to the data stream, reapply the policy and mark indexing as complete:

```console
PUT /.ds-logs-app-2026.09.01-000123/_settings
{
  "index.lifecycle.name": "logs-app-policy",
  "index.lifecycle.indexing_complete": true,
  "index.lifecycle.parse_origination_date": true
}
```

#### Index that uses a rollover alias

For an alias-based rollover lifecycle, also set the `index.lifecycle.rollover_alias` setting. Confirm that the alias has another write index and that the restored index is not its write index:

```console
PUT /logs-app-2026.09.01-000123/_settings
{
  "index.lifecycle.name": "logs-app-policy",
  "index.lifecycle.rollover_alias": "logs-app-write",
  "index.lifecycle.indexing_complete": true,
  "index.lifecycle.parse_origination_date": true
}
```

Refer to [Skip rollover manually](/manage-data/lifecycle/index-lifecycle-management/skip-rollover.md) for the requirements and behavior of `index.lifecycle.indexing_complete`.

### Use {{dlm-init}} [manage-restored-index-with-dlm]
```{applies_to}
stack: ga 9.5+
```

After you add the regular index to a {{dlm-init}}-managed data stream, the data stream lifecycle applies automatically. The `index.lifecycle.indexing_complete` setting is specific to {{ilm-init}} and is not required for {{dlm-init}}. No additional lifecycle assignment is required.

## Related pages [restore-searchable-snapshot-related-pages]

* [{{search-snaps-cap}}](searchable-snapshots.md)
* [Restore a snapshot](restore-snapshot.md)
* [Restore managed indices and manage {{ilm-init}} actions](/manage-data/lifecycle/index-lifecycle-management/restore-managed-data-stream-index.md)
* [{{ilm-init}} `searchable_snapshot` action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md)
* [{{search-snaps-cap}} for data streams](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md)
