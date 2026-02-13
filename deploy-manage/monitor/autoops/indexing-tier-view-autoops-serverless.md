---
applies_to:
  serverless:
navigation_title: Indexing Tier view
products:
  - id: cloud-serverless
---

# Indexing Tier view in AutoOps for {{serverless-short}}

The **Indexing Tier** view in AutoOps for {{serverless-short}} provides visibility into the consumption of ingest VCUs, which are a type of [compute billing dimension](/deploy-manage/monitor/autoops/autoops-for-serverless.md#compute-billing-dimensions) for {{es}} projects. This view helps you understand how indexing activities and performance contribute to your ingest VCU consumption and, as a result, your project's bill. 

This view provides both high-level project summaries and detailed index-level and data stream-level breakdowns. 

To get to the **Indexing Tier** view, [access AutoOps](/deploy-manage/monitor/autoops/access-autoops-for-serverless.md) in your project and then select **Indexing Tier** from the navigation menu.

## Project-level insights

The top half of the **Indexing Tier** page offers general insights at the project level.

:::{image} /deploy-manage/images/indexing-tier-project-level-features.png
:screenshot:
:alt: Screenshot showing the features in the top half of the Indexing Tier page
:::

Use the following features to explore this view:
* Use the built-in **project picker** to switch between projects. This allows you to make quick context changes without needing to navigate back to your {{ecloud}} home page to select a different project.
* Select **custom time windows** to explore usage and performance data up to the last 10 days. For time periods up to 72 hours, the data on the chart is displayed per hour. For time periods greater than 72 hours, the data is displayed per day.
* Explore different **visualizations** presenting the trend of ingest VCU usage over time and how it compares to the performance of the indexing tier in terms of indexing rate and latency.
* Gain insights from the **performance charts** depicting indexing rate and latency trends to understand why your VCU consumption might fluctuate over time.

## Index and data stream-level insights
 
The bottom half of the **Indexing Tier** page offers a more granular breakdown table of index-level and data stream-level insights into indexing performance. 

:::{image} /deploy-manage/images/indexing-tier-breakdown-table.png
:screenshot:
:alt: Screenshot showing an expanded row in the Data Streams table on the bottom half of the Indexing Tier page
:::

Each row of the table represents a single index or data stream, providing the following information:
* The **number of documents** in the index or data stream.
* The latest **indexing rate** in the selected time period.
* The latest **indexing latency** in the selected time period.
* The timestamp of the **last indexing operation** on the index or data stream.

Using this table, you can detect which of your indices or data streams is currently being ingested and at what rate and latency. This helps you identify which indices have a high [ingestion load](https://www.elastic.co/search-labs/blog/elasticsearch-ingest-autoscaling#ingestion-load), so that you can deduce where that load is coming from and manage it accordingly.

For historical analysis, you can also expand each row to reveal performance trends over time, helping you detect patterns or anomalies in indexing performance for each index and data stream individually.

Also, this table is interactive and can be:

* filtered by index or data stream name.
* sorted by index or data stream name, documents count, indexing rate rate, indexing latency, or last indexing time.
* paginated to handle large sets of indices or data streams.

## Factors affecting ingest VCU consumption
The **Indexing Tier** view shows you how many ingest VCUs are consumed in your project and how your usage changes over time. This section explains the possible factors behind these changes so you can adjust them to manage your consumption.

The consumption of ingest VCUs is directly related to [autoscaling](/deploy-manage/autoscaling.md), which depends on your ingest rate and the complexity of your data. When your project scales up, more VCUs are consumed, and when your project scales down, fewer VCUs are consumed. When no data is being indexed, the indexing tier scales down to zero (with some [exceptions](https://www.elastic.co/search-labs/pt/blog/elasticsearch-serverless-pricing-vcus-ecus#minimum-ingest-vcus)).

The following factors might cause upscaling or downscaling and consequently an increase or decrease in the number of ingest VCUs consumed:

### Indexing rate
A higher indexing rate will lead to a larger [ingestion load](https://www.elastic.co/search-labs/blog/elasticsearch-ingest-autoscaling#ingestion-load), which means the project might be upscaled and more ingest VCUs might be consumed. Similarly, a smaller indexing load means fewer ingest VCUs being consumed.

The indexing rate on your project can increase for many different reasons, such as when more clients start issuing indexing requests at the same time, or when you have [transforms](/explore-analyze/transforms.md) scheduled to run too frequently.

When that happens, the indexing tier will try to respond to all requests as quickly as possible, but might not be able to serve them all with the currently allocated resources. As a result, indexing requests will start backing up in the queue and the indexing latency will start rising. The ingestion load will eventually reach a point that will trigger upscaling of the indexing tier, causing ingest VCUs to be consumed at a higher rate.

### Indexing latency

Alternatively, the indexing rate on your project might remain steady, but the indexing latency might increase because some computationally heavy indexing queries have been executing for several minutes, preventing the tier from serving newer indexing queries.

This could be caused by a number of reasons:

* You might have a lot of small indices (less than 1GB) that are causing overhead
* Indexed documents might need to be processed by resource-intensive ingest pipelines, such as pipelines with complex grok patterns or inference requirements
* Transforms might be running on large amounts of data
* Index mappings might be inefficient or they might be defining too many fields, causing higher memory consumption

As a result, the indexing tier gets slowly saturated and the new indexing requests get queued up waiting for the long-running ones to terminate. This increase in indexing latency can trigger upscaling and in turn increase your ingest VCU consumption. Similarly, low indexing latency means downscaling and decreased ingest VCU consumption.


:::{admonition} Coming soon to AutoOps
We plan to display long-running indexing requests in the **Indexing Tier** view so that you can learn which requests are causing increased indexing latency and improve their performance.
:::