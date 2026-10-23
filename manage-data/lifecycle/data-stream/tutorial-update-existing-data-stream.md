---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tutorial-manage-existing-data-stream.html
applies_to:
  stack: ga
  serverless: ga
type: how-to
description: Update the lifecycle of an Elasticsearch data stream. Change its data phases or remove the lifecycle.
products:
  - id: elasticsearch
---

# Update the lifecycle of a data stream [tutorial-manage-existing-data-stream]

Change the lifecycle configuration for a classic {{es}} data stream, such as its data retention or phases.

For wired data streams, go to [](/solutions/observability/streams/configure-retention.md).

For {{ilm-init}}, refer to [](/manage-data/lifecycle/index-lifecycle-management.md).

## Before you begin [update-data-stream-lifecycle-prereqs]

To follow these steps, you need:

* A classic data stream. To create one, refer to [](/manage-data/lifecycle/data-stream/tutorial-create-data-stream-with-lifecycle.md).
* The `manage_data_stream_lifecycle` [index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) on the data stream and its backing indices.
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` A default snapshot repository and an [appropriate license]({{subscriptions}}) for {{search-snaps}} if you turn on frozen phase transitions. Refer to [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md).

## Set a data stream's lifecycle [set-lifecycle]

Add or change the data stream lifecycle with the **{{index-manage-app}}** or **Streams** tools in {{kib}} or the {{es}} [lifecycle API]({{es-apis}}operation/operation-indices-put-data-lifecycle).

:::::{applies-switch}
::::{applies-item} serverless: ga

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data Streams** tab.
1. Search for the data stream.
1. Select the data stream to view its details.
1. In the data stream details pane, click the actions icon {icon}`gear` and select **Edit data lifecycle**.
1. You can choose to inherit lifecycle settings from the index template or customize the lifecycle for this data stream:

   ![Edit data lifecycle page](/manage-data/images/elasticsearch-serverless-edit-data-lifecycle.png "=50%")

   * On the **Successful data** tab, select the **Delete phase** to choose how long to retain your data, in days, hours, minutes, or seconds.
    <!--TBD: This did not work for me, it always reverted to inheriting from the lifecycle instead. If you deselect the delete phase, {{es}} does not delete the data. -->
   * On the **Failed data** tab, select **Enable failure store** to turn on a [failure store](/manage-data/data-store/data-streams/failure-store.md). Select how long to retain failure store data, in days, hours, minutes, or seconds.

1. Click **Apply** to save the changes.

<!-- TO-DO: Dependent on https://github.com/elastic/docs-builder/pull/4541
   :::{image} /manage-data/images/elasticsearch-serverless-edit-data-lifecycle.png
   :screenshot:
   :width: 50%
   :::
-->

Lifecycle changes apply to every backing index of the data stream.

::::

::::{applies-item} stack: ga 9.5+

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data Streams** tab.
1. Search for the data stream.
1. Select the data stream to view its details.
1. In the data stream details pane, click the actions icon {icon}`gear` and select **Edit data lifecycle**.
1. Select the **Data stream lifecycle** method.
1. You can choose to inherit lifecycle settings from the index template or customize the lifecycle for this data stream:

   ![Edit data lifecycle page](/manage-data/images/elasticsearch-edit-data-lifecycle.png "=50%")

   * On the **Successful data** tab:

     Select the **Delete phase** to choose how long to retain your data, in days, hours, minutes, or seconds. If you deselect the delete phase, {{es}} does not delete the data.

     Select the **Frozen phase** to choose when to move your data to {{search-snaps}}, in days, hours, minutes, or seconds. This period must be shorter than the delete phase. To change the default snapshot repository, refer to [{{ech}}](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md#snapshot-repo-default) or [self-managed](/deploy-manage/tools/snapshot-and-restore/self-managed.md#snapshot-repo-default) instructions.
     $$$configure-dlm-searchable-snapshots$$$

   * On the **Failed data** tab, select **Enable failure store** to turn on a [failure store](/manage-data/data-store/data-streams/failure-store.md). Select how long to retain failure store data, in days, hours, minutes, or seconds.

1. Click **Apply** to save the changes.

1. Reopen the data stream flyout to confirm the change. The flyout shows the successful and failure ingest lifecycle details.

Lifecycle changes apply to every backing index of the data stream.

::::

::::{applies-item} stack: ga 9.0-9.4

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data Streams** tab.
1. Search for the data stream.
1. Select the data stream to view its details.
1. In the data stream details pane, select **Manage** → **Edit data retention**.

   ![Edit data retention page](/manage-data/images/elasticsearch-edit-data-retention.png "=50%")

   You can do any of the following:

   * Select how long to retain your data, in days, hours, minutes, or seconds.
   * Select **Keep data indefinitely**. The data stream stays managed but {{es}} does not delete the data. Managing a {{tsds}}, such as logs or metrics, helps {{es}} store your data even when you don't set a retention period.
   * Turn off **Enable data retention** to stop data stream lifecycle management for this data stream.

1. Reopen the data stream flyout to confirm the change. The flyout shows the effective data retention settings.

Lifecycle changes apply to every backing index of the data stream.

::::

:::::

$$$data-retention-streams$$$
{applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` Alternatively, you can use the **Streams** page in {{kib}}, which is a centralized interface for common data management tasks, including how your data streams retain data. Refer to [](/solutions/observability/streams/configure-retention.md).

