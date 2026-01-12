---
navigation_title: Snapshot policy failures
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/repeated-snapshot-failures.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Fix repeated snapshot policy failures [repeated-snapshot-failures]

Repeated snapshot failures are usually an indicator of a problem with your deployment. Continuous failures of automated snapshots can leave a deployment without recovery options in cases of data loss or outages.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

{{es}} keeps track of the number of repeated failures when executing automated snapshots with [{{slm}} ({{slm-init}})](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) policies. If an automated snapshot fails too many times without a successful execution, the health API will report a warning. The number of repeated failures before reporting a warning is controlled by the [`slm.health.failed_snapshot_warn_threshold`](elasticsearch://reference/elasticsearch/configuration-reference/snapshot-restore-settings.md#slm-health-failed-snapshot-warn-threshold) setting.

## Review snapshot policy failures

In the event that an automated {{slm-init}} policy execution is experiencing repeated failures, follow these steps to get more information about the problem:

:::::::{tab-set}

::::::{tab-item} Using {{kib}}
In {{kib}}, you can view all configured {{slm-init}} policies and review their status and execution history. If the UI does not provide sufficient details about the failure, use the Console to retrieve the [snapshot policy information](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-lifecycle) with the {{es}} API.

1. Go to **Snapshot and Restore > Policies** to see the list of configured policies. You can find the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /troubleshoot/images/elasticsearch-reference-slm-policies.png
    :alt: {{kib}} Console
    :screenshot:
    :::

2. The policies table should be visible. Click on any of the policies to review the details and execution history.

3. To get more detailed information about the failure, open {{kib}} **Dev Tools > Console**. You can find the **Console** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /troubleshoot/images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :screenshot:
    :::

4. [Retrieve the affected {{slm-init}} policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-lifecycle):

    ```console
    GET _slm/policy/<affected-policy-name>
    ```

    The response looks like this:

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
::::::

::::::{tab-item} Using the {{es}} API
[Retrieve the affected {{slm-init}} policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-lifecycle):

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

::::::

:::::::

## Possible causes

Snapshots can fail for a variety of reasons. If the failures are due to configuration errors, consult the documentation for the repository type that the snapshot policy is using. Refer to the [guide on managing repositories in ECE](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) if you are using an Elastic Cloud Enterprise deployment.

One common failure scenario is repository corruption. This occurs most often when multiple instances of {{es}} write to the same repository location. There is a [separate troubleshooting guide](diagnosing-corrupted-repositories.md) to fix this problem.

In the event that snapshots are failing for other reasons check the logs on the elected master node during the snapshot execution period for more information.
