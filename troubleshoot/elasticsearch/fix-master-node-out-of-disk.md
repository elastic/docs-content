---
navigation_title: Master nodes out of disk
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-master-node-out-of-disk.html
---

% marciw move to new "out of disk" subsection

# Fix master nodes out of disk [fix-master-node-out-of-disk]

{{es}} is using master nodes to coordinate the cluster. If the master or any master eligible nodes are running out of space, you need to ensure that they have enough disk space to function. If the [health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report) reports that your master node is out of space you need to increase the disk capacity of your master nodes.

:::::::{tab-set}

::::::{tab-item} {{ech}}
1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the gear under the `Manage deployment` column that corresponds to the name of your deployment.
3. Go to `Actions > Edit deployment` and then go to the `Master instances` section:

    :::{image} ../../images/elasticsearch-reference-increase-disk-capacity-master-node.png
    :alt: Increase disk capacity of master nodes
    :class: screenshot
    :::

4. Choose a larger than the pre-selected capacity configuration from the drop-down menu and click `save`. Wait for the plan to be applied and the problem should be resolved.
::::::

::::::{tab-item} Self-managed
In order to increase the disk capacity of a master node, you will need to replace **all** the master nodes with master nodes of higher disk capacity.

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

2. The next step is to find out the current disk usage, this will allow to calculate how much extra space is needed. In the following example, we show only the master nodes for readability purposes:

    ```console
    GET /_cat/nodes?v&h=name,master,node.role,disk.used_percent,disk.used,disk.avail,disk.total
    ```

    The response will look like this:

    ```console-result
    name                master node.role disk.used_percent disk.used disk.avail disk.total
    instance-0000000000 *      m                    85.31    3.4gb     500mb       4gb
    instance-0000000001 *      m                    50.02    2.1gb     1.9gb       4gb
    instance-0000000002 *      m                    50.02    1.9gb     2.1gb       4gb
    ```

3. The desired situation is to drop the disk usages below the relevant threshold, in our example 90%. Consider adding some padding, so it will not go over the threshold soon. If you have multiple master nodes you need to ensure that **all** master nodes will have this capacity. Assuming you have the new nodes ready, follow the next three steps for every master node.
4. Bring down one of the master nodes.
5. Start up one of the new master nodes and wait for it to join the cluster. You can check this via:

    ```console
    GET /_cat/nodes?v&h=name,master,node.role,disk.used_percent,disk.used,disk.avail,disk.total
    ```

6. Only after you have confirmed that your cluster has the initial number of master nodes, move forward to the next one until all the initial master nodes have been replaced.
::::::

:::::::