::::{dropdown} API example

To update the lifecycle of a data stream, use the {{es}} [lifecycle API]({{es-apis}}operation/operation-indices-put-data-lifecycle):

* Set an indefinite retention period so {{es}} does not delete the data. For example:

    ```console
    PUT _data_stream/my-data-stream-test/_lifecycle
    { } <1>
    ```

    1. An empty payload means that your data stream is managed but {{es}} does not delete the data. Managing a {{tsds}}, such as logs or metrics, helps {{es}} store your data even when you don't set a retention period.

* Alternatively, set a retention period. For example:

    ```console
    PUT _data_stream/my-data-stream-test/_lifecycle
    {
      "data_retention": "30d" <1>
    }
    ```

    1. The retention period of this data stream is 30 days. {{es}} can delete data older than 30 days.

* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` Optionally add `frozen_after` so older backing indices become partially mounted {{search-snaps}} on the frozen tier. For example:

  ```console
  PUT _data_stream/my-data-stream-test/_lifecycle
  {
    "data_retention": "365d",
    "frozen_after": "30d" <1>
  }
  ```

  1. If you specify both `data_retention` and `frozen_after`, the latter duration must be shorter than the former.

  In this example, backing indices older than 30 days are converted to frozen {{search-snaps}}.
  {{es}} can still delete indices when their `generation_time` exceeds the effective retention period, even after they are frozen.
  For prerequisites, how conversion works, and troubleshooting, refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).

These lifecycle changes apply to every backing index of the data stream.
To check the settings, use the {{es}} [explain API]({{es-apis}}operation/operation-indices-explain-data-lifecycle):

```console
GET my-data-stream-test/_lifecycle/explain
```

**Result:**

```console-result
{
  "indices": {
    ".ds-my-data-stream-test-2026.10.17-000001": {
      "index": ".ds-my-data-stream-test-2026.10.17-000001", <1>
      "managed_by_lifecycle": true, <2>
      "index_creation_date_millis": 1792195511314,
      "time_since_index_creation": "2.97d", <3>
      "rollover_date_millis": 1792440980120,
      "time_since_rollover": "3.12h", <4>
      "generation_time": "3.12h", <5>
      "lifecycle": {
        "enabled": true,
        "data_retention": "30d", <6>
        "retention_determined_by": "data_stream_configuration"
      }
    },
    ".ds-my-data-stream-test-2026.10.19-000002": {
      "index": ".ds-my-data-stream-test-2026.10.19-000002",
      "managed_by_lifecycle": true,
      "index_creation_date_millis": 1792440980129,
      "time_since_index_creation": "3.12h",
      "lifecycle": {
        "enabled": true,
        "data_retention": "30d",
        "retention_determined_by": "data_stream_configuration"
      }
    }
  }
}
```

1. The name of the backing index.
1. This index is managed by a data stream lifecycle.
1. The time since this index was created.
1. The time since this index was [rolled over](/manage-data/lifecycle/index-lifecycle-management/rollover.md).
1. The time used to determine when it's safe to delete this index and its data.
1. The data retention for this index is at least 30 days, because the lifecycle was updated recently.

::::

## Remove the lifecycle for a data stream [delete-lifecycle]
```{applies_to}
stack: ga
serverless: unavailable
```

Remove the lifecycle with the **{{index-manage-app}}** tools in {{kib}} or the {{es}} [delete lifecycle API]({{es-apis}}operation/operation-indices-delete-data-lifecycle).

:::::{applies-switch}

::::{applies-item} stack: ga 9.5+

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data Streams** tab.
1. Search for the data stream.
1. Select the data stream to view its details.
1. In the data stream details pane, click the actions icon {icon}`gear` and select **Edit data lifecycle**.
1. On the **Successful data** tab, select the **Data stream lifecycle** method and deselect all optional phases.
1. Click **Apply** to save the changes.
1. Reopen the data stream flyout to confirm the change. **Successful ingest lifecycle** shows an infinity icon {icon}`infinity` to indicate that it keeps data indefinitely.

::::
::::{applies-item} stack: ga 9.0-9.4

1. Find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data Streams** tab.
1. Search for the data stream.
1. Select the data stream to view its details.
1. In the data stream details pane, select **Manage** → **Edit data retention**.
1. Turn off **Enable data retention** and save your changes.
1. Reopen the data stream flyout to confirm the change. **Effective data retention** shows **Disabled**.

::::

:::::

<!-- TBD: In 9.6 test these Kibana methods don't seem to have the same result as the API i.e. do not make the stream `"managed_by_lifecycle": false` -->

::::{dropdown} API example

To remove a data stream's lifecycle:

```console
DELETE _data_stream/my-data-stream-test/_lifecycle
```

After this request, the maintenance operations from the lifecycle no longer apply to the data stream or its backing indices.

Use the [explain API]({{es-apis}}operation/operation-indices-explain-data-lifecycle) to verify that the indices are no longer managed.

```console
GET my-data-stream-test/_lifecycle/explain
```

```console-result
{
  "indices": {
    ".ds-my-data-stream-test-2026.10.17-000001": {
      "index": ".ds-my-data-stream-test-2026.10.17-000001", <1>
      "managed_by_lifecycle": false, <2>
      "unmanaged_reason": "Index [.ds-my-data-stream-test-2026.10.17-000001] belongs to data stream [my-data-stream-test] which does not have data stream lifecycle configuration." <3>
    },
    ".ds-my-data-stream-test-2026.10.19-000002": {
      "index": ".ds-my-data-stream-test-2026.10.19-000002",
      "managed_by_lifecycle": false,
      "unmanaged_reason": "Index [.ds-my-data-stream-test-2026.10.19-000002] belongs to data stream [my-data-stream-test] which does not have data stream lifecycle configuration."
    }
  }
}
```

1. The name of the backing index.
1. The data stream lifecycle does not manage the index.
1. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` The reason the data stream is not managed.

::::

## Related pages [update-data-stream-lifecycle-related]

* [](/manage-data/lifecycle/data-stream.md)
* [](/manage-data/data-store/data-streams.md)
* [](/manage-data/lifecycle/index-lifecycle-management.md)
* [](/deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md)
* [](/manage-data/data-store/data-streams/manage-data-stream.md)
