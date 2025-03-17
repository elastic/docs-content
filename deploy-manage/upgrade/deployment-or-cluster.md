---
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/upgrade.html
  - https://www.elastic.co/guide/en/kibana/current/upgrade-migrations-rolling-back.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elasticsearch.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-kibana.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrade-deployment.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-upgrade-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-upgrade-deployment.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrade-elastic-stack-for-elastic-cloud.html
  - https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elastic-stack-on-prem.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-upgrading-stack.html
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

**This page is a work in progress.** The documentation team is working to combine content pulled from the following pages:

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

When upgrading the version of an existing cluster, you perform either a minor or major upgrade. The difference is that a minor upgrade takes you from version 9.0 to 9.1, for example, while a major upgrade takes you from version 8 to 9. 

The procedures you follow to upgrade depend on whether you’ve installed Elastic components using Elastic-managed infrastructure or self-managed infrastructure.

If you’re running Elastic-managed infrastructure, your options are to:

* [Upgrade on {{ech}}](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md)
* Upgrade on {{serverless-full}} (updates are automatic and require no user management)

If you’re running your own self-managed infrastructure — either on-prem or on public cloud — your options are to:

* [Upgrade the {{stack}}](/deploy-manage/upgrade/deployment-or-cluster/self-managed.md) (upgrade each component individually)
* [Upgrade on {{ece}} (ECE)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md)
* [Upgrade on {{eck}} (ECK)](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md)

## Prepare to upgrade [prepare-to-upgrade]

Before you upgrade Elastic, it's important to take some preparation steps. These steps vary based on your current version. 

:::{important}
Upgrading from a release candidate build, such as 9.0.0-rc1 or 9.0.0-rc2, is not supported. Pre-releases should only be used for testing in a temporary environment.
:::

## Prepare to upgrade from 8.x [prepare-upgrade-from-8.x]

To upgrade to 9.0 from 8.17 or earlier, you must first upgrade to the latest patch version of 8.18. This enables you to use the [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md) to identify and resolve issues, reindex indices created before 8.0, and then perform a rolling upgrade. Upgrading to 8.18 before upgrading to 9.x is required even if you opt to do a full-cluster restart of your {{es}} cluster. If you're running a pre-8.x version, you might need to perform multiple upgrades or a full-cluster restart to get to 8.18 to prepare to upgrade to 9.0.

