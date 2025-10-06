---
applies_to:
  serverless: preview
  stack: preview 9.1, ga 9.2
---

# Manage data quality [streams-data-retention]

Use the **Data quality** tab to find failed and degraded documents in your stream. The **Data quality** tab is made up of the following components:

- **Degraded documents**: Documents with the `ignored` property usually because of malformed fields or exceeding the limit of total fields when `ignore_above:false`. This component shows the total number of degraded documents, the percentage, and status (**Good**, **Degraded**, **Poor**).
- **Failed documents**: Documents that were rejected during ingestion.
- **Issues**: {applies_to}`stack: preview 9.2`Find issues with specific fields, how often they've occurred, and when they've occurred.

For more information on data quality, refer to the [data set quality](../../data-set-quality-monitoring.md) documentation.