---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-storage-guide.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Storage and sizing guide [apm-storage-guide]

APM processing and storage costs are largely dominated by transactions, spans, and stack frames.

* [**Transactions**](/solutions/observability/apm/transactions.md) describe an event captured by an Elastic {{apm-agent}} instrumenting a service. They are the highest level of work being measuring within a service.
* [**Spans**](/solutions/observability/apm/spans.md) belong to transactions. They measure from the start to end of an activity, and contain information about a specific code path that has been executed.
* **Stack frames** belong to spans. Stack frames represent a function call on the call stack, and include attributes like function name, file name and path, line number, etc. Stack frames can heavily influence the size of a span.

## Typical transactions [_typical_transactions]

Due to the high variability of APM data, it’s difficult to classify a transaction as typical. Regardless, this guide will attempt to classify Transactions as *Small*, *Medium*, or *Large*, and make recommendations based on those classifications.

The size of a transaction depends on the language, agent settings, and what services the agent instruments. For instance, an agent auto-instrumenting a service with a popular tech stack (web framework, database, caching library, etc.) is more likely to generate bigger transactions.

In addition, all agents support manual instrumentation. How little or much you use these APIs will also impact what a typical transaction looks like.

If your sampling rate is very small, transactions will be the dominate storage cost.

Here’s a speculative reference:

| Transaction size | Number of Spans | Number of stack frames |
| --- | --- | --- |
| *Small* | 5-10 | 5-10 |
| *Medium* | 15-20 | 15-20 |
| *Large* | 30-40 | 30-40 |

There will always be transaction outliers with hundreds of spans or stack frames, but those are very rare. Small transactions are the most common.

## Typical storage [_typical_storage]

Consider the following typical storage reference. These numbers do not account for {{es}} compression.

* 1 unsampled transaction is **~1 KB**
* 1 span with 10 stack frames is **~4 KB**
* 1 span with 50 stack frames is **~20 KB**
* 1 transaction with 10 spans, each with 10 stack frames is **~50 KB**
* 1 transaction with 25 spans, each with 25 spans is **250-300 KB**
* 100 transactions with 10 spans, each with 10 stack frames, sampled at 90% is **600 KB**

APM data compresses quite well, so the storage cost in {{es}} will be considerably less:

* Indexing 100 unsampled transactions per second for 1 hour results in 360,000 documents. These documents use around **50 MB** of disk space.
* Indexing 10 transactions per second for 1 hour, each transaction with 10 spans, each span with 10 stack frames, results in 396,000 documents. These documents use around **200 MB** of disk space.
* Indexing 25 transactions per second for 1 hour, each transaction with 25 spans, each span with 25 stack frames, results in 2,340,000 documents. These documents use around **1.2 GB** of disk space.

::::{note}
These examples were indexing the same data over and over with minimal variation. Because of that, the compression ratios observed of 80-90% are somewhat optimistic.
::::
