---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/anomaly-detection-scale.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Working with anomaly detection at scale [anomaly-detection-scale]

There are many advanced configuration options for {{anomaly-jobs}}, some of them affect the performance or resource usage significantly. This guide contains a list of considerations to help you plan for using {{anomaly-detect}} at scale.

In this guide, you’ll learn how to:

* Understand the impact of configuration options on the performance of {{anomaly-jobs}}

Prerequisites:

* This guide assumes you’re already familiar with how to create {{anomaly-jobs}}. If not, refer to [{{anomaly-detect-cap}}](../anomaly-detection.md).

The following recommendations are not sequential – the numbers just help to navigate between the list items; you can take action on one or more of them in any order. You can implement some of these changes on existing jobs; others require you to clone an existing job or create a new one.

## 1. Consider autoscaling, node sizing, and configuration [node-sizing]

An {{anomaly-job}} runs on a single node and requires sufficient resources to hold its model in memory. When a job is opened, it will be placed on the node with the most available memory at that time.

The memory available to the {{ml}} native processes can roughly be thought of as total machine RAM minus that which is required for the operating system, {{es}} and any other software that is running on the same machine.

The available memory for {{ml}} on a node must be sufficient to accommodate the size of the largest model. The total available memory across all {{ml}} nodes must be sufficient to accommodate the memory requirement for all simultaneously open jobs.

In {{ecloud}}, dedicated {{ml}} nodes are provisioned with most of the RAM automatically being available to the {{ml}} native processes. If deploying self-managed, then we recommend deploying dedicated {{ml}} nodes and increasing the value of `xpack.ml.max_machine_memory_percent` from the default 30%. The default of 30% has to be set low in case other software is running on the same machine and to leave memory free for an OS file system cache on {{ml}} nodes that are also data nodes. If you use dedicated {{ml}} nodes as recommended and do not run any other software on them then it would be reasonable to run with a 2GB JVM heap and set `xpack.ml.max_machine_memory_percent` to 90% on machines with at least 24GB of RAM. This maximizes the number of {{ml}} jobs that can be run.

Increasing the number of nodes will allow distribution of job processing as well as fault tolerance. If running many jobs, even small memory ones, then consider increasing the number of nodes in your environment.

In {{ecloud}}, you can enable [autoscaling](../../../deploy-manage/autoscaling.md) so that the {{ml}} nodes in your cluster scale up or down based on current {{ml}} memory and CPU requirements. The {{ecloud}} infrastructure allows you to create {{ml-jobs}} up to the size that fits on the maximum node size that the cluster can scale to (usually somewhere between 58GB and 64GB) rather than what would fit in the current cluster. If you attempt to use autoscaling outside of {{ecloud}}, then set `xpack.ml.max_ml_node_size` to define the maximum possible size of a {{ml}} node. Creating {{ml-jobs}} with model memory limits larger than the maximum node size can support is not allowed, as autoscaling cannot add a node big enough to run the job. On a self-managed deployment, you can set `xpack.ml.max_model_memory_limit` according to the available resources of the {{ml}} node. This prevents you from creating jobs with model memory limits too high to open in your cluster.

## 2. Use dedicated results indices [dedicated-results-index]

For large jobs, use a dedicated results index. This ensures that results from a single large job do not dominate the shared results index. It also ensures that the job and results (if `results_retention_days` is set) can be deleted more efficiently and improves renormalization performance. By default, {{anomaly-job}} results are stored in a shared index. To change to use a dedicated result index, you need to clone or create a new job.

## 3. Disable model plot [model-plot]

