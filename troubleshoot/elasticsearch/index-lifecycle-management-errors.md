---
navigation_title: "Index lifecycle management errors"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-error-handling.html
---

% TODO restructure ILM and SLM dtopics
% TODO dropdowns or break it up

# Fix index lifecycle management errors [index-lifecycle-error-handling]

When [{{ilm-init}}](../../manage-data/lifecycle/index-lifecycle-management.md) executes a lifecycle policy, it’s possible for errors to occur while performing the necessary index operations for a step. When this happens, {{ilm-init}} moves the index to an `ERROR` step. If {{ilm-init}} cannot resolve the error automatically, execution is halted until you resolve the underlying issues with the policy, index, or cluster.

See [this video](https://www.youtube.com/watch?v=VCIqkji3IwY) for a walkthrough of troubleshooting current {{ilm-init}} health issues, and [this video](https://www.youtube.com/watch?v=onrnnwjYWSQ) for a walkthrough of troubleshooting historical {{ilm-init}} issues.

For example, you might have a `shrink-index` policy that shrinks an index to four shards once it is at least five days old:

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
%  TEST

There is nothing that prevents you from applying the `shrink-index` policy to a new index that has only two shards:

```console
PUT /my-index-000001
{
  "settings": {
    "index.number_of_shards": 2,
    "index.lifecycle.name": "shrink-index"
  }
}
```
%  TEST[continued]

After five days, {{ilm-init}} attempts to shrink `my-index-000001` from two shards to four shards. Because the shrink action cannot *increase* the number of shards, this operation fails and {{ilm-init}} moves `my-index-000001` to the `ERROR` step.

You can use the [{{ilm-init}} Explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-explain-lifecycle) to get information about what went wrong:

```console
GET /my-index-000001/_ilm/explain
```
%  TEST[continued]

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
6. The step that failed to execute: `shrink`
7. The type of error and a description of that error.
8. The definition of the current phase from the `shrink-index` policy
%  TESTRESPONSE[skip:no way to know if we will get this response immediately]

To resolve this, you could update the policy to shrink the index to a single shard after 5 days:

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
%  TEST[continued]


## Retrying failed lifecycle policy steps [_retrying_failed_lifecycle_policy_steps]

Once you fix the problem that put an index in the `ERROR` step, you might need to explicitly tell {{ilm-init}} to retry the step:

```console
POST /my-index-000001/_ilm/retry
```
%  TEST[skip:we can’t be sure the index is ready to be retried at this point]

{{ilm-init}} subsequently attempts to re-run the step that failed. You can use the [{{ilm-init}} Explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-explain-lifecycle) to monitor the progress.


## Common {{ilm-init}} setting issues [_common_ilm_init_setting_issues]


### How `min_age` is calculated [min-age-calculation]

When setting up an [{{ilm-init}} policy](../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) or [automating rollover with {{ilm-init}}](../../manage-data/lifecycle/index-lifecycle-management.md), be aware that `min_age` can be relative to either the rollover time or the index creation time.

If you use [{{ilm-init}} rollover](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md), `min_age` is calculated relative to the time the index was rolled over. This is because the [rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover) generates a new index and updates the `age` of the previous index to reflect the rollover time. If the index hasn’t been rolled over, then the `age` is the same as the `creation_date` for the index.

You can override how `min_age` is calculated using the `index.lifecycle.origination_date` and `index.lifecycle.parse_origination_date` [{{ilm-init}} settings](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md).


## Common {{ilm-init}} errors [_common_ilm_init_errors]

Here’s how to resolve the most common errors reported in the `ERROR` step.

::::{tip}
Problems with rollover aliases are a common cause of errors. Consider using [data streams](/manage-data/data-store/data-streams.md) instead of managing rollover with aliases.
::::



### Rollover alias [x] can point to multiple indices, found duplicated alias [x] in index template [z] [_rollover_alias_x_can_point_to_multiple_indices_found_duplicated_alias_x_in_index_template_z]

The target rollover alias is specified in an index template’s `index.lifecycle.rollover_alias` setting. You need to explicitly configure this alias *one time* when you [bootstrap the initial index](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-alias-bootstrap). The rollover action then manages setting and updating the alias to [roll over](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover#rollover-index-api-desc) to each subsequent index.

Do not explicitly configure this same alias in the aliases section of an index template.

See this [resolving `duplicate alias` video](https://www.youtube.com/watch?v=Ww5POq4zZtY) for an example troubleshooting walkthrough.


### index.lifecycle.rollover_alias [x] does not point to index [y] [_index_lifecycle_rollover_alias_x_does_not_point_to_index_y]

Either the index is using the wrong alias or the alias does not exist.

Check the `index.lifecycle.rollover_alias` [index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings). To see what aliases are configured, use [_cat/aliases](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-aliases).

See this [resolving `not point to index` video](https://www.youtube.com/watch?v=NKSe67x7aw8) for an example troubleshooting walkthrough.


### Setting [index.lifecycle.rollover_alias] for index [y] is empty or not defined [_setting_index_lifecycle_rollover_alias_for_index_y_is_empty_or_not_defined]

The `index.lifecycle.rollover_alias` setting must be configured for the rollover action to work.

Update the index settings to set `index.lifecycle.rollover_alias`.

See this [resolving `empty or not defined` video](https://www.youtube.com/watch?v=LRpMC2GS_FQ) for an example troubleshooting walkthrough.


### Alias [x] has more than one write index [y,z] [_alias_x_has_more_than_one_write_index_yz]

Only one index can be designated as the write index for a particular alias.

Use the [aliases](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases) API to set `is_write_index:false` for all but one index.

See this [resolving `more than one write index` video](https://www.youtube.com/watch?v=jCUvZCT5Hm4) for an example troubleshooting walkthrough.


### index name [x] does not match pattern ^.*-\d+ [_index_name_x_does_not_match_pattern_d]

The index name must match the regex pattern `^.*-\d+` for the rollover action to work. The most common problem is that the index name does not contain trailing digits. For example, `my-index` does not match the pattern requirement.

Append a numeric value to the index name, for example `my-index-000001`.

See this [resolving `does not match pattern` video](https://www.youtube.com/watch?v=9sp1zF6iL00) for an example troubleshooting walkthrough.


### CircuitBreakingException: [x] data too large, data for [y] [_circuitbreakingexception_x_data_too_large_data_for_y]

This indicates that the cluster is hitting resource limits.

Before continuing to set up {{ilm-init}}, you’ll need to take steps to alleviate the resource issues. For more information, see [Circuit breaker errors](circuit-breaker-errors.md).


### High disk watermark [x] exceeded on [y] [_high_disk_watermark_x_exceeded_on_y]

This indicates that the cluster is running out of disk space. This can happen when you don’t have {{ilm}} set up to roll over from hot to warm nodes. For more information, see [Fix watermark errors](fix-watermark-errors.md).


### security_exception: action [<action-name>] is unauthorized for user [<user-name>] with roles [<role-name>], this action is granted by the index privileges [manage_follow_index,manage,all] [_security_exception_action_action_name_is_unauthorized_for_user_user_name_with_roles_role_name_this_action_is_granted_by_the_index_privileges_manage_follow_indexmanageall]

This indicates the ILM action cannot be executed because the user used by ILM to perform the action doesn’t have the proper privileges. This can happen when user’s privileges has been dropped after updating the ILM policy. ILM actions are run as though they were performed by the last user who modify the policy. The account used to create or modify the policy from should have permissions to perform all operations that are part of that policy.

