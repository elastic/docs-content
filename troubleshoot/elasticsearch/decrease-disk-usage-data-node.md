---
navigation_title: Decrease disk usage
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/decrease-disk-usage-data-node.html
---

# Decrease the disk usage of data nodes [decrease-disk-usage-data-node]

In order to decrease the disk usage in your cluster without losing any data, you can try reducing the replicas of indices.

::::{note}
Reducing the replicas of an index can potentially reduce search throughput and data redundancy. However, it can quickly give the cluster breathing room until a more permanent solution is in place.
::::


:::::::{tab-set}

::::::{tab-item} {{ech}}
**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Stack Management > Index Management**.
4. In the list of all your indices, click the `Replicas` column twice to sort the indices based on their number of replicas starting with the one that has the most. Go through the indices and pick one by one the index with the least importance and higher number of replicas.

    ::::{warning}
    Reducing the replicas of an index can potentially reduce search throughput and data redundancy.
    ::::

5. For each index you chose, click on its name, then on the panel that appears click `Edit settings`, reduce the value of the `index.number_of_replicas` to the desired value and then click `Save`.

    :::{image} ../../images/elasticsearch-reference-reduce_replicas.png
    :alt: Reducing replicas
    :class: screenshot
    :::

6. Continue this process until the cluster is healthy again.
::::::

::::::{tab-item} Self-managed
In order to estimate how many replicas need to be removed, first you need to estimate the amount of disk space that needs to be released.

1. First, retrieve the relevant disk thresholds that will indicate how much space should be released. The relevant thresholds are the [high watermark](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high) for all the tiers apart from the frozen one and the [frozen flood stage watermark](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-flood-stage-frozen) for the frozen tier. The following example demonstrates disk shortage in the hot tier, so we will only retrieve the high watermark:

    ```console
    GET _cluster/settings?include_defaults&filter_path=*.cluster.routing.allocation.disk.watermark.high*
    ```

    The response will look like this:

    ```console-result
    {
      "defaults": {
        "cluster": {
          "routing": {
            "allocation": {
              "disk": {
                "watermark": {
                  "high": "90%",
                  "high.max_headroom": "150GB"
                }
              }
            }
          }
        }
      }
    }
    ```

    The above means that in order to resolve the disk shortage we need to either drop our disk usage below the 90% or have more than 150GB available, read more on how this threshold works [here](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high).

2. The next step is to find out the current disk usage; this will indicate how much space should be freed. For simplicity, our example has one node, but you can apply the same for every node over the relevant threshold.

    ```console
    GET _cat/allocation?v&s=disk.avail&h=node,disk.percent,disk.avail,disk.total,disk.used,disk.indices,shards
    ```

    The response will look like this:

    ```console-result
    node                disk.percent disk.avail disk.total disk.used disk.indices shards
    instance-0000000000           91     4.6gb       35gb    31.1gb       29.9gb    111
    ```

3. The high watermark configuration indicates that the disk usage needs to drop below 90%. Consider allowing some padding, so the node will not go over the threshold in the near future. In this example, let’s release approximately 7GB.
4. The next step is to list all the indices and choose which replicas to reduce.

    ::::{note}
    The following command orders the indices with descending number of replicas and primary store size. We do this to help you choose which replicas to reduce under the assumption that the more replicas you have the smaller the risk if you remove a copy and the bigger the replica the more space will be released. This does not take into consideration any functional requirements, so please see it as a mere suggestion.
    ::::


    ```console
    GET _cat/indices?v&s=rep:desc,pri.store.size:desc&h=health,index,pri,rep,store.size,pri.store.size
    ```

    The response will look like:

    ```console-result
    health index                                                      pri rep store.size pri.store.size
    green  my_index                                                     2   3      9.9gb          3.3gb
    green  my_other_index                                               2   3      1.8gb        470.3mb
    green  search-products                                              2   3    278.5kb         69.6kb
    green  logs-000001                                                  1   0      7.7gb          7.7gb
    ```

5. In the list above we see that if we reduce the replicas to 1 of the indices `my_index` and  `my_other_index` we will release the required disk space. It is not necessary to reduce the replicas of `search-products` and `logs-000001` does not have any replicas anyway. Reduce the replicas of one or more indices with the [index update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings):

    ::::{warning}
    Reducing the replicas of an index can potentially reduce search throughput and data redundancy.
    ::::


    ```console
    PUT my_index,my_other_index/_settings
    {
      "index.number_of_replicas": 1
    }
    ```
::::::

:::::::
