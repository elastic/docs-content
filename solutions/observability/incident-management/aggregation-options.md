---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/aggregation-options.html
  - https://www.elastic.co/guide/en/serverless/current/observability-aggregationOptions.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Aggregation options [aggregation-options]

Aggregations summarize your data to make it easier to analyze. In some alerting rules, you can specify aggregations to gather data for the rule.

The following aggregations are available in some rules:

| Aggregation | Description |
| --- | --- |
| Average | Average value of a numeric field. |
| Cardinality | Approximate number of unique values in a field. |
| Document count | Number of documents in the selected dataset. |
| Max | Highest value of a numeric field. |
| Min | Lowest value of a numeric field. |
| Percentile | Numeric value which represents the point at which n% of all values in the selected dataset are lower (choices are 95th or 99th). |
| Rate | Rate at which a specific field changes over time. To learn about how the rate is calculated, refer to [Rate aggregation](/solutions/observability/incident-management/rate-aggregation.md). |
| Sum | Total of a numeric field in the selected dataset. |