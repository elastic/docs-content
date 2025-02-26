---
navigation_title: Snapshot policy failures
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/repeated-snapshot-failures.html
---

# Fix repeated snapshot policy failures [repeated-snapshot-failures]

Repeated snapshot failures are usually an indicator of a problem with your deployment. Continuous failures of automated snapshots can leave a deployment without recovery options in cases of data loss or outages.

Elasticsearch keeps track of the number of repeated failures when executing automated snapshots. If an automated snapshot fails too many times without a successful execution, the health API will report a warning. The number of repeated failures before reporting a warning is controlled by the [`slm.health.failed_snapshot_warn_threshold`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/snapshot-restore-settings.md#slm-health-failed-snapshot-warn-threshold) setting.

In the event that an automated {{slm}} policy execution is experiencing repeated failures, follow these steps to get more information about the problem:

:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to check the status of failing {{slm}} policies we need to go to Kibana and retrieve the [Snapshot Lifecycle Policy information](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-lifecycle).

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

4. [Retrieve](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-lifecycle) the {{slm}} policy:

    ```console
    GET _slm/policy/<affected-policy-name>
    ```

    The response will look like this:

    ```console-result
    {
      "affected-policy-name": { <1>
        "version": 1,
        "modified_date": "2099-05-06T01:30:00.000Z",
        "modified_date_millis": 4081757400000,
        "policy" : {
          "schedule": "0 30 1 * * ?",
          "name": "<daily-snap-{now/d}>",
          "repository": "my_repository",
          "config": {
            "indices": ["data-*", "important"],
            "ignore_unavailable": false,
            "include_global_state": false
          },
          "retention": {
            "expire_after": "30d",
            "min_count": 5,
            "max_count": 50
          }
        },
        "last_success" : {
          "snapshot_name" : "daily-snap-2099.05.30-tme_ivjqswgkpryvnao2lg",
          "start_time" : 4083782400000,
          "time" : 4083782400000
        },
        "last_failure" : { <2>
          "snapshot_name" : "daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq",
          "time" : 4085251200000, <3>
          "details" : """{"type":"snapshot_exception","reason":"[daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq] failed to create snapshot successfully, 5 out of 149 total shards failed"}""" <4>
        },
        "stats": {
          "policy": "daily-snapshots",
          "snapshots_taken": 0,
          "snapshots_failed": 0,
          "snapshots_deleted": 0,
          "snapshot_deletion_failures": 0
        },
        "next_execution": "2099-06-17T01:30:00.000Z",
        "next_execution_millis": 4085343000000
      }
    }
    ```

    1. The affected snapshot lifecycle policy.
    2. The information about the last failure for the policy.
    3. The time when the failure occurred in millis. Use the `human=true` request parameter to see a formatted timestamp.
    4. Error details containing the reason for the snapshot failure.


    Snapshots can fail for a variety reasons. If the failures are due to configuration errors, consult the documentation for the repository that the automated snapshots are using. Refer to the [guide on managing repositories in ECE](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) if you are using such a deployment.


One common failure scenario is repository corruption. This occurs most often when multiple instances of {{es}} write to the same repository location. There is a [separate troubleshooting guide](diagnosing-corrupted-repositories.md) to fix this problem.

In the event that snapshots are failing for other reasons check the logs on the elected master node during the snapshot execution period for more information.
::::::

::::::{tab-item} Self-managed
[Retrieve](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-lifecycle) the {{slm}} policy:

```console
GET _slm/policy/<affected-policy-name>
```

The response will look like this:

```console-result
{
  "affected-policy-name": { <1>
    "version": 1,
    "modified_date": "2099-05-06T01:30:00.000Z",
    "modified_date_millis": 4081757400000,
    "policy" : {
      "schedule": "0 30 1 * * ?",
      "name": "<daily-snap-{now/d}>",
      "repository": "my_repository",
      "config": {
        "indices": ["data-*", "important"],
        "ignore_unavailable": false,
        "include_global_state": false
      },
      "retention": {
        "expire_after": "30d",
        "min_count": 5,
        "max_count": 50
      }
    },
    "last_success" : {
      "snapshot_name" : "daily-snap-2099.05.30-tme_ivjqswgkpryvnao2lg",
      "start_time" : 4083782400000,
      "time" : 4083782400000
    },
    "last_failure" : { <2>
      "snapshot_name" : "daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq",
      "time" : 4085251200000, <3>
      "details" : """{"type":"snapshot_exception","reason":"[daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq] failed to create snapshot successfully, 5 out of 149 total shards failed"}""" <4>
    },
    "stats": {
      "policy": "daily-snapshots",
      "snapshots_taken": 0,
      "snapshots_failed": 0,
      "snapshots_deleted": 0,
      "snapshot_deletion_failures": 0
    },
    "next_execution": "2099-06-17T01:30:00.000Z",
    "next_execution_millis": 4085343000000
  }
}
```

1. The affected snapshot lifecycle policy.
2. The information about the last failure for the policy.
3. The time when the failure occurred in millis. Use the `human=true` request parameter to see a formatted timestamp.
4. Error details containing the reason for the snapshot failure.


Snapshots can fail for a variety reasons. If the failures are due to configuration errors, consult the documentation for the repository that the automated snapshots are using.

One common failure scenario is repository corruption. This occurs most often when multiple instances of {{es}} write to the same repository location. There is a [separate troubleshooting guide](diagnosing-corrupted-repositories.md) to fix this problem.

In the event that snapshots are failing for other reasons check the logs on the elected master node during the snapshot execution period for more information.
::::::

:::::::
::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::