Alternatively, you can create a new 9.0 deployment and reindex from remote. For more information, refer to [Reindex to upgrade](#reindex-to-upgrade).

:::{note}
{{beats}} and {{ls}} 8.18 are compatible with {{es}} 9.x to give you flexibility in scheduling the upgrade. {{es}} 8.x clients are also compatible with 9.x and use [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) by default to help ensure compatibility between 8.x clients and the 9.x {{es}} server. 
:::

With the exception of serverless, the following recommendations are best practices for all deployment methods.

1. Run the [Upgrade Assistant](prepare-to-upgrade/upgrade-assistant.md) to prepare for your upgrade from 8.18 to 9.0. The Upgrade Assistant identifies deprecated settings, and guides you through resolving issues, and reindexing data streams and indices created before 8.0. 

    :::{note}
    Please be aware that depending on your setup, if your indices change due to reindexing, you might need to change alerts, transforms, or other code that was targeting the old index.
    :::

2. Ensure you have a current [snapshot](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md) before making configuration changes or reindexing. 

    :::{tip}
    Tip: From version 8.3, snapshots are generally available as simple archives. Use the [archive functionality](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) to search snapshots as old as version 5.0 without the need of an old {{es}} cluster. This ensures that data you store in {{es}} doesn’t have an end of life and is still accessible when you upgrade, without requiring a reindex process.
    :::

    You must resolve all critical issues before proceeding with the upgrade. If you make any additional changes, take a new snapshot to back up your data. 

3. Review the deprecation logs from the Upgrade Assistant to determine if your applications are using features that are not supported or behave differently in 9.x. 

4. Major version upgrades can include breaking changes that require you to take additional steps to ensure that your applications behave as expected after the upgrade. Review all breaking changes for each product you use to review more information about changes that could affect your application. Make sure you test against the new version before upgrading existing deployments.

5. Make the recommended changes to ensure that your clients continue to operate as expected after the upgrade. 

    :::{note}
    As a temporary solution, you can submit requests to 9.x using the 8.x syntax with the REST API compatibility mode. While this enables you to submit requests that use the old syntax, it does not guarantee the same behavior. REST API compatibility should be a bridge to smooth out the upgrade process, not a long term strategy. For more information about how to best leverage REST API compatibility during an upgrade, refer to [REST API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md). 
    :::

6. If you use any {{es}} plugins, make sure there is a version of each plugin that is compatible with the {{es}} version you're upgrading to.

7. We recommend creating a 9.0 test deployment and test the upgrade in an isolated environment before upgrading your production deployment. Ensure that both your test and production environments have the same settings.

    :::{important}
    You cannot downgrade {{es}} nodes after upgrading. If you cannot complete the upgrade process, you will need to [restore from the snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).
    :::

8. If you use a separate [monitoring cluster](/deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md), you should upgrade the monitoring cluster before the production cluster. In general, the monitoring cluster and the clusters being monitored should be running the same version of the {{stack}}. A monitoring cluster cannot monitor production clusters running newer versions of the {{stack}}. If necessary, the monitoring cluster can monitor production clusters running the latest release of the previous major version.

    :::{note}
    If you use {{ccs}}, note that 9.0+ can only search remote clusters running the  previous minor version, the same version, or a newer minor version in the same major version. For more information, refer to [Cross-cluster search](../../solutions/search/cross-cluster-search.md).

    If you use {{ccr}}, a cluster that contains follower indices must run the same or newer (compatible) version as the remote cluster. For more information and to view the version compatibility matrix, refer to [Cross cluster replication](/deploy-manage/tools/cross-cluster-replication.md). You can view your remote clusters from **Stack Management > Remote Clusters**.
    ::::

9. Consider closing {{ml}} jobs before you start the upgrade process. While {{ml}} jobs can continue to run during a rolling upgrade, it increases the overhead on the cluster during the upgrade process.

10. If you have any anomaly detection result indices `.ml-anomalies-*` that were created in {{es}} 7.x, they must be reindexed, marked as read-only, or deleted before upgrading to 9.x. To learn how to do this, refer to [Anomaly detection results migration](#anomaly-migration). 


11. If you have any transform destination indices that were created in {{es}} 7.x, they must be reset, reindexed, or deleted before upgrading to 9.x. To learn how to do this, refer to [Transform destination indices migration](#transform-migration). 


## Reindex to upgrade (optional) [reindex-to-upgrade]

To create a new 9.0 deployment and reindex from remote:

1. Provision an additional deployment running 9.0.
2. Reindex your data into the new {{es}} cluster using the [reindex documents API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-reindex) and temporarily send new index requests to both clusters.
3. Verify that the new cluster performs as expected, fix any problems, and then permanently swap in the new cluster.
4. Delete the old deployment. On {ecloud}, you are billed only for the time that the new deployment runs in parallel with your old deployment. Usage is billed on an hourly basis.


## Anomaly detection results migration [anomaly-migration]

The {{anomaly-detect}} result indices `.ml-anomalies-*` created in {{es}} 7.x must be either reindexed, marked read-only, or deleted before upgrading to 9.x.

**Reindexing**: While {{anomaly-detect}} results are being reindexed, jobs continue to run and process new data. However, you cannot completely delete an {{anomaly-job}} that stores results in this index until the reindexing is complete.

**Marking indices as read-only**: This is useful for large indexes that contain the results of only one or a few {{anomaly-jobs}}. If you delete these jobs later, you will not be able to create a new job with the same name.

**Deleting**: Delete jobs that are no longer needed in the {{ml-app}} app in {{kib}}. The result index is deleted when all jobs that store results in it have been deleted.

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

## Transform destination indices migration [transform-migration]
=======

% EEDUGON note: when working on this document, or in the ECK upgrade documentation we should include a link to [nodes orchestration](../deploy/cloud-on-k8s/nodes-orchestration.md) as reference to learn the details on how ECK orchestates / manages the upgrade of the individual instances.

