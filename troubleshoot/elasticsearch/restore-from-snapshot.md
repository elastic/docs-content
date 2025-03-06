---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/restore-from-snapshot.html
---

# Restore from snapshot [restore-from-snapshot]

Elasticsearch is using snapshots to store a copy of your data outside a cluster. You can restore a snapshot to recover indices and data streams for which there are no copies of the shards in the cluster. This can happen if the data (indices or data streams) was deleted or if the cluster membership changed and the current nodes in the system do not contain a copy of the data anymore.

::::{important}
Restoring the missing data requires you to have a backup of the affected indices and data streams that is up-to-date enough for your use case. Please do not proceed without confirming this.
::::


:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to restore the indices and data streams that are missing data:

**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} ../../images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

4. To view the affected indices using the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices).

    ```console
    GET _cat/indices?v&health=red&h=index,status,health
    ```

    The response will look like this:

    ```console-result
    index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   red
    kibana_sample_data_flights           open   red
    ```

    The `red` health of the indices above indicates that these indices are missing primary shards, meaning they are missing data.

5. In order to restore the data we need to find a snapshot that contains these two indices. To find such a snapshot use the [get snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get).

    ```console
    GET _snapshot/my_repository/*?verbose=false
    ```

    The response will look like this:

    ```console-result
    {
      "snapshots" : [
        {
          "snapshot" : "snapshot-20200617",                                     <1>
          "uuid" : "dZyPs1HyTwS-cnKdH08EPg",
          "repository" : "my_repository",                                       <2>
          "indices" : [                                                         <3>
            ".apm-agent-configuration",
            ".apm-custom-link",
            ".ds-ilm-history-5-2022.06.17-000001",
            ".ds-my-data-stream-2022.06.17-000001",
            ".geoip_databases",
            ".kibana-event-log-8.2.2-000001",
            ".kibana_8.2.2_001",
            ".kibana_task_manager_8.2.2_001",
            "kibana_sample_data_ecommerce",
            "kibana_sample_data_flights",
            "kibana_sample_data_logs"
          ],
          "data_streams" : [ ],
          "state" : "SUCCESS"                                                     <4>
        }
      ],
      "total" : 1,
      "remaining" : 0
    }
    ```

    1. The name of the snapshot.
    2. The repository of the snapshot.
    3. The indices backed up in the snapshot.
    4. If the snapshot was successful.

6. The snapshot `snapshot-20200617` contains the two indices we want to restore. You might have multiple snapshots from which you could restore the target indices. Choose the latest snapshot.
7. Now that we found a snapshot, we will proceed with the data stream preparation for restoring the lost data. We will check the index metadata to see if any index is part of a data stream:

    ```console
    GET kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001?features=settings&flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      ".ds-my-data-stream-2022.06.17-000001" : {                                <1>
        "aliases" : { },
        "mappings" : { },
        "settings" : {                                                          <2>
          "index.creation_date" : "1658406121699",
          "index.hidden" : "true",
          "index.lifecycle.name" : "my-lifecycle-policy",
          "index.number_of_replicas" : "1",
          "index.number_of_shards" : "1",
          "index.provided_name" : ".ds-my-data-stream-2022.06.17-000001",
          "index.routing.allocation.include._tier_preference" : "data_hot",
          "index.uuid" : "HmlFXp6VSu2XbQ-O3hVrwQ",
          "index.version.created" : "8020299"
        },
        "data_stream" : "my-data-stream"                                        <3>
      },
      "kibana_sample_data_flights" : {                                          <4>
        "aliases" : { },
        "mappings" : { },
        "settings" : {
          "index.creation_date" : "1655121541454",
          "index.number_of_replicas" : "0",
          "index.number_of_shards" : "1",
          "index.provided_name" : "kibana_sample_data_flights",
          "index.routing.allocation.include._tier_preference" : "data_content",
          "index.uuid" : "jMOlwKPPSzSraeeBWyuoDA",
          "index.version.created" : "8020299"
        }
      }
    }
    ```

    1. The name of an index.
    2. The settings of this index that contains the metadata we are looking for.
    3. This indicates that this index is part of a data stream and displays the data stream name.
    4. The name of the other index we requested.


    The response above shows that `kibana_sample_data_flights` is not part of a data stream because it doesn’t have a field called `data_stream` in the settings.

    On the contrary, `.ds-my-data-stream-2022.06.17-000001` is part of the data stream called `my-data-stream`. When you find an index like this, which belongs to a data stream, you need to check if data are still being indexed. You can see that by checking the `settings`, if you can find this property: `"index.lifecycle.indexing_complete" : "true"`, it means that indexing is completed in this index and you can continue to the next step.

    If `index.lifecycle.indexing_complete` is not there or is configured to `false` you need to rollover the data stream so you can restore the missing data without blocking the ingestion of new data. The following command will achieve that.

    ```console
    POST my-data-stream/_rollover
    ```

