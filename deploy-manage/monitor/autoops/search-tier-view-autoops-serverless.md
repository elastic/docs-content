---
applies_to:
  serverless:
navigation_title: Search Tier view
---

# Search Tier view in AutoOps for Serverless

The **Search Tier** view in AutoOps for Serverless provides visibility into Search VCUs, which are a type of [compute billing dimension](/deploy-manage/monitor/autoops/autoops-for-serverless.md#compute-billing-dimensions). The Search Tier view helps you understand how search activities and performance contribute to your compute usage and as a result, your project's bill. 

This view provides both high-level project summaries and detailed index-level and data stream-level breakdowns. 

## Project-level usage and performance insights

The Search Tier view shows you how many Search VCUs your search tier consumes as it scales up or down to balance performance and availability. You can view these metrics at the project and index level as well as the data stream level.

The view offers the following features:

* A built-in project picker makes it easy to switch between projects, allowing for quick context changes without needing to navigate back to your {{ecloud}} home page to select a different project.
* You can also select custom time windows to explore usage and performance data—ranging from the last 3 hours to the last 10 days. When selecting a period of up to 24 hours, the charted data is bucketed per hour, otherwise it is bucketed per day.
* In the top half of the screen, there are different visualizations that show the trend over time of the Search VCU usage and how that usage compares to the performance of the Search Tier, mainly in terms of search rate and latency.
* In addition, the Search VCUs usage chart is overlaid with annotations indicating when the two main project performance settings, i.e. the search power and boost window, changed during the selected time period, and how that might have affected the autoscaling of your project, and consequently your VCU consumption. Also note that the search boost window and retention period settings are only applicable to time series data.
* The two performance charts located just below the Search VCUs usage chart depict search rate and latency trends and provide some more depth as to why your VCU consumption might fluctuate over time. Those two charts can help explain different upscaling situations, such as the two most common ones described below, where search latency can be seen as an implicit proxy for system stress:

### Upscaling situation 1: Increased search rate
The search rate on your project can increase for many different reasons, for instance when more clients start issuing search requests at the same time, or when a complex dashboard with many visualizations is configured with an auto-refresh rate that is too low. When that happens, the search tier will try to respond to all requests as fast as possible but might not be able to serve them all with the currently allocated compute power.
As a result, search requests will start backing up in the queue and the search latency will start rising accordingly. At some point, the search load will reach a specific threshold that will trigger an upscaling of the search tier, which in turn will provision more Search VCUs.

### Upscaling situation 2: Increased search latency
The search rate on your project stays steady, but there are a few computationally heavy search queries that have been executing for several minutes and prevent the search tier from serving the newer search queries that are flowing in. 
For instance, that could be caused by a user sending complex full-text queries, possibly including regular expressions or leading wildcards. Another typical example could be a dashboard issuing search queries running on a too big time frame, and thus, including non-search-ready (i.e. non-cached) data. Also important are the index mappings. Inefficient mappings or mappings defining too many fields can also drive up memory consumption.
Any combination of the previous situations are also possible, which is why it is important to pay attention to how you design your queries and dashboards and stay in control of your index mappings.
As a result, the search tier gets slowly saturated and the new search queries get queued up waiting for the long-running ones to terminate. In this case, you might also witness an increasing search latency, which can trigger upscaling decisions, and hence, increase your Search VCU consumption.
In the future, AutoOps will also surface the long-running search queries that are responsible for your increased search load, so that you can review them and eventually improve their performance.

## Data-level usage and performance insights

In the bottom half of the screen, the view includes a more granular breakdown table that provides index- and data stream-level insights on search performance, such as search rate and latency. Each row of the table represents a single index or data stream and displays:
The number of documents in the index or data stream
The latest search rate in the selected time period.
The latest search latency in the selected time period.
The timestamp of the most recent search on the index or data stream.
Using that table, you can more easily detect which of your indexes or data streams are currently being searched, at what rate and latency. That can help you quickly identify which indexes are suffering from search pressure, and from there it might be potentially easier for you to deduce where that load is coming from.
To support historical analysis, each row can be expanded to reveal performance trends over time, helping you detect patterns or anomalies in search performance over time for each index and data stream individually.
Also note that the table is interactive and can be:
* filtered by index or data stream name.
* sorted by index or data stream name, documents count, search rate, search latency or last searched time.
* paginated to handle large sets of indices or data streams.

## Factors that influence Search VCU consumption
The consumption of Search VCUs is directly related to autoscaling. When your project is upscaled, more VCUs are consumed, and when your project is downscaled, fewer VCUs are consumed. The following factors may cause upscaling or downscaling and consequently an increase or decrease in the number of Search VCUs consumed:

### Increase in search activities over time
A higher search rate or more complex queries will lead to a larger search load, which means the project will be upscaled and more Search VCUs will be consumed. Similarly, a smaller search load means fewer Search VCUs being consumed.

### Project settings
Increasing the search power, boost window, or retention period in your project will cause upscaling, which consumes more Search VCUs. Decreasing these settings will lead to lower consumption of VCUs.

### Data ingestion rate
If your project settings are constant but your project is ingesting and retaining more data over time, there will be more data that needs to be search-ready or "boosted". This will cause upscaling, leading to higher consumption of VCUs. In the same way, less data ingestion and retention will cause downscaling and so fewer Search VCUs will be consumed.

