---
navigation_title: Shards
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-shards-view.html
applies_to:
  stack:
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Shards view in AutoOps [ec-autoops-shards-view]

The **Shards** view allows you to monitor the shards allocated to each node in your cluster. With this granular view into your cluster's health, you can get to the root cause of issues and resolve them to ensure optimal performance and reliability of your search and indexing operations.

Use the **Deployment** or **Cluster** dropdown at the top of the screen to select which deployment or cluster you want to view, and use the controls on the right side of the screen to drill down on specific nodes, indices, metrics, and time ranges.

:::{image} /deploy-manage/images/cloud-autoops-shard-view.png
:screenshot:
:alt: Screenshot showing the Shards view in AutoOps
:::

To get to the **Shards** view, go to AutoOps in your deployment or cluster and select **Shards** from the side navigation.

The **Shards** view provides the following insights:

* **Detailed shard breakdown**: Gain insights into each shard with a granular breakdown. View stats for shards from specific indices on any given node, allowing for in-depth performance and distribution analysis.
* **Size information**: Assess the storage footprint of each shard with precise size metrics, facilitating efficient resource management.
* **Document count**: Monitor the number of documents contained within each shard to track and manage the shard load effectively.
* **Indexing rate and latency**: Keep an eye on indexing performance with real-time indexing rates and latencies. This ensures efficient and timely data indexing, helping maintain optimal performance.
* **Search rate and latency**: Optimize search functionalities by monitoring search rates and latencies. This ensures your search queries are processed quickly and effectively.

## Metrics in the Shards view

Use the metrics dropdown to view shard information sorted by different metrics. Select from the following:

* Indexing Latency
* Indexing Rate
* Merge Latency
* Merge Rate
* Search Latency
* Search Rate
* Size in Bytes

You can also use the time slider at the top of the screen to move forward and backward and observe how shards data changes over time.

