---
navigation_title: ILM tutorials
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# {{ilm-cap}} tutorials

A collection of tutorials is available to help you control the lifecycle of your data using {{ilm}}.

## Configuring rollover

When you continuously index timestamped documents into {{es}}, you typically use a [data stream](../../data-store/data-streams.md) so you can periodically [roll over](rollover.md) to a new index. This enables you to implement a [hot-warm-cold architecture](../data-tiers.md) to meet the performance requirements for your newest data, control costs over time, enforce retention policies, and still get the most out of your data.

To simplify index management and automate rollover, select one of the scenarios that best applies to your situation:

* **Roll over data streams with ILM.** When ingesting write-once, timestamped data that doesn't change, follow the steps in [](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md) for simple, automated data stream rollover. ILM-managed backing indices are automatically created under a single data stream alias. ILM also tracks and transitions the backing indices through the lifecycle automatically. 
* **Roll over time series indices with ILM.** Data streams are best suited for [append-only](../../data-store/data-streams.md#data-streams-append-only) use cases. If you need to update or delete existing time series data, you can perform update or delete operations directly on the data stream backing index. If you frequently send multiple documents using the same `_id` expecting last-write-wins, you may want to use an index alias with a write index instead. You can still use {{ilm-init}} to manage and roll over the alias’s indices. Follow the steps in [](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md) for more information.
* **Roll over general content as data streams with ILM.** If some of your indices store data that isn't timestamped, but you would like to get the benefits of automatic rotation when the index reaches a certain size or age, or delete already rotated indices after a certain amount of time, follow the steps in [](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md). These steps include injecting a timestamp field during indexing time to mimic time series data.

## Customizing a built-in {{ilm-init}} policy

When your data streams have been set up automatically, for example when you're ingesting data by means of an [Elastic integration](https://docs.elastic.co/en/integrations), the data is typically managed using a built-in {{ilm-init}} policy. To customize the lifecycle policy for managed indices, refer to: [](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md).

