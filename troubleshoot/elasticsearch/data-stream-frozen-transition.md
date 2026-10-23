---
navigation_title: Data stream lifecycle transitions
description: Diagnose and resolve data stream backing indices that are not converting to frozen {{search-snaps}}.
type: troubleshooting
applies_to:
  stack: ga 9.5
  serverless: unavailable
products:
  - id: elasticsearch
---

# Troubleshoot data stream lifecycle transitions

If the data stream lifecycle has frozen phase transitions turned on, older backing indices convert to [frozen {{search-snaps}}](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md) instead of staying on hot or warm nodes.
Until the conversion finishes, those indices keep using local storage.

Ue the following troubleshooting information to diagnose problems with these transitions.

## Symptoms

- The [explain data lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle) reports a conversion error on a backing index.
- {applies_to}`stack: ga 9.6` The `dlm_frozen_transitions` indicator of the [health report API]({{es-apis}}operation/operation-health-report) is `yellow` or `unknown`.
- Backing indices older than the `frozen_after` lifecycle setting remain on non-frozen tiers.

## Diagnosis

Inspect the backing index with the [explain data lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle).
For example:

```console
GET .ds-my-stream-*/_lifecycle/explain
```

Note the error on each blocked index. For transient failures, {{es}} records the error and retries the conversion on the next poll cycle. Each conversion step is idempotent, so retries resume from the point at which the error occurred. Conversions stop retrying when the explain output reports an unrecoverable error, such as a missing snapshot repository or a license compliance failure.

### Check frozen transition health
```{applies_to}
stack: ga 9.6
```

Use the [health report API]({{es-apis}}operation/operation-health-report) to view overdue frozen conversions across the cluster:

```console
GET _health_report/dlm_frozen_transitions
```

Example response:

```console-result
{
  "cluster_name": "my-cluster",
  "indicators": {
    "dlm_frozen_transitions": {
      "status": "yellow",
      "symptom": "An issue affecting DLM frozen-tier transitions was detected",
      "details": {
        "overdue_indices_count_by_state": {
          "unmarked": 1
        },
        "default_repository_configured": true,
        "overdue_indices_sample": [
          {
            "index_name": ".ds-my-data-stream-test-2026.10.17-000001",
            "transition_state": "unmarked"
          }
        ],
        "service_running": true,
        "overdue_indices_count": 1,
        "transitions_enabled": true
      },
      "impacts": [
        {
          "id": "elasticsearch:health:dlm_frozen_transitions:impact:frozen_transition_blocked",
          "severity": 3,
          "description": "Data stream backing indices may be delayed or blocked from transitioning to the frozen tier. Storage size and cost management could be impacted.",
          "impact_areas": [
            "deployment_management"
          ]
        }
      ],
      "diagnosis": [
        {
          "id": "elasticsearch:health:dlm_frozen_transitions:diagnosis:eligible_indices_unmarked",
          "cause": "Some indices are eligible for conversion to the frozen tier but have not been marked for conversion, even though a default snapshot repository is configured. 1 index is affected.",
          "action": "Check the current master node's logs for errors related to the data stream lifecycle and the DLM frozen transition service.",
          "help_url": "https://ela.st/health-dlm-frozen-transitions",
          "affected_resources": {
            "indices": [
              ".ds-my-data-stream-test-2026.10.17-000001"
            ]
          }
        }
      ]
    }
  }
}
```

Read the `status`, `symptom`, and each `diagnosis.action`.
In `details`, check `transitions_enabled`, `default_repository_configured`, and `overdue_indices_count_by_state` (`unmarked`, `marked`, or `queued`).

A conversion that is already running is not overdue, so the indicator stays `green` while that work is in progress.

- `green`: No overdue conversions or every overdue conversion is already running.
- `yellow`: Conversions are blocked, queued, or waiting while frozen transitions are turned off.
- `unknown`: The master node has not published health information for three [`dlm.frozen_transitions.health.publish_interval`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#dlm-frozen-transition-health-publish-interval) intervals.

An index is overdue only after it has been past the `frozen_after` setting for longer than [`dlm.frozen_transitions.health.stuck_threshold`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#dlm-frozen-transition-health-stuck-threshold).

## Resolution

Use the option that matches the error or diagnosis.

{applies_to}`stack: ga 9.6` When the health report is `yellow`, follow `diagnosis.action`.

1. If the error or diagnosis reports a missing default snapshot repository, register one. Refer to [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md).
2. If the error reports a license compliance failure, renew the license. Refer to [{{es}} pricing and subscriptions]({{subscriptions}}).
3. If frozen transitions are turned off, set [`dlm.frozen_transitions.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#dlm-frozen-transition-enabled) to `true`. Transitions that are already running continue either way. Indices that are marked or queued stay overdue until you turn on the setting:

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "dlm.frozen_transitions.enabled": true
      }
    }
    ```

4. If the diagnosis reports queued transitions, inspect the `dlm_frozen_transition` thread pool with the [cat thread pool API]({{es-apis}}operation/operation-cat-thread-pool):

    ```console
    GET _cat/thread_pool/dlm_frozen_transition?v
    ```

    A persistently full queue means conversions complete more slowly than indices become eligible. Wait for in-flight work to drain or add capacity so more conversions can run at once.

5. If the diagnosis reports that the frozen transition service is not running on the current master node, check that node's logs for frozen transition errors. Restart the master node if the service stays down.
6. {applies_to}`stack: ga 9.6` If the health indicator is `unknown`, check the current master node's logs and confirm the master is publishing frozen transition health on the [`dlm.frozen_transitions.health.publish_interval`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#dlm-frozen-transition-health-publish-interval) schedule.

## Resources

- [{{search-snaps-cap}} for data streams](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md)
- [Data stream lifecycle](/manage-data/lifecycle/data-stream.md)
- [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md)
- [Frozen tier transition settings](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#_frozen_tier_transition_settings)
