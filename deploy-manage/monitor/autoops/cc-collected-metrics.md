---
applies_to:
  deployment:
    self:
navigation_title: Collected metrics
---

# Collected metrics

When you connect your self-managed cluster to AutoOps on Elastic Cloud, the following metrics are collected:

| API | Description | Collected data |
| --- | --- | --- |
| [_cat/shards](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards) | Returns detailed information about the shards within the cluster | Shard states, node allocation, index names, sizes, and replica information |
| [_nodes/stats](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats) | Retrieves statistics from cluster nodes including JVM, OS, process, and transport metrics | CPU usage, memory utilization, thread pools, file system stats |
| [_cluster/settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) | Returns the settings configured for the cluster | Persistent and transient settings such as cluster-wide configurations |
| [_cluster/health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) | Provides information about the overall health of the cluster | Status (green/yellow/red), number of nodes, number of shards |
| [_cat/template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-templates) | Lists all index templates in the cluster | Template names, patterns, and basic settings |
| [_index_template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-templates) | Retrieves composable index templates | Index settings, mappings, and aliases |
| [_component_template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-component-template) | Fetches component templates used for building index templates | Metadata for re-usable mappings and settings |
| [_tasks](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks) | Displays information about currently running tasks on the cluster | Task descriptions, start times, running nodes, and execution details |
| [_template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-template) | Retrieves legacy index templates | Similar to composable index templates but in older format |
| [_resolve/index/*](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-resolve-index) | Resolves index, data stream, and alias names to their current definitions | Mappings between names and underlying data objects |