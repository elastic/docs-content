# JVM heap usage exceeds the allowed threshold on master nodes [ech-jvm-heap-usage-exceed-allowed-threshold]

**Health check**

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the {{es}} Service panel, click the **Quick link** icon corresponding to the deployment that you want to manage.

    :::{image} ../../../images/cloud-heroku-ec-quick-link-to-deployment.png
    :alt: Quick link to the deployment page
    :::

3. On your deployment page, scroll down to **Instances** and check if the JVM memory pressure for your {{es}} instances is high.

    :::{image} ../../../images/cloud-heroku-ec-deployment-instances-config.png
    :alt: Deployment instances configuration
    :::


**Possible causes**

* The master node is overwhelmed by a large number of snapshots or shards.

    * External tasks initiated by clients

        * Index, search, update
        * Frequent template updates due to the Beats configuration

    * Internal tasks initiated by users

        * Machine Learning jobs, watches, monitoring, ingest pipeline

    * Internal tasks initiated by {es}

        * Nodes joining and leaving due to hardware failures
        * Shard allocation due to nodes joining and leaving
        * Configuration of ILM policies.


**Resolutions**

* If the master node is overwhelmed by external tasks initiated by clients:

    Investigate which clients might be overwhelming the cluster and reduce the request rate or pause ingesting, searching, or updating from the client. If you are using Beats, temporarily stop the Beat that’s overwhelming the cluster to avoid frequent template updates.

* If the master node is overwhelmed by internal tasks initiated by users:

    * Check [cluster-level pending tasks](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-pending-tasks.html).
    * Reduce the number of Machine Learning jobs or watches.
    * Change the number of ingest pipelines or processors to use less memory.

* If the master node is overwhelmed by internal tasks initiated by {{es}}:

    * For nodes joining and leaving, this should resolve itself. If increasing the master nodes size doesn’t resolve the issue, contact support.
    * For shard allocation, inspect the progress of shards recovery.

        * Make sure `indices.recovery.max_concurrent_operations` is not aggressive, which could cause the master to be unavailable.
        * Make sure `indices.recovery.max_bytes_per_sec` is set adequately to avoid impact on ingest and search workload.

    * Check ILM policies to avoid index rollover and relocate actions that are concurrent and aggressive.

* If the master node is overwhelmed by a large number of snapshots, reduce the number of snapshots in the repo.
* If the master node is overwhelmed by a large number of shards, delete unneeded indices and shrink read-only indices to fewer shards. For more information, check [Reduce a cluster’s shard count](../../../deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count).

