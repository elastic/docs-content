# Prepare to upgrade

% What needs to be done: Write from scratch

% Scope notes: Prerequisites and requirements

⚠️ **This page is a work in progress.** ⚠️


## Anomaly detection results migration

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