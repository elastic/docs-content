---
navigation_title: {{ilm-init}} automation tutorials
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# {{ilm-cap}} automation tutorials

A collection of tutorials is available to help you control the lifecycle of your data using {{ilm}}.

## Configuring rollover


{{ilm}} ({{ilm-init}}) in {{es}} is a powerful feature that helps automate the management of your indices through their entire lifecycle — from creation to rollover, to retention and deletion. Whether you're handling large volumes of time series data or general content, {{ilm-init}} enables you to optimize performance, control storage costs, and enforce data retention policies with ease. These tutorials guide you step-by-step through setting up {{ilm-init}} policies, configuring automated rollover, and monitoring your indices, so you can efficiently manage your {{es}} data lifecycle.

When you continuously index timestamped documents into {{es}}, you typically use a [data stream](../../data-store/data-streams.md) so you can periodically [roll over](rollover.md) to a new index. To simplify index management and automate rollover, select one of the scenarios that best applies to your situation:

* **Roll over data streams with ILM.** When ingesting write-once, timestamped data that doesn't change, follow the steps in [](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md) for simple, automated data stream rollover. ILM-managed backing indices are automatically created under a single data stream alias. ILM also tracks and transitions the backing indices through the lifecycle automatically. 
* **Roll over time series indices with ILM.** Data streams are best suited for [append-only](../../data-store/data-streams.md#data-streams-append-only) use cases. If you need to update or delete existing time series data, you can perform update or delete operations directly on the data stream backing index. If you frequently send multiple documents using the same `_id` expecting last-write-wins, you may want to use an index alias with a write index instead. You can still use {{ilm-init}} to manage and roll over the alias’s indices. Follow the steps in [](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md) for more information.
* **Roll over general content as data streams with ILM.** If some of your indices store data that isn't timestamped, but you would like to get the benefits of automatic rotation when the index reaches a certain size or age, or delete already rotated indices after a certain amount of time, follow the steps in [](/manage-data/lifecycle/index-lifecycle-management/tutorial-general-content-with-data-streams.md). These steps include injecting a timestamp field during indexing time to mimic time series data.

## Customizing a built-in {{ilm-init}} policy

When your data streams have been set up automatically, for example when you're ingesting data by means of an [Elastic integration](https://docs.elastic.co/en/integrations), the data is typically managed using a built-in {{ilm-init}} policy. To customize the lifecycle policy for managed indices, refer to: [](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md).

