# Rolling up historical data [xpack-rollup]

::::{admonition} Deprecated in 8.11.0.
:class: warning

Rollups will be removed in a future version. Please [migrate](../../../manage-data/lifecycle/rollup/migrating-from-rollup-to-downsampling.md) to [downsampling](../../../manage-data/data-store/index-types/downsampling-time-series-data-stream.md) instead.
::::


Keeping historical data around for analysis is extremely useful but often avoided due to the financial cost of archiving massive amounts of data. Retention periods are thus driven by financial realities rather than by the usefulness of extensive historical data.

The {{stack}} {rollup-features} provide a means to summarize and store historical data so that it can still be used for analysis, but at a fraction of the storage cost of raw data.

* [Overview](../../../manage-data/lifecycle/rollup.md)
* [Getting started](../../../manage-data/lifecycle/rollup/getting-started-with-rollups.md)
* [API quick reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/rollup-api-quickref.html)
* [Understanding rollup grouping](../../../manage-data/lifecycle/rollup/understanding-groups.md)
* [Rollup aggregation limitations](../../../manage-data/lifecycle/rollup/rollup-aggregation-limitations.md)
* [Rollup search limitations](../../../manage-data/lifecycle/rollup/rollup-search-limitations.md)
* [Migrating to downsampling](../../../manage-data/lifecycle/rollup/migrating-from-rollup-to-downsampling.md)








