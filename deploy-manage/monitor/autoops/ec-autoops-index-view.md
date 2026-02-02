---
navigation_title: Indices
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-index-view.html
applies_to:
  deployment:
    ess: all
    self:
    ece:
    eck:
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Indices view in AutoOps [ec-autoops-index-view]

The **Indices** view provides detailed statistics for each {{es}} index in your deployment, allowing you to visualize index performance and trends to detect anomalies and optimize search efficiency. 

Information about each index is organized into a clear table with columns for the index's name, primary and total shards, indexing and search rate per second, and more. You can expand each index entry to dive deeper into real-time metrics.

To get to the **Indices** view, go to AutoOps in your deployment or cluster and select **Indices** from the side navigation.

:::{image} /deploy-manage/images/cloud-autoops-index-view.png
:screenshot:
:alt: Screenshot showing the Indices view in AutoOps
:::

## Metrics in the Indices view [ec-autoops-index-metrics]

The following table lists all the metrics available in the **Indices** view, along with a description of what each metric means. 

| Metric name | Description |
| --- | --- |
| Size | Total size of all primary shards of the index |
| Indexing rate | Number of documents being indexed per second on primary shards of the index |
| Search rate | Number of search requests being executed per second on all shards of the index |
| Document count | Total number of non-deleted documents in all primary shards of the index, including nested documents |
| Indexing latency | Average latency for indexing documents, which is the time it takes to index documents divided by the number that were indexed in primary shards of the index |
| Search latency | Average latency for searching, which is the time it takes to execute searches divided by the number of searches submitted to all shards of the index |
| Errors | Number of failed indexing operations for the index |
| Merge rate | Number of merge operations being executed per second on all primary shards of the index |

