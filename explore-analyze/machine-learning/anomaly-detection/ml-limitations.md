---
applies:
  stack:
  serverless:
navigation_title: "Limitations"
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-limitations.html
---

# Limitations [ml-limitations]

The following limitations and known problems apply to the 9.0.0-beta1 release of the Elastic {{ml-features}}. The limitations are grouped into four categories:

* [Platform limitations](#ad-platform-limitations) are related to the platform that hosts the {{ml}} feature of the {{stack}}.
* [Configuration limitations](#ad-config-limitations) apply to the configuration process of the {{anomaly-jobs}}.
* [Operational limitations](#ad-operational-limitations) affect the behavior of the {{anomaly-jobs}} that are running.
* [Limitations in {{kib}}](#ad-ui-limitations) only apply to {{anomaly-jobs}} managed via the user interface.

## Platform limitations [ad-platform-limitations]

### CPUs must support SSE4.2 [ml-limitations-sse]

{{ml-cap}} uses Streaming SIMD Extensions (SSE) 4.2 instructions, so it works only on machines whose CPUs [support](https://en.wikipedia.org/wiki/SSE4#Supporting_CPUs) SSE4.2. If you run {{es}} on older hardware you must disable {{ml}} by setting `xpack.ml.enabled` to `false`. See [{{ml-cap}} settings in {{es}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-settings.html).

### CPU scheduling improvements apply to Linux and MacOS only [ml-scheduling-priority]

When there are many {{ml}} jobs running at the same time and there are insufficient CPU resources, the JVM performance must be prioritized so search and indexing latency remain acceptable. To that end, when CPU is constrained on Linux and MacOS environments, the CPU scheduling priority of native analysis processes is reduced to favor the {{es}} JVM. This improvement does not apply to Windows environments.

### License limitations for {{ml-jobs}} with CCS [ml-license-ccs-limitations]

You must have an appropriate license to initiate {{ml-jobs-cap}} on datasets from remote clusters accessed through Cross-Cluster Search (CCS). Refer to the [Subscriptions](https://www.elastic.co/subscriptions) page for details on features available with different subscription levels.

## Configuration limitations [ad-config-limitations]

### Terms aggregation size affects data analysis [_terms_aggregation_size_affects_data_analysis]

By default, the `terms` aggregation returns the buckets for the top ten terms. You can change this default behavior by setting the `size` parameter.

If you send pre-aggregated data to a job for analysis, you must ensure that the `size` is configured correctly. Otherwise, some data might not be analyzed.

### Scripted metric aggregations are not supported [_scripted_metric_aggregations_are_not_supported]

Using [scripted metric aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-scripted-metric-aggregation.html) in {{dfeeds}} is not supported. Refer to the [Aggregating data for faster performance](ml-configuring-aggregation.md) page to learn more about aggregations in {{dfeeds}}.

### Fields named "by", "count", or "over" cannot be used to split data [_fields_named_by_count_or_over_cannot_be_used_to_split_data]

You cannot use the following field names in the `by_field_name` or `over_field_name` properties in a job: `by`; `count`; `over`. This limitation also applies to those properties when you create advanced jobs in {{kib}}.

### Arrays in analyzed fields are turned into comma-separated strings [ml-arrays-limitations]

If an {{anomaly-job}} is configured to analyze an aggregatable field (a field that is part of the index mapping definition), and this field contains an array, then the array is turned into a comma-separated concatenated string. The items in the array are sorted alphabetically and the duplicated items are removed. For example, the array `["zebra", "dog", "cat", "alligator", "cat"]` becomes `alligator,cat,dog,zebra`. The Anomaly Explorer charts don’t display any results for the job as the string does not exist in the source data. The Single Metric Viewer displays results if the model plot is enabled.

If an array field is not aggregatable and is retrieved from `_source`, the array is also turned into a comma-separated, concatenated list. However, the list items are not sorted alphabetically, nor are they deduplicated. Taking the example above, the comma-separated list, in this case, would be `zebra,dog,cat,alligator,cat`.

Analyzing large arrays results in long strings which may require more system resources. Consider using a query in the {{dfeed}} that filters on the relevant items of the array.

### {{anomaly-jobs-cap}} on frozen tier data cannot be created in {{kib}} [ml-frozen-tier-limitations]

You cannot create {{anomaly-jobs}} on [frozen tier](../../../manage-data/lifecycle/data-tiers.md#frozen-tier) data through the job wizards in {{kib}}. If you want to create such jobs, use the APIs instead.

### Unsupported forecast configurations [ml-forecast-config-limitations]

There are some limitations that affect your ability to create a forecast:

* You can generate only three forecasts per {{anomaly-job}} concurrently. There is no limit to the number of forecasts that you retain. Existing forecasts are not overwritten when you create new forecasts. Rather, they are automatically deleted when they expire.
* If you use an `over_field_name` property in your {{anomaly-job}} (that is to say, it’s a *population job*), you cannot create a forecast.
* If you use any of the following analytical functions in your {{anomaly-job}}, you cannot create a forecast:

  * `lat_long`
  * `rare` and `freq_rare`
  * `time_of_day` and `time_of_week`

    For more information about any of these functions, see [*Function reference*](ml-functions.md).

### {{anomaly-detect-cap}} performs better on indexed fields [ml-limitations-runtime]

{{anomaly-jobs-cap}} sort all data by a user-defined time field, which is frequently accessed. If the time field is a [runtime field](../../../manage-data/data-store/mapping/runtime-fields.md), the performance impact of calculating field values at query time can significantly slow the job. Use an indexed field as a time field when running {{anomaly-jobs}}.

### Deprecation warnings for Painless scripts in {{dfeeds}} [ml-limitations-painless-script]

If a {{dfeed}} contains Painless scripts that use deprecated syntax, deprecation warnings are displayed when the {{dfeed}} is previewed or started. However, it is not possible to check for deprecation warnings across all {{dfeeds}} as a bulk action because running the required queries might be a resource intensive process. Therefore any deprecation warnings due to deprecated Painless syntax are not available in the Upgrade assistant.

## Operational limitations [ad-operational-limitations]

### Categorization uses English dictionary words [_categorization_uses_english_dictionary_words]

Categorization identifies static parts of unstructured logs and groups similar messages together. The default categorization tokenizer assumes English language log messages. For other languages you must define a different `categorization_analyzer` for your job.

Additionally, a dictionary used to influence the categorization process contains only English words. This means categorization might work better in English than in other languages. The ability to customize the dictionary will be added in a future release.

### Misleading high missing field counts [_misleading_high_missing_field_counts]

One of the counts associated with a {{ml}} job is `missing_field_count`, which indicates the number of records that are missing a configured field.

Since jobs analyze JSON data, the `missing_field_count` might be misleading. Missing fields might be expected due to the structure of the data and therefore do not generate poor results.

For more information about `missing_field_count`, see the [get {{anomaly-job}} statistics API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-job-stats.html).

### Security integration [_security_integration]

When the {{es}} {{security-features}} are enabled, a {{dfeed}} stores the roles of the user who created or updated the {{dfeed}} **at that time**. This means that if the roles the user has are changed after they create or update a {{dfeed}} then the {{dfeed}} continues to run without change. However, if instead the permissions associated with the roles that are stored with the {{dfeed}} are changed then this affects the {{dfeed}}. For more information, see [{{dfeeds-cap}}](ml-ad-run-jobs.md#ml-ad-datafeeds).

### Job and {{dfeed}} APIs have a maximum search size [ml-result-size-limitations]

In 6.6 and later releases, the [get jobs API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-job.html) and the [get job statistics API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-job-stats.html) return a maximum of 10,000 jobs. Likewise, the [get {{dfeeds}} API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-datafeed.html) and the [get {{dfeed}} statistics API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-datafeed-stats.html) return a maximum of 10,000 {{dfeeds}}.

### Forecast operational limitations [ml-forecast-limitations]

There are some factors that may be considered when you run forecasts:

* Forecasts run concurrently with real-time {{ml}} analysis. That is to say, {{ml}} analysis does not stop while forecasts are generated. Forecasts can have an impact on {{anomaly-jobs}}, however, especially in terms of memory usage. For this reason, forecasts run only if the model memory status is acceptable.
* The {{anomaly-job}} must be open when you create a forecast. Otherwise, an error occurs.
* If there is insufficient data to generate any meaningful predictions, an error occurs. In general, forecasts that are created early in the learning phase of the data analysis are less accurate.

## Limitations in {{kib}} [ad-ui-limitations]

### Pop-ups must be enabled in browsers [_pop_ups_must_be_enabled_in_browsers]

The {{ml-features}} in {{kib}} use pop-ups. You must configure your web browser so that it does not block pop-up windows or create an exception for your {{kib}} URL.

### Anomaly Explorer and Single Metric Viewer omissions and limitations [_anomaly_explorer_and_single_metric_viewer_omissions_and_limitations]

In {{kib}}, **Anomaly Explorer** and **Single Metric Viewer** charts are not displayed:

* for anomalies that were due to categorization (if model plot is not enabled),
* if the {{dfeed}} uses scripted fields and model plot is not enabled (except for scripts that define metric fields),
* if the {{dfeed}} uses [composite aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html) that have composite sources other than `terms` and `date_histogram`,
* if your [{{dfeed}} uses aggregations with nested `terms` aggs](ml-configuring-aggregation.md#aggs-dfeeds) and model plot is not enabled,
* `freq_rare` functions,
* `info_content`, `high_info_content`, `low_info_content` functions,
* `lat_long` geographic functions
* `time_of_day`, `time_of_week` functions,
* `varp`, `high_varp`, `low_varp` functions.

Refer to the table below for a more detailed view of supported detector functions.

The charts can also look odd in circumstances where there is very little data to plot. For example, if there is only one data point, it is represented as a single dot. If there are only two data points, they are joined by a line. The following table shows which detector functions are supported in the Single Metric Viewer.

| Detector functions | Function description | Supported |
| --- | --- | --- |
| count, high_count, low_count, non_zero_count, low_non_zero_count | [Count functions](https://www.elastic.co/guide/en/machine-learning/current/ml-count-functions.html) | yes |
| count, high_count, low_count, non_zero_count, low_non_zero_count with summary_count_field_name that is not doc_count (model plot not enabled) | [Count functions](https://www.elastic.co/guide/en/machine-learning/current/ml-count-functions.html) | yes |
| non_zero_count with summary_count_field that is not doc_count using cardinality aggregation in datafeed config (model plot not enabled) | [Count functions](https://www.elastic.co/guide/en/machine-learning/current/ml-count-functions.html) | yes |
| distinct_count, high_distinct_count, low_distinct_count | [Count functions](https://www.elastic.co/guide/en/machine-learning/current/ml-count-functions.html) | yes |
| mean, high_mean, low_mean | [Mean, high_mean, low_mean](https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html#ml-metric-mean) | yes |
| min | [Min](https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html#ml-metric-min) | yes |
| max | [Max](https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html#ml-metric-max) | yes |
| metric | [Metric](https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html#ml-metric-metric) | yes |
| median, high_median, low_median | [Median, high_median, low_median](https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html#ml-metric-median) | yes |
| sum, high_sum ,low_sum, non_null_sum, high_non_null_sum, low_non_null_sum | [Sum functions](https://www.elastic.co/guide/en/machine-learning/current/ml-sum-functions.html) | yes |
| varp, high_varp, low_varp | [Varp, high_varp, low_varp](https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html#ml-metric-varp) | yes (only if model plot is enabled) |
| lat_long | [Lat_long](https://www.elastic.co/guide/en/machine-learning/current/ml-geo-functions.html#ml-lat-long) | no (but map is displayed in the Anomaly Explorer) |
| info_content, high_info_content, low_info_content | [Info_content, High_info_content, Low_info_content](https://www.elastic.co/guide/en/machine-learning/current/ml-info-functions.html#ml-info-content) | yes (only if model plot is enabled) |
| rare | [Rare](https://www.elastic.co/guide/en/machine-learning/current/ml-rare-functions.html#ml-rare) | yes |
| freq_rare | [Freq_rare](https://www.elastic.co/guide/en/machine-learning/current/ml-rare-functions.html#ml-freq-rare) | no |
| time_of_day, time_of_week | [Time functions](https://www.elastic.co/guide/en/machine-learning/current/ml-time-functions.html) | no |

### Jobs created in {{kib}} must use {{dfeeds}} [_jobs_created_in_kib_must_use_dfeeds]

If you create jobs in {{kib}}, you must use {{dfeeds}}. If the data that you want to analyze is not stored in {{es}}, you cannot use {{dfeeds}} and therefore you cannot create your jobs in {{kib}}. You can, however, use the {{ml}} APIs to create jobs. For more information, see [{{dfeeds-cap}}](ml-ad-run-jobs.md#ml-ad-datafeeds) and [*API quick reference*](ml-api-quickref.md).

### Jobs created in {{kib}} use model plot config and pre-aggregated data [_jobs_created_in_kib_use_model_plot_config_and_pre_aggregated_data]

If you create single or multi-metric jobs in {{kib}}, it might enable some options under the covers that you’d want to reconsider for large or long-running jobs.

For example, when you create a single metric job in {{kib}}, it generally enables the `model_plot_config` advanced configuration option. That configuration option causes model information to be stored along with the results and provides a more detailed view into {{anomaly-detect}}. It is specifically used by the **Single Metric Viewer** in {{kib}}. When this option is enabled, however, it can add considerable overhead to the performance of the system. If you have jobs with many entities, for example data from tens of thousands of servers, storing this additional model information for every bucket might be problematic. If you are not certain that you need this option or if you experience performance issues, edit your job configuration to disable this option.

Likewise, when you create a single or multi-metric job in {{kib}}, in some cases it uses aggregations on the data that it retrieves from {{es}}. One of the benefits of summarizing data this way is that {{es}} automatically distributes these calculations across your cluster. This summarized data is then fed into {{ml}} instead of raw results, which reduces the volume of data that must be considered while detecting anomalies. However, if you have two jobs, one of which uses pre-aggregated data and another that does not, their results might differ. This difference is due to the difference in precision of the input data. The {{ml}} analytics are designed to be aggregation-aware and the likely increase in performance that is gained by pre-aggregating the data makes the potentially poorer precision worthwhile. If you want to view or change the aggregations that are used in your job, refer to the `aggregations` property in your {{dfeed}}.

When the aggregation interval of the {{dfeed}} and the bucket span of the job don’t match, the values of the chart plotted in both the **Single Metric Viewer** and the **Anomaly Explorer** differ from the actual values of the job. To avoid this behavior, make sure that the aggregation interval in the {{dfeed}} configuration and the bucket span in the {{anomaly-job}} configuration have the same values.

### Calendars and filters are visible in all {{kib}} spaces [ml-space-limitations]

[Spaces](../../../deploy-manage/manage-spaces.md) enable you to organize your {{anomaly-jobs}} in {{kib}} and to see only the jobs and other saved objects that belong to your space. However, this limited scope does not apply to [calendars](https://www.elastic.co/guide/en/machine-learning/current/ml-ad-run-jobs.html#ml-ad-calendars) and [filters](https://www.elastic.co/guide/en/machine-learning/current/ml-ad-run-jobs.html#ml-ad-rules); they are visible in all spaces.

### Rollup indices are not supported in {{kib}} [ml-rollup-limitations]

Rollup indices and {{data-sources}} with rolled up indices cannot be used in {{anomaly-jobs}} or {{dfeeds}} in {{kib}}. If you try to analyze data that exists in an index that uses the experimental [{{rollup-features}}](../../../manage-data/lifecycle/rollup.md), the {{anomaly-job}} creation wizards fail. If you use APIs to create {{anomaly-jobs}} that use {{rollup-features}}, the job results might not display properly in the **Single Metric Viewer** or **Anomaly Explorer** in {{kib}}.
