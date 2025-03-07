---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/restart-cluster.html
applies_to:
  deployment:
     self:
---

# Full Cluster restart and rolling restart procedures [restart-cluster]

There may be [situations where you want to perform a full-cluster restart](../../security/secure-cluster-communications.md) or a rolling restart. In the case of [full-cluster restart](#restart-cluster-full), you shut down and restart all the nodes in the cluster while in the case of [rolling restart](#restart-cluster-rolling), you shut down only one node at a time, so the service remains uninterrupted.

::::{warning}
Nodes exceeding the low watermark threshold will be slow to restart. Reduce the disk usage below the [low watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-low) before restarting nodes.

::::

## Full-cluster restart [restart-cluster-full]

1. **Disable shard allocation.**
   When you shut down a data node, the allocation process waits for `index.unassigned.node_left.delayed_timeout` (by default, one minute) before starting to replicate the shards on that node to other nodes in the cluster, which can involve a lot of I/O. Since the node is shortly going to be restarted, this I/O is unnecessary. You can avoid racing the clock by [disabling allocation](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) of replicas before shutting down [data nodes](../../distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role):

   ```console
   PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": "primaries"
      }
    }
   ```

   You can also consider [gateway settings](elasticsearch://reference/elasticsearch/configuration-reference/local-gateway.md) when restarting large clusters to reduce initial strain while nodes are processing [through discovery](../../distributed-architecture/discovery-cluster-formation.md).

2. **Stop indexing and perform a flush.**
   Performing a [flush](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-flush) speeds up shard recovery.

   ```console
   POST /_flush
   ```

3. **Temporarily stop the tasks associated with active {{ml}} jobs and {{dfeeds}}.** (Optional)

    {{ml-cap}} features require specific [subscriptions](https://www.elastic.co/subscriptions).

    You have two options to handle {{ml}} jobs and {{dfeeds}} when you shut down a cluster:

    * Temporarily halt the tasks associated with your {{ml}} jobs and {{dfeeds}} and prevent new jobs from opening by using the [set upgrade mode API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-set-upgrade-mode):

        ```console
        POST _ml/set_upgrade_mode?enabled=true
        ```

        When you disable upgrade mode, the jobs resume using the last model state that was automatically saved. This option avoids the overhead of managing active jobs during the shutdown and is faster than explicitly stopping {{dfeeds}} and closing jobs.

    * [Stop all {{dfeeds}} and close all jobs](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-close-job). This option saves the model state at the time of closure. When you reopen the jobs after the cluster restart, they use the exact same model. However, saving the latest model state takes longer than using upgrade mode, especially if you have a lot of jobs or jobs with large model states.

4. **Shut down all nodes.**

    * If you are running {{es}} with `systemd`:

        ```sh
        sudo systemctl stop elasticsearch.service
        ```

    * If you are running {{es}} with SysV `init`:

        ```sh
        sudo -i service elasticsearch stop
        ```

    * If you are running {{es}} as a daemon:

        ```sh
        kill $(cat pid)
        ```

5. **Perform any needed changes.**
6. **Restart nodes.**
   If you have dedicated master nodes, start them first and wait for them to form a cluster and elect a master before proceeding with your data nodes. You can check progress by looking at the logs.
   As soon as enough master-eligible nodes have discovered each other, they form a cluster and elect a master. At that point, you can use the [cat health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-health) and [cat nodes](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) APIs to monitor nodes joining the cluster:

    ```console
    GET _cat/health

    GET _cat/nodes
    ```
    %  TEST[continued]

   The `status` column returned by `_cat/health` shows the health of each node in the cluster: `red`, `yellow`, or `green`.

7. **Wait for all nodes to join the cluster and report a status of yellow.**
   When a node joins the cluster, it begins to recover any primary shards that are stored locally. The [`_cat/health`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-health) API initially reports a `status` of `red`, indicating that not all primary shards have been allocated.
   Once a node recovers its local shards, the cluster `status` switches to `yellow`, indicating that all primary shards have been recovered, but not all replica shards are allocated. This is to be expected because you have not yet re-enabled allocation. Delaying the allocation of replicas until all nodes are `yellow` allows the master to allocate replicas to nodes that already have local shard copies.

8. **Re-enable allocation.**
   When all nodes have joined the cluster and recovered their primary shards, re-enable allocation by restoring `cluster.routing.allocation.enable` to its default:

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": null
      }
    }
    ```

   Once allocation is re-enabled, the cluster starts allocating replica shards to the data nodes. At this point it is safe to resume indexing and searching, but your cluster will recover more quickly if you can wait until all primary and replica shards have been successfully allocated and the status of all nodes is `green`.
   You can monitor progress with the [`_cat/health`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-health) and [`_cat/recovery`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery) APIs:

    ```console
    GET _cat/health

    GET _cat/recovery
    ```

9. **Restart machine learning jobs.** (Optional)
   If you temporarily halted the tasks associated with your {{ml}} jobs, use the [set upgrade mode API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-set-upgrade-mode) to return them to active states:

    ```console
    POST _ml/set_upgrade_mode?enabled=false
    ```
    %  TEST[continued]

   If you closed all {{ml}} jobs before stopping the nodes, open the jobs and start the datafeeds from {{kib}} or with the [open jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-open-job) and [start datafeed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-datafeed) APIs.

## Rolling restart [restart-cluster-rolling]

1. **Disable shard allocation.**
   When you shut down a data node, the allocation process waits for `index.unassigned.node_left.delayed_timeout` (by default, one minute) before starting to replicate the shards on that node to other nodes in the cluster, which can involve a lot of I/O. Since the node is shortly going to be restarted, this I/O is unnecessary. You can avoid racing the clock by [disabling allocation](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) of replicas before shutting down [data nodes](../../distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role):

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": "primaries"
      }
    }
    ```

   You can also consider [gateway settings](elasticsearch://reference/elasticsearch/configuration-reference/local-gateway.md) when restarting large clusters to reduce initial strain while nodes are processing [through discovery](../../distributed-architecture/discovery-cluster-formation.md).

2. **Stop non-essential indexing and perform a flush.** (Optional)
   While you can continue indexing during the rolling restart, shard recovery can be faster if you temporarily stop non-essential indexing and perform a [flush](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-flush).

    ```console
    POST /_flush
    ```

3. **Temporarily stop the tasks associated with active {{ml}} jobs and {{dfeeds}}.** (Optional)
   {{ml-cap}} features require specific [subscriptions](https://www.elastic.co/subscriptions).
   You have two options to handle {{ml}} jobs and {{dfeeds}} when you shut down a cluster:
      * Temporarily halt the tasks associated with your {{ml}} jobs and {{dfeeds}} and prevent new jobs from opening by using the [set upgrade mode API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-set-upgrade-mode):

        ```console
        POST _ml/set_upgrade_mode?enabled=true
        ```

      When you disable upgrade mode, the jobs resume using the last model state that was automatically saved. This option avoids the overhead of managing active jobs during the shutdown and is faster than explicitly stopping {{dfeeds}} and closing jobs.

      * [Stop all {{dfeeds}} and close all jobs](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-close-job). This option saves the model state at the time of closure. When you reopen the jobs after the cluster restart, they use the exact same model. However, saving the latest model state takes longer than using upgrade mode, especially if you have a lot of jobs or jobs with large model states.

      * If you perform a rolling restart, you can also leave your machine learning jobs running. When you shut down a machine learning node, its jobs automatically move to another node and restore the model states. This option enables your jobs to continue running during the shutdown but it puts increased load on the cluster.

4. **Shut down a single node in case of rolling restart.**

    * If you are running {{es}} with `systemd`:

        ```sh
        sudo systemctl stop elasticsearch.service
        ```

    * If you are running {{es}} with SysV `init`:

        ```sh
        sudo -i service elasticsearch stop
        ```

    * If you are running {{es}} as a daemon:

        ```sh
        kill $(cat pid)
        ```

5. **Perform any needed changes.**
6. **Restart the node you changed.**
   Start the node and confirm that it joins the cluster by checking the log file or by submitting a `_cat/nodes` request:

    ```console
    GET _cat/nodes
    ```

7. **Reenable shard allocation.**
   For data nodes, once the node has joined the cluster, remove the `cluster.routing.allocation.enable` setting to enable shard allocation and start using the node:

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": null
      }
    }
    ```

8. **Repeat in case of rolling restart.**
   When the node has recovered and the cluster is stable, repeat these steps for each node that needs to be changed.

9. **Restart machine learning jobs.** (Optional)
   If you temporarily halted the tasks associated with your {{ml}} jobs, use the [set upgrade mode API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-set-upgrade-mode) to return them to active states:

    ```console
    POST _ml/set_upgrade_mode?enabled=false
    ```
    %  TEST[continued]

   If you closed all {{ml}} jobs before stopping the nodes, open the jobs and start the datafeeds from {{kib}} or with the [open jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-open-job) and [start datafeed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-datafeed) APIs.
