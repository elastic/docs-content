---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-rollup.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rollup-overview.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
---

# Rollup

::::{admonition} Deprecated in 8.11.0.
:class: warning

Rollups will be removed in a future version. [Migrate](/manage-data/lifecycle/rollup/migrating-from-rollup-to-downsampling.md) to [downsampling](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) instead.
::::

Keeping historical data around for analysis is extremely useful but often avoided due to the financial cost of archiving massive amounts of data. For example, your system may be generating 500 documents every second. That will generate 43 million documents per day, and nearly 16 billion documents a year. Retention periods are thus driven by financial realities rather than by the usefulness of extensive historical data.

While your analysts and data scientists may wish you stored that data indefinitely for analysis, time is never-ending and so your storage requirements will continue to grow without bound. Retention policies are therefore often dictated by the simple calculation of storage costs over time, and what the organization is willing to pay to retain historical data. Often these policies start deleting data after a few months or years.

Storage cost is a fixed quantity. It takes X money to store Y data. But the utility of a piece of data often changes with time. Sensor data gathered at millisecond granularity is extremely useful right now, reasonably useful if from a few weeks ago, and only marginally useful if older than a few months.

So while the cost of storing a millisecond of sensor data from ten years ago is fixed, the value of that individual sensor reading often diminishes with time. It’s not useless — it could easily contribute to a useful analysis — but it’s reduced value often leads to deletion rather than paying the fixed storage cost.


## Rollup stores historical data at reduced granularity [_rollup_stores_historical_data_at_reduced_granularity]

That’s where Rollup comes into play. The Rollup functionality summarizes old, high-granularity data into a reduced granularity format for long-term storage. By "rolling" the data up into a single summary document, historical data can be compressed greatly compared to the raw data.

For example, consider the system that’s generating 43 million documents every day. The second-by-second data is useful for real-time analysis, but historical analysis looking over ten years of data are likely to be working at a larger interval such as hourly or daily trends.

If we compress the 43 million documents into hourly summaries, we can save vast amounts of space. The Rollup feature automates this process of summarizing historical data.

Details about setting up and configuring Rollup are covered in [Create Job API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rollup-put-job).


## Rollup uses standard Query DSL [_rollup_uses_standard_query_dsl]

The Rollup feature exposes a new search endpoint (`/_rollup_search` vs the standard `/_search`) which knows how to search over rolled-up data. Importantly, this endpoint accepts 100% normal {{es}} Query DSL. Your application does not need to learn a new DSL to inspect historical data, it can simply reuse existing queries and dashboards.

There are some limitations to the functionality available; not all queries and aggregations are supported, certain search features (highlighting, etc) are disabled, and available fields depend on how the rollup was configured. These limitations are covered more in [Rollup Search limitations](/manage-data/lifecycle/rollup/rollup-search-limitations.md).

But if your queries, aggregations and dashboards only use the available functionality, redirecting them to historical data is trivial.


## Rollup merges "live" and "rolled" data [_rollup_merges_live_and_rolled_data]

A useful feature of Rollup is the ability to query both "live", realtime data in addition to historical "rolled" data in a single query.

For example, your system may keep a month of raw data. After a month, it is rolled up into historical summaries using Rollup and the raw data is deleted.

If you were to query the raw data, you’d only see the most recent month. And if you were to query the rolled up data, you would only see data older than a month. The RollupSearch endpoint, however, supports querying both at the same time. It will take the results from both data sources and merge them together. If there is overlap between the "live" and "rolled" data, live data is preferred to increase accuracy.


## Rollup is multi-interval aware [_rollup_is_multi_interval_aware]

Finally, Rollup is capable of intelligently utilizing the best interval available. If you’ve worked with summarizing features of other products, you’ll find that they can be limiting. If you configure rollups at daily intervals…  your queries and charts can only work with daily intervals. If you need a monthly interval, you have to create another rollup that explicitly stores monthly averages, etc.

The Rollup feature stores data in such a way that queries can identify the smallest available interval and use that for their processing. If you store rollups at a daily interval, queries can be executed on daily or longer intervals (weekly, monthly, etc) without the need to explicitly configure a new rollup job. This helps alleviate one of the major disadvantages of a rollup system; reduced flexibility relative to raw data.
