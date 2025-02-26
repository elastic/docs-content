---
navigation_title: Other nodes out of disk
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-other-node-out-of-disk.html
---

% marciw move to new "out of disk" subsection

# Fix other role nodes out of disk [fix-other-node-out-of-disk]

{{es}} can use dedicated nodes to execute other functions apart from storing data or coordinating the cluster, for example machine learning. If one or more of these nodes are running out of space, you need to ensure that they have enough disk space to function. If the [health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report) reports that a node that is not a master and does not contain data is out of space you need to increase the disk capacity of this node.

:::::::{tab-set}

::::::{tab-item} {{ech}}
1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the gear under the `Manage deployment` column that corresponds to the name of your deployment.
3. Go to `Actions > Edit deployment` and then go to the `Coordinating instances` or the `Machine Learning instances` section depending on the roles listed in the diagnosis:

    :::{image} ../../images/elasticsearch-reference-increase-disk-capacity-other-node.png
    :alt: Increase disk capacity of other nodes
    :class: screenshot
    :::

4. Choose a larger than the pre-selected capacity configuration from the drop-down menu and click `save`. Wait for the plan to be applied and the problem should be resolved.
::::::

::::::{tab-item} Self-managed
In order to increase the disk capacity of any other node, you will need to replace the instance that has run out of space with one of higher disk capacity.

1. First, retrieve the disk threshold that will indicate how much disk space is needed. The relevant threshold is the [high watermark](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high) and can be retrieved via the following command:

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
    ```

    The above means that in order to resolve the disk shortage we need to either drop our disk usage below the 90% or have more than 150GB available, read more how this threshold works [here](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high).

2. The next step is to find out the current disk usage, this will allow to calculate how much extra space is needed. In the following example, we show only a machine learning node for readability purposes:

    ```console
    GET /_cat/nodes?v&h=name,node.role,disk.used_percent,disk.used,disk.avail,disk.total
    ```

    The response will look like this:

    ```console-result
    name                node.role disk.used_percent disk.used disk.avail disk.total
    instance-0000000000     l                 85.31    3.4gb     500mb       4gb
    ```

3. The desired situation is to drop the disk usage below the relevant threshold, in our example 90%. Consider adding some padding, so it will not go over the threshold soon. Assuming you have the new node ready, add this node to the cluster.
4. Verify that the new node has joined the cluster:

    ```console
    GET /_cat/nodes?v&h=name,node.role,disk.used_percent,disk.used,disk.avail,disk.total
    ```

    The response will look like this:

    ```console-result
    name                node.role disk.used_percent disk.used disk.avail disk.total
    instance-0000000000     l                 85.31    3.4gb     500mb       4gb
    instance-0000000001     l                 41.31    3.4gb     4.5gb       8gb
    ```

5. Now you can remove the out of disk space instance.
::::::

:::::::
