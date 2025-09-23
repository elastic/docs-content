---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-manage-storage.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Manage data storage [profiling-manage-storage]

Universal Profiling provides the following ways to manage how your data is stored.

* [Index lifecycle management](universal-profiling-index-life-cycle-management.md) automatically manages your indices according to age or size metric thresholds. Universal Profiling ships with a default index lifecycle policy, but you can create a custom policy to meet your requirements.
* [Probabilistic profiling](configure-probabilistic-profiling.md) mode uses representative samples of profiling data to reduce storage needs even further.

::::{important}
Additional storage efficiencies provided by [Synthetic `_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md) are available to users with an [appropriate license](https://www.elastic.co/subscriptions).

::::




