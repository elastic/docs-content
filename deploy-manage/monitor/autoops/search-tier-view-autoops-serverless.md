---
applies_to:
  serverless:
navigation_title: Search Tier view
---

# Search Tier view in AutoOps for {{serverless-short}}

The Search Tier view in AutoOps for {{serverless-short}} provides visibility into the consumption of search VCUs, which are a type of [compute billing dimension](/deploy-manage/monitor/autoops/autoops-for-serverless.md#compute-billing-dimensions). This view helps you understand how search activities and performance contribute to your search VCU consumption and, as a result, your project's bill. 

This view provides both high-level project summaries and detailed index-level and data stream-level breakdowns. 

To get to the Search Tier view, [access AutoOps](/deploy-manage/monitor/autoops/access-autoops-for-serverless.md) in your project and then select **Search Tier** from the navigation menu.

## Project-level insights

On the **Search Tier** page, the top half of the page offers general insights at the project level.

:::{image} /deploy-manage/images/search-tier-project-level-features.png
:screenshot:
:alt: Screenshot showing the features in the top half of the Search Tier page
:::

Use the following features to explore this view:
* Use the built-in **project picker** to switch between projects. This allows you to make quick context changes without needing to navigate back to your {{ecloud}} home page to select a different project.
* Select **custom time windows** to explore usage and performance data up to the last 10 days. The charted data is bucketed per day except when you select a period of up to 72 hours, when it is bucketed per hour.
* Explore different **visualizations** presenting the trend of search VCU usage over time and how it compares to the performance of the search tier in terms of search rate and latency.
* View the **annotations** overlaying the search VCUs usage chart to understand when the search power and boost window changed during the selected time period and how that might have affected the autoscaling of your project (and consequently your VCU consumption). 
* Gain insights from the **performance charts** depicting search rate and search latency trends to understand why your VCU consumption might fluctuate over time. 

## Index and data stream-level insights
 
The bottom half of the page offers a more granular breakdown table of index-level and data stream-level insights into search performance. 

:::{image} /deploy-manage/images/search-tier-breakdown-table.png
:screenshot:
:alt: Screenshot showing an expanded row in the data set table in the bottom half of the Search Tier page
:::

Each row of the table represents a single index or data stream, providing the following information:
* The **number of documents** in the index or data stream.
* The latest **search rate** in the selected time period.
* The latest **search latency** in the selected time period.
* The timestamp of the **last search** on the index or data stream.

Using this table, you can detect which of your indices or data streams is currently being searched and at what rate and latency. This helps you identify which indices are suffering from high [search load](https://www.elastic.co/search-labs/blog/elasticsearch-serverless-tier-autoscaling#what-is-search-load?), so that you can deduce where that load is coming from and manage it accordingly.

For historical analysis, you can also expand each row to reveal performance trends over time, helping you detect patterns or anomalies in search performance for each index and data stream individually.

Also, this table is interactive and can be:

* filtered by index or data stream name.
* sorted by index or data stream name, documents count, search rate, search latency, or last searched time.
* paginated to handle large sets of indices or data streams.

## Factors affecting search VCU consumption
The Search Tier view shows you how many search VCUs are consumed in your project and how your usage changes over time. This section explains the possible factors behind these changes so you can adjust them to manage your consumption. 

The consumption of search VCUs is directly related to autoscaling. When your project is upscaled, more VCUs are consumed, and when your project is downscaled, fewer VCUs are consumed. 

The following factors may cause upscaling or downscaling and consequently an increase or decrease in the number of search VCUs consumed:

### Search rate
A higher search rate will lead to a larger [search load](https://www.elastic.co/search-labs/blog/elasticsearch-serverless-tier-autoscaling#what-is-search-load?), which means the project will be upscaled and more search VCUs will be consumed. Similarly, a smaller search load means fewer search VCUs being consumed.

The search rate on your project can increase for many different reasons, such as when more clients start issuing search requests at the same time, or when a complex dashboard with many visualizations is configured with a low auto-refresh rate. 

When that happens, the search tier will try to respond to all requests as quickly as possible, but might not be able to serve them all with the currently allocated compute power. As a result, search requests will start backing up in the queue and the search latency will start rising. The search load will eventually reach a point that will trigger upscaling of the search tier, leading to higher consumption of search VCUs.

### Search latency

Alternatively, the search rate on your project may remain steady, but the search latency may increase because some computationally heavy search queries have been executing for several minutes, preventing the search tier from serving the newer search queries. 

This could be caused by a number of reasons:

* A user may be sending complex full-text queries including regular expressions or leading wildcards
* A dashboard may be issuing search queries running on a very large time frame including non-search-ready data
* Index mappings may be inefficient or they may be defining too many fields, causing higher memory consumption

As a result, the search tier gets slowly saturated and the new search queries get queued up waiting for the long-running ones to terminate. This increase in search latency can trigger upscaling and in turn increase your search VCU consumption. Low search latency means decreased search VCU consumption.

:::{admonition} Coming soon to AutoOps
We plan to display long-running search queries in the Search Tier view so that you can learn which queries are causing increased search latency and improve their performance.
:::

### Project settings
Increasing the search power, boost window, or retention period in your project will cause upscaling, which consumes more search VCUs. Decreasing these settings will lead to lower consumption of VCUs.

:::{note}
The search boost window and retention period settings are only applicable to time series data.
:::

### Data ingestion rate
If your project settings are constant but your project is ingesting and retaining more data over time, there will be more data that needs to be search-ready or "boosted". 

This will cause upscaling, leading to higher consumption of VCUs. In the same way, less data ingestion and retention will cause downscaling and so fewer search VCUs will be consumed.