By default, model plot is enabled when you create jobs in {{kib}}. If you have a large job, however, consider disabling it. You can disable model plot for existing jobs by using the [Update {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-update-job).

Model plot calculates and stores the model bounds for each analyzed entity, including both anomalous and non-anomalous entities. These bounds are used to display the shaded area in the Single Metric Viewer charts. Model plot creates one result document per bucket per split field value. If you have high cardinality fields and/or a short bucket span, disabling model plot reduces processing workload and results stored.

## 4. Understand how detector configuration can impact model memory [detector-configuration]

The following factors are most significant in increasing the memory required for a job:

* High cardinality of the `by` or `partition` fields
* Multiple detectors
* A high distinct count of influencers within a bucket

Optimize your {{anomaly-job}} by choosing only relevant influencer fields and detectors.

If you have high cardinality `by` or `partition` fields, ensure you have sufficient memory resources available for the job. Alternatively, consider if the job can be split into smaller jobs by using a {{dfeed}} query. For very high cardinality, using a population analysis may be more appropriate.

To change partitioning fields, influencers and/or detectors, you need to clone or create a new job.

## 5. Optimize the bucket span [optimize-bucket-span]

Short bucket spans and high cardinality detectors are resource intensive and require more system resources.

Bucket span is typically between 15m and 1h. The recommended value always depends on the data, the use case, and the latency required for alerting. A job with a longer bucket span uses less resources because fewer buckets require processing and fewer results are written. Bucket spans that are sensible dividers of an hour or day work best as most periodic patterns have a daily cycle.

If your use case is suitable, consider increasing the bucket span to reduce processing workload. To change the bucket span, you need to clone or create a new job.

## 6. Set the `scroll_size` of the {{dfeed}} [set-scroll-size]

This consideration only applies to {{dfeeds}} that **do not** use aggregations. The `scroll_size` parameter of a {{dfeed}} specifies the number of hits to return from {{es}} searches. The higher the `scroll_size` the more results are returned by a single search. When your {{anomaly-job}} has a high throughput, increasing `scroll_size` may decrease the time the job needs to analyze incoming data, however may also increase the pressure on your cluster. You cannot increase `scroll_size` to more than the value of `index.max_result_window` which is 10,000 by default. If you update the settings of a {{dfeed}}, you must stop and start the {{dfeed}} for the change to be applied.

## 7. Set the model memory limit [set-model-memory-limit]

The `model_memory_limit` job configuration option sets the approximate maximum amount of memory resources required for analytical processing. When you create an {{anomaly-job}} in {{kib}}, it provides an estimate for this limit. The estimate is based on the analysis configuration details for the job and cardinality estimates, which are derived by running aggregations on the source indices as they exist at that specific point in time.

If you change the resources available on your {{ml}} nodes or make significant changes to the characteristics or cardinality of your data, the model memory requirements might also change. You can update the model memory limit for a job while it is closed. If you want to decrease the limit below the current model memory usage, however, you must clone and re-run the job.

::::{tip}
You can view the current model size statistics with the [get {{anomaly-job}} stats](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-job-stats) and [get model snapshots](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-model-snapshots) APIs. You can also obtain a model memory limit estimate at any time by running the [estimate {{anomaly-jobs}} model memory API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-estimate-model-memory). However, you must provide your own cardinality estimates.
::::

As a job approaches its model memory limit, the memory status is `soft_limit` and older models are more aggressively pruned to free up space. If you have categorization jobs, no further examples are stored. When a job exceeds its limit, the memory status is `hard_limit` and the job no longer models new entities. It is therefore important to have appropriate memory model limits for each job. If you reach the hard limit and are concerned about the missing data, ensure that you have adequate resources then clone and re-run the job with a larger model memory limit.

## 8. Pre-aggregate your data [pre-aggregate-data]

You can speed up the analysis by summarizing your data with aggregations.

{{anomaly-jobs-cap}} use summary statistics that are calculated for each bucket. The statistics can be calculated in the job itself or via aggregations. It is more efficient to use an aggregation when it’s possible, as in this case, the data node does the heavy-lifting instead of the {{ml}} node.

You may want to use `chunking_config` to tune your search speed when your {{dfeeds}} use aggregations. In these cases, set `chunking_config.mode` to `manual` and experiment with the `time_span` value. Increasing it may speed up search. However, the higher the chunking `time_span`, the higher number of buckets are included in the search response. Thus, if you hit the `search.max_buckets` limit, decrease `time_span` to reduce the number of buckets per response.

In certain cases, you cannot do aggregations to increase performance. For example, categorization jobs use the full log message to detect anomalies, so this data cannot be aggregated. If you have many influencer fields, it may not be beneficial to use an aggregation either. This is because only a few documents in each bucket may have the combination of all the different influencer fields.

See [Aggregating data for faster performance](ml-configuring-aggregation.md) to learn more.

## 9. Optimize the results retention [results-retention]

Set a results retention window to reduce the amount of results stored.

{{anomaly-detect-cap}} results are retained indefinitely by default. Results build up over time, and your result index may be quite large. A large results index is slow to query and takes up significant space on your cluster. Consider how long you wish to retain the results and set `results_retention_days` accordingly – for example, to 30 or 60 days – to avoid unnecessarily large result indices. Deleting old results does not affect the model behavior. You can change this setting for existing jobs.

## 10. Optimize the renormalization window [renormalization-window]

Reduce the renormalization window to reduce processing workload.

When a new anomaly has a much higher score than any anomaly in the past, the anomaly scores are adjusted on a range from 0 to 100 based on the new data. This is called renormalization. It can mean rewriting a large number of documents in the results index. Renormalization happens for results from the last 30 days or 100 bucket spans (depending on which is the longer) by default. When you are working at scale, set `renormalization_window_days` to a lower value, so the workload is reduced. You can change this setting for existing jobs and changes will take effect after the job has been reopened.

## 11. Optimize the model snapshot retention [model-snapshot-retention]

Model snapshots are taken periodically, to ensure resilience in the event of a system failure and to allow you to manually revert to a specific point in time. These are stored in a compressed format in an internal index and kept according to the configured retention policy. Load is placed on the cluster when indexing a model snapshot and index size is increased as multiple snapshots are retained.

When working with large model sizes, consider how frequently you want to create model snapshots using `background_persist_interval`. The default is every 3 to 4 hours. Increasing this interval reduces the periodic indexing load on your cluster, but in the event of a system failure, you may be reverting to an older version of the model.

Also consider how long you wish to retain snapshots using `model_snapshot_retention_days` and `daily_model_snapshot_retention_after_days`. Retaining fewer snapshots substantially reduces index storage requirements for model state, but also reduces the granularity of model snapshots from which you can revert.

For more information, refer to [Model snapshots](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-model-snapshots).

## 12. Optimize your search queries [search-queries]

If you are operating on a big scale, make sure that your {{dfeed}} query is as efficient as possible. There are different ways to write {{es}} queries and some of them are more efficient than others. See [Tune for search speed](../../../deploy-manage/production-guidance/optimize-performance/search-speed.md) to learn more about {{es}} performance tuning.

You need to clone or recreate an existing job if you want to optimize its search query.

## 13. Consider using population analysis [population-analysis]

Population analysis is more memory efficient than individual analysis of each series. It builds a profile of what a "typical" entity does over a specified time period and then identifies when one is behaving abnormally compared to the population. Use population analysis for analyzing high cardinality fields if you expect that the entities of the population generally behave in the same way.

## 14. Reduce the cost of forecasting [forecasting]

There are two main performance factors to consider when you create a forecast: indexing load and memory usage. Check the cluster monitoring data to learn the indexing rate and the memory usage.

Forecasting writes a new document to the result index for every forecasted element of the  for every bucket. Jobs with high partition or by field cardinality create more result documents, as do jobs with small bucket span and longer forecast duration. Only three concurrent forecasts may be run for a single job.

To reduce indexing load, consider a shorter forecast duration and/or try to avoid concurrent forecast requests. Further performance gains can be achieved by reviewing the job configuration; for example by using a dedicated results index, increasing the bucket span and/or by having lower cardinality partitioning fields.

The memory usage of a forecast is restricted to 20 MB by default. From 7.9, you can extend this limit by setting `max_model_memory` to a higher value. The maximum value is 40% of the memory limit of the {{anomaly-job}} or 500 MB. If the forecast needs more memory than the provided value, it spools to disk. Forecasts that spool to disk generally run slower. If you need to speed up forecasts, increase the available memory for the forecast. Forecasts that would take more than 500 MB to run won’t start because this is the maximum limit of disk space that a forecast is allowed to use.
