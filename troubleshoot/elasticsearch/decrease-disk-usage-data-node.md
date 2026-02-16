---
navigation_title: Decrease disk usage
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/decrease-disk-usage-data-node.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Decrease the disk usage of data nodes [decrease-disk-usage-data-node]

To decrease the disk usage in your cluster without losing any data, you can try reducing the replicas of indices.

::::{note}
Reducing the replicas of an index can potentially reduce search throughput and data redundancy. However, it can quickly give the cluster breathing room until a more permanent solution is in place.

Some permanent solutions you can investigate are: 
* Storing less frequently accessed data in [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), which require less disk space
* Increasing available disk space by [scaling up your cluster](/deploy-manage/production-guidance/scaling-considerations.md#how-to-scale)
* Deleting data that is no longer needed
::::


:::::::{tab-set}

::::::{tab-item} Using {{kib}}
1. Open your deployment’s side navigation menu and go to the **Index Management** page. You can find this page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the list of all your indices, click the `Replicas` column twice to sort the indices based on their number of replicas starting with the one that has the most. Go through the indices, and pick one by one the index with the least importance and higher number of replicas.

    ::::{warning}
    Reducing the replicas of an index can potentially reduce search throughput and data redundancy.
    ::::

3. For each index you chose, click on its name, then on the panel that appears click `Edit settings`, reduce the value of the `index.number_of_replicas` to the desired value and then click `Save`.

    :::{image} /troubleshoot/images/elasticsearch-reference-reduce_replicas.png
    :alt: Reducing replicas
    :screenshot:
    :::

4. Continue this process until the cluster is healthy again.
::::::

::::::{tab-item} Using the {{es}} API
To estimate how many replicas need to be removed, first you need to estimate the amount of disk space that needs to be released.

1. First, retrieve the relevant disk thresholds to determine how much space should be released. The relevant thresholds are the [high watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high) for all the tiers apart from the frozen one and the [frozen flood stage watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-flood-stage-frozen) for the frozen tier. The following example demonstrates disk shortage in the hot tier, so you can retrieve only the high watermark:

    ```console
    GET _cluster/settings?include_defaults&filter_path=*.cluster.routing.allocation.disk.watermark.high*
    ```

    The response looks like this:

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

    The above means that, to resolve the disk shortage, we need to either drop our disk usage below the 90% or have more than 150GB available, read more on how this threshold works [here](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high).

2. The next step is to find out the current disk usage; this indicates how much space should be freed. For simplicity, our example has one node, but you can apply the same for every node over the relevant threshold.

    ```console
    GET _cat/allocation?v&s=disk.avail&h=node,disk.percent,disk.avail,disk.total,disk.used,disk.indices,shards
    ```

    The response looks like this:

    ```console-result
    node                disk.percent disk.avail disk.total disk.used disk.indices shards
    instance-0000000000           91     4.6gb       35gb    31.1gb       29.9gb    111
    ```

3. The high watermark configuration indicates that the disk usage needs to drop below 90%. Consider padding the amount of disk space you make available, so the node doesn't immediately exceed the threshold again. In this example, let’s release approximately 7GB.
4. The next step is to list all the indices and choose which replicas to reduce.

    ::::{note}
    The following command lists indices in descending order by the number of replicas and primary store size. This can help you identify which replicas to reduce, based on the assumption that:

    * More replicas generally mean lower risk when removing a copy.
    * Larger replicas free up more disk space when removed.
    This is only a suggestion and does not account for any functional or business requirements. Review your cluster’s needs before making changes.
    ::::


    ```console
    GET _cat/indices?v&s=rep:desc,pri.store.size:desc&h=health,index,pri,rep,store.size,pri.store.size
    ```

    The response looks like:

    ```console-result
    health index                                                      pri rep store.size pri.store.size
    green  my_index                                                     2   3      9.9gb          3.3gb
    green  my_other_index                                               2   3      1.8gb        470.3mb
    green  search-products                                              2   3    278.5kb         69.6kb
    green  logs-000001                                                  1   0      7.7gb          7.7gb
    ```

5. Using the information returned by the API, we can determine that, if we reduce the replicas to one for the indices `my_index` and  `my_other_index`, the required disk space is released. It is not necessary to reduce the replicas of `search-products` and `logs-000001` does not have any replicas anyway. Reduce the replicas of one or more indices with the [index update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings):

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
