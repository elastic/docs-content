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

The **Indices** view provides detailed statistics for each {{es}} index in your deployment.

:::{image} /deploy-manage/images/cloud-autoops-index-view.png
:alt: The Indices view
:::

The **Indices** view is essential for monitoring {{es}} indices, and offers comprehensive insights at a glance by displaying a clear and informative table about the following metrics:

* Index Name
* Primary Shards and Total Shards
* Shard Size
* Size in Bytes
* Doc Count
* Indexing Rate/Sec
* Search Rate/Sec
* Index Latency
* Search Latency

You can expand each index entry to dive deeper into real-time metrics. This is an intuitive and dynamic feature that allows you to visualize index activities and trends, in order to detect anomalies and optimize search efficiency.

The **Indices** view offers you a powerful tool for managing and optimizing your {{es}} indices. By providing a detailed and up-to-date overview of index performance and usage, AutoOps ensures that your search and indexing operations run smoothly and efficiently.


## Index metrics [ec-autoops-index-metrics]

| Metrics name | Metrics description |
| --- | --- |
| Size | Total size of all primary shards of the index |
| Indexing rate | Number of documents being indexed per second on primary shards of the index |
| Search rate | Number of search requests being executed per second on all shards of the index |
| Document count | Total number of non-deleted documents in all primary shards of the index, including nested documents |
| Indexing latency | Average latency for indexing documents, which is the time it takes to index documents divided by the number that were indexed in primary shards of the index |
| Search latency | Average latency for searching, which is the time it takes to execute searches divided by the number of searches submitted to all shards of the index |
| Errors | Number of failed indexing operations for the index |
| Merge rate | Number of merge operations being executed per second on all primary shards of the index |

