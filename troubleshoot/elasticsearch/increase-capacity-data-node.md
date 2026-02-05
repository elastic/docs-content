---
navigation_title: Increase disk capacity
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/increase-capacity-data-node.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Increase the disk capacity of data nodes [increase-capacity-data-node]

Disk capacity pressures may cause index failures, unassigned shards, and cluster instability. 

{{es}} uses [disk-based shard allocation watermarks](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation) to manage disk space on nodes, which can block allocation or indexing when nodes run low on disk space. Refer to [](/troubleshoot/elasticsearch/fix-watermark-errors.md) for additional details on how to address this situation.

To increase the disk capacity of the data nodes in your cluster, complete these steps:

1. [Estimate how much disk capacity you need](#estimate-required-capacity).
1. [Increase the disk capacity](#increase-disk-capacity-of-data-nodes).


## Estimate the amount of required disk capacity [estimate-required-capacity]

The following steps explain how to retrieve the current disk watermark configuration of the cluster and how to check the current disk usage on the nodes.

1. Retrieve the relevant disk thresholds that indicate how much space should be available. The relevant thresholds are the [high watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high) for all the tiers apart from the frozen one and the [frozen flood stage watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-flood-stage-frozen) for the frozen tier. The following example demonstrates disk shortage in the hot tier, so only the high watermark is retrieved:

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

    The above means that in order to resolve the disk shortage, disk usage must drop below the 90% or have more than 150GB available. Read more on how this threshold works [here](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high).

1. Find the current disk usage, which in turn indicates how much extra space is required. For simplicity, our example has one node, but you can apply the same for every node over the relevant threshold.

    ```console
    GET _cat/allocation?v&s=disk.avail&h=node,disk.percent,disk.avail,disk.total,disk.used,disk.indices,shards
    ```

    The response looks like this:

    ```console-result
    node                disk.percent disk.avail disk.total disk.used disk.indices shards
    instance-0000000000           91     4.6gb       35gb    31.1gb       29.9gb    111
    ```

In this scenario, the high watermark configuration indicates that the disk usage needs to drop below 90%, while the current disk usage is 91%.


## Increase the disk capacity of your data nodes [increase-disk-capacity-of-data-nodes]

Here are the most common ways to increase disk capacity:

* You can expand the disk space of the existing nodes. This is typically achieved by replacing your nodes with ones with higher capacity.
* You can add additional data nodes to the data tier that is short of disk space, increasing the overall capacity of that tier and potentially improving performance by distributing data and workload across more resources.

If in the response the shards' state is `RELOCATING`, it means that shards are still moving. Wait until all shards turn to `STARTED`.

To resize your deployment, follow the recommendations that apply to your deployment type:

:::{include} /troubleshoot/elasticsearch/_snippets/resize-your-deployment.md
:::


When you add another data node, the cluster doesn't recover immediately and it might take some time until shards are relocated to the new node. 
You can check the progress with the following API call:

```console
GET /_cat/shards?v&h=state,node&s=state
```