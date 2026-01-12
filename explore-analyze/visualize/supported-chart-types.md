---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/chart-types.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Supported chart types [chart-types]

$$$aggregation-reference$$$

| Panel type | **Lens** | **TSVB** | **Aggregation-based** | **Vega** | **Timelion** |
| --- | --- | --- | --- | --- | --- |
| Table | &check; | &check; | &check; |  |  |
| Bar, line, and area | &check; | &check; | &check; | &check; | &check; |
| Split chart and small multiples |  | &check; | &check; | &check; |  |
| Pie and donut | &check; |  | &check; | &check; |  |
| Sunburst | &check; |  | &check; | &check; |  |
| Treemap | &check; |  |  | &check; |  |
| Heatmap | &check; |  | &check; | &check; |  |
| Gauge and Goal | &check; | &check; | &check; | &check; |  |
| Markdown |  | &check; |  |  |  |
| Metric | &check; | &check; | &check; | &check; |  |
| Tag cloud | &check; |  | &check; | &check; |  |


## Bar, line, and area chart features [xy-features]

For step-by-step guidance on time series, see [Build line charts](charts/line-charts.md).

| Feature | **Lens** | **TSVB** | **Aggregation-based** | **Vega** | **Timelion** |
| --- | --- | --- | --- | --- | --- |
| Dense time series | Customizable | &check; | Customizable | &check; | &check; |
| Percentage mode | &check; | &check; | &check; | &check; |  |
| Break downs | 1 | 1 | 3 | ∞ | 1 |
| Custom color with break downs |  | Only for Filters | &check; | &check; |  |
| Fit missing values | &check; |  | &check; | &check; | &check; |
| Synchronized tooltips | &check; | &check; |  |  |  |


## Advanced features [other-features]

| Feature | **Lens** | **TSVB** | **Vega** | **Timelion** |
| --- | --- | --- | --- | --- |
| Math | &check; | &check; | &check; | &check; |
| Math across indices |  |  | &check; | &check; |
| Visualize two indices | &check; | &check; | &check; | &check; |
| Time shift | &check; | &check; | &check; | &check; |
| Custom {{es}} queries |  |  | &check; |  |
| Normalize by time | &check; | &check; |  |  |
| Automatically generated suggestions | &check; |  |  |  |
| Annotations | &check; | &check; |  |  |


## Table features [table-features]

| Feature | **Lens** | **TSVB** | **Aggregation-based** |
| --- | --- | --- | --- |
| Summary row | &check; |  | &check; |
| Pivot table | &check; |  |  |
| Calculated column | Formula | &check; | Percent only |
| Color by value | &check; | &check; |  |


## Functions [custom-functions]

| Function | **Lens** | **TSVB** |
| --- | --- | --- |
| Counter rate | &check; | &check; |
| [Filter ratio](legacy-editors/tsvb.md#tsvb-function-reference) | Use [formula](lens.md#lens-formulas) | &check; |
| [Positive only](legacy-editors/tsvb.md#tsvb-function-reference) |  | &check; |
| [Series agg](legacy-editors/tsvb.md#tsvb-function-reference) | Use [formula](lens.md#lens-formulas) | &check; |
| Static value | &check; | &check; |


## Metrics aggregations [metrics-aggregations]

Metric aggregations are calculated from the values in the aggregated documents. The values are extracted from the document fields.

| Aggregation | **Lens** | **TSVB** | **Aggregation-based** | **Vega** |
| --- | --- | --- | --- | --- |
| Metrics with filters | &check; |  |  | &check; |
| Average, Sum, Max, Min | &check; | &check; | &check; | &check; |
| Unique count (Cardinality) | &check; | &check; | &check; | &check; |
| Percentiles and Median | &check; | &check; | &check; | &check; |
| Percentiles Rank | &check; | &check; | &check; | &check; |
| Standard deviation |  | &check; | &check; | &check; |
| Sum of squares |  | &check; |  | &check; |
| Top hit (Last value) | &check; | &check; | &check; | &check; |
| Value count | &check; |  | &check; | &check; |
| Variance | &check; | &check; |  | &check; |

For information about {{es}} metrics aggregations, refer to [Metrics aggregations](elasticsearch://reference/aggregations/metrics.md).


## Bucket aggregations [bucket-aggregations]

Bucket aggregations group, or bucket, documents based on the aggregation type. To define the document buckets, bucket aggregations compute and return the number of documents for each bucket.

| Aggregation | **Lens** | **TSVB** | **Aggregation-based** | **Vega** |
| --- | --- | --- | --- | --- |
| Histogram | &check; |  | &check; | &check; |
| Date histogram | &check; | &check; | &check; | &check; |
| Date range | Use filters | &check; | &check; | &check; |
| Filter |  | &check; |  | &check; |
| Filters | &check; | &check; | &check; | &check; |
| GeoHash grid |  |  | &check; | &check; |
| IP prefix | Use filters | Use filters | &check; | &check; |
| IP range | Use filters | Use filters | &check; | &check; |
| Range | &check; | Use filters | &check; | &check; |
| Terms | &check; | &check; | &check; | &check; |
| Significant terms | &check; |  | &check; | &check; |

For information about {{es}} bucket aggregations, refer to [Bucket aggregations](elasticsearch://reference/aggregations/bucket.md).


## Pipeline aggregations [pipeline-aggregations]

Pipeline aggregations are dependent on the outputs calculated from other aggregations. Parent pipeline aggregations are provided with the output of the parent aggregation, and compute new buckets or aggregations that are added to existing buckets. Sibling pipeline aggregations are provided with the output of a sibling aggregation, and compute new aggregations for the same level as the sibling aggregation.

| Aggregation | **Lens** | **TSVB** | **Aggregation-based** | **Vega** |
| --- | --- | --- | --- | --- |
| Avg bucket | [`overall_average` formula](lens.md#lens-formulas) | &check; | &check; | &check; |
| Derivative | &check; | &check; | &check; | &check; |
| Max bucket | [`overall_max` formula](lens.md#lens-formulas) | &check; | &check; | &check; |
| Min bucket | [`overall_min` formula](lens.md#lens-formulas) | &check; | &check; | &check; |
| Sum bucket | [`overall_sum` formula](lens.md#lens-formulas) | &check; | &check; | &check; |
| Moving average | &check; | &check; | &check; | &check; |
| Cumulative sum | &check; | &check; | &check; | &check; |
| Bucket script |  | &check; | &check; | &check; |
| Bucket selector |  |  |  | &check; |
| Serial differencing |  | &check; | &check; | &check; |

For information about {{es}} pipeline aggregations, refer to [Pipeline aggregations](elasticsearch://reference/aggregations/pipeline.md).

