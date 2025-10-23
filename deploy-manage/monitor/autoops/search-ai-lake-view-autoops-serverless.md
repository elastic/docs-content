---
applies_to:
  serverless:
navigation_title: Search AI Lake view
---

# Search AI Lake view in AutoOps for Serverless

The Search AI Lake view in AutoOps for Serverless provides visibility into the key [storage billing dimensions](/deploy-manage/monitor/autoops/autoops-for-serverless.md#storage-billing-dimensions) that drive the costs of your serverless projects. This view helps you understand how ingest and storage activities contribute to your storage usage costs with both high-level summaries and detailed index-level and data stream-levels breakdowns.

The Search AI Lake view is available in all regions across AWS, Azure, and GCP.

To get to this view, [access AutoOps](/deploy-manage/monitor/autoops/access-autoops-for-serverless.md) in your project and then select **Search AI Lake** from the navigation menu.

## Project-level insights

{applies_to}`observability:` {applies_to}`security:` On the **Search AI Lake** page, the top half of the screen offers project-level insights into the ingest rate and storage retained usage metrics over a selected time period.

:::{image} /deploy-manage/images/search-ai-lake-project-level-features.png
:screenshot:
:alt: Screenshot showing the features in the top half of the Search AI Lake page
:::

Use the following features to explore this view:
* Use the built-in **project picker** to switch between projects. This allows you to make quick context changes without needing to navigate back to your {{ecloud}} home page to select a different project.
* Select **custom time windows** to explore usage and performance data up to the last 10 days. The charted data is bucketed per day except when you select a period of up to 72 hours, when it is bucketed per hour.

{applies_to}`elasticsearch:` {{es-serverless}} projects offer the same experience, except that unlike Observability and Security Serverless projects, they only focus on storage retained and not on ingest rate usage metrics.

## Index and data-stream level insights

{applies_to}`observability:` {applies_to}`security:` The bottom half of the screen offers a more granular breakdown table of index-level and data stream-level insights into ingest rate and storage retained metrics. 

:::{image} /deploy-manage/images/search-ai-lake-breakdown-table.png
:screenshot:
:alt: Screenshot showing an expanded row in the table in the bottom half of the Search AI Lake page
:::

Each row of the table represents a single index or data stream and provides the following information:
* the **aggregated ingest rate** for the selected time period
* the **latest recorded storage retained value** during that period
* the timestamp of the **latest update** for these usage metrics

For historical analysis, you can also expand each row to reveal usage trends over time, helping you detect patterns or anomalies in data growth or ingest activity.

Also, this table is interactive and can be:

* filtered by index or data stream name.
* sorted by name, ingest rate, storage retained, or latest update time.
* paginated to handle large sets of indices or data streams.

{applies_to}`elasticsearch:` {{es-serverless}} projects offer the same experience, except that unlike Observability and Security Serverless projects, they only focus on storage retained and not on ingest rate usage metrics.

## Factors affecting storage consumption

The Search AI Lake view shows you how your project's ingest rate and storage retention changes over time. This section explains what might be causing these changes so you can make adjustments to manage your consumption. 

The main factor that influences storage consumption is the data retention duration set on your data streams. A longer retention period means more storage space needs to be allocated to accommodate that retention. 

A long data retention duration combined with a high ingest rate will consume even more storage. Let's say your project is ingesting a significantly large amount of data in a certain time period, causing your ingest rate to increase. If your data retention duration is not adjusted accordingly, you will require even more storage to store the additional data.

This is why you should adjust your data retention duration to fit your requirements so that you can make the most effective use of your storage.