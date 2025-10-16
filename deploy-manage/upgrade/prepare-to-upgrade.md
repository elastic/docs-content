---
navigation_title: Preparation steps
applies_to:
  stack: ga
products:
  - id: kibana
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: elasticsearch
---
# Prepare to upgrade

This document describes the preparation steps for upgrading {{es}}, which vary depending on the type of upgrade. These steps follow the [upgrade planning](./plan-upgrade.md) phase, and should be completed before proceeding to [upgrade your deployment or cluster](./deployment-or-cluster.md).

When upgrading an existing cluster, you perform a major, minor, or patch upgrade. A minor upgrade, for example, can take you from version 9.0.2 to 9.1.x; a major upgrade from 8.19.x to {{version.stack}}; and a patch upgrade from 9.0.1 to 9.0.4.

:::{important}
Upgrading from a release candidate build, such as 9.0.0-rc1, is unsupported. Use pre-releases only for testing in a temporary environment.
:::

## Common preparation steps for all upgrades

The following steps and recommendations are common to all types of upgrades, regardless if you are upgrading from 8.x (major upgrade), or if you are already running a 9.x version.

:::::{stepper}

::::{step} Review breaking changes
Although breaking changes typically affect [major upgrades](#prepare-upgrade-from-8.x), they can also occur in minor or patch releases. Review the [breaking changes](../../release-notes/index.md) for each product you use to learn more about potential impacts on your applications. Ensure you test with the new version before upgrading production deployments.

If you are affected by a breaking change, you have to take action before upgrading. This can include updating your code, change configuration settings, or other steps.
::::

::::{step} Verify plugin compatibility
If you use [{{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md), ensure each plugin is compatible with the {{es}} version you're upgrading to.
::::

::::{step} Create a snapshot for backup
Take a [snapshot](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md) of your cluster before starting the upgrade. This provides a recovery point in case the upgrade needs to be rolled back.

:::{important}
After you start to upgrade your {{es}} cluster, you cannot downgrade any of its nodes. If you can't complete the upgrade process, you must [restore from a snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) which was taken before starting the upgrade.
:::
::::

::::{step} Test in a non-production environment
Before upgrading your production deployment, test the upgrade using a non-production environment. Make sure the test environment mirrors production as closely as possible, including configuration and client interactions. Refer to [](./plan-upgrade.md#test-in-a-non-production-environment) for more details and recommendations.

:::{note}
The upgraded version of {{es}} may interact with its environment in different ways from the version you are currently running. It is possible that your environment behaves incorrectly in a way that does not matter to the version of {{es}} that you are currently running, but which does matter to the upgraded version. In this case, the upgraded version will not work correctly until you address the incorrect behavior in your environment.
:::

::::

::::{step} Upgrade your monitoring cluster first
If you use a separate [monitoring cluster](/deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md), upgrade the monitoring cluster before the production cluster.

The monitoring cluster should be running the same version, or a newer one, than the clusters being monitored. It cannot monitor clusters running a newer version of the {{stack}}. If necessary, the monitoring cluster can monitor clusters running the latest release of the previous major version.
::::

::::{step} Upgrade remote clusters first
If you use {{ccs}}, versions 9.0.0 and later can search only remote clusters running the previous minor version, the same version, or a newer minor version in the same major version. For more information, refer to [{{ccs-cap}}](../../solutions/search/cross-cluster-search.md).

If you use {{ccr}}, a cluster that contains follower indices must run the same or newer (compatible) version as the remote cluster. For more information and to view the version compatibility matrix, refer to [{{ccr-cap}}](/deploy-manage/tools/cross-cluster-replication.md).

To view your remote clusters in {{kib}}, Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
::::

::::{step} (Optional) Close machine learning jobs
To reduce overhead on the cluster during the upgrade, close [{{ml}} jobs](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) before starting the upgrade, and open them after the upgrade is complete. Although {{ml}} jobs can run during a rolling upgrade, doing so increases the cluster workload.
::::

:::::

If you are preparing a minor or patch upgrade, you're ready to [upgrade your deployment or cluster](./deployment-or-cluster.md). If you are preparing a major upgrade, continue with the [preparations to upgrade from 8.x](#prepare-upgrade-from-8.x).

## Additional preparation steps to upgrade from 8.x [prepare-upgrade-from-8.x]

Major upgrades require additional planning and preparation, as they often introduce a significant number of breaking changes and require additional steps to ensure a smooth transition.

To assist with this process, use the [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md), which helps detect deprecated settings, highlights upgrade blockers, and guides you through the required actions.

Follow these steps to prepare for a successful major upgrade from 8.x to 9.x:

:::::{stepper}

::::{step} Upgrade to the latest 8.19 patch release

To perform a major upgrade from 8.x to 9.x of {{es}}, you must first upgrade to 8.19.x. This allows you to use the [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md) to identify and resolve issues, reindex indices created before 8.0.0, and prepare the cluster for the actual upgrade. Upgrading to 8.19 is required regardless of whether you perform a rolling upgrade or a full cluster restart to upgrade.

:::{note}
Because 8.18.0 and 9.0.0 were released simultaneously, upgrading from 8.18.x to 9.0.x is supported, as long as the versions comply with the supported [upgrade paths](../upgrade.md#upgrade-paths). However, upgrading to 9.1.0 or later requires starting from 8.19.x.

If you're upgrading to the current {{version.stack}} release from an earlier 8.x version, first upgrade to the latest available 8.19 release.
:::

If you are already running an 8.19.x version, it's also recommended to upgrade to the latest 8.19 patch release before upgrading to 9.x. This ensures that the latest version of the upgrade assistant is used, and any bug fixes that could have implications for the upgrade are applied.

If you're using 7.x and earlier, you may need to complete multiple upgrades to reach the latest 8.19 patch release before upgrading to 9.x. As an alternative method to upgrading the cluster, you can create a new 9.x deployment and reindex from the original cluster. For more information, refer to [Reindex to upgrade](#reindex-to-upgrade).

:::{note}
For flexible upgrade scheduling, 8.19.x {{agent}}, {{beats}} and {{ls}} are compatible with all 9.x versions of {{es}}.

By default, 8.x {{es}} clients are compatible with 9.x and use [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) to maintain compatibility with the 9.x {{es}} server.
:::
::::

::::{step} Run the Upgrade Assistant

The [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md) identifies deprecated settings in your configuration and guides you through resolving issues that could prevent a successful upgrade. The Upgrade Assistant also helps resolve issues with older indices created before version 8.0.0, providing the option to reindex older indices or mark them as read-only. To prevent upgrade failures, we strongly recommend you **do not** skip this step.

:::{note}
  Depending on your setup, reindexing can change your indices, and you may need to update alerts, transforms, or other code targeting the old index.
:::

Considerations when using the upgrade assistant:

* For a successful upgrade, **resolve all critical issues reported by the assistant**. {{es}} nodes will fail to start if incompatible indices are present.

* Before you apply configuration changes or reindex, ensure you have a current [snapshot](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md).

* Indices created in 7.x or earlier must be reindexed, deleted, or [archived](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) (marked as read-only) before upgrading to 9.x.

  :::{tip}
  In Elasticsearch 9.x, you can also use the [archive functionality](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) to access snapshots of 7.x or earlier indices, without needing to reindex or run an older cluster. This provides a convenient option to retain historical data in case you choose to delete those indices and keep them only in existing snapshots.
  :::

* Review the deprecation logs from the Upgrade Assistant to determine if your applications are using features that are not supported or behave differently in 9.x. See the [breaking changes](elasticsearch://release-notes/breaking-changes.md) for more information about changes in 9.x that could affect your application.

  :::{note}
  Make sure you check the breaking changes for each 9.x release up to your target release.
  :::

* Make the recommended changes to ensure your clients continue operating as expected after the upgrade.

  :::{note}
  As a temporary solution, use the 8.x syntax to submit requests to 9.x with REST API compatibility mode. While this allows you to submit requests using the old syntax, it doesn’t guarantee the same behavior. REST API compatibility should serve as a bridge during the upgrade, not a long-term solution. For more details on how to effectively use REST API compatibility during an upgrade, refer to [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md).
  :::
::::

::::{step} Manage CCR follower data streams
If you have {{ccr-cap}} (CCR) data streams, and your indices require reindexing, refer to [Upgrade uni-directional {{ccr}} clusters with followed data streams](#upgrade-ccr-data-streams) for specific instructions.
::::

::::{step} Manage old machine learning indices
If you have `.ml-anomalies-*` anomaly detection result indices created in {{es}} 7.x, reindex them, mark them as read-only, or delete them before you upgrade to 9.x. For more information, refer to [Migrate anomaly detection results](#anomaly-migration).
::::

::::{step} Manage old transform indices
If you have transform destination indices created in {{es}} 7.x, reset, reindex, or delete them before you upgrade to 9.x. For more information, refer to [Migrate transform destination indices](#transform-migration).
::::

:::::

After completing all the preparation steps, you're ready to [upgrade your deployment or cluster](./deployment-or-cluster.md).

## Upgrade uni-directional {{ccr}} clusters with followed data streams [upgrade-ccr-data-streams]

When moving to a new major version of {{es}}, you must perform specific actions to ensure that indices — including those that back a data stream — are compatible with the latest Lucene version. With a {{ccr-init}}-enabled cluster, consider whether you want to keep your older data writable or read-only to ensure you make changes to the cluster in the correct order.

:::{note}
{{ccr-init}}-replicated data streams only allow writing to the most recent backing index, as ILM automatically injects an unfollow event after every rollover. Therefore, you can't reindex {{ccr-init}}-followed data streams since older backing indices are no longer replicated by {{ccr-init}}.
:::

### Migrate read-only historical data

If you want to keep your older data as read-only:

1. Issue a rollover for all replicated data streams on the follower cluster to ensure the write index is compatible with the version you're upgrading to.
2. Run the Upgrade Assistant on the {{ccr-init}} follower cluster and resolve any data stream deprecation notices, selecting the option to not reindex and allow the backing indices to become read-only after upgrading.
3. Upgrade the {{ccr-init}} follower cluster to the appropriate version. Ensure you take a snapshot before starting the upgrade.
4. Run the Upgrade Assistant on the {{ccr-init}} leader cluster and repeat the same steps as the follower cluster, opting not to reindex.
5. Upgrade the leader cluster and ensure {{ccr-init}} replication is healthy.

### Migrate read-write historical data

If you need to write directly to non-write backing indices of data streams in a {{ccr-init}}-replicated cluster pair:

1. Before upgrading, remove the data stream and all follower indices from the {{ccr-init}} follower.
2. Run the Upgrade Assistant and select the “Reindex” option.
3. Once the reindexing is complete and the leader cluster is upgraded, re-add the newly reindexed backing indexes as follower indices on the {{ccr-init}} follower.


## Migrate anomaly detection results [anomaly-migration]

Reindex, mark as read-only, or delete the `.ml-anomalies-*` {{anomaly-detect}} result indices created in {{es}} 7.x.

**Reindex**: While {{anomaly-detect}} results are being reindexed, jobs continue to run and process new data. You cannot delete an {{anomaly-job}} that stores results in the index until the reindexing is complete.

**Mark indices as read-only**: This is useful for large indexes that contain the results of one or two {{anomaly-jobs}}. If you delete these jobs later, you cannot create a new job with the same name.

**Delete**: Delete jobs that are no longer needed in the {{ml-app}} app in {{kib}}. The result index is deleted when all jobs that store results in it have been deleted.

:::{dropdown} Which indices require attention?
To identify indices that require action, use the [Deprecation info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-migration-deprecations-1):

```
GET /.ml-anomalies-*/_migration/deprecations
```

The response contains the list of critical deprecation warnings in the `index_settings` section:

```json
  "index_settings": {
    ".ml-anomalies-shared": [
      {
        "level": "critical",
        "message": "Index created before 8.0",
        "url": "https://ela.st/es-deprecation-8-reindex",
        "details": "This index was created with version 7.8.23 and is not compatible with 9.0. Reindex or remove the index before upgrading.",
        "resolve_during_rolling_upgrade": false
      }
    ]
  }
```
:::

:::{dropdown} Reindexing anomaly result indices
If an index size is less than 10 GB and contains results from multiple jobs that are still required, we recommend reindexing into a new format using the UI. You can use the [Get index information API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices-1) to obtain the size of an index:

```
GET _cat/indices/.ml-anomalies-custom-example?v&h=index,store.size
```

Use the Upgrade Assistant to initiate reindexing.

If an index size is greater than 10 GB, we recommend using the Reindex API. Reindexing consists of the following steps:

1. Set the original index to read-only.

```
PUT .ml-anomalies-custom-example/_block/read_only
```

2. Create a new index from the legacy index.

```
POST _create_from/.ml-anomalies-custom-example/.reindexed-v9-ml-anomalies-custom-example
```

3. Reindex documents. To accelerate the reindexing process, we recommend setting the number of replicas to `0` before reindexing, then set it back to the original number once completed.

    1. Get the number of replicas.

    ```
    GET /.reindexed-v9-ml-anomalies-custom-example/_settings
    ```

    Note the number of replicas in the response. For example:

    ```json
    {
      ".reindexed-v9-ml-anomalies-custom-example": {
        "settings": {
          "index": {
            "number_of_replicas": "1",
            "number_of_shards": "1"
          }
        }
      }
    }
    ```

    2. Set the number of replicas to `0`. You must also set the `auto_expand_replicas` parameter to `false` to change the number of replicas:

    ```json
    PUT /.reindexed-v9-ml-anomalies-custom-example/_settings
    {
      "index": {
        "auto_expand_replicas": false,
        "number_of_replicas": 0
      }
    }
    ```

    3. Start the reindexing process in asynchronous mode.

    ```json
    POST _reindex?wait_for_completion=false
    {
      "source": {
        "index": ".ml-anomalies-custom-example"
      },
      "dest": {
        "index": ".reindexed-v9-ml-anomalies-custom-example"
      }
    }
    ```

    The response will contain a `task_id`. You can check when the task is completed using the following command:

    ```
    GET _tasks/<task_id>
    ```

    4. Set the number of replicas to the original number when the reindexing is finished. Optionally, you can set the `auto_expand_replicas` parameter back to its default value (`0-1`) to allow the number of replicas to be automatically adjusted based on the number of data nodes in the cluster.

    ```json
    PUT /.reindexed-v9-ml-anomalies-custom-example/_settings
    {
      "index": {
        "number_of_replicas": "<original_number_of_replicas>",
        "auto_expand_replicas": "0-1"
      }
    }
    ```

4. Get the aliases the original index is pointing to.

```
GET .ml-anomalies-custom-example/_alias
```

The response may contain multiple aliases if the results of multiple jobs are stored in the same index.

```json
{
  ".ml-anomalies-custom-example": {
    "aliases": {
      ".ml-anomalies-example1": {
        "filter": {
          "term": {
            "job_id": {
              "value": "example1"
            }
          }
        },
        "is_hidden": true
      },
      ".ml-anomalies-example2": {
        "filter": {
          "term": {
            "job_id": {
              "value": "example2"
            }
          }
        },
        "is_hidden": true
      }
    }
  }
}
```

5. Now you can reassign the aliases to the new index and delete the original index in one step. Note that when adding the new index to the aliases, you must use the same `filter` and `is_hidden` parameters as the original index.

```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": ".reindexed-v9-ml-anomalies-custom-example",
        "alias": ".ml-anomalies-example1",
        "filter": {
          "term": {
            "job_id": {
              "value": "example1"
            }
          }
        },
        "is_hidden": true
      }
    },
    {
      "add": {
        "index": ".reindexed-v9-ml-anomalies-custom-example",
        "alias": ".ml-anomalies-example2",
        "filter": {
          "term": {
            "job_id": {
              "value": "example2"
            }
          }
        },
        "is_hidden": true
      }
    },
    {
      "remove": {
        "index": ".ml-anomalies-custom-example",
        "aliases": ".ml-anomalies-*"
      }
    },
    {
      "remove_index": {
        "index": ".ml-anomalies-custom-example"
      }
    },
    {
      "add": {
        "index": ".reindexed-v9-ml-anomalies-custom-example",
        "alias": ".ml-anomalies-custom-example",
        "is_hidden": true
      }
    }
  ]
}
```
:::


:::{dropdown} Marking anomaly result indices as read-only
Legacy indices created in {{es}} 7.x can be made read-only and supported in {{es}} 9.x. Making an index with a large amount of historical results read-only allows for a quick migration to the next major release, since you don’t have to wait for the data to be reindexed into the new format. However, it has the limitation that even after deleting an {{anomaly-job}}, the historical results associated with this job are not completely deleted. Therefore, the system will prevent you from creating a new job with the same name.

Make sure to upgrade or delete all deprecated model snapshots using the [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md) **before** marking the index `.ml-anomalies-shared` as read-only. 

To set the index as read-only, add the write block to the index:

```
PUT .ml-anomalies-custom-example/_block/write
```

Indices created in {{es}} 7.x that have a write block will not raise a critical deprecation warning.
:::

:::{dropdown} Deleting anomaly result indices
If an index contains results of the jobs that are no longer required. To list all jobs that stored results in an index, use the terms aggregation:

```json
GET .ml-anomalies-custom-example/_search
{
  "size": 0,
  "aggs": {
    "job_ids": {
      "terms": {
        "field": "job_id",
        "size": 100
      }
    }
  }
}
```

The jobs can be deleted in the UI. After the last job is deleted, the index will be deleted as well.
:::

## Migrate transform destination indices [transform-migration]

The transform destination indices created in {{es}} 7.x must be either reset, reindexed, or deleted before upgrading to 9.x.

**Resetting**: You can reset the transform to delete all state, checkpoints, and the destination index (if it was created by the transform). The next time you start the transform, it will reprocess all data from the source index, creating a new destination index in {{es}} 8.x compatible with 9.x. However, if data had been deleted from the source index, you will lose all previously computed results that had been stored in the destination index.

**Reindexing**: You can reindex the destination index and then update the transform to write to the new destination index. This is useful if there are results that you want to retain that may not exist in the source index. To prevent the transform and reindex tasks from conflicting with one another, you can either pause the transform while the reindex runs, or write to the new destination index while the reindex backfills old results.

**Deleting**: You can delete any transform that's no longer being used. Once the transform is deleted, you can delete the destination index or make it read-only.

:::{dropdown} Which indices require attention?
To identify indices that require action, use the [Deprecation info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-migration-deprecations-1):

```json
GET /_migration/deprecations
```

The response contains the list of critical deprecation warnings in the `index_settings` section:

```json
"index_settings": {
    "my-destination-index": [
      {
        "level": "critical",
        "message": "One or more Transforms write to this index with a compatibility version < 9.0",
        "url": "https://www.elastic.co/guide/en/elasticsearch/reference/master/migrating-9.0.html#breaking_90_transform_destination_index",
        "details": "Transforms [my-transform] write to this index with version [7.8.23].",
        "resolve_during_rolling_upgrade": false
      }
    ]
  }
```
:::

:::{dropdown} Resetting the transform
If the index was created by the transform, you can use the [Transform Reset API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-reset-transform) to delete the destination index and recreate it the next time the transform runs.

If the index was not created by the transform and you still want to reset it, you can manually delete and recreate the index, then call the Reset API.

```json
POST _transform/my-transform/_reset
```
:::

:::{dropdown} Reindexing the transform’s destination index while the transform is paused
When the Upgrade Assistant reindexes the documents, {{kib}} will put a write block on the old destination index, copy the results to a new index, delete the old index, and create an alias to the new index. During this time, the transform will pause and wait for the destination to become writable again. If you do not want the transform to pause, continue to reindexing the transform’s destination index while the transform is running.

If an index size is less than 10 GB, we recommend using the Upgrade Assistant to automatically migrate the index. You can use the [Get index information API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices-1) to obtain the size of an index:

```
GET _cat/indices/.transform-destination-example?v&h=index,store.size
```

Use the Upgrade Assistant to initiate reindexing.

If an index size is greater than 10 GB, we recommend using the Reindex API. Reindexing consists of the following steps:

1. Set the original index to read-only.

```
PUT .transform-destination-example/_block/read_only
```

2. Create a new index from the legacy index.

```
POST _create_from/.transform-destination-example/.reindexed-v9-transform-destination-example
```

3. Reindex documents. To accelerate the reindexing process, we recommend setting the number of replicas to 0 before reindexing, then set it back to the original number once completed.

    1. Get the number of replicas.

    ```
    GET /.reindexed-v9-transform-destination-example/_settings
    ```

    Note the number of replicas in the response. For example:

    ```json
    {
      ".reindexed-v9-transform-destination-example": {
        "settings": {
          "index": {
            "number_of_replicas": "1",
            "number_of_shards": "1"
          }
        }
      }
    }
    ```

    2. Set the number of replicas to `0.`

    ```json
    PUT /.reindexed-v9-transform-destination-example/_settings
    {
      "index": {
        "number_of_replicas": 0
      }
    }
    ```

    3. Start the reindexing process in asynchronous mode.

    ```json
    POST _reindex?wait_for_completion=false
    {
      "source": {
        "index": ".transform-destination-example"
      },
      "dest": {
        "index": ".reindexed-v9-transform-destination-example"
      }
    }
    ```

    The response will contain a `task_id`. You can check when the task is completed using the following command:

    ```
    GET _tasks/<task_id>
    ```

    4. Set the number of replicas to the original number when the reindexing is finished.

    ```json
    PUT /.reindexed-v9-transform-destination-example/_settings
    {
      "index": {
        "number_of_replicas": "<original_number_of_replicas>"
      }
    }
    ```

4. Get the aliases the original index is pointing to.

```
GET .transform-destination-example/_alias
```

The response may contain multiple aliases if the results of multiple jobs are stored in the same index.

```json
{
  ".transform-destination-example": {
    "aliases": {
      ".transform-destination-example1": {
        "filter": {
          "term": {
            "job_id": {
              "value": "example1"
            }
          }
        },
        "is_hidden": true
      },
      ".transform-destination-example2": {
        "filter": {
          "term": {
            "job_id": {
              "value": "example2"
            }
          }
        },
        "is_hidden": true
      }
    }
  }
}
```

5. Now you can reassign the aliases to the new index and delete the original index in one step. Note that when adding the new index to the aliases, you must use the same `filter` and `is_hidden` parameters as the original index.

```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": ".reindexed-v9-transform-destination-example",
        "alias": ".transform-destination-example1",
        "filter": {
          "term": {
            "job_id": {
              "value": "example1"
            }
          }
        },
        "is_hidden": true
      }
    },
    {
      "add": {
        "index": ".reindexed-v9-transform-destination-example",
        "alias": ".transform-destination-example2",
        "filter": {
          "term": {
            "job_id": {
              "value": "example2"
            }
          }
        },
        "is_hidden": true
      }
    },
    {
      "remove": {
        "index": ".transform-destination-example",
        "aliases": ".transform-destination-*"
      }
    },
    {
      "remove_index": {
        "index": ".transform-destination-example"
      }
    },
    {
      "add": {
        "index": ".reindexed-v9-transform-destination-example",
        "alias": ".transform-destination-example",
        "is_hidden": true
      }
    }
  ]
}
```
:::


:::{dropdown} Reindexing the transform’s destination index while the transform is running
If you want the transform and the reindex task to write documents to the new destination index at the same time:

1. Set the original index to read-only.

```
POST _create_from/my-destination-index/my-new-destination-index
```

2. Update the transform to write to the new destination index:

```
POST _transform/my-transform/_update
{
 "dest": {
   "index": "my-new-destination-index"
 }
}
```

3. Reindex documents. To accelerate the reindexing process, we recommend setting the number of replicas to 0 before reindexing, then set it back to the original number once completed.

    1. Get the number of replicas.

    ```
    GET /my-destination-index/_settings
    ```

    2. Note the number of replicas in the response. For example:

    ```json
    {
      "my-destination-index":: {
        "settings": {
          "index": {
            "number_of_replicas": "1",
            "number_of_shards": "1"
          }
        }
      }
    }
    ```

    3. Set the number of replicas to `0.`

    ```json
    PUT /my-destination-index/_settings
    {
      "index": {
        "number_of_replicas": 0
      }
    }
    ```

    4. Start the reindexing process in asynchronous mode. Set the `op_type` to `create` so the reindex does not overwrite work that the transform is doing.

    ```json
    POST _reindex
    {
      "conflicts": "proceed",
      "source": {
        "index": "my-destination-index"
      },
      "dest": {
        "index": "my-new-destination-index",
        "op_type": "create"
      }
    }
    ```

    The response will contain a `task_id`. You can check when the task is completed using the following command:

    ```
    GET _tasks/<task_id>
    ```

    5. Set the number of replicas to the original number when the reindexing is finished.

    ```json
    PUT /my-new-destination-index/_settings
    {
      "index": {
        "number_of_replicas": "<original_number_of_replicas>"
      }
    }
    ```

4. Get the aliases the original index is pointing to.

    ```json
    GET my-destination-index/_alias
    {
      "my-destination-index": {
        "aliases": {
          "my-destination-alias": {},
        }
      }
    }
    ```

5. Now you can reassign the aliases to the new index and delete the original index in one step. Note that when adding the new index to the aliases, you must use the same `filter` and `is_hidden` parameters as the original index.

    ```json
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "my-new-destination-index",
            "alias": "my-destination-alias"
          }
        },
        {
          "remove": {
            "index": "my-destination-index",
            "aliases": "my-destination-alias"
          }
        },
        {
          "remove_index": {
            "index": "my-destination-index"
          }
        }
      ]
    }
    ```

:::

:::{dropdown} Deleting the transform
You can use the [Transform Delete API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-delete-transform) to delete the transform and stop it from writing to the destination index.

```json
DELETE _transform/my-transform
```
If the destination index is no longer needed, it can be deleted with the transform.

```json
DELETE _transform/my-transform?delete_dest_index
```
:::

## Reindex to upgrade [reindex-to-upgrade]

If you are running a pre-8.x version, you might need to perform multiple upgrades before being able to upgrade to 9.x. As an alternative method to upgrading the cluster, you can create a new deployment in the target version and reindex from remote:

1. Provision an additional deployment running the desired version, such as {{version.stack}}.
2. To reindex your data into the new {{es}} cluster, use the [reindex documents API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-reindex) and temporarily send new indexing requests to both clusters.
3. Verify the new cluster performs as expected, fix any problems, and then permanently swap in the new cluster.
4. Delete the old deployment. On {{ecloud}}, you are billed for the time the new deployment runs in parallel with your old deployment. Usage is billed on an hourly basis.