8. Now that the data stream preparation is done, we will close the target indices by using the [close indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-close).

    ```console
    POST kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001/_close
    ```

    You can confirm that they are closed with the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices).

    ```console
    GET _cat/indices?v&health=red&h=index,status,health
    ```

    The response will look like this:

    ```console-result
    index                                status health
    .ds-my-data-stream-2022.06.17-000001 close   red
    kibana_sample_data_flights           close   red
    ```

9. The indices are closed, now we can restore them from snapshots without causing any complications using the [restore snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore):

    ```console
    POST _snapshot/my_repository/snapshot-20200617/_restore
    {
      "indices": "kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001", <1>
      "include_aliases": true                                                       <2>
    }
    ```

    1. The indices to restore.
    2. We also want to restore the aliases.


    ::::{note}
    If any [feature states](../../deploy-manage/tools/snapshot-and-restore.md#feature-state) need to be restored we’ll need to specify them using the `feature_states` field and the indices that belong to the feature states we restore must not be specified under `indices`. The [Health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report) returns both the `indices` and `feature_states` that need to be restored for the restore from snapshot diagnosis. e.g.:
    ::::


    ```console
    POST _snapshot/my_repository/snapshot-20200617/_restore
    {
      "feature_states": [ "geoip" ],
      "indices": "kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001",
      "include_aliases": true
    }
    ```

10. Finally we can verify that the indices health is now `green` via the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices).

    ```console
    GET _cat/indices?v&index=.ds-my-data-stream-2022.06.17-000001,kibana_sample_data_flightsh=index,status,health
    ```

    The response will look like this:

    ```console-result
    index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   green
    kibana_sample_data_flights           open   green
    ```

    As we can see above the indices are `green` and open. The issue is resolved.


For more guidance on creating and restoring snapshots see [this guide](../../deploy-manage/tools/snapshot-and-restore.md).
::::::

::::::{tab-item} Self-managed
In order to restore the indices that are missing shards:

1. View the affected indices using the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices).

    ```console
    GET _cat/indices?v&health=red&h=index,status,health
    ```

    The response will look like this:

    ```console-result
    index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   red
    kibana_sample_data_flights           open   red
    ```

    The `red` health of the indices above indicates that these indices are missing primary shards, meaning they are missing data.

2. In order to restore the data we need to find a snapshot that contains these two indices. To find such a snapshot use the [get snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get).

    ```console
    GET _snapshot/my_repository/*?verbose=false
    ```

    The response will look like this:

    ```console-result
    {
      "snapshots" : [
        {
          "snapshot" : "snapshot-20200617",                                     <1>
          "uuid" : "dZyPs1HyTwS-cnKdH08EPg",
          "repository" : "my_repository",                                       <2>
          "indices" : [                                                         <3>
            ".apm-agent-configuration",
            ".apm-custom-link",
            ".ds-ilm-history-5-2022.06.17-000001",
            ".ds-my-data-stream-2022.06.17-000001",
            ".geoip_databases",
            ".kibana-event-log-8.2.2-000001",
            ".kibana_8.2.2_001",
            ".kibana_task_manager_8.2.2_001",
            "kibana_sample_data_ecommerce",
            "kibana_sample_data_flights",
            "kibana_sample_data_logs"
          ],
          "data_streams" : [ ],
          "state" : "SUCCESS"                                                     <4>
        }
      ],
      "total" : 1,
      "remaining" : 0
    }
    ```

    1. The name of the snapshot.
    2. The repository of the snapshot.
    3. The indices backed up in the snapshot.
    4. If the snapshot was successful.

