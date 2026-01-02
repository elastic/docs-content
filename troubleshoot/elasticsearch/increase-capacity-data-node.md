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

:::::::{applies-switch}

::::::{applies-item} { ess:, ece: }

:::{warning}
:applies_to: ece:
In ECE, resizing is limited by your [allocator capacity](/deploy-manage/deploy/cloud-enterprise/ece-manage-capacity.md).
:::

To increase the disk capacity of the data nodes in your cluster:

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body) or ECE Cloud UI.
1. On the home page, find your deployment and select **Manage**.
1. Go to **Actions** > **Edit deployment** and check that autoscaling is enabled. Adjust the **Enable Autoscaling for** dropdown menu as needed and select **Save**.
1. If autoscaling is successful, the cluster returns to a `healthy` status.
If the cluster is still out of disk, check if autoscaling has reached its set limits and [update your autoscaling settings](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md#ec-autoscaling-update).
::::::

::::::{applies-item} { self: }
To increase the data node capacity in your cluster, you need to calculate the amount of extra disk space needed.

1. First, retrieve the relevant disk thresholds that will indicate how much space should be available. The relevant thresholds are the [high watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high) for all the tiers apart from the frozen one and the [frozen flood stage watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-flood-stage-frozen) for the frozen tier. The following example demonstrates disk shortage in the hot tier, so we will only retrieve the high watermark:

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

    The above means that in order to resolve the disk shortage we need to either drop our disk usage below the 90% or have more than 150GB available, read more on how this threshold works [here](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high).

1. The next step is to find out the current disk usage, this will indicate how much extra space is needed. For simplicity, our example has one node, but you can apply the same for every node over the relevant threshold.

    ```console
    GET _cat/allocation?v&s=disk.avail&h=node,disk.percent,disk.avail,disk.total,disk.used,disk.indices,shards
    ```

    The response will look like this:

    ```console-result
    node                disk.percent disk.avail disk.total disk.used disk.indices shards
    instance-0000000000           91     4.6gb       35gb    31.1gb       29.9gb    111
    ```

1. The high watermark configuration indicates that the disk usage needs to drop below 90%. To achieve this, 2 things are possible:

    * to add an extra data node to the cluster (this requires that you have more than one shard in your cluster), or
    * to extend the disk space of the current node by approximately 20% to allow this node to drop to 70%. This will give enough space to this node to not run out of space soon.

1. In the case of adding another data node, the cluster will not recover immediately. It might take some time to relocate some shards to the new node. You can check the progress here:

    ```console
    GET /_cat/shards?v&h=state,node&s=state
    ```

    If in the response the shards' state is `RELOCATING`, it means that shards are still moving. Wait until all shards turn to `STARTED` or until the health disk indicator turns to `green`.
::::::

::::::{applies-item}  { eck: }
To increase the disk capacity of data nodes in your {{eck}} cluster, you can either add more data nodes or increase the storage size of existing nodes.

**Option 1: Add more data nodes**

1. Update the `count` field in your data node NodeSet to add more nodes:

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      nodeSets:
      - name: data-nodes
        count: 5  # Increase from previous count
        config:
          node.roles: ["data"]
        volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 100Gi
    ```

1. Apply the changes:

    ```sh
    kubectl apply -f your-elasticsearch-manifest.yaml
    ```

    ECK automatically creates the new nodes and {{es}} will relocate shards to balance the load. You can monitor the progress using:

    ```console
    GET /_cat/shards?v&h=state,node&s=state
    ```

**Option 2: Increase storage size of existing nodes**

1. If your storage class supports [volume expansion](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims), you can increase the storage size in the `volumeClaimTemplates`:

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      nodeSets:
      - name: data-nodes
        count: 3
        config:
          node.roles: ["data"]
        volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 200Gi  # Increased from previous size
    ```

1. Apply the changes. If the volume driver supports `ExpandInUsePersistentVolumes`, the filesystem will be resized online without restarting {{es}}. Otherwise, you may need to manually delete the Pods after the resize so they can be recreated with the expanded filesystem.

For more information, refer to [](/deploy-manage/deploy/cloud-on-k8s/update-deployments.md) and [](/deploy-manage/deploy/cloud-on-k8s/volume-claim-templates.md).

::::::
:::::::