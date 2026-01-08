---
applies_to:
  serverless: preview
  stack: preview =9.1, ga 9.2+
---

# Manage data quality [streams-data-retention]

From the **Streams** page, use the **Data quality** menu to filter your streams by data quality status, then select a stream to examine it more closely. After selecting a stream, use the **Data quality** tab to find failed and degraded documents in your stream.

Use the following components to monitor the health of your data and identify and fix issues:

* **Degraded documents:** Documents from the last backing index of the stream with the `ignored` property, usually because of malformed fields or exceeding the limit of total fields when `ignore_above:false`. This component shows:
  * the total number of degraded documents
  * the percentage of degraded documents relative to the total document count from the stream's last backing
  * the quality status (**Good**, **Degraded**, **Poor**).
* **Failed documents:**: Documents that were rejected during ingestion because of mapping conflicts or pipeline failures. This component shows all documents in the failure store that correspond with this stream, within the time range specified in the date picker. For example, for a stream called `my-stream`, Streams fetches all documents from the `my-stream::failures` index within the specified time range. Refer to [Failure store](#streams-data-quality-failure) for more.
* **Quality score:** Streams calculates the overall quality score (**Good**, **Degraded**, **Poor**) based on the percentage of degraded and failed documents. Refer to [Data quality calculation](#streams-data-quality-calculation) for more.
* **Trends over time:** A time-series chart so you can track how degraded and failed documents are accumulating over time. Use the date picker to zoom into a specific range and understand when problems are spiking.
* **Issues:** {applies_to}`stack: preview 9.2`Find issues with specific fields, how often they've occurred, and when they've occurred.

## Data quality calculation [streams-data-quality-calculation]

Streams calculates data quality as follows:

* **Good**: Both the **Degraded documents** percentage and the **Failed documents** percentage are 0.
* **Degraded**: Either the **Degraded documents** percentage or the **Failed documents** percentage are greater than 0 and less than or equal to 3.
* **Poor**: Either the **Degraded documents** percentage or the **Failed documents** percentage are greater than 3%.

## Failure store [streams-data-quality-failure]

A [failure store](../../../../manage-data/data-store/data-streams/failure-store.md) is a secondary set of indices inside a data stream, dedicated to storing failed documents. Instead of losing documents that are rejected during ingestion, a failure store retains it in a `::failures` index, so you can review failed documents to understand what went wrong and how to fix it.

### Required permissions
To view and modify failure store in {{stack}}, you need the following data stream level privileges:
- `read_failure_store`
- `manage_failure_store`

For more information, refer to [Granting privileges for data streams and aliases](../../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).

### Turn on failure stores
In Streams, you need to turn on failure stores to get failed documents. To do this, select **Enable failure store** in the **Failed documents** component. From here you can set your failure store retention period.

For more information on data quality, refer to the [data set quality](../../data-set-quality-monitoring.md) documentation.