---
applies_to:
  serverless: preview
  stack: preview =9.1, ga 9.2+
---

# Manage data quality [streams-data-retention]

After selecting a stream, use the **Data quality** tab to find failed and degraded documents in your stream. Use the following components to monitor the health of your data and identify and fix issues:

- **Degraded documents:** Documents with the `ignored` property usually because of malformed fields or exceeding the limit of total fields when `ignore_above:false`. This component shows the total number of degraded documents, the percentage, and status (**Good**, **Degraded**, **Poor**).
- **Failed documents:**: Documents that were rejected during ingestion because of mapping conflicts or pipeline failures.
- **Quality score:** Streams calculates the overall quality score (**Good**, **Degraded**, **Poor**) based on the percentage of degraded and failed documents.
- **Trends over time:** A time-series chart so you can track how degraded and failed documents are accumulating over time. Use the date picker to zoom into a specific range and understand when problems are spiking.
- **Issues:** {applies_to}`stack: preview 9.2`Find issues with specific fields, how often they've occurred, and when they've occurred.

## Failure store

A [failure store](../../../../manage-data/data-store/data-streams/failure-store.md) is a secondary set of indices inside a data stream, dedicated to storing failed documents. Instead of losing documents that are rejected during ingestion, a failure store retains it in a `::failures` index, so you can review failed documents to understand what went wrong and how to fix it.

### Required permissions
To view and modify failure store in {{stack}}, you need the following data stream level privileges:
- `read_failure_store`
- `manage_failure_store`

For more information, refer to [Granting privileges for data streams and aliases](../../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).

### Turn on failure stores
In Streams, you need to turn on failure stores to get failed documents. To do this, select **Enable failure store** in the **Failed documents** component. From here you can set your failure store retention period.

For more information on data quality, refer to the [data set quality](../../data-set-quality-monitoring.md) documentation.