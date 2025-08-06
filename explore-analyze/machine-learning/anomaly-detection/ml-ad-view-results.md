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

After the {{anomaly-job}} has processed some data, you can view the results in {{kib}}.

::::{tip}
Depending on the capacity of your machine, you might need to wait a few seconds for the {{ml}} analysis to generate initial results.
::::

There are two tools for examining the results from {{anomaly-jobs}} in {{kib}}: the **Anomaly Explorer** and the **Single Metric Viewer**.

## Bucket results [ml-ad-bucket-results]

When you view your {{ml}} results, each bucket has an anomaly score. This score is a statistically aggregated and normalized view of the combined anomalousness of all the record results in the bucket.

The {{ml}} analytics enhance the anomaly score for each bucket by considering contiguous buckets. This extra *multi-bucket analysis* effectively uses a sliding window to evaluate the events in each bucket relative to the larger context of recent events. When you review your {{ml}} results, there is a `multi_bucket_impact` property that indicates how strongly the final anomaly score is influenced by multi-bucket analysis. In {{kib}}, anomalies with medium or high multi-bucket impact are depicted in the **Anomaly Explorer** and the **Single Metric Viewer** with a cross symbol instead of a dot. For example:

:::{image} /explore-analyze/images/machine-learning-multibucketanalysis.jpg
:alt: Examples of anomalies with multi-bucket impact in {{kib}}
:screenshot:
:::

In this example, you can see that some of the anomalies fall within the shaded blue area, which represents the bounds for the expected values. The bounds are calculated per bucket, but multi-bucket analysis is not limited by that scope.

Both the **Anomaly Explorer** and the **Single Metric Viewer** contain an **Anomalies** table that shows key details about each anomaly such as time, typical and actual values, and probability. The **Anomaly explanation** section helps you to interpret a given anomaly by providing further insights about its type, impact, and score.

If you have [{{anomaly-detect-cap}} alert rules](/explore-analyze/machine-learning/anomaly-detection/ml-configuring-alerts.md#creating-anomaly-alert-rules) applied to an {{anomaly-job}} and an alert has occured for the rule, you can view how the alert correlates with the {{anomaly-detect}} results in the **Anomaly Explorer** by using the **Anomaly timeline** swimlane and the **Alerts** panel. The **Alerts** panel contains a line chart with the alerts count over time. The cursor on the line chart is in sync with the anomaly swimlane making it easier to review anomalous buckets with the spike produced by the alerts. The panel also contains aggregated information for each alert rule associated with the job selection such as the total number of active, recovered, and untracked alerts for the selected job and time range. An alert context menu is displayed when an anomaly swimlane cell is selected with alerts in the chosen time range. The context menu contains the alert counters for the selected time buckets.

:::{image} /explore-analyze/images/machine-learning-anomaly-explorer-alerts.png
:alt: Alerts table in the Anomaly Explorer
:screenshot:
:::

If you have more than one {{anomaly-job}}, you can also obtain *overall bucket* results, which combine and correlate anomalies from multiple jobs into an overall score. When you view the results for job groups in {{kib}}, it provides the overall bucket scores. For more information, see [Get overall buckets API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-overall-buckets).

Bucket results provide the top level, overall view of the {{anomaly-job}} and are ideal for alerts. For example, the bucket results might indicate that at 16:05 the system was unusual. This information is a summary of all the anomalies, pinpointing when they occurred. When you identify an anomalous bucket, you can investigate further by examining the pertinent records.

## Influencer results [ml-ad-influencer-results]

The influencer results show which entities were anomalous and when. One influencer result is written per bucket for each influencer that affects the anomalousness of the bucket. The {{ml}} analytics determine the impact of an influencer by performing a series of experiments that remove all data points with a specific influencer value and check whether the bucket is still anomalous. That means that only influencers with statistically significant impact on the anomaly are reported in the results. For jobs with more than one detector, influencer scores provide a powerful view of the most anomalous entities.

For example, the `high_sum_total_sales` {{anomaly-job}} for the eCommerce orders sample data uses `customer_full_name.keyword` and `category.keyword` as influencers. You can examine the influencer results with the [get influencers API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-influencers). Alternatively, you can use the **Anomaly Explorer** in {{kib}}:

:::{image} /explore-analyze/images/machine-learning-influencers.png
:alt: Influencers in the {{kib}} Anomaly Explorer
:screenshot:
:::

On the left is a list of the top influencers for all of the detected anomalies in that same time period. The list includes maximum anomaly scores, which in this case are aggregated for each influencer, for each bucket, across all detectors. There is also a total sum of the anomaly scores for each influencer. You can use this list to help you narrow down the contributing factors and focus on the most anomalous entities.

You can also explore swim lanes that correspond to the values of an influencer. In this example, the swim lanes correspond to the values for the `customer_full_name.keyword`. By default, the swim lanes are sorted according to which entity has the maximum anomaly score values. You can click on the sections in the swim lane to see details about the anomalies that occurred in that time interval.

::::{tip}
The anomaly scores that you see in each section of the **Anomaly Explorer** might differ slightly. This disparity occurs because for each {{anomaly-job}}, there are bucket results, influencer results, and record results. Anomaly scores are generated for each type of result. The anomaly timeline in {{kib}} uses the bucket-level anomaly scores. If you view swim lanes by influencer, it uses the influencer-level anomaly scores, as does the list of top influencers. The list of anomalies uses the record-level anomaly scores.
::::
