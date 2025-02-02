---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/operator-only-functionality.html
---

# Operator-only functionality [operator-only-functionality]

::::{note} 
{cloud-only}
::::


Operator privileges provide protection for APIs and dynamic cluster settings. Any API or cluster setting that is protected by operator privileges is known as *operator-only functionality*. When the operator privileges feature is enabled, operator-only APIs can be executed only by operator users. Likewise, operator-only settings can be updated only by operator users. The list of operator-only APIs and dynamic cluster settings are pre-determined in the codebase. The list may evolve in future releases but it is otherwise fixed in a given {{es}} version.

## Operator-only APIs [operator-only-apis]

* [Voting configuration exclusions](https://www.elastic.co/guide/en/elasticsearch/reference/current/voting-config-exclusions.html)
* [Delete license](https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-license.html)
* [Update license](https://www.elastic.co/guide/en/elasticsearch/reference/current/update-license.html)
* [Create or update autoscaling policy](https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-put-autoscaling-policy.html)
* [Delete autoscaling policy](https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-delete-autoscaling-policy.html)
* [Create or update desired nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/update-desired-nodes.html)
* [Get desired nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/get-desired-nodes.html)
* [Delete desired nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-desired-nodes.html)
* [Get desired balance](https://www.elastic.co/guide/en/elasticsearch/reference/current/get-desired-balance.html)
* [Reset desired balance](https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-desired-balance.html)


## Operator-only dynamic cluster settings [operator-only-dynamic-cluster-settings]

* All [IP filtering](../../security/ip-traffic-filtering.md) settings
* The following dynamic [machine learning settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-settings.html):

    * `xpack.ml.node_concurrent_job_allocations`
    * `xpack.ml.max_machine_memory_percent`
    * `xpack.ml.use_auto_machine_memory_percent`
    * `xpack.ml.max_lazy_ml_nodes`
    * `xpack.ml.process_connect_timeout`
    * `xpack.ml.nightly_maintenance_requests_per_second`
    * `xpack.ml.max_ml_node_size`
    * `xpack.ml.enable_config_migration`
    * `xpack.ml.persist_results_max_retries`

* The [`cluster.routing.allocation.disk.threshold_enabled` setting](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#cluster-routing-disk-threshold)
* The following [recovery settings for managed services](https://www.elastic.co/guide/en/elasticsearch/reference/current/recovery.html#recovery-settings-for-managed-services):

    * `node.bandwidth.recovery.operator.factor`
    * `node.bandwidth.recovery.operator.factor.read`
    * `node.bandwidth.recovery.operator.factor.write`
    * `node.bandwidth.recovery.operator.factor.max_overcommit`



