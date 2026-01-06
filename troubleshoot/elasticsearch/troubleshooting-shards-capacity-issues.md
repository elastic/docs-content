---
navigation_title: Shard capacity issues
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/troubleshooting-shards-capacity-issues.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Troubleshoot shard capacity health issues [troubleshooting-shards-capacity-issues]

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

{{es}} limits the maximum number of shards to be held per node using the [`cluster.max_shards_per_node`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) and [`cluster.max_shards_per_node.frozen`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node-frozen) settings. The current shards capacity of the cluster is available in the [health API shards capacity section](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report).


## Cluster is close to reaching the configured maximum number of shards for data nodes[_cluster_is_close_to_reaching_the_configured_maximum_number_of_shards_for_data_nodes]

The [`cluster.max_shards_per_node`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) cluster setting limits the maximum number of open shards for a cluster, only counting data nodes that do not belong to the frozen tier.

This symptom indicates that action should be taken, otherwise, either the creation of new indices or upgrading the cluster could be blocked.

If you're confident your changes won't destabilize the cluster, you can temporarily increase the limit using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).

You can perform the following steps using either [API console](/explore-analyze/query-filter/tools/console.md), or direct [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

1. Check the current status of the cluster according the shards capacity indicator:

    ```console
    GET _health_report/shards_capacity
    ```

    The response will look like this:

    ```console-result
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "yellow",
          "symptom": "Cluster is close to reaching the configured maximum number of shards for data nodes.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000, <1>
              "current_used_shards": 988 <2>
            },
            "frozen": {
              "max_shards_in_cluster": 3000,
              "current_used_shards": 0
            }
          },
          "impacts": [
            ...
          ],
          "diagnosis": [
            ...
        }
      }
    }
    ```

    1. Current value of the setting `cluster.max_shards_per_node`
    2. Current number of open shards across the cluster

2. Update the [`cluster.max_shards_per_node`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) setting with a proper value using the [cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings):

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": 1200
      }
    }
    ```

    This increase should only be temporary. As a long-term solution, we recommend you add nodes to the oversharded data tier or [reduce your cluster's shard count](../../deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count) on nodes that do not belong to the frozen tier.

3. To verify that the change has fixed the issue, check the current status of the `shards_capacity` indicator:

    ```console
    GET _health_report/shards_capacity
    ```

    The response will look like this:

    ```console-result
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "green",
          "symptom": "The cluster has enough room to add new shards.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3000
            }
          }
        }
      }
    }
    ```

4. When a long-term solution is in place, reset the `cluster.max_shards_per_node` limit:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": null
      }
    }
    ```

## Cluster is close to reaching the configured maximum number of shards for frozen nodes[_cluster_is_close_to_reaching_the_configured_maximum_number_of_shards_for_frozen_nodes]

The [`cluster.max_shards_per_node.frozen`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node-frozen) cluster setting limits the maximum number of open shards for a cluster, only counting data nodes that belong to the frozen tier.

This symptom indicates that action should be taken, otherwise, either the creation of new indices or upgrading the cluster could be blocked.

If you're confident your changes won't destabilize the cluster, you can temporarily increase the limit using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).

You can perform the following steps using either [API console](/explore-analyze/query-filter/tools/console.md), or direct [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

1. Check the current status of the cluster according the shards capacity indicator:

    ```console
    GET _health_report/shards_capacity
    ```

    The response will look like this:

    ```console-result
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "yellow",
          "symptom": "Cluster is close to reaching the configured maximum number of shards for frozen nodes.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3000, <1>
              "current_used_shards": 2998 <2>
            }
          },
          "impacts": [
            ...
          ],
          "diagnosis": [
            ...
        }
      }
    }
    ```

    1. Current value of the setting `cluster.max_shards_per_node.frozen`
    2. Current number of open shards used by frozen nodes across the cluster

2. Update the [`cluster.max_shards_per_node.frozen`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node-frozen) setting using the [cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings):

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node.frozen": 3200
      }
    }
    ```

    This increase should only be temporary. As a long-term solution, we recommend you add nodes to the oversharded data tier or [reduce your cluster's shard count](../../deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count) on nodes that belong to the frozen tier.

3. To verify that the change has fixed the issue, check the current status of the `shards_capacity` indicator:

    ```console
    GET _health_report/shards_capacity
    ```

    The response will look like this:

    ```console-result
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "green",
          "symptom": "The cluster has enough room to add new shards.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3200
            }
          }
        }
      }
    }
    ```

4. When a long-term solution is in place, reset the `cluster.max_shards_per_node.frozen` limit:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node.frozen": null
      }
    }
    ```