3. The snapshot `snapshot-20200617` contains the two indices we want to restore. You might have multiple snapshots from which you could restore the target indices. Choose the latest snapshot.
4. Now that we found a snapshot, we will proceed with the data stream preparation for restoring the lost data. We will check the index metadata to see if any index is part of a data stream:

    ```console
    GET kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001?features=settings&flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      ".ds-my-data-stream-2022.06.17-000001" : {                                <1>
        "aliases" : { },
        "mappings" : { },
        "settings" : {                                                          <2>
          "index.creation_date" : "1658406121699",
          "index.hidden" : "true",
          "index.lifecycle.name" : "my-lifecycle-policy",
          "index.number_of_replicas" : "1",
          "index.number_of_shards" : "1",
          "index.provided_name" : ".ds-my-data-stream-2022.06.17-000001",
          "index.routing.allocation.include._tier_preference" : "data_hot",
          "index.uuid" : "HmlFXp6VSu2XbQ-O3hVrwQ",
          "index.version.created" : "8020299"
        },
        "data_stream" : "my-data-stream"                                        <3>
      },
      "kibana_sample_data_flights" : {                                          <4>
        "aliases" : { },
        "mappings" : { },
        "settings" : {
          "index.creation_date" : "1655121541454",
          "index.number_of_replicas" : "0",
          "index.number_of_shards" : "1",
          "index.provided_name" : "kibana_sample_data_flights",
          "index.routing.allocation.include._tier_preference" : "data_content",
          "index.uuid" : "jMOlwKPPSzSraeeBWyuoDA",
          "index.version.created" : "8020299"
        }
      }
    }
    ```

    1. The name of an index.
    2. The settings of this index that contains the metadata we are looking for.
    3. This indicates that this index is part of a data stream and displays the data stream name.
    4. The name of the other index we requested.


    The response above shows that `kibana_sample_data_flights` is not part of a data stream because it doesn’t have a field called `data_stream` in the settings.

    On the contrary, `.ds-my-data-stream-2022.06.17-000001` is part of the data stream called `my-data-stream`. When you find an index like this, which belongs to a data stream, you need to check if data are still being indexed. You can see that by checking the `settings`, if you can find this property: `"index.lifecycle.indexing_complete" : "true"`, it means that indexing is completed in this index and you can continue to the next step.

    If `index.lifecycle.indexing_complete` is not there or is configured to `false` you need to rollover the data stream so you can restore the missing data without blocking the ingestion of new data. The following command will achieve that.

    ```console
    POST my-data-stream/_rollover
    ```

5. Now that the data stream preparation is done, we will close the target indices by using the [close indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-close).

    ```console
    POST kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001/_close
    ```

    You can confirm that they are closed with the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices).

    ```console
    GET _cat/indices?v&health=red&h=index,status,health
    ```

    The response will look like this:

    ```console-result
    index                                status health
    .ds-my-data-stream-2022.06.17-000001 close   red
    kibana_sample_data_flights           close   red
    ```

6. The indices are closed, now we can restore them from snapshots without causing any complications using the [restore snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore):

    ```console
    POST _snapshot/my_repository/snapshot-20200617/_restore
    {
      "indices": "kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001", <1>
      "include_aliases": true                                                       <2>
    }
    ```

    1. The indices to restore.
    2. We also want to restore the aliases.


    ::::{note}
    If any [feature states](../../deploy-manage/tools/snapshot-and-restore.md#feature-state) need to be restored we’ll need to specify them using the `feature_states` field and the indices that belong to the feature states we restore must not be specified under `indices`. The [Health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report) returns both the `indices` and `feature_states` that need to be restored for the restore from snapshot diagnosis. e.g.:
    ::::


    ```console
    POST _snapshot/my_repository/snapshot-20200617/_restore
    {
      "feature_states": [ "geoip" ],
      "indices": "kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001",
      "include_aliases": true
    }
    ```

7. Finally we can verify that the indices health is now `green` via the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices).

    ```console
    GET _cat/indices?v&index=.ds-my-data-stream-2022.06.17-000001,kibana_sample_data_flightsh=index,status,health
    ```

    The response will look like this:

    ```console-result
    index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   green
    kibana_sample_data_flights           open   green
    ```

    As we can see above the indices are `green` and open. The issue is resolved.


For more guidance on creating and restoring snapshots see [this guide](../../deploy-manage/tools/snapshot-and-restore.md).
::::::

:::::::
