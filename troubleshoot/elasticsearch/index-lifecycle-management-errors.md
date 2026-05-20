---
navigation_title: Index lifecycle management errors
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-error-handling.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Fix {{ilm}} errors [index-lifecycle-error-handling]

[{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) runs actions asynchronously on your cluster's indices, according to the conditions you define in your policy. {{ilm-init}} [phases and actions](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md) run sequentially on each index, using the permissions of the user who last edited the [{{ilm-init}} policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md).

{{ilm-init}} can surface two types of issues:

- **Direct errors:** The {{es}} API call itself fails.
- **Indirect configuration issues:** The API call succeeds, but the intended result doesn't take effect.

This guide explains how to check overall {{ilm-init}} health, investigate individual indices, and resolve common errors.

## Check for {{ilm-init}} issues [ilm-check-issues]

This section covers the symptoms of stuck tasks and erring tasks, then shows  common investigative API commands.

### {{ilm-init}} transient steps [ilm-steps-transient]

{{ilm-init}} purposely holds an index on a couple of steps for its logic-based and time-based conditions. The following [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) `phase/action/step` combinations wait:

* `hot/rollover/check-rollover-ready` until [{{ilm-init}} rollover requirements](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md#ilm-rollover-options) are met.
* `*/complete/complete` until the index's `age` qualifies for the next phase's `min_age`. Refer to [how `min_age` is calculated](#min-age-calculation) for more information.

This page refers to steps other than these as _transient_ steps, where {{ilm-init}} asynchronously applies an operation against the index instead of waiting for a logic-based or time-based condition.

{{ilm-init}} [polls for work on an interval basis](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md) (default `10m`). For more information, refer to [{{ilm-init}} phase transitions](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md#ilm-phase-execution). 

An index moves through its {{ilm-init}} steps as fast as the underlying operation finishes, plus the wait for the next poll. Transient steps that depend on an asynchronous operation can therefore be affected by [task backlogs](/troubleshoot/elasticsearch/task-queue-backlog.md). Common examples:

* `*/migrate/check-migration` monitors the index's [shards' allocation and recoveries](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery.md).
* `*/*/forcemerge` waits for the index's [force merge](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md), noting the guide's performance considerations.
* `delete/wait_for_snapshot/wait-for-snapshot` delays until the [{{ilm-init}} Delete](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-delete.md)'s [{{slm-cap}} ({{slm-init}}) policy](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md) is successfully completed for the index.

It's fine if these transient steps appear in the [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) output. But if an index doesn't progress past a step for an extended period, investigate. The cause is often specific to your setup or use case, rather than a cluster problem.

### {{ilm-init}} erring steps [ilm-steps-errors]

When errors occur, the [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) response includes the following:

* `failed_step`, set to the active step name
* `step`, set to `ERROR`
* `is_auto_retryable_error` flag, set
* `failed_step_retry_count`, incremented

All erring indices automatically run the [Retry policy API]({{es-apis}}operation/operation-ilm-retry) on each {{ilm-init}} polling interval. During automatic or manual retry:

* The `step` resets to the active step description and `failed_step` is removed.
* The `is_auto_retryable_error` persists.
* The `failed_step_retry_count` persists and increments again if another error is encountered.

Non-erring indices do not report the fields `failed_step`, `is_auto_retryable_error`, nor `failed_step_retry_count`. Indices that have recovered from previous errors also remove these temporary fields. This is why the [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) supports the `only_errors` flag, which returns only indices that are currently failing or are retrying a step:

```console
GET _all/_ilm/explain?human=true&expand_wildcards=all&only_errors=true
```

For troubleshooting, [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) emits `step_info`. This field is returned only when further context is available, such as `message` for information and `reason` for errors.

If {{ilm-init}} cannot automatically resolve the error for this index, execution is halted until the underlying issue with the policy, index, or cluster is resolved. For example, shard migrations might block until [Elastic Cloud Autoscaling](/deploy-manage/autoscaling.md) scales or adds necessary [data tiers](/manage-data/lifecycle/data-tiers.md).

### {{ilm-init}} health [ilm-health-overall]

Use the following APIs to check {{ilm-init}} health across all indices.

{{es}}'s [Cluster health API]({{es-apis}}operation/operation-health-report) reports `stagnating_indices` for indices that have been attempting a step longer than expected:

```console
GET _health_report/ilm
```

This report's thresholds are controlled by [Read cluster settings API]({{es-apis}}operation/operation-cluster-get-settings):

* `health.ilm.max_retries_per_step` (default `100`)
* `health.ilm.max_time_on_action` (default `1d`)
* `health.ilm.max_time_on_step` (default `1d`)

This report consolidates actionable interventions to consider for your {{ilm-init}} and cluster health.

For a high-level summary of all index statuses (not just those needing intervention), use the [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle). To save an overview of all `phase/action/step` index statuses to `ilm_explain.json`, processed with [jq](https://jqlang.github.io/jq/):

```bash
$ cat ilm_explain.json | jq -c '.indices[]|select(.managed==true)|.phase+"/"+.action+"/"+.step' | sort | uniq -c | sort -r
```

:::{tip}
For example {{ilm-init}} troubleshooting walkthroughs, refer to

* [Monitoring {{ilm-init}} {{es}} Health](https://www.youtube.com/watch?v=VCIqkji3IwY) for resolving erring steps.
* [{{ilm-init}} History Index](https://www.youtube.com/watch?v=onrnnwjYWSQ) for an explanation of step sequences and how to review historical index statuses.
:::

### Troubleshooting {{ilm-init}} for an index [ilm-health-index]

The following example demonstrates troubleshooting {{ilm-init}} for a newly created index. Consider a `shrink-index` policy that [shrinks](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-shrink.md) an index to four shards once it is at least five days old:

```console
PUT _ilm/policy/shrink-index
{
  "policy": {
    "phases": {
      "warm": {
        "min_age": "5d",
        "actions": {
          "shrink": {
            "number_of_shards": 4
          }
        }
      }
    }
  }
}
```

To [create an index]({{es-apis}}operation/operation-indices-create) `my-index-000001` that has only two primary shards and [apply the {{ilm-init}} policy](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md) `shrink-index`:

```console
PUT /my-index-000001
{
  "settings": {
    "index.number_of_shards": 2,
    "index.lifecycle.name": "shrink-index"
  }
}
```

After five days, {{ilm-init}} attempts to run the [shrink index API]({{es-apis}}operation/operation-indices-shrink) against index `my-index-000001` from two shards to four shards. Because the shrink action cannot *increase* the number of shards, this operation fails and {{ilm-init}} moves `my-index-000001` to the `step` of `ERROR`.

Use the [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) to get information about what went wrong:

```console
GET /my-index-000001/_ilm/explain
```

Which returns the following information:

```console-result
{
  "indices" : {
    "my-index-000001" : {
      "index" : "my-index-000001",
      "managed" : true,
      "index_creation_date_millis" : 1541717265865,
      "time_since_index_creation": "5.1d",
      "policy" : "shrink-index",                <1>
      "lifecycle_date_millis" : 1541717265865,
      "age": "5.1d",                            <2>
      "phase" : "warm",                         <3>
      "phase_time_millis" : 1541717272601,
      "action" : "shrink",                      <4>
      "action_time_millis" : 1541717272601,
      "step" : "ERROR",                         <5>
      "step_time_millis" : 1541717272688,
      "failed_step" : "shrink",                 <6>
      "step_info" : {
        "type" : "illegal_argument_exception",  <7>
        "reason" : "the number of target shards [4] must be less that the number of source shards [2]"
      },
      "phase_execution" : {
        "policy" : "shrink-index",
        "phase_definition" : {                  <8>
          "min_age" : "5d",
          "actions" : {
            "shrink" : {
              "number_of_shards" : 4
            }
          }
        },
        "version" : 1,
        "modified_date_in_millis" : 1541717264230
      }
    }
  }
}
```

1. The policy being used to manage the index: `shrink-index`
2. The index age: 5.1 days
3. The phase the index is currently in: `warm`
4. The current action: `shrink`
5. The step the index is currently in: `ERROR`
6. The step that failed to run: `shrink`
7. The type of error and a description of that error.
8. The definition of the current phase from the `shrink-index` policy


To resolve this, update the policy to shrink the index to a single shard after 5 days:

```console
PUT _ilm/policy/shrink-index
{
  "policy": {
    "phases": {
      "warm": {
        "min_age": "5d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          }
        }
      }
    }
  }
}
```

After resolving the underlying problem, wait for {{ilm-init}}'s poll interval to automatically retry the index's `ERROR` step, or apply the [retry policy API]({{es-apis}}operation/operation-ilm-retry) to run it on demand:

```console
POST /my-index-000001/_ilm/retry
```

{{ilm-init}} subsequently attempts to re-run the step that failed. You can use the [{{ilm-init}} Explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) to monitor the progress.

## Key {{ilm-init}} concepts [ilm-faq]

The following behaviors come up often when troubleshooting {{ilm-init}}. For more details, refer to the [{{ilm-init}} guide](/manage-data/lifecycle/index-lifecycle-management.md) or [contact us](/troubleshoot/index.md#contact-us).
### How `min_age` is calculated [min-age-calculation]

When setting up an [{{ilm-init}} policy](../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) or [automating rollover with {{ilm-init}}](../../manage-data/lifecycle/index-lifecycle-management/rollover.md), be aware that `min_age` can be relative to either the rollover time or the index creation time.

If you use [{{ilm-init}} rollover](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md), `min_age` is calculated relative to the time the index was rolled over. This is because the [rollover API]({{es-apis}}operation/operation-indices-rollover) generates a new index and updates the `age` of the previous index to reflect the rollover time. If the index hasn’t been rolled over, then the `age` is the same as the `creation_date` for the index.

You can override how `min_age` is calculated using the `index.lifecycle.origination_date` and `index.lifecycle.parse_origination_date` [{{ilm-init}} settings](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md).

### Steps proceed sequentially [ilm-sequential-steps]

{{ilm-init}} does not skip steps due to logic-based or time-based conditions. It proceeds through all steps [in the enabled action's order](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md#phases-availability). For example, this means it's possible for an index stagnated at `phase/action/step` of `warm/migrate/check-migration` to surpass its expected deletion time. Make sure to review and resolve {{ilm-init}} errors to maintain a healthy cluster. For more information, refer to [{{ilm-init}} phase transitions](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md#ilm-phase-transitions).

### Policy changes apply forward [ilm-policy-changes]

When an index enters a phase, it caches the {{ilm-init}} policy's current definition. For more information, refer to [phase execution](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md#ilm-phase-execution). This enables {{ilm-init}} to protect the index from policy changes which might cause data corruption. 

As described in [how changes are applied](/manage-data/lifecycle/index-lifecycle-management/policy-updates.md#ilm-apply-changes), {{ilm-init}} applies safe updates to an index's `phase_execution` immediately. Updates that aren't safe to apply retroactively are forward-applied, taking effect only as indices enter the phase after the update.

You might need to apply a policy change to indices that are already stagnant. It's not possible to run a single {{ilm-init}} step on demand, because doing so might corrupt the index. Instead, apply the relevant changes to those indices manually.

In rare cases, a policy change can leave indices stagnant. The only fix is the [move to an {{ilm-init}} step API]({{es-apis}}operation/operation-ilm-move-to-step). This is an advanced API -- [contact us](/troubleshoot/index.md#contact-us) with an [{{es}} diagnostic](/troubleshoot/elasticsearch/diagnostic.md) before using it.

## Common {{ilm-init}} errors [ilm-errors]

Each entry below shows the message you'll see in the `ERROR` step, the cause, and the recommended fix. Errors are grouped by the {{ilm-init}} action where they typically occur.

### Rollover errors [ilm-errors-rollover]

::::{tip}
Problems with rollover aliases are a common cause of errors. You should consider using [data streams](/manage-data/data-store/data-streams.md) instead of managing rollover with aliases.
::::

These errors can occur when the [{{ilm-init}} rollover](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) action runs:

:::{dropdown} Rollover alias [x] can point to multiple indices, found duplicated alias [x] in index template [z]
:name: _rollover_alias_x_can_point_to_multiple_indices_found_duplicated_alias_x_in_index_template_z

The target rollover alias is specified in an index template’s `index.lifecycle.rollover_alias` setting. You need to explicitly configure this alias *one time* when you [bootstrap the initial index](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md#ilm-gs-alias-bootstrap). The rollover action then manages setting and updating the alias to [roll over]({{es-apis}}operation/operation-indices-rollover#rollover-index-api-desc) to each subsequent index.

Do not explicitly configure this same alias in the aliases section of an index template.

For an example, refer to this [resolving duplicate alias video](https://www.youtube.com/watch?v=Ww5POq4zZtY).
:::

:::{dropdown} index.lifecycle.rollover_alias [x] does not point to index [y]
:name: _index_lifecycle_rollover_alias_x_does_not_point_to_index_y

Either the index is using the wrong alias or the alias does not exist.

Check the `index.lifecycle.rollover_alias` [index setting]({{es-apis}}operation/operation-indices-get-settings). To see what aliases are configured, use [_cat/aliases]({{es-apis}}operation/operation-cat-aliases).

For an example, refer to this [resolving alias not pointing to index video](https://www.youtube.com/watch?v=NKSe67x7aw8).
:::

:::{dropdown} setting [index.lifecycle.rollover_alias] for index [y] is empty or not defined
:name: _setting_index_lifecycle_rollover_alias_for_index_y_is_empty_or_not_defined

The `index.lifecycle.rollover_alias` setting must be configured for the rollover action to work.

Update the index settings to set `index.lifecycle.rollover_alias`.

For an example, refer to this [resolving empty or not defined video](https://www.youtube.com/watch?v=LRpMC2GS_FQ).
:::

:::{dropdown} alias [x] has more than one write index [y,z]
:name: _alias_x_has_more_than_one_write_index_yz

Only one index can be designated as the write index for a particular alias.

Use the [aliases]({{es-apis}}operation/operation-indices-update-aliases) API to set `is_write_index:false` for all but one index.

For an example, refer to this [resolving more than one write index video](https://www.youtube.com/watch?v=jCUvZCT5Hm4).
:::

:::{dropdown} index name [x] does not match pattern ^.*-\d+ 
:name: _index_name_x_does_not_match_pattern_d

The index name must match the regex pattern `^.*-\d+` for the rollover action to work. The most common problem is that the index name does not contain trailing digits. For example, `my-index` does not match the pattern requirement.

Append a numeric value to the index name, for example `my-index-000001`.

For an example, refer to this [resolving does not match pattern video](https://www.youtube.com/watch?v=9sp1zF6iL00).
:::


### {{ilm-init}} migrate errors [ilm-errors-migrate]

The following errors usually surface during shard recovery, which can occur when you use [{{ilm-init}} migrate](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) operations or [{{ilm-init}} searchable snapshots](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-searchable-snapshot.md). Because these operations run asynchronously, the error reported by {{ilm-init}} often shows only a symptom of the real problem. To troubleshoot the underlying cause, refer to [cluster allocation API examples](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md).


:::{dropdown} index has a preference for tiers [xxx] and node does not meet the required [xxx] tier
:name: _index_has_a_preference_for_tiers

If the [allocation explain API]({{es-apis}}operation/operation-cluster-allocation-explain) returns this error, it indicates that shards cannot be assigned according to the current attribute-based or data tier allocation rules. For detailed guidance on resolving this issue, refer to [Unable to assign shards based on the allocation rule](https://www.elastic.co/docs/troubleshoot/monitoring/unavailable-shards#ec-cannot-assign-shards-on-allocation-rule).
:::

### General {{ilm-init}} errors [ilm-errors-general]

The following errors can surface on any {{ilm-init}} step.

:::{dropdown} CircuitBreakingException: [x] data too large, data for [y]
:name: _circuitbreakingexception_x_data_too_large_data_for_y

This indicates that the cluster is hitting resource limits.

Before continuing to set up {{ilm-init}}, you’ll need to take steps to alleviate the resource issues. For more information, see [Circuit breaker errors](circuit-breaker-errors.md).
:::

:::{dropdown} high disk watermark [x] exceeded on [y]
:name: _high_disk_watermark_x_exceeded_on_y

This indicates that the cluster is running out of disk space. This can happen when you don’t have {{ilm}} set up to roll over from hot to warm nodes. For more information, see [](fix-watermark-errors.md).

:::

:::{dropdown} security_exception: action [<action-name>] is unauthorized for user [<user-name>] with roles [<role-name>], this action is granted by the index privileges [manage_follow_index,manage,all]
:name: _security_exception

{{ilm-init}} runs each action as the user who last modified the policy, with the privileges they held at that time. This error means the action requires privileges that user doesn't have.

To fix it, make sure the account that creates or modifies the policy has the necessary permission for every operation it includes. If this error surfaces on system indices, refer to [File-based access recovery](/troubleshoot/elasticsearch/file-based-recovery.md).
:::

:::{dropdown} policy [<policy-name>] does not exist
:name: _policy_policy_name_does_not_exist

The error occurs because the index is assigned to an {{ilm-init}} policy that does not exist in the cluster. To fix this, you can either [create the missing policy]({{es-apis}}operation/operation-ilm-put-lifecycle) with the required settings or [link the index to an existing {{ilm-init}} policy](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md#index-lifecycle-name).
:::
