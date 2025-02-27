---
navigation_title: Shard capacity issues
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/troubleshooting-shards-capacity-issues.html
---

# Troubleshoot shard capacity health issues [troubleshooting-shards-capacity-issues]

{{es}} limits the maximum number of shards to be held per node using the [`cluster.max_shards_per_node`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) and [`cluster.max_shards_per_node.frozen`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node-frozen) settings. The current shards capacity of the cluster is available in the [health API shards capacity section](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report).


## Cluster is close to reaching the configured maximum number of shards for data nodes. [_cluster_is_close_to_reaching_the_configured_maximum_number_of_shards_for_data_nodes]

The [`cluster.max_shards_per_node`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) cluster setting limits the maximum number of open shards for a cluster, only counting data nodes that do not belong to the frozen tier.

This symptom indicates that action should be taken, otherwise, either the creation of new indices or upgrading the cluster could be blocked.

If you’re confident your changes won’t destabilize the cluster, you can temporarily increase the limit using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings):

:::::::{tab-set}

::::::{tab-item} {{ech}}
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

4. Check the current status of the cluster according the shards capacity indicator:

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

5. Update the [`cluster.max_shards_per_node`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) setting with a proper value:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": 1200
      }
    }
    ```

    This increase should only be temporary. As a long-term solution, we recommend you add nodes to the oversharded data tier or [reduce your cluster’s shard count](../../deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count) on nodes that do not belong to the frozen tier.

6. To verify that the change has fixed the issue, you can get the current status of the `shards_capacity` indicator by checking the `data` section of the [health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report):

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

7. When a long-term solution is in place, we recommend you reset the `cluster.max_shards_per_node` limit.

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": null
      }
    }
    ```
::::::

::::::{tab-item} Self-managed
Check the current status of the cluster according the shards capacity indicator:

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
          "max_shards_in_cluster": 3000
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


Using the [`cluster settings API`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings), update the [`cluster.max_shards_per_node`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) setting:

```console
PUT _cluster/settings
{
  "persistent" : {
    "cluster.max_shards_per_node": 1200
  }
}
```

This increase should only be temporary. As a long-term solution, we recommend you add nodes to the oversharded data tier or [reduce your cluster’s shard count](../../deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count) on nodes that do not belong to the frozen tier. To verify that the change has fixed the issue, you can get the current status of the `shards_capacity` indicator by checking the `data` section of the [health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report):

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
          "max_shards_in_cluster": 1200
        },
        "frozen": {
          "max_shards_in_cluster": 3000
        }
      }
    }
  }
}
```

When a long-term solution is in place, we recommend you reset the `cluster.max_shards_per_node` limit.

```console
PUT _cluster/settings
{
  "persistent" : {
    "cluster.max_shards_per_node": null
  }
}
```
::::::

:::::::

## Cluster is close to reaching the configured maximum number of shards for frozen nodes. [_cluster_is_close_to_reaching_the_configured_maximum_number_of_shards_for_frozen_nodes]

The [`cluster.max_shards_per_node.frozen`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node-frozen) cluster setting limits the maximum number of open shards for a cluster, only counting data nodes that belong to the frozen tier.

This symptom indicates that action should be taken, otherwise, either the creation of new indices or upgrading the cluster could be blocked.

If you’re confident your changes won’t destabilize the cluster, you can temporarily increase the limit using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings):

:::::::{tab-set}

::::::{tab-item} {{ech}}
**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} ../../images/kibana-console.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

4. Check the current status of the cluster according the shards capacity indicator:

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

5. Update the [`cluster.max_shards_per_node.frozen`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node-frozen) setting:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node.frozen": 3200
      }
    }
    ```

    This increase should only be temporary. As a long-term solution, we recommend you add nodes to the oversharded data tier or [reduce your cluster’s shard count](../../deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count) on nodes that belong to the frozen tier.

6. To verify that the change has fixed the issue, you can get the current status of the `shards_capacity` indicator by checking the `data` section of the [health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report):

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

7. When a long-term solution is in place, we recommend you reset the `cluster.max_shards_per_node.frozen` limit.

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node.frozen": null
      }
    }
    ```
::::::

::::::{tab-item} Self-managed
Check the current status of the cluster according the shards capacity indicator:

```console
GET _health_report/shards_capacity
```

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

1. Current value of the setting `cluster.max_shards_per_node.frozen`.
2. Current number of open shards used by frozen nodes across the cluster.


Using the [`cluster settings API`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings), update the [`cluster.max_shards_per_node.frozen`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node-frozen) setting:

```console
PUT _cluster/settings
{
  "persistent" : {
    "cluster.max_shards_per_node.frozen": 3200
  }
}
```

This increase should only be temporary. As a long-term solution, we recommend you add nodes to the oversharded data tier or [reduce your cluster’s shard count](../../deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count) on nodes that belong to the frozen tier. To verify that the change has fixed the issue, you can get the current status of the `shards_capacity` indicator by checking the `data` section of the [health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report):

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

When a long-term solution is in place, we recommend you reset the `cluster.max_shards_per_node.frozen` limit.

```console
PUT _cluster/settings
{
  "persistent" : {
    "cluster.max_shards_per_node.frozen": null
  }
}
```
::::::

:::::::
::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::
