---
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/upgrade.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elasticsearch.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-kibana.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrade-deployment.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-upgrade-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-upgrade-deployment.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrade-elastic-stack-for-elastic-cloud.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elastic-stack-on-prem.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-upgrading-stack.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-upgrade.html
---


% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/kibana/kibana/upgrade.md
% - [ ] ./raw-migrated-files/kibana/kibana/upgrade-migrations-rolling-back.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-elasticsearch.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-kibana.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-upgrade-deployment.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-upgrade-deployment.md
%      Notes: redirect only
% - [ ] ./raw-migrated-files/cloud/cloud/ec-upgrade-deployment.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrade-elastic-stack-for-elastic-cloud.md
% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack-on-prem.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-upgrading-stack.md
%      Notes: upgrade explanations

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$preventing-migration-failures$$$

$$$prepare-to-upgrade$$$

$$$k8s-nodesets$$$

$$$k8s-orchestration-limitations$$$

$$$k8s-statefulsets$$$

$$$k8s-upgrade-patterns$$$

$$$k8s-upgrading$$$

$$$prepare-to-upgrade-8x$$$

$$$rolling-upgrades$$$

$$$upgrading-reindex$$$

% * [/raw-migrated-files/kibana/kibana/upgrade.md](/raw-migrated-files/kibana/kibana/upgrade.md)
% * [/raw-migrated-files/kibana/kibana/upgrade-migrations-rolling-back.md](/raw-migrated-files/kibana/kibana/upgrade-migrations-rolling-back.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-elasticsearch.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-elasticsearch.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-kibana.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-kibana.md)
% * [/raw-migrated-files/cloud/cloud-enterprise/ece-upgrade-deployment.md](/raw-migrated-files/cloud/cloud-enterprise/ece-upgrade-deployment.md)
% * [/raw-migrated-files/cloud/cloud-heroku/ech-upgrade-deployment.md](/raw-migrated-files/cloud/cloud-heroku/ech-upgrade-deployment.md)
% * [/raw-migrated-files/cloud/cloud/ec-upgrade-deployment.md](/raw-migrated-files/cloud/cloud/ec-upgrade-deployment.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrade-elastic-stack-for-elastic-cloud.md](/raw-migrated-files/stack-docs/elastic-stack/upgrade-elastic-stack-for-elastic-cloud.md)
% * [/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack-on-prem.md](/raw-migrated-files/stack-docs/elastic-stack/upgrading-elastic-stack-on-prem.md)
% * [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-upgrading-stack.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-upgrading-stack.md)
% * [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-orchestration.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-orchestration.md)

# Upgrade your deployment or cluster [upgrade-deployment-cluster]

When upgrading an existing cluster, you perform a minor or major upgrade. For example, a minor upgrade takes you from version 9.0.0 to 9.1.0, while a major upgrade takes you from version 8.0.0 to 9.0.0.

Upgrade procedures depend on whether you installed Elastic components using Elastic-managed or self-managed infrastructure.

If you’re using Elastic-managed infrastructure, use the following options:

