---
navigation_title: View the results
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-ad-view-results.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# View the results [ml-ad-view-results]

After the {{anomaly-job}} has processed some data, you can [view the results in {{kib}}](#ml-ad-view-results-kibana) or [query them with {{esql}}](#ml-ad-view-results-esql).

::::{tip}
Depending on the capacity of your machine, you might need to wait a few seconds for the {{ml}} analysis to generate initial results.
::::

## View results in {{kib}} [ml-ad-view-results-kibana]

You can examine the results with the **Anomaly Explorer** and the **Single Metric Viewer**.

::::{tip}
:applies_to: {"stack": "ga 9.4", "serverless": "ga"}
Use the date picker to adjust the time range for your results. You can use the **Zoom in** and **Zoom out** buttons next to the date picker to quickly narrow or widen the time range.
::::

### Bucket results [ml-ad-bucket-results]

When you view your {{ml}} results, each bucket has an anomaly score. This score is a statistically aggregated and normalized view of the combined anomalousness of all the record results in the bucket.

The {{ml}} analytics enhance the anomaly score for each bucket by considering contiguous buckets. This extra *multi-bucket analysis* effectively uses a sliding window to evaluate the events in each bucket relative to the larger context of recent events. When you review your {{ml}} results, there is a `multi_bucket_impact` property that indicates how strongly the final anomaly score is influenced by multi-bucket analysis. In {{kib}}, anomalies with medium or high multi-bucket impact are depicted in the **Anomaly Explorer** and the **Single Metric Viewer** with a cross symbol instead of a dot. For example:

:::{image} /explore-analyze/images/machine-learning-multibucketanalysis.jpg
:alt: Examples of anomalies with multi-bucket impact in {{kib}}
:screenshot:
:::

In this example, you can see that some of the anomalies fall within the shaded blue area, which represents the bounds for the expected values. The bounds are calculated per bucket, but multi-bucket analysis is not limited by that scope.

Both the **Anomaly Explorer** and the **Single Metric Viewer** contain an **Anomalies** table that shows key details about each anomaly such as time, typical and actual values, and probability. The **Anomaly explanation** section helps you to interpret a given anomaly by providing further insights about its type, impact, and score.

If you have [{{anomaly-detect-cap}} alert rules](/explore-analyze/machine-learning/anomaly-detection/ml-configuring-alerts.md#creating-anomaly-alert-rules) applied to an {{anomaly-job}} and an alert has occurred for the rule, you can view how the alert correlates with the {{anomaly-detect}} results in the **Anomaly Explorer** by using the **Anomaly timeline** swimlane and the **Alerts** panel. The **Alerts** panel contains a line chart with the alerts count over time. The cursor on the line chart is in sync with the anomaly swimlane making it easier to review anomalous buckets with the spike produced by the alerts. The panel also contains aggregated information for each alert rule associated with the job selection such as the total number of active, recovered, and untracked alerts for the selected job and time range. An alert context menu is displayed when an anomaly swimlane cell is selected with alerts in the chosen time range. The context menu contains the alert counters for the selected time buckets.

:::{image} /explore-analyze/images/machine-learning-anomaly-explorer-alerts.png
:alt: Alerts table in the Anomaly Explorer
:screenshot:
:::

If you have more than one {{anomaly-job}}, you can also obtain *overall bucket* results, which combine and correlate anomalies from multiple jobs into an overall score. When you view the results for job groups in {{kib}}, it provides the overall bucket scores. For more information, see [Get overall buckets API]({{es-apis}}operation/operation-ml-get-overall-buckets).

Bucket results provide the top level, overall view of the {{anomaly-job}} and are ideal for alerts. For example, the bucket results might indicate that at 16:05 the system was unusual. This information is a summary of all the anomalies, pinpointing when they occurred. When you identify an anomalous bucket, you can investigate further by examining the pertinent records. Use the **Actions** menu in the **Anomalies** table to explore the source data. Refer to [Adding custom URLs](ml-configuring-url.md).

::::{include} _snippets/ml-ad-cps-results-links.md
::::

### Influencer results [ml-ad-influencer-results]

The influencer results show which entities were anomalous and when. One influencer result is written per bucket for each influencer that affects the anomalousness of the bucket. The {{ml}} analytics determine the impact of an influencer by performing a series of experiments that remove all data points with a specific influencer value and check whether the bucket is still anomalous. That means that only influencers with statistically significant impact on the anomaly are reported in the results. For jobs with more than one detector, influencer scores provide a powerful view of the most anomalous entities.

For example, the `high_sum_total_sales` {{anomaly-job}} for the eCommerce orders sample data uses `customer_full_name.keyword` and `category.keyword` as influencers. You can examine the influencer results with the [get influencers API]({{es-apis}}operation/operation-ml-get-influencers). Alternatively, you can use the **Anomaly Explorer** in {{kib}}:

:::{image} /explore-analyze/images/machine-learning-influencers.png
:alt: Influencers in the {{kib}} Anomaly Explorer
:screenshot:
:::

On the left is a list of the top influencers for all of the detected anomalies in that same time period. The list includes maximum anomaly scores, which in this case are aggregated for each influencer, for each bucket, across all detectors. There is also a total sum of the anomaly scores for each influencer. You can use this list to help you narrow down the contributing factors and focus on the most anomalous entities.

You can also explore swim lanes that correspond to the values of an influencer. In this example, the swim lanes correspond to the values for the `customer_full_name.keyword`. By default, the swim lanes are sorted according to which entity has the maximum anomaly score values. You can click on the sections in the swim lane to see details about the anomalies that occurred in that time interval.

::::{tip}
The anomaly scores that you see in each section of the **Anomaly Explorer** might differ slightly. This disparity occurs because for each {{anomaly-job}}, there are bucket results, influencer results, and record results. Anomaly scores are generated for each type of result. The anomaly timeline in {{kib}} uses the bucket-level anomaly scores. If you view swim lanes by influencer, it uses the influencer-level anomaly scores, as does the list of top influencers. The list of anomalies uses the record-level anomaly scores.
::::

## View results with {{esql}} [ml-ad-view-results-esql]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

You can also query bucket, record, and influencer results with {{esql}}, using the `.ml-anomalies` [reserved view](elasticsearch://reference/query-languages/esql/esql-views.md#esql-views-reserved). The following examples show how to query this view.

Get the maximum record score for each 10-minute interval for one job. Replace `response_code_rates` with the ID of your job:

```esql
FROM .ml-anomalies
| WHERE job_id == "response_code_rates"
| WHERE is_interim == false
| STATS max_score = MAX(score)
    WHERE result_type == "record"
    BY timestamp = BUCKET(timestamp, 600s)
| WHERE max_score > 0
| SORT max_score DESC NULLS LAST
```

Get the maximum record score, the top influencers, and the top records for each job and 10-minute interval:

```esql
FROM .ml-anomalies
| WHERE is_interim == false
| STATS max_score = MAX(score) WHERE result_type == "record",
    influencers = TOP(score, 3, "DESC", JSON_STRING(
      "score", score,
      "field_name", influencer_field_name,
      "field_value", influencer_field_value
    )) WHERE result_type == "influencer" AND score >= 75,
    records = TOP(score, 3, "DESC", JSON_STRING(
      "score", score,
      "function", function,
      "over_field_name", over_field_name,
      "over_field_value", over_field_value
    )) WHERE result_type == "record" AND score >= 0
    BY job_id, _index, timestamp = BUCKET(timestamp, 600s)
| WHERE max_score > 0
| SORT job_id, max_score DESC NULLS LAST
| KEEP job_id, timestamp, max_score, influencers, records, _index
| LIMIT 10
```

### Query remote clusters [ml-ad-view-results-esql-ccs]

`FROM .ml-anomalies` isn't supported with {{ccs}}. As a workaround, create your own view from the reserved query, and replace the local index pattern with a remote one:

1. Get the reserved view's query:

   ```console
   GET _query/view/.ml-anomalies
   ```

   :::{dropdown} Example response
   :open:
   ```json
   {
     "views": [
       {
         "name": ".ml-anomalies",
         "query": """ <1>
   FROM .ml-anomalies-* METADATA _index
   | WHERE result_type IN ("bucket", "record", "influencer")
   | EVAL score = COALESCE(anomaly_score, record_score, influencer_score),
          initial_score = COALESCE(initial_anomaly_score, initial_record_score, initial_influencer_score)
   | KEEP timestamp,
          event.ingested,
          job_id,
          result_type,
          is_interim,
          score,
          initial_score,
          bucket_span,
          function,
          function_description,
          field_name,
          by_field_name,
          by_field_value,
          over_field_name,
          over_field_value,
          partition_field_name,
          partition_field_value,
          influencer_field_name,
          influencer_field_value,
          detector_index,
          actual,
          typical,
          event_count,
          processing_time_ms,
          _index
   """,
         "description": "View that contains the results of machine learning anomaly detection jobs.",
         "reserved": true
       }
     ]
   }
   ```
   1. Copy this query.
   :::

2. Create a view with that query. Replace `.ml-anomalies-*` with `*:.ml-anomalies-*`, and leave the rest of the query unchanged:

   ```console
   PUT _query/view/.ml-anomalies-ccs
   {
     "query": """
         FROM *:.ml-anomalies-* METADATA _index
         | WHERE ... <1>
         """
   }
   ```
   1. Copy the rest of the query from step 1. The `...` is a placeholder.

You can then query the new view with `FROM .ml-anomalies-ccs`.
