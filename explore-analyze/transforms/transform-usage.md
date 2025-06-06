---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-usage.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# When to use transforms [transform-usage]

{{es}} aggregations are a powerful and flexible feature that enable you to summarize and retrieve complex insights about your data. You can summarize complex things like the number of web requests per day on a busy website, broken down by geography and browser type. If you use the same data set to try to calculate something as simple as a single number for the average duration of visitor web sessions, however, you can quickly run out of memory.

Why does this occur? A web session duration is an example of a behavioral attribute not held on any one log record; it has to be derived by finding the first and last records for each session in our weblogs. This derivation requires some complex query expressions and a lot of memory to connect all the data points. If you have an ongoing background process that fuses related events from one index into entity-centric summaries in another index, you get a more useful, joined-up picture. This new index is sometimes referred to as a *{{dataframe}}*.

You might want to consider using {{transforms}} instead of aggregations when:

* You need a complete *feature index* rather than a top-N set of items.

    In {{ml}}, you often need a complete set of behavioral features rather just the top-N. For example, if you are predicting customer churn, you might look at features such as the number of website visits in the last week, the total number of sales, or the number of emails sent. The {{stack}} {{ml-features}} create models based on this multi-dimensional feature space, so they benefit from the full feature indices that are created by {{transforms}}.

    This scenario also applies when you are trying to search across the results of an aggregation or multiple aggregations. Aggregation results can be ordered or filtered, but there are [limitations to ordering](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md#search-aggregations-bucket-terms-aggregation-order) and [filtering by bucket selector](elasticsearch://reference/aggregations/search-aggregations-pipeline-bucket-selector-aggregation.md) is constrained by the maximum number of buckets returned. If you want to search all aggregation results, you need to create the complete {{dataframe}}. If you need to sort or filter the aggregation results by multiple fields, {{transforms}} are particularly useful.

* You need to sort aggregation results by a pipeline aggregation.

    [Pipeline aggregations](elasticsearch://reference/aggregations/pipeline.md) cannot be used for sorting. Technically, this is because pipeline aggregations are run during the reduce phase after all other aggregations have already completed. If you create a {{transform}}, you can effectively perform multiple passes over the data.

* You want to create summary tables to optimize queries.

    For example, if you have a high level dashboard that is accessed by a large number of users and it uses a complex aggregation over a large dataset, it may be more efficient to create a {{transform}} to cache results. Thus, each user doesn’t need to run the aggregation query.

* You need to account for late-arriving data.

    In some cases, data might not be immediately available when a {{transform}} runs, leading to missing records in the destination index. This can happen due to ingestion delays, where documents take a few seconds or minutes to become searchable after being indexed. To handle this, the `delay` parameter in the {{transform}}’s sync configuration allows you to postpone processing new data. Instead of always querying the most recent records, the {{transform}} will skip a short period of time (for example, 60 seconds) to ensure all relevant data has arrived before processing.

    For example, if a {{transform}} runs every 5 minutes, it usually processes data from 5 minutes ago up to the current time. However, if you set `delay` to 60 seconds, the {{transform}} will instead process data from 6 minutes ago up to 1 minute ago, making sure that any documents that arrived late are included. By adjusting the `delay` parameter, you can improve the accuracy of transformed data while still maintaining near real-time results.