* [Upgrade on {{ech}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md)
* Upgrade on [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), which is automatically performed by Elastic and requires no user management

If you’re using self-managed infrastructure - either on-prem or public cloud - use the following options:

* [Upgrade the {{stack}}](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md)
* [Upgrade on {{ece}} (ECE)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md)
* [Upgrade on {{eck}} (ECK)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)

## Prepare to upgrade [prepare-to-upgrade]

Before you upgrade, review and complete the necessary preparation steps, which vary by version. 

:::{important}
Upgrading from a release candidate build, such as 9.0.0-rc1, is unsupported. Use pre-releases only for testing in a temporary environment.
:::

## Prepare to upgrade from 8.x [prepare-upgrade-from-8.x]

To upgrade from 8.17.0 or earlier to 9.0.0, you must first upgrade to the latest 8.18 patch release. This enables you to use the [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md) to identify and resolve issues, reindex indices created before 8.0.0, and perform a rolling upgrade. Upgrading to the latest 8.18 patch release is required even if you choose a full {{es}} cluster restart. If you're using 7.x and earlier, you may need to complete multiple upgrades or perform a full-cluster restart to reach the latest 8.18 patch release before upgrading to 9.0.0.

Alternatively, you can create a 9.0 deployment and reindex from remote. For more information, refer to [Reindex to upgrade](#reindex-to-upgrade).

:::{note}
For flexible upgrade scheduling, 8.18.0 {{beats}} and {{ls}} are compatible with 9.0.0 {{es}}. 
By default, 8.x {{es}} clients are compatible with 9.0.0 and use [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) to maintain compatibility with the 9.0.0 {{es}} server. 
:::

Review the best practices to upgrade your deployments.

1. Run the [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md), which identifies deprecated settings, helps resolve issues, and reindexes data streams and indices created in 8.0.0 and earlier.

    :::{note}
     Depending on your setup, reindexing can change your indices, and you may need to update alerts, transforms, or other code targeting the old index.
    :::

2. Before you change configurations or reindex, ensure you have a current [snapshot](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md). 

    :::{tip}
    Tip: In 8.3.0 and later, snapshots are generally available as simple archives. Use the [archive functionality](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) to search snapshots from 5.0.0 and later, without needing an old {{es}} cluster. This ensures that your {{es}} data remains accessible after upgrades, without requiring a reindex process.
    :::

    To successfully upgrade, resolve all critical issues. If you make additional changes, create a snapshot to back up your data.

3. To identify if your applications use unsupported features or behave differently in 9.0.0, review the deprecation logs in the Upgrade Assistant. 

4. Major version upgrades can include breaking changes that require additional steps to ensure your applications function as expected. Review the breaking changes for each product you use to learn more about potential impacts on your application. Ensure you test with the new version before upgrading existing deployments.

5. To ensure your clients continue to operate as expected after the upgrade, make the recommended changes. 

    :::{note}
       As a temporary solution, use the 8.x syntax to submit requests to 9.0.0 with REST API compatibility mode. While this allows you to submit requests using the old syntax, it doesn’t guarantee the same behavior. REST API compatibility should serve as a bridge during the upgrade, not a long-term solution. For more details on how to effectively use REST API compatibility during an upgrade, refer to [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md). 
    :::

6. If you use {{es}} plugins, ensure each plugin is compatible with the {{es}} version you're upgrading.

7. Before upgrading your production deployment, we recommend creating a 9.0.0 test deployment and testing the upgrade in an isolated environment. Ensure the test and production environments use the same settings.

    :::{important}
    After you upgrade, you cannot downgrade {{es}} nodes. If you can't complete the upgrade process, you must [restore from the snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).
    :::

8. If you use a separate [monitoring cluster](/deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md), upgrade the monitoring cluster before the production cluster. The monitoring cluster and the clusters being monitored should be running the same version of the {{stack}}. Monitoring clusters are unable to monitor production clusters running newer versions of the {{stack}}. If necessary, the monitoring cluster can monitor production clusters running the latest release of the previous major version.

    :::{note}
    If you use {{ccs}}, 9.0.0 and later can search only remote clusters running the previous minor version, the same version, or a newer minor version in the same major version. For more information, refer to [Cross-cluster search](../../solutions/search/cross-cluster-search.md).

    If you use {{ccr}}, a cluster that contains follower indices must run the same or newer (compatible) version as the remote cluster. For more information and to view the version compatibility matrix, refer to [Cross cluster replication](/deploy-manage/tools/cross-cluster-replication.md). To view your remote clusters in {{kib}}, go to **Stack Management > Remote Clusters**.
    ::::

9. To reduce overhead on the cluster during the upgrade, close {{ml}} jobs. Although {{ml}} jobs can run during a rolling upgrade, doing so increases the cluster workload.

10. If you have `.ml-anomalies-*`anomaly detection result indices created in {{es}} 7.x, reindex, mark as read-only, or delete them before you upgrade to 9.0.0. For more information, refer to [Migrate anomaly detection results](#anomaly-migration). 

11. If you have transform destination indices created in {{es}} 7.x, reset, reindex, or delete them before you upgrade to 9.0.0. For more information, refer to [Migrate transform destination indices](#transform-migration). 


## Reindex to upgrade [reindex-to-upgrade]

Optionally create a 9.0.0 deployment and reindex from remote:

1. Provision an additional deployment running 9.0.0.
2. To reindex your data into the new {{es}} cluster, use the [reindex documents API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-reindex) and temporarily send new index requests to both clusters.
3. Verify the new cluster performs as expected, fix any problems, and then permanently swap in the new cluster.
4. Delete the old deployment. On {ecloud}, you are billed only for the time the new deployment runs in parallel with your old deployment. Usage is billed on an hourly basis.


## Migrate anomaly detection results [anomaly-migration]

Reindex, mark as read-only, or delete the `.ml-anomalies-*` {{anomaly-detect}} result indices created in {{es}} 7.x.

**Reindex**: While {{anomaly-detect}} results are being reindexed, jobs continue to run and process new data. You are unable to delete an {{anomaly-job}} that stores results in the index until the reindexing is complete.

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
For an index with less than 10GB that contains results from multiple jobs that are still required, we recommend reindexing into a new format using UI. You can use the [Get index information API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices-1) to obtain the size of an index:

```
GET _cat/indices/.ml-anomalies-custom-example?v&h=index,store.size
```

The reindexing can be initiated in the {{kib}} Upgrade Assistant.

If an index size is greater than 10 GB, it is recommended to use the Reindex API. Reindexing consists of the following steps:

1. Set the original index to read-only.

```
PUT .ml-anomalies-custom-example/_block/read_only
```

2. Create a new index from the legacy index.

```
POST _create_from/.ml-anomalies-custom-example/.reindexed-v9-ml-anomalies-custom-example
```

3. Reindex documents. To accelerate the reindexing process, it is recommended that the number of replicas be set to `0` before the reindexing and then set back to the original number once it is completed.

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

    2. Set the number of replicas to `0.`

    ```json
    PUT /.reindexed-v9-ml-anomalies-custom-example/_settings
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

    4. Set the number of replicas to the original number when the reindexing is finished.

    ```json
    PUT /.reindexed-v9-ml-anomalies-custom-example/_settings
    {
      "index": {
        "number_of_replicas": "<original_number_of_replicas>"
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

5. Now you can reassign the aliases to the new index and delete the original index in one step. Note that when adding the new index to the aliases, you must use the same `filter` and `is_hidden` parameters as for the original index.

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
=======


