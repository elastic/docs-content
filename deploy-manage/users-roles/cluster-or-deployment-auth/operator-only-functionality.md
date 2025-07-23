---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/operator-only-functionality.html
applies_to:
  deployment:
    ess:
    ece:
    eck:
products:
  - id: elasticsearch
---

# Operator-only functionality [operator-only-functionality]

::::{admonition} Indirect use only
This feature is designed for indirect use by {{ech}}, {{ece}}, and {{eck}}. Direct use is not supported.
::::


Operator privileges provide protection for APIs and dynamic cluster settings. Any API or cluster setting that is protected by operator privileges is known as *operator-only functionality*. When the operator privileges feature is enabled, operator-only APIs can be executed only by operator users. Likewise, operator-only settings can be updated only by operator users. The list of operator-only APIs and dynamic cluster settings are pre-determined in the codebase. The list may evolve in future releases but it is otherwise fixed in a given {{es}} version.

## Operator-only APIs [operator-only-apis]

* [Voting configuration exclusions](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-post-voting-config-exclusions)
* [Delete license](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-license-delete)
* [Update license](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-license-post)
* [Create or update autoscaling policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-autoscaling-put-autoscaling-policy)
* [Delete autoscaling policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-autoscaling-delete-autoscaling-policy)
* [Create or update desired nodes](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-cluster)
* [Get desired nodes](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-cluster)
* [Delete desired nodes](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-cluster)
* [Get desired balance](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-cluster)
* [Reset desired balance](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-cluster)


## Operator-only dynamic cluster settings [operator-only-dynamic-cluster-settings]

* All [IP filtering](../../security/ip-filtering.md) settings
* The following dynamic [machine learning settings](elasticsearch://reference/elasticsearch/configuration-reference/machine-learning-settings.md):

    * `xpack.ml.node_concurrent_job_allocations`
    * `xpack.ml.max_machine_memory_percent`
    * `xpack.ml.use_auto_machine_memory_percent`
    * `xpack.ml.max_lazy_ml_nodes`
    * `xpack.ml.process_connect_timeout`
    * `xpack.ml.nightly_maintenance_requests_per_second`
    * `xpack.ml.max_ml_node_size`
    * `xpack.ml.enable_config_migration`
    * `xpack.ml.persist_results_max_retries`

* The [`cluster.routing.allocation.disk.threshold_enabled` setting](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-disk-threshold)
* The following [recovery settings for managed services](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md#recovery-settings-for-managed-services):

    * `node.bandwidth.recovery.operator.factor`
    * `node.bandwidth.recovery.operator.factor.read`
    * `node.bandwidth.recovery.operator.factor.write`
    * `node.bandwidth.recovery.operator.factor.max_overcommit`



